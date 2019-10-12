from tanapol.log import logger


class MessageResponder:

    def get_response(self, message):
        message = message.strip()
        if not message:
            return 'よんだ？'
        logger.info(f'No suitable response with message {message}')
        return ''


message_responder = MessageResponder()
