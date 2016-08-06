#!/bin/python

import sys
import time
import json
import requests
import calendar
import ast

class Firebase(object):
    def __init__(self, url):
        self.url = url

    def child(self, url):
        return Firebase(self.url + url)

    def get(self, url = ''):
        json = requests.get(self.url + url + '.json').text

        try:
            print(self.url + url, json)

            if json == 'null':
                return None
            return ast.literal_eval(json)
        except ValueError:
            raise

    def delete(self, url = ''):
        return requests.delete(self.url + url + '.json')

    def update(self, payload, url = ''):
        return ast.literal_eval(requests.patch(self.url + url + '.json', data=json.dumps(payload)).text)

bot_id = sys.argv[1]

if not bot_id:
    print('failed to get bot_if, exitting...')
    sys.exit(1)

bot_ref = Firebase('https://meowth-aed86.firebaseio.com/bots/{}/'.format(bot_id))
# get bot object
bot = bot_ref.get()

# user credits ref
credits_ref = Firebase('https://meowth-aed86.firebaseio.com/credits/')

# TODO: check if bot contains a good config
if not 'vm' in bot:
    print("bot doesn't have a vm assigned, exiting...")
    sys.exit(1)

# simulate 12 ticks
for i in range(4):
    # consume credits
    current_credit_value = credits_ref.get(bot['user'])

    if not current_credit_value:
        break

    credits_ref.update({ bot['user']: current_credit_value - 1 })

    # heartbeat
    response = bot_ref.update({ 'status': 'online', 'timestamp': calendar.timegm(time.gmtime()) })

    # simulate a tick
    time.sleep(5)

# Set bot to offline
bot_ref.update({
    'status': 'offline',
    'timestamp': calendar.timegm(time.gmtime())
})

bot_ref.delete('vm')

# Remove bot from VM's bot list
url = 'https://meowth-aed86.firebaseio.com/vms/{}/bots/{}'.format(bot['vm'], bot_id)
response = Firebase(url).delete()
