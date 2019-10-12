import json

import requests

from tanapol.log import logger


API_URL = 'https://slack.com/api'


class SlackResponse:

    def __init__(self, response):
        self.response = response
        self.content = response.json()
        response_show = json.dumps(self.content, indent=2, ensure_ascii=False)
        logger.debug(f'response {response_show}')
        self._log_error()

    def _log_error(self):
        try:
            if self.content['error'] == 'already_reacted':
                logger.warning(f'Message with timestamp'
                               f' is already reacted.')
            else:
                logger.error(self)
        except KeyError:
            pass

    def __repr__(self):
        return json.dumps(self.content,
                          indent=2,
                          ensure_ascii=False)

    def __bool__(self):
        if self.content['ok']:
            return True
        else:
            logger.error(f'slack api error: {self.content["error"]}')
            return False


class SlackClient:

    def __init__(self, secret):
        self.post_auth_headers = {
            'Content-type': 'application/json',
            'Authorization': f'Bearer {secret}',
            }
        self.get_auth_headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            }
        self.get_auth_params = {
            'token': secret,
            }

    def _get(self, entry, **request_params):
        params = dict(self.get_auth_params)
        params.update(request_params)
        response = requests.get(f'{API_URL}{entry}',
                                params=params,
                                headers=self.get_auth_headers,
                                )
        return SlackResponse(response)

    def _post(self, entry, **data):
        json_data = json.dumps(data)
        response = requests.post(f'{API_URL}/{entry}',
                                 headers=self.post_auth_headers,
                                 data=json_data,
                                 )
        return SlackResponse(response)

    def check_auth(self):
        return bool(self._get('/channels.list'))

    def get_channel_id(self, channel_name):
        data = self._get('/conversations.list',
                         types='public_channel, private_channel',
                         )
        channels = data.content['channels']
        for channel in channels:
            if channel['name'] == channel_name:
                return channel['id']

    def peek_channel(self, channel_name=None, channel_id=None, count=3):
        if channel_name is not None and channel_id is None:
            channel_id = self.get_channel_id(channel_name)
        return self._get('/conversations.history',
                         channel=channel_id,
                         count=count,
                         )

    def _react_message(self, reaction, channel_id, timestamp):
        self._post('/reactions.add',
                    name=reaction,
                    timestamp=timestamp,
                    channel=channel_id,
                    )

    def react_latest_message(self, reaction, channel):
        channel_id = self.get_channel_id(channel)
        data = self.peek_channel(channel_id=channel_id, count=1)
        message = data.content['messages'][0]
        self._react_message(reaction, channel_id, message['ts'])

    def post_message(self, message, channel_id, thread_ts=None):
        self._post('/chat.postMessage',
                   channel=channel_id,
                   text=message,
                   thread_ts=thread_ts,
                   # icon_emoji=':+1:',
                   as_user=True,
                   )
