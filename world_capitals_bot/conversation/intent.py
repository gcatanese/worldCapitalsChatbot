from enum import Enum
import logging


def get_intent(text):
    if is_greet(text):
        return Intent.GREET
    elif is_bye(text):
        return Intent.BYE
    elif is_game_on(text):
        return Intent.GAME_ON
    elif is_game_over(text):
        return Intent.GAME_OVER
    else:
        return None


def is_game_on(text):
    l = ['game on', 'lets start', 'lets go']

    return text.lower() in l


def is_game_over(text):
    l = ['game over']

    return text.lower() in l


def is_greet(text):
    l = ['hi', 'hello', 'good day']

    return text.lower() in l


def is_bye(text):
    l = ['bye', 'see you', 'goodbye']

    return text.lower() in l


class Intent(Enum):
    GREET = 1
    GAME_ON = 2
    GAME_OVER = 3
    BYE = 4
