import unittest

from conversation._intent import *


class IntentTest(unittest.TestCase):

    def test_is_greet(self):
        self.assertTrue(is_greet("Hello"))

    def test_is_not_greet(self):
        self.assertFalse(is_greet("Bye"))
