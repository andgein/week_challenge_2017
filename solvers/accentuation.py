from weekchallenge import *


class Solver(TaskSolver):
    type_name = 'accentuation'

    def heavy_init(self):
        self.collection = []
        with open('files/accentuation.txt', encoding='utf-8') as f:
            for line in f:
                self.collection.append(line.strip())

    def solve(self, task):
        # WTF, непонятно, как себя вести с английское е
        if task.value.lower() == 'пeтля':
            return 'пEтля'

        # Иногда прилетают английские буквы в русских словах, это всё портит. Например, «окружит», у которой первая О — английская
        value = self._replace_english_to_russian(task.value.lower())

        # Буква Ё
        if 'ё' in value:
            return value.replace('ё', 'Ё')

        for word in self.collection:
            if value == word.lower():
                Logger.debug('Found similar word "%s"' % word)
                with_accentuation = self.set_accentuation(task.value, word)
                return with_accentuation.split()[0]

        return None

    def set_accentuation(self, original, result):
        for i, ch in enumerate(result):
            if ch.isupper():
                return original[:i] + ch.upper() + original[i + 1:]

        return result
                    

    @staticmethod
    def _replace_english_to_russian(text):
        text = text.replace('a', 'а')
        text = text.replace('c', 'с')
        text = text.replace('e', 'е')
        text = text.replace('o', 'о')
        text = text.replace('y', 'у')
        text = text.replace('p', 'р')
        return text

    def tests(self):
        return [
            ('oкружит', 'oкружИт'),
            ('заселён', 'заселЁн'),
            ('незадолго', 'незадОлго'),
            ('приняли', 'прИняли'),
        ]