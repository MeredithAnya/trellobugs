import os
import sentry_sdk

from flask import Flask, json, request, Response

from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk import push_scope, capture_exception

from client import TrelloClient, SentryClient
from utils import get_release_sha

sentry_sdk.init(
    dsn="https://4c0b4d78a85e4531a128a4730cd4c70b@o49697.ingest.sentry.io/4511291",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    release=get_release_sha()
)

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "GET":
        return "Hello"

    if request.method == "POST":
        # check the webhook event type 
        resource = request.headers.get("Sentry-Hook-Resource") 
        if resource == "issue":
            issue = request.json["data"]["issue"]
            # look up external issue and get trello card id
            external_issue = SentryClient().get_external_issue(issue["id"])
            if external_issue:
                card_id = external_issue["displayName"].split("#")[1]
                TrelloClient().resolve_card(card_id)
                return Response(status=200)
            
            return Response(status=404)
        
        if resource == "event_alert":
            event = request.json["data"]["event"]
            name = event["title"]
            url = event["web_url"]
            desc = "Sentry Event: [Take me der]({})".format(url)

            card = TrelloClient().create_card({"name": name, "desc": desc})

            SentryClient().link_issue(card, event)
            return Response(status=201)

@app.route('/cards/create', methods=['POST'])
def create_card():
    fields = request.json["fields"]

    name = fields["title"]
    desc = fields["description"]
    card = TrelloClient().create_card({"name": name, "desc": desc})
    
    data = {
        "identifier": card["id"],
        "webUrl": card["url"],
        "project": "SentryBugs"
    }

    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    return response 

@app.route('/cards/link', methods=['POST'])
def link_card():
    fields = request.json["fields"]

    data = {
        "identifier": fields["card_id"],
        "webUrl": fields["card_url"],
        "project": "SentryBugs"
    }
    
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    return response 

@app.route('/boards', methods=['GET'])
def boards():
    boards = TrelloClient().get_boards()
    data = []
    for b in boards:
        data.append({
            "label": b["name"],
            "value": b["id"]
        })
    
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    return response

@app.route('/bugs', methods=['GET'])
def bugs():
    try:
        wqokayyq()
    except Exception as e:
        with push_scope() as scope:
            scope.set_tag("plan", "enterprise")
            capture_exception(e)
            return "OOPS"


if __name__ == '__main__':
    app.run()