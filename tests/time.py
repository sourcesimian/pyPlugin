from tests.base import Parser1


class Time(Parser1):
    def tick(self):
        return 'tock'
