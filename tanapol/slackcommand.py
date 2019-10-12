import abc
import argparse
import json
import os

import tanapol
from tanapol.argparse import db
from tanapol.log import logger


class Command(abc.ABC):

    def __init__(self, cargs, event):
        self.cargs = cargs
        self.event = event

    @abc.abstractmethod
    def execute(self):
        pass


class SubscribeChannelCommand(Command):

    def execute(self):
        if 'subscribed_channels' not in db:
            db['subscribed_channels'] = [self.event['channel']]
        else:
            if self.event['channel'] not in db['subscribed_channels']:
                db['subscribed_channels'].append(self.event['channel'])
        with open(tanapol.DB_PATH, 'w') as db_file:
            json.dump(db, db_file, indent=4, ensure_ascii=False)
        logger.info(f'Subscribed to channel_id {db["subscribed_channels"]}')
        return 'おおよ！'


class MyParser(argparse.ArgumentParser):

    def error(self, message):
        m = f'cannot parse {message}'
        raise argparse.ArgumentError(None, m)


def get_argparser():
    parser = MyParser()
    subparsers = parser.add_subparsers(dest='command')

    subscribe = subparsers.add_parser('subscribe')
    subscribe.set_defaults(command_cls=SubscribeChannelCommand)

    return parser


class CommandInvoker:

    parser = get_argparser()

    def execute_command(self, message, event):
        try:
            cargs = self.parser.parse_args(message.split(' '))
            command = cargs.command_cls(cargs, event)
            return command.execute()
        except argparse.ArgumentTypeError:
            return 'invalid command'
        except argparse.ArgumentError:
            return 'invalid command'


invoker = CommandInvoker()
