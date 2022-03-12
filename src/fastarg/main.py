from __future__ import annotations
import sys
import inspect
from inspect import signature
import functools
import argparse

class Option:
    def __init__(self, default_value, help):
        self.default_value = default_value
        self.help = help

class Argument:
    def __init__(self, help):
        self.help = help

class Command:
    def __init__(self, function):
        self.function = function

    def get_name(self):
        return self.function.__name__

class Fastarg:
    def __init__(self, description: str = "", help: str = "", prog=""):
        self.commands = []
        self.fastargs = []
        self.description = description
        self.help = help
        self.prog = prog

    def command(self):
        def decorator(func):
            self.commands.append(Command(func))

        return decorator

    def run(self):
        # recursively parse all child fastargs

        # if root fastarg, then generate the root parser object
        self.parser = argparse.ArgumentParser(prog=self.prog, description=self.description)

        # after root is generated, traverse tree of fastargs
        self.traverse_fastargs(self)

        # finally, parse the arguments
        args = self.parser.parse_args()

        argqueue = sys.argv[1:]

        # traverse tree of fastargs for the subparser or command to invoke
        self.search_to_invoke(self, argqueue, args)

    def search_to_invoke(self, fastarg, argqueue, commandargs):
        arg = None
        if len(argqueue) > 0:
            arg = argqueue.pop(0)

        if not arg:
            return

        # search fastargs for name of current sys argv
        for cfastarg in fastarg.fastargs:
            if cfastarg.name == arg:
                # if match, recurse on the fastarg with same name
                self.search_to_invoke(cfastarg, argqueue, commandargs)
                return


        # if no match, search commands for current sys argv
        for command in fastarg.commands:
            if command.get_name() == arg:
                # if found, invoke the function
                ka = dict(commandargs._get_kwargs())
                command.function(**ka)




    def traverse_fastargs(self, fastarg: Fastarg):
        fastarg.subparsers = fastarg.parser.add_subparsers()

        # process commands
        for command in fastarg.commands:
            sig = signature(command.function)
            parser_a = fastarg.subparsers.add_parser(command.function.__name__, help=command.function.__doc__)

            for name, param in sig.parameters.items():
                annotation = param.annotation

                if annotation is bool:
                    action = argparse.BooleanOptionalAction
                else:
                    action = None

                if annotation.__name__ == "_empty":
                    raise Exception(f"Type must be defined for parameter {name} of function {command.function.__name__}")

                if annotation is bool and type(param.default) is Argument:
                    raise Exception(f"Error: Do not use Argument for booleans. Use Option instead.")
                
                if annotation is bool and param.default is inspect._empty:
                    arg_name = '--' + name
                    default = False
                    parser_a.add_argument(arg_name, type=annotation, help=f"[{annotation.__name__}]", default=default, action=action)
                if param.default is inspect._empty: # required argument
                    arg_name = name
                    parser_a.add_argument(arg_name, type=annotation, help=f"[{annotation.__name__}]", default=param.default, action=action)
                elif type(param.default) is Argument:
                    arg_name = name
                    help_text = param.default.help
                    parser_a.add_argument(arg_name, type=annotation, help=f"[{annotation.__name__}] {help_text}", action=action)
                elif type(param.default) is Option:
                    arg_name = '--' + name
                    default = param.default.default_value
                    help_text = param.default.help
                    parser_a.add_argument(arg_name, type=annotation, help=f"[{annotation.__name__}] {help_text}", default=default, action=action)
                else:
                    arg_name = '--' + name
                    default = param.default
                    help_text = ""
                    parser_a.add_argument(arg_name, type=annotation, help=f"[{annotation.__name__}] {help_text}", default=default, action=action)



        for child in fastarg.fastargs:
            child.parser = fastarg.subparsers.add_parser(child.name, help=child.help)
            self.traverse_fastargs(child)

    def add_fastarg(self, fastarg: Fastarg, name=None):
        fastarg.name = name
        self.fastargs.append(fastarg)
