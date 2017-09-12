import json
import requests
import os

slack_channel = os.getenv('SLACK_CHANNEL')


class SlackClient:

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def __init__(self, url):
        self.url = url

    def send_to_slack(self, data):
        requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return "OK"

    @staticmethod
    def prepare_data(text):
        final_data = {'channel': slack_channel, 'text': text, 'username': "Upsource BOT"}
        return final_data
