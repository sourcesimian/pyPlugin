from tests.base import Parser1


class Foo(Parser1):
    def visit(self, foo):
        return 'bar'
