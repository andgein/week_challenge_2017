from weekchallenge import *


class Solver(TaskSolver):
    type_name = 'colors'

    def __init__(self):
        self.colors = []
        with open('files/colors.txt', encoding='utf-8') as f:
            for line in f:
                color, description = line.strip().split(' ', 1)
                self.colors.append((color, description))

    def solve(self, task):
        value = task.value.lower()
        for color, description in self.colors:
            if value in description.lower():
                return color


    def tests(self):
        return [
            ('#ff8c00', 'DarkOrange'),
            ('rgb(250, 235, 215)', 'AntiqueWhite'),
        ]
