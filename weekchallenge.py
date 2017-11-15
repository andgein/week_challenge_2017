import requests
import logging
from urllib.parse import urlencode
import collections
import time
import threading
import os
import os.path
import time
import telegram


TELEGRAM_TOKEN = '482407150:AAGSbEoKWnd15YhL5GyOubLjPBoFvAvVqLA'
TELEGRAM_CHAT_ID = '-1001270614477'


def get_solvers():
    import solvers.colors
    import solvers.accentuation
    import solvers.tts
    import solvers.aplusb
    import solvers.i_like_time
    import solvers.s_like_dollar
    import solvers.poems
    import solvers.tsya
    import solvers.tsya_strikes_back
    import solvers.bruce_schneier

    return [
        solvers.colors.Solver(),
        solvers.accentuation.Solver(),
        solvers.tts.Solver(),
        solvers.aplusb.Solver(),
        solvers.i_like_time.Solver(),
        solvers.s_like_dollar.Solver(),
        solvers.poems.Solver(),
        solvers.tsya.Solver(),
        solvers.tsya_strikes_back.Solver(),
        solvers.bruce_schneier.Solver(),
    ]


class _InternalLogger:
    def __init__(self, filename):
        self.logger = logging.getLogger('WeekChallenge')
        self.logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter('{%(thread)d} [%(levelname)s] %(message)s'))
        self.logger.addHandler(stream_handler)

        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(logging.Formatter('%(asctime)s {%(thread)d} [%(levelname)s] %(message)s'))
        self.logger.addHandler(file_handler)


class Logger:
    instance = None

    @classmethod
    def init(cls, filename='weekchallenge.log'):
        """ Если надо переинициализировать логгер """
        cls.instance = _InternalLogger(filename)
        cls.enabled = True

    @classmethod
    def setup(cls, filename):
        cls.init(filename)

    @classmethod
    def init_if_needed(cls):
        if cls.instance is None:
            cls.init()

    @classmethod
    def disable(cls):
        cls.enabled = False

    @classmethod
    def enable(cls):
        cls.enabled = True

    @classmethod
    def info(cls, message):  
        cls.init_if_needed()
        if cls.enabled:
            cls.instance.logger.info(message)

    @classmethod
    def warn(cls, message):  
        cls.init_if_needed()
        if cls.enabled:
            cls.instance.logger.warn(message)

    @classmethod
    def error(cls, message, dont_send_to_telegram=False):
        cls.init_if_needed()      
        if cls.enabled:
            cls.instance.logger.error(message)
            # if not dont_send_to_telegram:
            #     TelegramChat.send_message('*ОШИБКА*\n%s' % message)

    @classmethod
    def debug(cls, message):
        cls.init_if_needed()      
        if cls.enabled:
            cls.instance.logger.debug(message)


class JsonClient:
    def __init__(self, base_url=''):
        self.base_url = base_url

    def get_or_die(self, url, tries=3):
        return self._make_request_or_die(url, lambda url: requests.get(url), tries=tries)

    def post_or_die(self, url, data=None, tries=3):
        if data is None:
            data = {}
        return self._make_request_or_die(url, lambda url: requests.post(url, data=data), tries=tries)
    
    def _make_request_or_die(self, url, request_function, tries=3):
        for try_index in range(tries):
            try:
                return self._try_make_request_or_die(url, request_function)
            except Exception as e:
                Logger.debug('Exception: %s. Let\'s try one more time (%d/%d)' % (e, try_index + 1, tries))
                time.sleep(0.2)
                last_exception = e
        raise last_exception
        

    def _try_make_request_or_die(self, url, request_function):
        url = self.base_url + url
        Logger.debug('Send request to %s' % url)
        r = request_function(url)
        if not r.ok:
            Logger.warn('HTTP status code is %d' % (r.status_code))
            # Костыль для отправки старых ответов
            if r.status_code == 400:
                return None    
            raise Exception('Can\'t get response from %s' % url);

        Logger.debug('HTTP status code is %d, response: "%s"' % (r.status_code, r.text))
        return r.json()
    

class Api:
    base_url = 'http://wc.kontur.cloud'

    def __init__(self, token):
        self.token = token
        self.client = JsonClient(self.base_url)

    def get_task(self):
        task = self.client.get_or_die('/tasks?token=%s' % self.token)
        return Task(**task)

    def submit_answer(self, task, answer, gracefully=False):
        """
            task = api.get_task()
            is_correct = api.submit_answer(task, 'Your answer')
            ** OR **
            is_correct = api.submit_answer(task.id, 'Your answer')
        """
        if type(task) is str:
            task_id = task
        else:
            # task can be Task.id or Task itself
            task_id = task.id
        Logger.info('Try to submit answer "%s" for task %s' % (answer, task_id))
        try:
            is_correct = self.client.post_or_die('/tasks?%s' % urlencode({'token': self.token, 'task': task_id, 'answer': answer}), tries=15)
        except:
            if gracefully:
                return None
            else:
                raise
        Logger.debug('Received response for answer submitting: %s' % is_correct) 

        if is_correct:
            Logger.info('Yahoo, it\'s correct!')
        elif is_correct is not None:
            Logger.info('No, it\'s wrong :-(')
        
        return is_correct

        
class Task(collections.namedtuple('Task', ['availability', 'deadline_seconds', 'description', 'format', 'id', 'scores', 'type', 'value'])):
    @staticmethod
    def with_value(value):
        return Task(availability='', deadline_seconds=0, description='', format='', id='', scores=0, type='', value=value)


class TaskSolver:
    type_name = ''

    def solve(self, task):
        raise NotImplementedException('Each child should has its own .solve(task)')

    def heavy_init(self):
        pass

    def tests(self):
        return []

    def run_tests(self):
        for test_input, correct_answer in self.tests():
            Logger.info('Test %s.%s with input data "%s"' % (type(self).__module__, type(self).__name__, test_input))
            answer = self.solve(Task.with_value(test_input))
            if answer == correct_answer:
                continue
            
            raise AssertionError('Output "%s" is not equal to correct answer "%s"' % (answer, correct_answer))


class MegaSolver:
    def __init__(self, token, *solvers):
        self.api = Api(token)
        self.solvers = solvers

    def run(self, ask_after_each_task=True, ignore_unknown=False, ignore_wrong=False, ignore_when_solver_cant_solve=False, ignore_internal_errors=False):
        Logger.info('Run infinity loop for task solvers (ask_after_each_task=%s, ignore_unknown=%s)' % (ask_after_each_task, ignore_unknown))
        while True:
            try:
                is_correct = self.get_task_and_solve_it(ignore_unknown=ignore_unknown, ignore_when_solver_cant_solve=ignore_when_solver_cant_solve)
            except Exception as e:
                if not ignore_internal_errors:
                    raise
                Logger.error('Ignore exception, sleep 1 second and retry: %s' % e)
                time.sleep(1)
                continue

            if not is_correct and not ignore_wrong:
                Logger.info('Something has gone wrong... Answer is not correct. Stop the process')
                break

            if ask_after_each_task:
                print('\n\nContinue? [Y/N]')
                yesno = input().strip().lower()
                if 'y' != yesno:
                    break
        Logger.info('Exiting')

    def get_task_and_solve_it(self, ignore_unknown=False, ignore_when_solver_cant_solve=False):
        task = self.api.get_task()
        Logger.info('Received new task: %s' % str(task))
        task_type = task.type
        for solver in self.solvers:
            if solver.type_name == task_type:
                Logger.info('Found solver for this task: %s.%s' % (type(solver).__module__, type(solver).__name__))

                answer = None
                try:
                    answer = solver.solve(task)
                except Exception as e:
                    Logger.error('Solver raised the exception: %s' % e)
                else:
                    Logger.info('Solver returned answer: %s' % answer)

                if answer is None:
                    Logger.error('Answer is None -> Solver can\'t find answer :(')
                    if not ignore_when_solver_cant_solve:
                        print('Enter correct answer for this task:\n\n%s [%s]' % (task.description, task.value))
                        answer = input().strip()
                        Logger.info('User entered answer "%s"' % answer)

                break
        else:
            Logger.info('Can\'t find solver for this task type');
            if ignore_unknown:
                Logger.info('OK. Just ignore it')
                answer = None
            else:
                print('Enter correct answer for this task:\n\n%s [%s]' % (task.description, task.value))
                answer = input().strip()
                Logger.info('User entered answer "%s"' % answer)

        if answer is not None and len(answer) > 0:
            return self.api.submit_answer(task, answer)
    
        # Проигнорировали таск — как будто бы решили
        return True


class TelegramChat:
    bot = telegram.Bot(TELEGRAM_TOKEN)

    @classmethod
    def send_message(cls, message):
        Logger.debug('Sending message to our telegram chat: "%s"' % message)
        try:
            cls.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode=telegram.ParseMode.MARKDOWN)
        except Exception as e:
            Logger.error('Can\'t send message to our telegram chat: %s' % e, dont_send_to_telegram=True)

        
def stopped():
    return os.path.exists('stop.txt')