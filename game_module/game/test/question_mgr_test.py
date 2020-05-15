import unittest

from game.question_mgr import *


class QuestionMgtTest(unittest.TestCase):

    def test_get_bucket(self):
        bucket = get_bucket(1)

        self.assertIsNotNone(bucket)

    def test_get_buckets(self):
        buckets = get_buckets(3, 1)

        self.assertEqual(3, len(buckets))

    def test_get_filtered_df(self):
        df = get_filtered_df(1)
        self.assertEqual(3, len(df))

    def test_get_df(self):
        df = get_df()
        self.assertIsNotNone(df)

