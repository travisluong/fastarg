import sys
import inspect
from inspect import signature

def deco(func):
    def inner():
        print("running inner()")
    return inner


@deco
def target():
    print('running target()')


import time
def clock(func):
    def clocked(*args): #
        t0 = time.perf_counter()
        result = func(*args) #
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    
    return clocked #

@clock
def snooze(seconds):
    time.sleep(seconds)



import time
import functools
def clock(func): 
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs) 
        elapsed = time.time() - t0 
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args)) 
            if kwargs:
                pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
                arg_lst.append(', '.join(pairs))
            arg_str = ', '.join(arg_lst)
            print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result)) 
        return result
    return clocked

@clock
def snooze(seconds: int, foo: str = "hello"):
    time.sleep(seconds)

import argparse

parser = argparse.ArgumentParser(prog='PROG', description="cli tool")
# parser.add_argument('--foo', action='store_true', help='foo help')
subparsers = parser.add_subparsers(help="alkjsdhfaklshdf")
commands = []

def cli(func):
    global commands
    commands.append(func.__name__)

    sig = signature(func)
    parser_a = subparsers.add_parser(func.__name__, help=func.__doc__)
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
        args = parser.parse_args()
        ka = dict(args._get_kwargs())
        func(**ka)
    return wrapped

@cli
def hello(name: str = 'foo', age: int = 1):
    """hello world asfa sdfasd fasd"""
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
    # print('non')
    # foo()
    # hello()
    # goodbye()
    # target()
    # snooze(5)
    # sig = signature(snooze)
    # print(sig.parameters.get("seconds").annotation)
    # annotation = sig.parameters.get("seconds").annotation
    
    # parser = argparse.ArgumentParser(description='Process some integers.')

    # for name, param in sig.parameters.items():
    #     print(param.kind, ':', name, '=', param.default)
    #     annotation = param.annotation
    #     parser.add_argument(name, type=annotation, help="foo")

    # args = parser.parse_args()
    # print(args)