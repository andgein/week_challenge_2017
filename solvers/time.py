from weekchallenge import *

from urllib.parse import urlencode
import time
import re


GOOGLE_API_KEY = 'AIzaSyDHC29i6pfkjgBsVLIG9ZOY4CaZdaDR7cw'


class GoogleGeoApi:
    base_url = 'https://maps.googleapis.com'

    def __init__(self):
        self.client = JsonClient(self.base_url)

    def find_city(self, city_name):
        Logger.info('Looking for coordinates for "%s"' % city_name)
        url = '/maps/api/geocode/json?%s' % urlencode({'address': city_name})
        r = self.client.get_or_die(url)
        location = r['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        Logger.info('Found coordinates: %s, %s' % (lat, lng))
        return '%s,%s' % (lat, lng)

    def get_timezone_offset(self, location):
        Logger.info('Getting timezone for location: %s' % location)
        url = '/maps/api/timezone/json?%s' % urlencode({'location': location, 'timestamp': int(time.time()), 'key': GOOGLE_API_KEY})
        r = self.client.get_or_die(url)
        offset = r['dstOffset'] + r['rawOffset']
        Logger.info('Summary offset is %d' % offset)
        return offset


class Solver(TaskSolver):
    type_name = 'I-love-time'

    def __init__(self):
        self.api = GoogleGeoApi()

    def solve(self, task):
        splitted = task.value.split()
        time = splitted[-3]
        city_name = splitted[-2]

        location = self.api.find_city(city_name)
        offset = self.api.get_timezone_offset(location)
    
        hours, minutes = self._parse_time(time)
        Logger.info('Current time is %d:%d' % (hours, minutes))

        return '%02d:%02d' % (hours, minutes)


    def _parse_time(self, time):
        m = re.findall(r'\d+')
        return m.groups(1), m.groups(2)