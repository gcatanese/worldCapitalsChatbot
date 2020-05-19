
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
        self.correct_answer = ""
        self.correct_answer_position = -1

    def __init__(self, question, answers, correct_answer):
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer
        self.correct_answer_position = self.__get_correct_answer_position__()

    def __get_correct_answer_position__(self):
        ret = -1

        i = 0
        for answer in self.answers:
            if answer.lower() == self.correct_answer.lower():
                ret = i
                break
            i = i + 1

        return ret

    def __str__(self):
        return f"question:{self.question} answers:{self.answers} correct_answer:{self.correct_answer} correct_answer_position:{self.correct_answer_position} "

