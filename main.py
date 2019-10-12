import os

from flask import Flask, request

import tanapol
from tanapol.argparse import args, secrets
from tanapol.slackevent import SlackEventServer

app = Flask(__name__)


slack_event_server = SlackEventServer()


@app.route("/slack", methods=['POST'])
def slack_https():
    return slack_event_server.serve(request)


cert_path = secrets['https']['cert_path']
key_path= secrets['https']['key_path']
app.config['SERVER_NAME'] = 'oerba.tanapol.dev'


if __name__ == '__main__':
    from tanapol.log import logger
    logger.info('yes')
    app.run(ssl_context=(cert_path, key_path),
            host='0.0.0.0',
            port=443,
            )
