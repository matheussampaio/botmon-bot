import ast
import json
import logging
import requests

logger = logging.getLogger('cli')

class Firebase(object):
    def __init__(self, url):
        self.url = url

    def child(self, url):
        return Firebase(self.url + url)

    def get(self, url = ''):
        json_object = requests.get(self.url + url + '.json').text

        try:
            logger.debug('%s : %s', self.url + url, json_object)

            if json_object == 'null':
                return None
            return ast.literal_eval(json_object)
        except ValueError:
            raise

    def delete(self, url = ''):
        return requests.delete(self.url + url + '.json')

    # def post(self, url = ''):
        # return requests.post(self.url + url + '.json')

    def update(self, payload, url = ''):
        return ast.literal_eval(requests.patch(self.url + url + '.json', data=json.dumps(payload)).text)
