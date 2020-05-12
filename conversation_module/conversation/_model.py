
class TextMessage:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"message:{self.message}"


class MultiItems:

    def __init__(self):
        self.message = ""
        self.items = []

    def __init__(self, message, items):
        self.message = message
        self.items = items

    def __str__(self):
        return f"message:{self.message} items:{self.items}"


class MultiItemOption:
    def __init__(self):
        self.title = ""
        self.value = ""

    def __str__(self):
        return f"title:{self.title} value:{self.value}"
