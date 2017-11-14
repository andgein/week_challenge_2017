from weekchallenge import *


class Solver(TaskSolver):
    type_name = 'accentuation'

    base_url = 'http://accentonline.ru'

    exceptions = {
        # наша база почему-то предлагает двойные нормы
        'незадолго': 'незадОлго',
        'иначе': 'инАче',
        'включишь': 'включИшь',
        'петля': 'петлЯ',
    }

    def __init__(self):
        self.client = JsonClient(self.base_url)

    def solve(self, task):
        # Иногда прилетают английские буквы в русских словах, это всё портит. Например, «окружит», у которой первая О — английская
        value = self._replace_english_to_russian(task.value.lower())

        # Исключения
        if value in self.exceptions:
            return self.exceptions[value]

        # Буква Ё
        if 'ё' in value:
            return value.replace('ё', 'Ё')

        url = '/accents.json?q=' + value

        response = self.client.get_or_die(url)
        # Example of response: [{"value":"привет","accent":"приве́т"},{"value":"приветик","accent":"приве́тик"},{"value":"приветить","accent":"приве́тить"},{"value":"приветливость","accent":"приве́тливость"},{"value":"приветливый","accent":"приве́тливый"}]
        result = None
        for elem in response:
            if elem['value'].lower() == value:
                result = elem['accent']
                break
        else:
            # Если не нашли, то ищем похожее слово, начинающееся так же
            Logger.debug('Not found in results list, try to find similar word')
            for elem in response:
                if elem['value'].lower().startswith(value):
                    Logger.debug('Found similar word %s' % elem['value'])
                    result = elem['accent']
                    truncate = len(elem['value'].lower()) - len(value)
                    result = result[:len(result)-truncate]
                    break

        if result is None:
            return None

        answer = self._replace_accent(result, task.value.lower())
        return answer

    @staticmethod
    def _replace_english_to_russian(text):
        text = text.replace('a', 'а')
        text = text.replace('c', 'с')
        text = text.replace('e', 'е')
        text = text.replace('o', 'о')
        text = text.replace('y', 'у')
        text = text.replace('p', 'р')
        return text

    def _replace_accent(self, s, original_string):
        # Очень плохие задания. Сейчас мы попытаемся использовать оригинальную строчку, и вставить ударение на нужное место. Всё из-за английских букв в русских словах
        accent = '&#x301;'
        accent_index = s.index(accent)
        result = original_string[:accent_index - 1] + original_string[accent_index - 1].upper() + original_string[accent_index:]
        # Если нашли ещё ударение — удаляем
        return result

    def tests(self):
        return [
            ('корова', 'корОва'),
            ('ягода', 'Ягода'),
            ('ежевика', 'ежевИка'),
            ('арбуз', 'арбУз'),
            ('мама', 'мАма'),
            ('вечеря', 'вЕчеря'),
            ('oкружит', 'oкружИт'),
            ('заселён', 'заселЁн'),
            ('незадолго', 'незадОлго'),
        ]