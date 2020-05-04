import unittest

from game.question_mgr import *


class UtilsTest(unittest.TestCase):

    def test_get_bucket(self):
        bucket = get_bucket('Europe')
        print(bucket)

        self.assertIsNotNone(bucket)

    def test_get_buckets(self):
        buckets = get_buckets(3, 'Europe')

        self.assertEqual(3, len(buckets))

    def test_get_filtered_df(self):
        df = get_filtered_df('Asia')
        self.assertEqual(3, len(df))

    def test_get_df(self):
        df = get_df()
        self.assertIsNotNone(df)
