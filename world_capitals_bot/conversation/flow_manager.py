import logging
from conversation.intent import get_intent, Intent
from conversation._utterance import *
from conversation._model import *

from game.game_mgr import *

game: Game = None


def next(text):
    response = []

    intent = get_intent(text)

    if intent is Intent.GREET:
        response.append(TextMessage(say_hi()))
        response.append(TextMessage(say_intro()))
        response.append(MultiItems("Choose your level", ["Easy", "Medium", "Difficult"]))
    elif intent is Intent.START:
        response.append(MultiItems("Choose your level", ["Easy", "Medium", "Difficult"]))
    elif intent is Intent.BYE:
        response.append(TextMessage(say_bye()))
    elif intent is Intent.GAME_ON:
        # start game
        global game
        game = create(get_level(text))
        logging.info(game)

        n = game.next_question()
        response.append(MultiItems(n.question, n.options))
    else:

        answer = game.check(text)
        logging.info(f"{text}? {answer}")

        n = game.next_question()

        if n is None:
            get_feedback_on_answer(answer, response)
            response.append(TextMessage(f"{game.correct}/{game.total_questions}"))
            if game.correct == game.total_questions:
                response.append(TextMessage(say_well_done()))
                response.append(TextMessage(say_well_done_emoji()))
            response.append(MultiItems("And now?", ["Start Again", "Goodbye"]))
        else:
            get_feedback_on_answer(answer, response)
            response.append(MultiItems(n.question, n.options))

    return response


def get_feedback_on_answer(answer, response):
    if answer:
        response.append(TextMessage(say_correct()))
    else:
        response.append(TextMessage(say_incorrect()))


def get_level(text):
    if text.lower() == 'easy':
        return 1
    elif text.lower() == 'medium':
        return 2
    elif text.lower() == 'difficult':
        return 3
