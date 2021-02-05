class RecordPerMinute(Exception):

    BASE_MESSAGE = 'Record creation limit per minute'

    def __init__(self, salary, message=None):
        self.salary = salary
        self.message = message if message else self.BASE_MESSAGE
        super().__init__(self.message)

class GoogleApiError(Exception):

    BASE_MESSAGE = 'An error occurred while getting the url of the book'

    def __init__(self, salary, message=None):
        self.salary = salary
        self.message = message if message else self.BASE_MESSAGE
        super().__init__(self.message)