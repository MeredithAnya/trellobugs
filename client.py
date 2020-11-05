import requests 
import json

# installation uuid, not sentry app uuid
INSTALL_UUID = "a3af8751-8030-48db-b22d-43b16ebee531"

ORG_BOARD_PATH = "/organizations/%s/boards"
MEMBER_ORG_PATH = "/members/me/organizations"
LISTS_OF_BOARD_PATH = "/boards/%s/lists"
NEW_CARD_PATH = "/cards"
SINGLE_CARD_PATH = "/cards/%s"
ADD_COMMENT_PATH = "/cards/%s/actions/comments"
MEMBER_BOARD_PATH = "/members/me/boards"
SEARCH_PATH = "/search"

CARD_FIELDS = ",".join(["name", "shortLink", "idShort"])

BOARD_ID = "5f99ad496f417967da6cf06a"

LISTS = [
    {
        'id': '5f9c470e572ea3086b7dfe36',
        'name': 'Unresolved',
        'closed': False,
        'pos': 65535,
        'softLimit': None,
        'idBoard': '5f99ad496f417967da6cf06a',
        'subscribed': False
    }, 
    {
        'id': '5f9c476ef2896b3a6c546d66',
        'name': 'Triaged',
        'closed': False,
        'pos': 131071,
        'softLimit': None,
        'idBoard': '5f99ad496f417967da6cf06a',
        'subscribed': False
    },
    {
        'id': '5f9c4773b9438307c6c74462',
        'name': 'Resolved',
        'closed': False,
        'pos': 196607,
        'softLimit': None,
        'idBoard': '5f99ad496f417967da6cf06a',
        'subscribed': False
    }
]

class TrelloClient(object):
    base_url = "https://api.trello.com/1"

    def request(self, method, path, data=None, params=None):
        headers = {"Content-Type": "application/json"}
        params = {} if params is None else params.copy()
        params["token"] = "369d2bd6fc655b9f583b5a1b37917221583d616533fff620fa1380a536bcd29c"
        params["key"] = "4f39b7a6f3d8174c8936d290ab4d5b7e"

        url = u"{}{}".format(self.base_url, path)
        if method == "GET":
            resp = requests.get(url, headers=headers, params=params)
        
        if method == "POST":
            resp = requests.post(url, headers=headers, data=data, params=params)

        if method == "PUT":
            resp = requests.put(url, headers=headers, data=data, params=params)

        resp.raise_for_status()
        return resp.json()

    def get_boards(self):
        # fields = "name,url"
        return self.request("GET", MEMBER_BOARD_PATH)
    
    def get_list_of_board(self):
        return self.request("GET", LISTS_OF_BOARD_PATH % BOARD_ID)

    def create_card(self, data):
        data["idList"] = "5f9c470e572ea3086b7dfe36"
        return self.request("POST", NEW_CARD_PATH, data=json.dumps(data))
    
    def resolve_card(self, card_id):
        url = SINGLE_CARD_PATH % card_id
        return self.request("PUT", url, data=json.dumps({"idList": "5f9c4773b9438307c6c74462"}))

        
class SentryClient(object):
    def get_external_issue(self, issue_id):
        """
        [
            {
            "serviceType": "bleep-bloop-9d4dc3",
            "webUrl": "https://trello.com/c/gVBDRpaC/2-typeerror-expected-bytes",
            "displayName": "BLOP#5f9c4f583a03ca1850e8e1ae",
            "id": "25675",
            "groupId": "1993829682"
            }
        ]
        """
        sentry_token = "124055265b004bc9a870bddd310f3e576ddec29028304a33984e137368126b3c"
        headers = {"Content-Type": "application/json"}
        headers["Authorization"] = "Bearer {}".format(sentry_token)
        url = u"https://sentry.io/api/0/organizations/meredith/issues/{}/external-issues/".format(issue_id)
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()


    def link_issue(self, card, event):
        issue_id = event["issue_url"].split("/")[-2]
        sentry_token = "124055265b004bc9a870bddd310f3e576ddec29028304a33984e137368126b3c"
        headers = {"Content-Type": "application/json"}
        headers["Authorization"] = "Bearer {}".format(sentry_token)
        url = u"https://sentry.io/api/0/sentry-app-installations/{}/external-issues/".format(INSTALL_UUID)
        data = {
            "action": "link",
            "groupId": issue_id,
            "uri": "/cards/link",
            "card_url": card["url"],
            "card_id": card["id"],
        }
        resp = requests.post(url, headers=headers, data=json.dumps(data))
        resp.raise_for_status()
        return resp.json()