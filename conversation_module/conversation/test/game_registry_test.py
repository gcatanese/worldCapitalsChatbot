import unittest
from conversation.game_registry import *


class GameRegistryTest(unittest.TestCase):

    def test_get_from_dict(self):
        init({'01': 'test'})

        self.assertIsNotNone(get_from_dict("01"))

    def test_get_none_from_dict(self):
        self.assertIsNone(get_from_dict("02"))

    def test_add_to_dict(self):
        add_to_dict('03', 'test3')
        self.assertIsNotNone(get_from_dict("03"))

    def test_remove_from_dict(self):
        init({'03': 'test3'})

        remove_from_dict('03')

        self.assertIsNone(get_from_dict("03"))
