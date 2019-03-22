class IntentResponse:
    def __init__(self, intent, message, confidence):
        self.intent = intent
        self.message = message
        self.confidence = confidence


class FallbackResponse:
    def __init__(self, intent, message, confidence):
        self.intent = intent
        self.message = message
        self.confidence = confidence

