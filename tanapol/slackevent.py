import abc
import json
import traceback

from flask import make_response

from tanapol.argparse import args, db
from tanapol.log import logger
from tanapol.slackcommand import invoker
from tanapol.slackresponder import message_responder
from tanapol.clients import slack_client


def post_message_event(func):
    def wrapper(self, event):
        if 'text' not in event or 'subtype' in event:
            return False
        return func(self, event)
    return wrapper


def reaction_event(func):
    def wrapper(self, event):
        if 'reaction' not in event:
            return False
        return func(self, event)
    return wrapper


def in_subscribed_channel(func):
    def wrapper(self, event):
        if 'subscribed_channels' not in db:
            return False
        try:
            if 'item' in event:
                channel = event['item']['channel']
            else:
                channel = event['channel']
        except KeyError:
            logger.error('this event does not contain channel information'
                         ' or it does not relate to channel'
                         )
            return False
        if channel not in db['subscribed_channels']:
            return False
        return func(self, event)
    return wrapper


def reply(message, event):
    if not message:
        return
    thread_ts = event.get('thread_ts', event['ts'])
    slack_client.post_message(message, event['channel'], thread_ts=thread_ts)


class EventHandler(abc.ABC):

    @abc.abstractmethod
    def can_handle(self, event):
        pass

    @abc.abstractmethod
    def handle(self, event):
        pass


class SubscribeEventHandler(EventHandler):

    mention_text = f'<@{args.user_id}>'

    @post_message_event
    def can_handle(self, event):
        _, is_command, self.command = event['text'] \
            .partition(f'{self.mention_text} ~')
        if 'subscribe' not in self.command:
            return False
        return True

    def handle(self, event):
        logger.info(f'executing command {self.command}')
        resp_message = invoker.execute_command(self.command, event)
        logger.info(f'Replying with message {resp_message}')
        reply(resp_message, event)


class UserMentionEventHandler(EventHandler):

    mention_text = f'<@{args.user_id}>'

    @in_subscribed_channel
    @post_message_event
    def can_handle(self, event):
        if self.mention_text not in event['text']:
            return False
        channel = event['channel']
        if not db['subscribed_channels'][channel]['auto_reply']:
            return False
        return True

    def handle(self, event):
        _, is_command, command = event['text'] \
            .partition(f'{self.mention_text} ~')
        if is_command:
            logger.info(f'executing command {command}')
            resp_message = invoker.execute_command(command, event)
            logger.info(f'Replying with message {resp_message}')
            reply(resp_message, event)
        _, _, message = event['text'].partition(f'{self.mention_text}')
        reply_message = message_responder.get_response(message)
        reply(reply_message, event)


class OtherUserAddedReactionEventHandler(EventHandler):

    @in_subscribed_channel
    @reaction_event
    def can_handle(self, event):
        if event['type'] != 'reaction_added':
            return False
        if event['user'] == args.user_id:
            return False
        return True

    def handle(self, event):
        channel = event['item']['channel']
        if db['subscribed_channels'][channel]['repeat_reaction']:
            logger.info('adding reaction')
            slack_client.react_message(event['reaction'],
                                       event['item']['channel'],
                                       event['item']['ts'],
                                       )


class OtherUserRemovedReactionEventHandler(EventHandler):

    @in_subscribed_channel
    @reaction_event
    def can_handle(self, event):
        if event['type'] != 'reaction_removed':
            return False
        if event['user'] == args.user_id:
            return False
        return True

    def handle(self, event):
        channel = event['item']['channel']
        if db['subscribed_channels'][channel]['repeat_reaction']:
            logger.info('removing reaction')
            slack_client.remove_react(event['reaction'],
                                      event['item']['channel'],
                                      event['item']['ts'],
                                      )


EVENT_HANDLERS = [
    SubscribeEventHandler(),
    UserMentionEventHandler(),
    OtherUserAddedReactionEventHandler(),
    OtherUserRemovedReactionEventHandler(),
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
            except Exception:
                logger.error(traceback.format_exc())
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
        data_show = json.dumps(data, indent=2, ensure_ascii=False)
        logger.debug(f'Event info: {data_show}')
        for handler in EVENT_HANDLERS:
            event = data['event']
            if handler.can_handle(event):
                logger.debug(f'{type(self).__name__} is handling the event.')
                return handler.handle(event)
            else:
                logger.debug(f'{type(handler).__name__} could not handle'
                             f' the event.')
