from weekchallenge import *

import tempfile
import re
import ffmpy
import json
import glob


class Solver(TaskSolver):
    type_name = 'tsya-strikes-back'


    def __init__(self):
        self.content = '' 
        for filename in glob.glob('files/tsya-strikes-back/*'):
            with open(filename, encoding='utf-8') as f:
                self.content += f.read().lower()

    def solve(self, task):
        value = task.value.strip().lower()

        value = re.sub('\s+', ' ', value)

        words = value.split()
        need_word = None
        for word in words:
            if 'тся' in word or 'ться' in word:
                need_word = word
        if need_word is None:
            Logger.error('Can\'t find word with "т(ь)ся" in "%s"' % value)
            return None                                                   

        if 'тся' in need_word:
            other_form = need_word.replace('тся', 'ться')
        else:
            other_form = need_word.replace('ться', 'тся')

        value_with_other_form = value.replace(need_word, other_form)

        if value in self.content:
            Logger.info('Found "%s" in our collection\'s content' % value)
            return need_word
        elif value_with_other_form in self.content:
            Logger.info('Found other form — "%s" — in our collection\'s content' % value_with_other_form)
            return other_form
        elif need_word in self.content and other_form not in self.content:
            Logger.info('"%s" found, but "%s" — no in our collection\'s content' % (need_word, other_form))
            return need_word
        elif need_word not in self.content and other_form in self.content:
            Logger.info('"%s" found, but "%s" — no in our collection\'s content' % (other_form, need_word))
            return other_form

        return None

    def tests(self):
        return [
('призываю вас помолиться вместе со мной', 'помолиться'),
('дэрин смог только улыбнутся как можно более виновато', 'улыбнуться'),
('сейчас  все  должно  было решиться', 'решиться'),
('лансдейл  был серьезен  и  не позволил себе улыбнуться', 'улыбнуться'),
('когда мог поплатится за подобный приход и комсомольским', 'поплатиться'),
('как ей держаться на таком необычном свидании', 'держаться'),
('йорк мог справится с этой работой', 'справиться'),
('чтобы  принцесса смогла устроится у него на коленях', 'устроиться'),
        ]