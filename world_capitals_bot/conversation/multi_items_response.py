
def response_with_options(question, items):
    multiItems = MultiItems()

    multiItems.message = question
    multiItems.items = items

class MultiItems:

    def __init__(self):
        self.message = ""
        self.items = []

    def __init__(self, message, items):
        self.message = message
        self.items = items

    def __str__(self):
        return f"message:{self.message} items:{self.items}"
