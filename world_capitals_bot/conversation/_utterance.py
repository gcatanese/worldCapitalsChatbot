import random


def say_hi():
    options = ['Hello', 'Hi', "Goodday", 'Hallo', "Hey!"]

    return random.choice(options)


def say_intro():
    options = ["Do you know all capitals? Test your knowledge", "Are you a world's capital expert? Lets see"]

    return random.choice(options)


def say_bye():
    options = ['Bye', 'Have a good day']

    return random.choice(options)


def say_thank_you():
    options = ['Thank You', 'Thanks', "Many thanks"]

    return random.choice(options)


def say_well_done():
    options = ['You are the one!', 'Spot on champion!!', 'Amazing! 🥇']

    return random.choice(options)
