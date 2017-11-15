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

from weekchallenge import *

TOKEN = '745ba685-9cae-43ef-b1e6-2dbaf662b9c6'
SLEEP_INTERVAL = 0.1 # in seconds
TASKS_DIRECTORY = 'tasks'


def main():
    api = Api(TOKEN)
    while not stopped():
        try:
            find_answer_and_submit_it(api)
        except Exception as e:
            Logger.error('Exception: %s' % e)
        time.sleep(SLEEP_INTERVAL)

    Logger.info('Exiting')

def find_answer_and_submit_it(api):
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


if __name__ == '__main__':
    Logger.setup(filename='logs/answer_submitter.log')
    main()                