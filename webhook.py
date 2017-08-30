from flask import Flask, request
import json
import requests
import os

slack_url = os.getenv('SLACK_WEBHOOK_URL')


def find_json_key(key, data):
    results = []
    data2 = json.dumps(data)

    def _decode_dict(a_dict):
        try:
            results.append(a_dict[key])
        except KeyError:
            pass
        return a_dict

    json.loads(data2, object_hook=_decode_dict)
    return results[0]

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    file = json.loads(request.data)
    print(file)
    if file['dataType'] == 'ReviewCreatedFeedEventBean':
        reviewid = find_json_key('reviewId', file)
        print(reviewid)

        botname = "Upsource BOT"
        text = "Review <https://url_to_my_upsource|%s> has been created" % reviewid

        url = slack_url
        data = {'text': text, 'username': botname}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        requests.post(url, data=json.dumps(data), headers=headers)

    else:
        print('Something else has happened')
    return "OK"

if __name__ == '__main__':
    app.run()




