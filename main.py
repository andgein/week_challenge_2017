from weekchallenge import *
from solvers import *

import sys
import threading


TOKEN = '745ba685-9cae-43ef-b1e6-2dbaf662b9c6'


if __name__ == '__main__':
    solvers = [
        colors.Solver(),
        accentuation.Solver(),
        tts.Solver(),
        aplusb.Solver(),
        time.Solver(),
    ]

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        module_name = None
        if len(sys.argv) > 2:
            module_name = sys.argv[2]

        for solver in solvers:
            if module_name is not None and type(solver).__module__ != 'solvers.' + module_name:
                continue            
            solver.run_tests()

        print('OK! All tests done')
        sys.exit(0)
    
    if '--silent' in sys.argv[1:]:
        silent_mode = True
        args = dict(ask_after_each_task=False, ignore_unknown=True, ignore_wrong=True, ignore_when_solver_cant_solve=True, ignore_internal_errors=True)
    else:
        silent_mode = False
        args = {}

    if '--multithread' in sys.argv[1:]:
        threads = 8
    else:
        threads = 1

    mega_solver = MegaSolver(TOKEN, *solvers)
    for _ in range(threads):
        threading.Thread(target = mega_solver.run, kwargs=args).start()
                