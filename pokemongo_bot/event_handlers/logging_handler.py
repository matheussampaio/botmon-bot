# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
import requests

from pokemongo_bot.event_manager import EventHandler

class LoggingHandler(EventHandler):
    def __init__(self, bot_id):
        self.index = 0
        self.LOG_URL = 'https://meowth-aed86.firebaseio.com/bots/{}/logs.json'.format(bot_id)

    def handle_event(self, event, sender, level, formatted_msg, data):
        logger = logging.getLogger(type(sender).__name__)
        if formatted_msg:
            message = "[{}] {}".format(event, formatted_msg)
        else:
            message = '{}: {}'.format(event, str(data))
        getattr(logger, level)(message)

        requests.patch(self.LOG_URL, data=json.dumps({ self.index: '[{}] {}'.format(level, message) }))

        self.index = (self.index + 1) % 100
