import json
import os
from flask import Flask, request
from src.JsonParser import JsonObject
from src.SlackClient import SlackClient


SlackUrl = os.getenv('SLACK_WEBHOOK_URL')
UpsourceUrl = os.getenv('UPSOURCE_BASE_URL')
SlackChannel = os.getenv('SLACK_CHANNEL')

client = SlackClient(SlackUrl)


def find_project_id(json_payload):
    project_id = JsonObject(json_payload).find_json_key('projectId')
    return project_id


def find_review_url(project_id, review_id):
    review_url = UpsourceUrl + '/' + project_id + '/' + "review" + '/' + review_id
    return review_url


def find_review_id(json_payload):
    review_id = JsonObject(json_payload).find_json_key('reviewId')
    return review_id


def find_branch_url(json_payload, branch_id):
    branch_url = UpsourceUrl + '/' + find_project_id(json_payload) + '/' + "branch" + '/' + branch_id
    return branch_url


def find_user_name(json_payload):
    userName = JsonObject(json_payload).find_json_key('userName')
    return userName


def find_user_id_url(json_payload):
    user_id_url = UpsourceUrl + "user" + '/' + JsonObject(json_payload).find_json_key("userId")
    return user_id_url


app = Flask(__name__)


@app.route('/', methods=['POST'])


def index():
    json_payload = json.loads(request.data)

    print(json_payload)

    supported_events = ["ReviewCreatedFeedEventBean", "MergedToDefaultBranchEventBean",
                        "ReviewStateChangedFeedEventBean", "NewBranchEventBean"]

    # TODO: Not implemented events
    # ParticipantStateChangedFeedEventBean
    # RemovedParticipantFromReviewFeedEventBean
    # NewParticipantInReviewFeedEventBean
    # NewRevisionEventBean

    while json_payload['dataType'] in supported_events:
        pass

        project_id = find_project_id(json_payload)

        if json_payload['dataType'] == "ReviewCreatedFeedEventBean":

            review_id = find_review_id(json_payload)
            review_url = find_review_url(project_id, review_id)
            review_creator = find_user_name(json_payload)
            creator_url = find_user_id_url(json_payload)
            text = "Review <%s|%s> has been created by <%s|%s>." % (review_url, review_id, creator_url, review_creator)

            client.send_to_slack(client.prepare_data(text))

        if json_payload['dataType'] == "MergedToDefaultBranchEventBean":

            branch_id = JsonObject(json_payload).find_json_key('branches')[0]
            branch_url = find_branch_url(json_payload, branch_id)
            text = "Branch <%s|%s> has been merged to master" % (branch_url, branch_id)

            client.send_to_slack(client.prepare_data(text))

        if json_payload['dataType'] == "ReviewStateChangedFeedEventBean":

            review_id = find_review_id(json_payload)
            review_url = find_review_url(project_id, review_id)

            if JsonObject(json_payload).find_json_key('newState') == 1:
                text = "Review <%s|%s> has been closed" % (review_url, review_id)

            else:
                text = "Review <%s|%s> has been reopened" % (review_url, review_id)

            client.send_to_slack(client.prepare_data(text))

        if json_payload['dataType'] == "NewBranchEventBean":

            branch_id = JsonObject(json_payload).find_json_key('name')
            branch_url = find_branch_url(json_payload, branch_id)
            text = "New branch has been created: <%s|%s> " % (branch_url, branch_id)

            client.send_to_slack(client.prepare_data(text))

        return "OK"

    else:
        return '501'

if __name__ == '__main__':
    app.run()
