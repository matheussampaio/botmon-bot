#!/bin/python

import sys
import time
import json
import requests
import calendar

class Firebase(object):
    def __init__(self, url):
        self.url = url

    def child(self, url):
        return Firebase(self.url + url)

    def get(self, url = ''):
        return requests.get(self.url + url + '.json')

    def update(self, payload, url = ''):
        return requests.patch(self.url + url + '.json', data=json.dumps(payload))

bot_id = sys.argv[1]

url = '/bots/{}'.format(bot_id)

ref = Firebase('https://meowth-aed86.firebaseio.com/')

for i in range(12):
    response = ref.update({ 'status': 'online', 'timestamp': calendar.timegm(time.gmtime()) }, url)
    print(response.text)
    time.sleep(5)

response = ref.update({ 'status': 'offline', 'timestamp': calendar.timegm(time.gmtime()) }, url)
