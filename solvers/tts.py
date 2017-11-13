from weekchallenge import *

import tempfile
import speech_recognition as sr
import ffmpy
import json


class Solver(TaskSolver):
    """ Works on Google SpeechRecognition and SpeechRecognition module:
        https://pypi.python.org/pypi/SpeechRecognition/, 
        https://github.com/Uberi/speech_recognition/blob/master/examples/audio_transcribe.py
        It also uses ffmpeg wrapper ffmpy
    """
    type_name = 'tts'

    base_url = Api.base_url

    def __init__(self):
        self.sr = sr.Recognizer()
        with open('files/hacker_quotes.json', encoding='utf-8') as quotes_file:
            self.quotes = json.load(quotes_file)

    def solve(self, task):
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
