from weekchallenge import *
from solvers import *

import sys


TOKEN = '745ba685-9cae-43ef-b1e6-2dbaf662b9c6'


if __name__ == '__main__':
    solvers = [colors.Solver(), accentuation.Solver(), tts.Solver(), aplusb.Solver()]

    if len(sys.argv) > 1 and sys.argv[1] == 'test':        
        for solver in solvers:
            solver.run_tests()
        sys.exit(0)
    
    MegaSolver(TOKEN, *solvers).run(ask_after_each_task=False)
                