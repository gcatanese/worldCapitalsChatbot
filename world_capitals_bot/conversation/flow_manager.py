import logging
from conversation.intent import get_intent, Intent
from conversation.text_response import *
from conversation.multi_items_response import *

from game.game_mgr import *

game: Game = None


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
        global game
        game = create(get_level(text))
        logging.info(game)
        n = game.next_question()
        response = MultiItems(n.question, n.options)
    else:

        n = game.next_question()
        response = MultiItems(n.question, n.options)

    return response


def get_level(text):
    if text.lower() == 'easy':
        return 1
    elif text.lower() == 'medium':
        return 2
    elif text.lower() == 'high':
        return 3
