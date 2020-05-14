class UserProfile:
    def __init__(self, name: str = None):
        self.name = name

    def __str__(self):
        return f"name:{self.name}"