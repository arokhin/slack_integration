from flask import Flask, request
import json
import requests
import os

slack_url = os.getenv('SLACK_WEBHOOK_URL')
upsource_url = os.getenv('UPSOURCE_BASE_URL')
botname = "Upsource BOT"


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

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    file = json.loads(request.data)
    print(file)
    if file['dataType'] == 'ReviewCreatedFeedEventBean':
        reviewid = find_json_key('reviewId', file)
        print(reviewid)

        text = "Review <%s|%s> has been created" % (upsource_url, reviewid)
        data = {'channel': '#general', 'text': text, 'username': botname}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        requests.post(slack_url, data=json.dumps(data), headers=headers)

        print(data)
    else:
        print('Something else has happened')
    return "OK"

if __name__ == '__main__':
    app.run()




