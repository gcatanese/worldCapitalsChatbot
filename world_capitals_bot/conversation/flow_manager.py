import logging
from conversation.intent import get_intent, Intent
from conversation.text_response import *
from conversation.multi_items_response import *


def next(text):
    response = ''

    intent = get_intent(text)
    logging.info(intent)

    if intent is Intent.GREET:
        response = MultiItems("Choose your level", ["Easy", "Medium", "Difficult"])
    elif intent is Intent.BYE:
        response = response_to_bye()
    elif intent is Intent.GAME_ON:
        # start game
        response = MultiItems("What?", ["1", "2", "3"])
    else:
        response = MultiItems("What?", ["a", "b", "c"])

    return response
