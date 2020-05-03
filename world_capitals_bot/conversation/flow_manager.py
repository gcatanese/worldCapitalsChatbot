import logging
from conversation.intent import get_intent, Intent
from conversation.text_response import *
from conversation.multi_items_response import *


def next(text):

    response = ''

    intent = get_intent(text)
    logging.info(intent)

    if intent is Intent.GREET:
        response = response_to_greet()
        #responses.append(MultiItems("Choose your level", ["Easy", "Medium", "Difficult"]))

    elif intent is Intent.BYE:
        response = response_to_bye()
    elif intent is Intent.GAME_ON:
        # start game
        None
    else:
        multiItems = MultiItems()
        multiItems.message = 'What?'
        multiItems.items = ["a", "b", "c"]

        return multiItems

    return response