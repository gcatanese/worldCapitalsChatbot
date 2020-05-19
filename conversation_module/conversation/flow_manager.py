import logging
from conversation._intent import get_intent, Intent
from conversation._utterance import *
from conversation._model import *

from game.game_mgr import *

game: Game = None


def get_level(text):
    if text.lower() == 'easy':
        return 1
    elif text.lower() == 'medium':
        return 2
    elif text.lower() == 'difficult':
        return 3


class FlowManager:
    def __init__(self):
        None

    def __str__(self):
        return f"message:{self.message}"

    def say_intro(self):
        return TextMessage(say_intro())

    def get_feedback_on_answer(self, answer, response):
        if answer:
            response.append(TextMessage(say_correct()))
        else:
            response.append(TextMessage(say_incorrect()))

    def next(self, text):
        response = []

        intent = get_intent(text)

        if intent is Intent.GREET:
            response.append(TextMessage(say_hi()))
            response.append(TextMessage(say_intro()))
            response.append(MultiItems(say_choose_your_level(), level_list()))
        elif intent is Intent.HELP:
            response.append(TextMessage(say_help()))
        elif intent is Intent.BYE:
            response.append(TextMessage(say_bye()))
        elif intent is Intent.START_AGAIN:
            response.append(MultiItems(say_choose_your_level(), level_list()))
        elif intent is Intent.GAME_ON:
            # start game
            global game
            game = create(get_level(text))
            logging.info(game)

            n = game.next_question()
            # response.append(MultiItems(n.question, n.options))
            response.append(QuizQuestion(n.question, n.options, n.answer))
        else:

            answer = game.check(text)
            logging.info(f"{text}? {answer}")

            n = game.next_question()

            if n is None:
                #self.get_feedback_on_answer(answer, response)
                response.append(TextMessage(f"{game.correct}/{game.total_questions}"))
                if game.correct == game.total_questions:
                    response.append(TextMessage(say_well_done()))
                    response.append(TextMessage(say_well_done_emoji()))
                response.append(MultiItems("And now?", ["Start Again", "Goodbye"]))
            else:
                # self.get_feedback_on_answer(answer, response)
                # response.append(MultiItems(n.question, n.options))
                response.append(QuizQuestion(n.question, n.options, n.answer))

        return response
