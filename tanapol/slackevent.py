import abc
import json

from flask import make_response

from tanapol.log import logger
from tanapol.clients import (github_client,
                             slack_client,
                             backlog_client,
                             )


class EventHandler(abc.ABC):

    @abc.abstractmethod
    def can_handle(self, data):
        pass

    @abc.abstractmethod
    def handle(self, data):
        pass


class UserMentionEventHandler(EventHandler):

    def can_handle(self, data):
        pass

    def handle(self, data):
        pass


EVENT_HANDLERS = [
    UserMentionEventHandler(),
    ]


class SlackEventServer:

    def __init__(self):
        pass

    def serve(self, request):
        data = request.get_json()
        if data is None:
            logger.error(f'Slack event server got none json message.'
                         f'args: {request.args}, data: {request.data}'
                         )
            return self._response_code(404)
        if 'challenge' in data:
            return self._response_challenge(data['challenge'])
        else:
            self._handle_event(data)
            return self._response_code(200)
        return self._response_code(404)

    def _response_code(self, code):
        response = make_response()
        response.status = str(code)
        return response

    def _response_challenge(self, challenge_key):
        response = make_response()
        response.status = '200'
        response.headers['Content-Type'] = 'application/json'
        response.data = json.dumps(
            {
                'challenge': challenge_key,
                }
            )
        return response

    def _handle_event(self, data):
        logger.debug(f'Event info: {json.dumps(data, indent=2)}')
