
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


class QuizQuestion:

    def __init__(self):
        self.question = ""
        self.answers = []
        self.correct_answer = 0

    def __init__(self, question, answers, correct_answer):
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer

    def __str__(self):
        return f"question:{self.question} answers:{self.answers} correct_answer:{self.correct_answer}"

