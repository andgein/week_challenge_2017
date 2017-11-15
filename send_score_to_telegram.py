from weekchallenge import *

import requests
from bs4 import BeautifulSoup
import time
import sys


SEND_SCORE_EACH = 10 * 60 # seconds
SCORE_URL = 'http://wc.kontur.cloud/teams'
TEAM_NAME = 'Фантастическая четвёрка'


last_scores = {}

def main(to_stdout=False):
    last_sent_time = 0    

    while not stopped():
        current_time = int(time.time())
        if current_time - last_sent_time > SEND_SCORE_EACH:
            try:
                get_and_send_score(to_stdout=to_stdout)
            except Exception as e:
                Logger.error('Exception: %s' % e)
            last_sent_time = current_time
        time.sleep(1)        
    Logger.info('Exiting')


def get_and_send_score(to_stdout=False):
    global last_scores

    scores = list(get_scores())

    message = '*Текущие результаты*\n'
    if len(last_scores) == 0:
        message += '_Я только запустился. Буду присылать изменения в результатах каждые %d минут_\n' % (SEND_SCORE_EACH // 60)
    message += '\n'

    position = 1
    for team_name, score in scores:
        team_name = team_name.replace('*', r'\*').replace('_', r'\_')

        score_int = int(score.replace(' ', ''))

        team_message = '%02d. %s: %s' % (position, team_name, score)
        if team_name in last_scores:
            diff = score_int - last_scores[team_name]
            if diff >= 0:
                diff_str = '+%d' % diff
            else:
                diff_str = str(diff)

            team_message += ' (%s)' % diff_str

        if TEAM_NAME in team_name:
            team_message = '*%s*' % team_message

        message += team_message + '\n'

        position += 1
        last_scores[team_name] = score_int

    if to_stdout:
        print(message)
    else:
        TelegramChat.send_message(message)


def get_scores():
    Logger.info('Fetching scores from %s' % SCORE_URL)
    r = requests.get(SCORE_URL)
    if not r.ok:
        Logger.warn('HTTP status code is %d' % r.status_code)
        raise Exception('Can\'t fetch scores from %s' % SCORE_URL)

    s = BeautifulSoup(r.text, 'html.parser')

    team_names = s.select('tr td.team .team_name')
    scores = s.select('tr td.nowrap')

    for team, score in zip(team_names, scores):
        team_name = team.text
        score = score.text
        
        yield (team_name, score)

if __name__ == '__main__':
    Logger.setup(filename='logs/send_score_to_telegram.log')
    main('--stdout' in sys.argv[1:])