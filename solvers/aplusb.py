from weekchallenge import *

import re


class Solver(TaskSolver):
    type_name = 'a+b'

    def solve(self, task):
        Logger.info('Calculating "%s"' % task.value)
        value = self._prepare(task.value)
        if answer is not None:
            Logger.info('I prepared expression. Calculating "%s" via eval' % value)
        else:
            Logger.warn('Ha! I preverted injection! here is text: {}'.format(value))
            return None

        answer = int(eval(value))
        Logger.info('Result is %d' % answer)
        return str(answer)

    @staticmethod
    def _prepare(text):
        if re.search('[a-zA-Z]', text):
            return None
        if text == '0!':
            text = '1'

        text = re.sub(r'-(\d+)', r'(-\1)', text)

        # Степень
        text = text.replace('^', '**')
        # Двойные факториалы
        text = re.sub(r'(\d+)!!', lambda m: '(' + '*'.join(map(str, range(1 if int(m.group(1)) % 2 == 1 else 2, int(m.group(1)) + 1, 2))) + ')', text)
        # Факториалы
        text = re.sub(r'(\d+)!', lambda m: '(' + '*'.join(map(str, range(1, int(m.group(1)) + 1))) + ')', text)
        # Производная
        text = re.sub(r'^\(.+\)\'$', '0', text)
        return text


    def tests(self):
        return [
            ('-5023 - -5260', '237'),
            ('13!', '6227020800'),
            ('(10 + 20)\'', '0'),
            ('(-10 + -20)\'', '0'),
            ('10^2', '100'),
            ('3!!', '3'),
            ('-34^0', '1'),
        ]