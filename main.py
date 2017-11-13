from weekchallenge import *
from solvers import *

import requests
import logging
import sys
import tempfile
import json
import re


TOKEN = '745ba685-9cae-43ef-b1e6-2dbaf662b9c6'


def test_ColorsTask():
    solver = colors.Solver()
    assert(solver.solve(Task.with_value('#ff8c00')) == 'DarkOrange')
    assert(solver.solve(Task.with_value('rgb(250, 235, 215)')) == 'AntiqueWhite')


def test_AccentuationTask():
    solver = accentuation.Solver()
    assert(solver.solve(Task.with_value('корова')) == 'корОва')
    assert(solver.solve(Task.with_value('ягода')) == 'Ягода')
    assert(solver.solve(Task.with_value('ежевика')) == 'ежевИка')
    assert(solver.solve(Task.with_value('арбуз')) == 'арбУз')
    assert(solver.solve(Task.with_value('мама')) == 'мАма')
    assert(solver.solve(Task.with_value('вечеря')) == 'вЕчеря')
    assert(solver.solve(Task.with_value('oкружит')) == 'oкружИт')


def test_TtsTask():
    solver = tts.Solver()
    assert(solver.solve(Task.with_value('/tasks/tts/e2123149-e493-4857-b37a-e37cce3dc45d.mp4')) == 'Alan')
    assert(solver.solve(Task.with_value('/tasks/tts/66f39cb8-d89e-43dd-a56a-e35919df75b3.mp4')) == 'Bjarne')
    assert(solver.solve(Task.with_value('/tasks/tts/bfd4c005-9c16-4341-8c72-ed19e3eb8011.mp4')) == 'Ron')

def test_AplusbTask():
    solver = aplusb.Solver()
    assert(solver.solve(Task.with_value('-5023 - -5260')) == '237')
    assert(solver.solve(Task.with_value('13!')) == '6227020800')
    assert(solver.solve(Task.with_value('(10 + 20)\'')) == '0')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':        
        test_ColorsTask()
        test_AccentuationTask()
        test_TtsTask()
        test_AplusbTask()
        sys.exit(0)
    
    solver = MegaSolver(TOKEN, colors.Solver(), accentuation.Solver(), tts.Solver(), aplusb.Solver())
    solver.run(ask_after_each_task=False)   
                