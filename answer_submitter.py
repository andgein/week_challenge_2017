import time
import os
import os.path
import tempfile
import shutil
import json
import glob
import re
import random
import sys
import collections

from weekchallenge import *

TOKEN = '745ba685-9cae-43ef-b1e6-2dbaf662b9c6'
SLEEP_INTERVAL = 0.1 # in seconds
TASKS_DIRECTORY = 'tasks'

STATS_SPAM_INTERVAL = 10 * 60 # in seconds

stats = {}
temp_stats = {}
stats_sent_at = time.time()
failed_tasks = collections.defaultdict(list)


def main(to_stdout=False):
    api = Api(TOKEN)
    while not stopped():
        try:
            find_answer_and_submit_it(api, to_stdout=to_stdout)
        except Exception as e:
            Logger.error('Exception: %s' % e)
        time.sleep(SLEEP_INTERVAL)

    Logger.info('Exiting')

def find_answer_and_submit_it(api, to_stdout=False):
    files = glob.glob(os.path.join(TASKS_DIRECTORY, '*', '*.task.answer'))
    if len(files) == 0:
        Logger.info('No new answers found')
        return

    filename = random.choice(files)
    Logger.info('Found answer in %s' % filename)
    m = re.match(r'.+[/\\]([^/\\]+)[/\\]([^/\\]+)\.task\.answer', filename)
    if not m:
        Logger.error('Can\'t get task type and id from filename %s' % filename)
        return

    task_type = m.groups()[0]
    task_id = m.groups()[1]
    with open(filename, encoding='utf-8') as f:
        answer = f.read()

    Logger.info('OK, it\'s task %s from solver %s' % (task_id, task_type))

    is_correct = api.submit_answer(task_id, answer, gracefully=True)
    
    os.remove(filename)

    solving_filename = filename[:-len('.answer')] + '.solving'
    Logger.info('Found .solving-file for this task: %s' % solving_filename)
    with open(solving_filename, encoding='utf-8') as f:
        task = Task(**json.loads(f.read()))
    os.remove(solving_filename)

    if is_correct is not None:
        update_statistics(is_correct, task_type, task_id, task, answer, to_stdout=to_stdout)
    else:
        Logger.warn('is_correct = None, don\'t update statistics')
    

def update_statistics(is_correct, task_type, task_id, task, answer, to_stdout=False):
    if task_type not in temp_stats:
        temp_stats[task_type] = {'s': 0, 'f': 0}

    temp_stats[task_type]['s' if is_correct else 'f'] += 1

    if not is_correct:
        failed_tasks[task_type].append((task, answer))
    
    if time.time() - stats_sent_at > STATS_SPAM_INTERVAL:
        try:
            try_send_stats(to_stdout=to_stdout)
        except Exception as e:
            Logger.error('Exception: %s' % e)

def try_send_stats(to_stdout=False):
    global temp_stats
    global stats_sent_at

    Logger.info('Sending statistics to our telegram chat')

    for task in temp_stats:
        if task not in stats:
            stats[task] = temp_stats[task]
            continue
        stats[task]['s'] += temp_stats[task]['s']
        stats[task]['f'] += temp_stats[task]['f']

    for task in stats:
        if task not in temp_stats:
            temp_stats[task] = {'s':0, 'f':0}


    for t in stats:
        task_info = 'Статистика по таску *%s* за последние %d минут\n\n' % (t, STATS_SPAM_INTERVAL // 60)
        task_info += '*Успех: {} (всего {})*\n*Провал: {} (всего {})*\n'.format(temp_stats[t]['s'], stats[t]['s'], temp_stats[t]['f'], stats[t]['f'])

        failed_tasks_of_this_type = failed_tasks[t][:10]
        if len(failed_tasks_of_this_type) > 0:
            task_info: 'Примеры фейлов:\n'
        for task, answer in failed_tasks_of_this_type:
            task_info += '\t`%s`: «%s». Мы ответили «%s», получили %d очков\n' % (task.id, prepare_markdown(task.value.replace('\n', r'\n')), prepare_markdown(answer), task.scores['incorrect_answer'])

        if to_stdout:
            print(task_info)
        else:
            TelegramChat.send_message(task_info)

    temp_stats.clear()
    failed_tasks.clear()
    stats_sent_at = time.time()


def prepare_markdown(text):
    text = text.replace('_', r'\_')
    text = text.replace('*', r'\*')
    text = text.replace('`', r'\`')
    return text


if __name__ == '__main__':
    Logger.setup(filename='logs/answer_submitter.log')
    main('--stdout' in sys.argv[1:])