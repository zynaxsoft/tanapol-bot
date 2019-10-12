import abc
import json

from flask import make_response

from tanapol.argparse import args
from tanapol.log import logger
from tanapol.clients import (github_client,
                             slack_client,
                             backlog_client,
                             )


def post_message_event(func):
    def wrapper(self, event):
        if 'text' not in event or 'subtype' in event:
            return False
        return func(self, event)
    return wrapper


class EventHandler(abc.ABC):

    @abc.abstractmethod
    def can_handle(self, event):
        pass

    @abc.abstractmethod
    def handle(self, event):
        pass


class UserMentionEventHandler(EventHandler):

    mention_text = f'<@{args.user_id}>'

    @post_message_event
    def can_handle(self, event):
        text = event['text']
        if self.mention_text in text:
            return True
        return False

    def handle(self, event):
        slack_client.post_message(message='hai',
                                  channel_id=event['channel'],
                                  thread_ts=event['ts'],
                                  )


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
            try:
                self._handle_event(data)
            except Exception as error:
                logger.error(error)
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
        for handler in EVENT_HANDLERS:
            event = data['event']
            if handler.can_handle(event):
                logger.debug(f'{type(self).__name__} is handling the event.')
                handler.handle(event)
            else:
                logger.debug(f'{type(handler).__name__} could not handle'
                             f' the event.')
