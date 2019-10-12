from tanapol.argparse import args, secrets
from tanapol import backlog
from tanapol import github
from tanapol import slack


backlog_api_key = secrets['backlog']['api_key']
backlog_client = backlog.BacklogClient(backlog_api_key)
# print(backlog_client.check_auth())

github_token = secrets['github']['token']
github_client = github.GithubClient(github_token)

slack_token = secrets['slack']['token']
slack_client = slack.SlackClient(slack_token)
# print(slack_client.peek_channel('tanapon-to-asobu', count=1))
# slack_client.react_latest_message('thumbsup', 'tanapon-to-asobu')
