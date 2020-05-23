
games: dict = {}


def init(init_dict):
    global games
    games = init_dict


def add_to_dict(key, value):
    games[key] = value


def get_from_dict(key):
    if key in games:
        return games[key]
    else:
        return None


def remove_from_dict(key):
    del games[key]