import logging
from conversation.intent import get_intent, Intent
from conversation.response import *


def next(text):
    intent = get_intent(text)

    if intent is Intent.GREET:
        return response_to_greet()
    elif intent is Intent.BYE:
        return response_to_bye()
    elif intent is Intent.GAME_ON:
        # start game
        None