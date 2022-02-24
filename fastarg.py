import sys
import inspect
from inspect import signature
import functools
import argparse

class Fastarg:
    def __init__(self):
        self.commands = []
        self.parser = argparse.ArgumentParser(prog="PROG", description="cli tool")
        self.subparsers = self.parser.add_subparsers(help="asdasdfasdf")

    def command(self):
        def decorator(func):
            self.commands.append(func.__name__)

            sig = signature(func)
            parser_a = self.subparsers.add_parser(func.__name__, help=func.__doc__)
            for name, param in sig.parameters.items():
                # print(param.kind, ':', name, '=', param.default)
                annotation = param.annotation
                if annotation is bool:
                    action = argparse.BooleanOptionalAction
                else:
                    action = None
                
                if param.default is inspect._empty:
                    arg_name = name
                    parser_a.add_argument(arg_name, type=annotation, help=f"type: {annotation.__name__}", default=param.default, action=action)
                else:
                    arg_name = '--' + name
                    parser_a.add_argument(arg_name, type=annotation, help=f"type: {annotation.__name__}", default=param.default, action=action)

            @functools.wraps(func)
            def wrapped(*args, **kwargs):
                args = self.parser.parse_args()
                ka = dict(args._get_kwargs())
                func(**ka)
            return wrapped

        return decorator

    def run(self):
        self.parser.parse_args()

    def add_fastarg(self, fastarg, name=None):
        # self.subparsers.add_parser(name)
        print(fastarg)


app = Fastarg()

@app.command()
def hello(name: str = 'foo', age: int = 1):
    """hello world asfa sdfasd fasd"""
    print("hello " + name + " " + str(age))

@app.command()
def goodbye(name: str, age: int = 2):
    print("goodbye " + name + " " + str(age))

@app.command()
def foo(published: bool = False):
    print('foo')

@app.command()
def bar(num: float):
    print('bar')
    print(num + 1.5)

app.run()