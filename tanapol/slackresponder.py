class MessageResponder:

    def get_response(self, message):
        message = message.strip()
        if not message:
            return 'よんだ？'


message_responder = MessageResponder()
