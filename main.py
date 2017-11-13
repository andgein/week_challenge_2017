from weekchallenge import *

import requests
import logging
import sys
import tempfile
import json
import re


TOKEN = '745ba685-9cae-43ef-b1e6-2dbaf662b9c6'

class ColorsTask(TaskType):
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


class AccentuationTask(TaskType):
    type_name = 'accentuation'

    base_url = 'http://accentonline.ru'

    def __init__(self):
        self.client = JsonClient(self.base_url)

    def solve(self, task):
        # Иногда прилетают английские буквы в русских словах, это всё портит. Например, «окружит», у которой первая О — английская
        value = self._replace_english_to_russian(task.value.lower())
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
        text = text.replace('e', 'у')
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


class TtsTask(TaskType):
    """ Works on Google SpeechRecognition and SpeechRecognition module:
        https://pypi.python.org/pypi/SpeechRecognition/, 
        https://github.com/Uberi/speech_recognition/blob/master/examples/audio_transcribe.py
        It also uses ffmpeg wrapper ffmpy
    """
    type_name = 'tts'

    base_url = Api.base_url

    def __init__(self):
        import speech_recognition as sr
        self.sr = sr.Recognizer()
        with open('files/hacker_quotes.json', encoding='utf-8') as quotes_file:
            self.quotes = json.load(quotes_file)

    def solve(self, task):
        import speech_recognition as sr
        import ffmpy

        filename = task.value
        r = requests.get(self.base_url + filename)
        if not r.ok:
            Logger.error('Can\'t download file "%s"' % filename)
            return None

        mp4_tf = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        mp4_tf.write(r.content)
        mp4_tf.close()

        Logger.info('Saved audio to %s' % mp4_tf.name)
        Logger.info('Converting it into WAV')

        wav_tf = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        wav_tf.close()

        ff = ffmpy.FFmpeg(
            inputs={mp4_tf.name: None},
            outputs={wav_tf.name: ['-y']}
        )
        ff.run()

        with sr.AudioFile(wav_tf.name) as audio_file:
            audio = self.sr.record(audio_file)    

        Logger.info('Uploading file to Google Speech Recognition')
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            recognized = self.sr.recognize_google(audio)
            Logger.info('Google Speech Recognition thinks you said "%s"' % recognized)
        except sr.UnknownValueError:
            Logger.error('Google Speech Recognition could not understand audio')
        except sr.RequestError as e:
            Logger.error('Could not request results from Google Speech Recognition service; %s' % e)

        quote = self._find_suitable_quote(recognized)
        if quote is None:
            return None

        author = quote[':a'].split()
        name = author[0]
        print(name)
        return name

    def _find_suitable_quote(self, text):
        splitted = text.split()

        best_quote = None
        max_cnt = 0
        for quote in self.quotes:
            quote_text = quote[':c']
            splitted_quote_text = self._remove_special_chars(quote_text).lower().split()

            cnt = 0
            for part in splitted:
                part = part.lower()
                if part in splitted_quote_text:
                    cnt += 1

            if cnt >= max_cnt:
                Logger.debug('Found more similar quote: %s' % quote)
                best_quote = quote
                max_cnt = cnt

        Logger.info('Found best similar quote: %s' % best_quote)
        return best_quote

    @staticmethod
    def _remove_special_chars(text):
        for ch in ',.!?:;-!@#$%^&*()':
            text = text.replace(ch, '')
        return text


class AplusbTask(TaskType):
    type_name = 'a+b'

    def solve(self, task):
        Logger.info('Calculating "%s"' % task.value)
        value = self._prepare(task.value)
        Logger.info('I prepared expression. Calculating "%s" via eval' % value)
        answer = int(eval(value))
        Logger.info('Result is %d' % answer)
        return str(answer)    

    @staticmethod
    def _prepare(text):
        # Факториалы
        text = re.sub(r'(\d+)!', lambda m: '(' + '*'.join(map(str, range(1, int(m.group(1)) + 1))) + ')', text)
        # Производная
        text = re.sub(r'\([^()]+\)\'', '0', text)
        return text

def test_ColorsTask():
    colors = ColorsTask()
    assert(colors.solve(Task.with_value('#ff8c00')) == 'DarkOrange')
    assert(colors.solve(Task.with_value('rgb(250, 235, 215)')) == 'AntiqueWhite')


def test_AccentuationTask():
    accentuation = AccentuationTask()
    assert(accentuation.solve(Task.with_value('корова')) == 'корОва')
    assert(accentuation.solve(Task.with_value('ягода')) == 'Ягода')
    assert(accentuation.solve(Task.with_value('ежевика')) == 'ежевИка')
    assert(accentuation.solve(Task.with_value('арбуз')) == 'арбУз')
    assert(accentuation.solve(Task.with_value('мама')) == 'мАма')
    assert(accentuation.solve(Task.with_value('вечеря')) == 'вЕчеря')
    assert(accentuation.solve(Task.with_value('oкружит')) == 'oкружИт')


def test_TtsTask():
    tts = TtsTask()
    assert(tts.solve(Task.with_value('/tasks/tts/e2123149-e493-4857-b37a-e37cce3dc45d.mp4')) == 'Alan')
    assert(tts.solve(Task.with_value('/tasks/tts/66f39cb8-d89e-43dd-a56a-e35919df75b3.mp4')) == 'Bjarne')
    assert(tts.solve(Task.with_value('/tasks/tts/bfd4c005-9c16-4341-8c72-ed19e3eb8011.mp4')) == 'Ron')

def test_AplusbTask():
    aplusb = AplusbTask()
    assert(aplusb.solve(Task.with_value('-5023 - -5260')) == '237')
    assert(aplusb.solve(Task.with_value('13!')) == '6227020800')
    assert(aplusb.solve(Task.with_value('(10 + 20)\'')) == '0')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':        
        # test_ColorsTask()
        # test_AccentuationTask()
        # test_TtsTask()
        test_AplusbTask()
        sys.exit(0)
    
    solver = Solver(TOKEN, ColorsTask(), AccentuationTask(), TtsTask(), AplusbTask())
    solver.run(ask_after_each_task=False)   
                