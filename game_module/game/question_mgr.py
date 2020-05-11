import pandas as pd
import gettext

from random import sample

NUM_MULTI_CHOICE_OPTIONS = 3
#DATA_FILE_PATH = '../data/country-capitals.csv'
DATA_FILE_PATH = '../game_module/game/data/country-capitals.csv'

_ = gettext.gettext


def get_buckets(num, level):
    list = []

    for x in range(num):
        list.append(get_bucket(level))

    return list


def get_bucket(level):
    df = get_filtered_df(level)

    bucket = Bucket()

    bucket.question = get_question(df)
    bucket.answer = get_answer(df)
    bucket.options = get_options(df)

    return bucket


def get_filtered_df(level):
    df = get_df()

    df = df[df['Level'] == level].sample(n=NUM_MULTI_CHOICE_OPTIONS)

    return df


def get_question(df):
    return _("What is the capital of ") + df.iloc[0].CountryName + "?"


def get_answer(df):
    return df.iloc[0].CapitalName


def get_options(df):
    items = df['CapitalName'].tolist()
    return sample(items, len(items))


def get_df():
    return pd.read_csv(get_filename())


def get_filename():
    return DATA_FILE_PATH


class Bucket:

    def __init__(self):
        self.question = ""
        self.answer = ""
        self.options = []

    def __str__(self):
        return f"question:{self.question} answer:{self.answer} options:{self.options}"