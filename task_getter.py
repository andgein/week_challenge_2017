import time
import os
import os.path
import tempfile
import shutil
import json

from weekchallenge import *

TOKEN = '745ba685-9cae-43ef-b1e6-2dbaf662b9c6'
SLEEP_INTERVAL = 0.15 # in seconds
TASKS_DIRECTORY = 'tasks'


def main():
    if not os.path.exists(TASKS_DIRECTORY):
        os.makedirs(TASKS_DIRECTORY)

    api = Api(TOKEN)
    while True:
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
        except Exception as e:
            Logger.error('Exception occured: %s' % e)
        time.sleep(SLEEP_INTERVAL)


if __name__ == '__main__':
    Logger.setup(filename='logs/task_getter.log')
    main()                