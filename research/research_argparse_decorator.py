import sys
import inspect
import argparse
import functools
from inspect import signature

# argparse example
parser = argparse.ArgumentParser(prog="prog", description="cli tool")
subparsers = parser.add_subparsers(help="subparser help")
commands = []

# cli decorator prototype
def cli(func):
    global commands
    commands.append(func.__name__)

    sig = signature(func)
    parser_a = subparsers.add_parser(func.__name__, help=func.__doc__)
    for name, param in sig.parameters.items():
        print(param.kind, ':', name, '=', param.default)
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
        args = parser.parse_args()
        ka = dict(args._get_kwargs())
        func(**ka)
    return wrapped

@cli
def hello(name: str = 'foo', age: int = 1):
    """hello world"""
    print("hello " + name + " " + str(age))

@cli
def goodbye(name: str, age: int = 2):
    print("goodbye " + name + " " + str(age))

@cli
def foo(published: bool = False):
    print('foo')

@cli
def bar(num: float):
    print('bar')
    print(num + 1.5)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != '-h':
        a = sys.argv[1]
        print(a)
        print(commands)
        command = a
        locals()[command]()
    else:
        args = parser.parse_args()
