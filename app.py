from flask import Flask, request, jsonify, make_response
from github import Github, GithubException
import os

app = Flask(__name__)


@app.route('/')
def main():
    return "usage: POST https://token-requester.herokuapp.com/get-token\n{\"username\": \"<Github username>\",\"password\": \"<Github password>\"}"


@app.route('/tokenpls', methods=['POST'])
def get_token():
    try:
        token = token_collector(
            request.json["username"], request.json["password"])
        print(token)
    except KeyError:
        return result("missing username or password parameter", 2)
    if token == "":
        return result("bad credential", 1)
    return result(token, 0)


def token_collector(username, password):
    token = ""
    try:
        token = Github(username, password).get_user().\
            create_authorization(note="gf-ev-cli", client_id=os.
                                 getenv("GF_EV_CLIENT_ID"),
                                 client_secret=os.getenv("GF_EV_SECRET"),
                                 scopes=["repo", "read:org"]).token
    except (GithubException, AttributeError):
        pass
    return token


def result(message, returncode):
    return make_response(jsonify({"result": message, "returncode": returncode}))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
