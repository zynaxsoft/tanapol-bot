from threading import Thread

from flask import Flask, request

from tanapol.argparse import secrets
from tanapol.log import logger
from tanapol.slackevent import SlackEventServer

app = Flask(__name__)


slack_event_server = SlackEventServer()


def process_data(data):
    return slack_event_server.serve(data)


@app.route("/slack", methods=['POST'])
def slack_https():
    data = request.get_json()
    if data is None:
        logger.error(f'Slack event server got none json message.'
                     f'args: {request.args}, data: {request.data}'
                     )
        return 'OK'
    thread = Thread(target=process_data, args=(data,))
    thread.start()
    logger.info(f'Responding to slack with OK')
    return 'OK'


cert_path = secrets['https']['cert_path']
key_path = secrets['https']['key_path']
app.config['SERVER_NAME'] = 'oerba.tanapol.dev'


if __name__ == '__main__':
    app.run(ssl_context=(cert_path, key_path),
            host='0.0.0.0',
            port=443,
            )
