import random


def response_to_greet():
    responses = ['Hello', 'Welcome']

    return random.choice(responses)


def response_to_bye():
    responses = ['Bye', 'Have a good day']

    return random.choice(responses)