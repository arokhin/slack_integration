from flask import Flask, request
import json
import os
from SlackClient import SlackClient
from JsonParser import JsonObject


SlackUrl = os.getenv('SLACK_WEBHOOK_URL')
UpsourceUrl = os.getenv('UPSOURCE_BASE_URL')
SlackChannel = os.getenv('SLACK_CHANNEL')

client = SlackClient(SlackUrl)

app = Flask(__name__)


@app.route('/', methods=['POST'])


def index():
    json_payload = json.loads(request.data)

    supported_events = ["ReviewCreatedFeedEventBean", "MergedToDefaultBranchEventBean"]

    while json_payload['dataType'] in supported_events:
        pass

        project_id = JsonObject(json_payload).find_json_key('reviewId')

        if json_payload['dataType'] == 'ReviewCreatedFeedEventBean':

            review_id = JsonObject(json_payload).find_json_key('reviewId')
            review_url = UpsourceUrl + '/' + project_id + '/' + "review" + '/' + review_id
            text = "Review <%s|%s> has been created" % (review_url, review_id)

            client.send_to_slack(client.prepare_data(text))

        if json_payload['dataType'] == 'MergedToDefaultBranchEventBean':

            branch_id = JsonObject(json_payload).find_json_key('branches')[0]
            branch_url = UpsourceUrl + '/' + project_id + '/' + "branch" + '/' + branch_id
            text = "Branch <%s|%s> has been merged to master" % (branch_url, branch_id)

            client.send_to_slack(client.prepare_data(text))

        return "OK"

if __name__ == '__main__':
    app.run()
