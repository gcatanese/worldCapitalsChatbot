import unittest

from game.game_mgr import *


class GameMgtTest(unittest.TestCase):

    def setUp(self):
        set_file_path('../data/country-capitals.csv')

    def test_create(self):
        game = create()

        self.assertIsNotNone(game)
        self.assertEqual(5, game.total_questions)

    def test_load_questions(self):
        game = create()
        game.load_questions(1)

        self.assertIsNotNone(game)
        self.assertEqual(5, len(game.questions))

        print(game.questions[0])

    def test_next(self):
        game = self.create_mock()
        next_question = game.next_question()

        self.assertIsNotNone(next_question)
        self.assertEqual(0, game.current)

        print(next_question)

    def test_next_question_none(self):
        game = self.create_mock()

        next_question = game.next_question()
        self.assertIsNotNone(next_question)

        next_question = game.next_question()
        self.assertIsNotNone(next_question)

        next_question = game.next_question()
        self.assertIsNone(next_question)

    def test_check_answer(self):
        game = self.create_mock()

        next_question = game.next_question()
        self.assertIsNotNone(next_question)

        print(next_question)

        self.assertTrue(game.check('AMSTERDAM'))
        self.assertFalse(game.check('LONDON'))

    def create_mock(self):
        game = Game(2)

        questions = []

        b1 = Bucket()
        b1.question = 'What is the capital of NL?'
        b1.answer = 'Amsterdam'
        b1.options = ['Milan', 'Paris', 'Amsterdam']

        b2 = Bucket()
        b2.question = 'What is the capital of UK?'
        b2.answer = 'London'
        b2.options = ['Milan', 'London', 'Amsterdam']

        questions.append(b1)
        questions.append(b2)

        game.questions = questions

        return game
