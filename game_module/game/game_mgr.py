from conversation._model import MultiItemOption
from game.question_mgr import *

NUM_QUESTIONS = 5


def game_list():
    return [MultiItemOption("World Capitals", "World Capitals"), MultiItemOption("Flags!", "Flags")]


def level_list():
    return [MultiItemOption("Easy", "Easy"), MultiItemOption("Medium", "Medium"),
            MultiItemOption("Difficult", "Difficult")]


def create(level, num_questions=None):
    if num_questions is None:
        num_questions = NUM_QUESTIONS

    game = Game(num_questions)

    game.questions = get_buckets(NUM_QUESTIONS, level)

    return game


class Game:

    def __init__(self, total_questions):
        self.questions = Bucket
        self.current = -1
        self.total_questions = total_questions
        self.score = 0
        self.correct = 0
        self.incorrect = 0

    def next_question(self):

        self.current = self.current + 1

        if self.current == self.total_questions:
            return None

        question = self.questions[self.current]

        return question

    def check(self, answer):

        res = True if answer.lower() == self.questions[self.current].answer.lower() else False

        if res:
            self.correct = self.correct + 1
        else:
            self.incorrect = self.incorrect + 1

        return res

    def __str__(self):
        return f"total_questions:{self.total_questions} current:{self.current} score:{self.score}"
