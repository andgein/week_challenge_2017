import time
import os
import os.path
import tempfile
import shutil
import json
import sys
import glob
import random


from weekchallenge import *

TOKEN = '745ba685-9cae-43ef-b1e6-2dbaf662b9c6'
SLEEP_INTERVAL = 0.1 # in seconds
TASKS_DIRECTORY = 'tasks'


def main(task_type):
    solvers = get_solvers()

    solver = None
    for s in solvers:
        if s.type_name == task_type:
            solver = s

    if solver is None:
        Logger.error('Can\'t find solver for type %s' % task_type)
        return

    solver.heavy_init()

    rename_old_files(solver)

    while not stopped() and not stopped_solvers():
        try:
            find_task_and_solve_it(solver)
        except Exception as e:
            Logger.error('Exception: %s' % e)
        time.sleep(SLEEP_INTERVAL)

    Logger.info('Exiting')


def rename_old_files(solver):
    files = glob.glob(os.path.join(TASKS_DIRECTORY, solver.type_name, '*.solving'))
    for filename in files:
        new_filename = filename[:-len('.solving')]
        Logger.info('Recreate old solving file %s to %s' % (filename, new_filename))
        shutil.move(filename, new_filename)


def find_task_and_solve_it(solver):
    filename, task = find_task(solver.type_name)
        
    if task is None:
        Logger.info('No new tasks found')
        return

    Logger.info('Found task %s' % str(task))

    try:
        answer = solver.solve(task)
    except Exception as e:
        os.remove(filename + '.solving')
        raise
                
    if answer is not None:
        Logger.info('Solver returned answer "%s"' % answer)
        with open(filename + '.answer', 'w', encoding='utf-8') as f:
            f.write(answer)        
    else:
        # TelegramChat.send_message('Солвер %s не смог решить задание "%s" (%s) и честно признался в этом 🤷🏼‍♀️' % (task.type, task.value, task.id))
        Logger.warn('Solver can\'t solve task %s, it returned None' % task.id)
        os.remove(filename + '.solving')

    # теперь их удаляет answer_submitter
    # os.remove(filename + '.solving')       


def find_task(folder):
    files = glob.glob(os.path.join(TASKS_DIRECTORY, folder, '*.task'))
    if len(files) == 0:
        return (None, None)

    filename = random.choice(files)
    shutil.move(filename, filename + '.solving')

    content = ''
    with open(filename + '.solving', 'r') as f:
        content = f.read()

    d = json.loads(content)
    Logger.debug('Read from file task: %s' % str(d))
    task = Task(**d)

    return (filename, task)

def stopped_solvers():
    return os.path.exists('stop.solvers.txt')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        Logger.error('USAGE: ./%s <task_name>' % sys.argv[0])
        sys.exit(1)

    task_type = sys.argv[1]

    Logger.setup(filename='logs/solver_worker_%s.log' % task_type)
    main(task_type) 