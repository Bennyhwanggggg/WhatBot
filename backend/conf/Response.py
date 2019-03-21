class IntentResponse:
    def __init__(self, intent, message):
        self.intent = intent
        self.message = message


class FallbackResponse:
    def __init__(self, intent, message):
        self.intent = intent
        self.message = message

