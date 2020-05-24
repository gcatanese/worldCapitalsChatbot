import logging
from conversation._intent import get_intent, Intent
from conversation._utterance import *
from conversation._model import *
from conversation.game_registry import *

from metrics.bot_metrics_connector import *

from game.game_mgr import *


def get_level(text):
    if text.lower() == 'easy':
        return 1
    elif text.lower() == 'medium':
        return 2
    elif text.lower() == 'difficult':
        return 3


class FlowManager:
    def __init__(self, id, channel, user):
        self.id = id
        self.channel = channel
        self.user = user

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

            send_metrics(text, self.user, self.channel)

        elif intent is Intent.HELP:
            response.append(TextMessage(say_help()))
        elif intent is Intent.BYE:
            response.append(TextMessage(say_bye()))
        elif intent is Intent.START_AGAIN:
            response.append(MultiItems(say_choose_your_level(), level_list()))
        elif intent is Intent.GAME_ON:
            # (re)start game
            game = create()
            game.load_questions(get_level(text))
            add_to_dict(self.id, game)

            n = game.next_question()
            response.append(QuizQuestion(n.question, n.options, n.answer))
        else:

            game = get_from_dict(self.id)

            answer = game.check(text)
            logging.info(f"{text}? {answer}")

            n = game.next_question()

            if n is None:
                if self.channel != 'telegram':
                    # feedback message (non-telegram channels)
                    self.get_feedback_on_answer(answer, response)

                score = f"{game.correct}/{game.total_questions}"
                response.append(TextMessage(score))
                if game.correct == game.total_questions:
                    response.append(TextMessage(say_well_done()))
                    response.append(TextMessage(say_well_done_emoji()))
                response.append(MultiItems("And now?", ["Start Again", "Goodbye"]))

                # record Game Over
                msg = f'Score {score}'
                send_metrics(text, self.user, self.channel)
            else:
                if self.channel != 'telegram':
                    # feedback message (non-telegram channels)
                    self.get_feedback_on_answer(answer, response)

                response.append(QuizQuestion(n.question, n.options, n.answer))

        return response
