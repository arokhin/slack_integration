from flask import Flask, request
import json
import requests
import os

slack_url = os.getenv('SLACK_WEBHOOK_URL')
upsource_url = os.getenv('UPSOURCE_BASE_URL')
slack_channel = os.getenv('SLACK_CHANNEL')


def find_json_key(key, data):
    results = []
    in_json = json.dumps(data)

    def _decode_dict(a_dict):
        try:
            results.append(a_dict[key])
        except KeyError:
            pass
        return a_dict

    json.loads(in_json, object_hook=_decode_dict)
    return results[0]


def create_payload(text):
    final_data = {'channel': slack_channel, 'text': text, 'username': "Upsource BOT"}
    return final_data


class SlackClient:
    def __init__(self, url):
        self.url = url
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def send_to_slack(self, data):
        requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return "OK"

client = SlackClient(slack_url)

app = Flask(__name__)


@app.route('/', methods=['POST'])



def index():
    json_payload = json.loads(request.data)
    print(json_payload)
    supported_events = ["ReviewCreatedFeedEventBean", "MergedToDefaultBranchEventBean"]

    while json_payload['dataType'] in supported_events:
        pass

        project_id = find_json_key('projectId', json_payload)

        if json_payload['dataType'] == 'ReviewCreatedFeedEventBean':

            review_id = find_json_key('reviewId', json_payload)
            review_url = upsource_url + '/' + project_id + '/' + "review" + '/' + review_id

            text = "Review <%s|%s> has been created" % (review_url, review_id)

            client.send_to_slack(create_payload(text))

        if json_payload['dataType'] == 'MergedToDefaultBranchEventBean':

            branch_id = find_json_key('branches', json_payload)[0]
            branch_url = upsource_url + '/' + project_id + '/' + "branch" + '/' + branch_id

            text = "Branch <%s|%s> has been merged to master" % (branch_url, branch_id)

            client.send_to_slack(create_payload(text))

        return "OK"

if __name__ == '__main__':
    app.run()
