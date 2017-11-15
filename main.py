from time import sleep

from weekchallenge import *

import sys
import threading


TOKEN = '745ba685-9cae-43ef-b1e6-2dbaf662b9c6'

SOLVERS = get_solvers()

if __name__ == '__main__':
    # Запускаем тесты
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        module_name = None
        if len(sys.argv) > 2:
            module_name = sys.argv[2]

        for solver in SOLVERS:
            if module_name is not None and type(solver).__module__ != 'solvers.' + module_name:
                continue
            solver.heavy_init()                
            solver.run_tests()

        print('OK! All tests done')
        sys.exit(0)
    
    # Молчаливый режим — все ошибки игнорируются, минимум интерактива
    if '--silent' in sys.argv[1:]:
        silent_mode = True
        args = dict(ask_after_each_task=False, ignore_unknown=True, ignore_wrong=True, ignore_when_solver_cant_solve=True, ignore_internal_errors=True)
    else:
        silent_mode = False
        args = {}

    # Многопоточный режим. Шарашит в 8 потоков
    if '--multithread' in sys.argv[1:]:
        threads = 4
    else:
        threads = 1

    # Запускаем мега-солвер!
    mega_solver = MegaSolver(TOKEN, *SOLVERS)

    for _ in range(threads):
        threading.Thread(target = mega_solver.run, kwargs=args).start()
        sleep(1)
                