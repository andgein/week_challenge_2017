import time
import os
import os.path
import tempfile
import shutil
import json
import sys

from weekchallenge import *

TOKEN = '745ba685-9cae-43ef-b1e6-2dbaf662b9c6'
SLEEP_INTERVAL = 0.08 # in seconds
TASKS_DIRECTORY = 'tasks'


STOP_ON_UNKNOWN_TASKS = True
SOLVERS = get_solvers()


def main():
    if not os.path.exists(TASKS_DIRECTORY):
        os.makedirs(TASKS_DIRECTORY)

    api = Api(TOKEN)
    while not stopped():
        try:
            task = api.get_task()
            Logger.info('Received new task: %s' % str(task))
    
            task_directory = os.path.join(TASKS_DIRECTORY, task.type)
            if not os.path.exists(task_directory):
                os.makedirs(task_directory)
    
            task_filename = os.path.join(task_directory, task.id + '.task')
    
            tf = tempfile.NamedTemporaryFile(mode='w', suffix='.task', delete=False)
            tf.write(json.dumps(task._asdict()))
            tf.close()
            Logger.info('Dumped task to %s and copying it to %s' % (tf.name, task_filename))
                
            shutil.copy(tf.name, task_filename)

            if STOP_ON_UNKNOWN_TASKS and not is_task_known(task):
                Logger.warn('Received unknown task: %s' % str(task))
                TelegramChat.send_message('*ALARM*\n\nПодъехал новый вид заданий: ```%s```Я пока остановил всех демонов до вашего прихода. Вперёд!\n_И да пребудет с вами сила._' % task.type)
                sys.exit(1)

        except Exception as e:
            Logger.error('Exception occured: %s' % e)
        time.sleep(SLEEP_INTERVAL)

    Logger.info('Exiting')


def is_task_known(task):
    for solver in SOLVERS:
        if solver.type_name == task.type:
            return True

    return False

if __name__ == '__main__':
    Logger.setup(filename='logs/task_getter.log')
    main()                