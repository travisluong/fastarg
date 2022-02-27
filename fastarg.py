from __future__ import annotations
import sys
import inspect
from inspect import signature
import functools
import argparse

class Command:
    def __init__(self, function):
        self.function = function

    def get_name(self):
        return self.function.__name__

class Fastarg:
    def __init__(self):
        self.commands = []

        # fastarg branches
        self.fastargs = []

    def command(self):
        def decorator(func):
            self.commands.append(Command(func))

        return decorator

    def commandb(self):
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
        # self.parser.parse_args()
        # print(self.commands)

        # recursively parse all child fastargs

        # if root fastarg, then generate the root parser object
        self.parser = argparse.ArgumentParser(prog="root parser", description="root cli")

        # after root is generated, traverse tree of fastargs
        self.traverse_fastargs(self)

        # finally, parse the arguments
        args = self.parser.parse_args()
        print(args)

        print(sys.argv)

        argqueue = sys.argv[1:]

        # traverse tree of fastargs for the subparser or command to invoke
        self.search_to_invoke(self, argqueue, args)

    def search_to_invoke(self, fastarg, argqueue, commandargs):
        print(f"argqueue: {argqueue}")
        arg = None
        if len(argqueue) > 0:
            arg = argqueue.pop(0)

        if not arg:
            return

        # print(arg)
        # print(fastarg.subparsers.choices)
        # search fastargs for name of current sys argv
        for cfastarg in fastarg.fastargs:
            print("cfastarg " + cfastarg.name)
            print("arg " + arg)
            if cfastarg.name == arg:
                # if match, recurse on the fastarg with same name
                self.search_to_invoke(cfastarg, argqueue, commandargs)
                return


        # if no match, search commands for current sys argv
        for command in fastarg.commands:
            print("command " + command.get_name())
            if command.get_name() == arg:
                # if found, invoke the function
                ka = dict(commandargs._get_kwargs())
                print(ka)
                command.function(**ka)




    def traverse_fastargs(self, fastarg: Fastarg):
        fastarg.subparsers = fastarg.parser.add_subparsers(help="subcommand help")

        # process commands
        for command in fastarg.commands:
            # print(command.function.__name__)
            sig = signature(command.function)
            parser_a = fastarg.subparsers.add_parser(command.function.__name__, help=command.function.__doc__)

            for name, param in sig.parameters.items():
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



        for child in fastarg.fastargs:
            child.parser = fastarg.subparsers.add_parser(child.name, help="a subparser")
            self.traverse_fastargs(child)

    def add_fastarg(self, fastarg: Fastarg, name=None):
        # self.subparsers.add_parser(name)
        fastarg.name = name
        self.fastargs.append(fastarg)
        # print(fastarg)
