from weekchallenge import *
from solvers import *

import sys


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
    
    MegaSolver(TOKEN, *solvers).run(ask_after_each_task=False)
                