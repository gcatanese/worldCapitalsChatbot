def response_with_options(question, items):
    multi_items = MultiItems()

    multi_items.message = question
    multi_items.items = items


class MultiItems:

    def __init__(self):
        self.message = ""
        self.items = []

    def __init__(self, message, items):
        self.message = message
        self.items = items

    def __str__(self):
        return f"message:{self.message} items:{self.items}"
