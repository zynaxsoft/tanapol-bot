import os

import yaml

from flask import Flask, request

import tanapol
from tanapol.argparse import args
from tanapol import backlog
from tanapol import github
from tanapol import slack

app = Flask(__name__)

if args.secrets_file is None:
    secrets_path = os.path.join(tanapol.ROOT_DIR, 'secrets.yml')
else:
    secrets_path = args.secrets_file

with open(secrets_path, 'r') as secrets_file:
    secrets = yaml.load(secrets_file)

backlog_api_key = secrets['backlog']['api_key']
backlog_client = backlog.BacklogClient(backlog_api_key)
# print(backlog_client.check_auth())


github_token = secrets['github']['token']
github_client = github.GithubClient(github_token)

slack_token = secrets['slack']['token']
slack_client = slack.SlackClient(slack_token)
slack_event_server = slack.SlackEventServer()
# print(slack_client.peek_channel('tanapon-to-asobu', count=1))
# slack_client.react_latest_message('thumbsup', 'tanapon-to-asobu')


@app.route("/slack")
def slack_https():
    return slack_event_server.serve(request)

cert_path = secrets['https']['cert_path']
key_path= secrets['https']['key_path']
app.config['SERVER_NAME'] = 'oerba.tanapol.dev'
app.run(ssl_context=(cert_path, key_path),
        host='0.0.0.0',
        port=443,
        )
