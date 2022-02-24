import argparse

# create the top-level parser
parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--foo', action='store_true', help='foo help')
subparsers = parser.add_subparsers(help='sub-command help')
# create the parser for the "a" command
parser_a = subparsers.add_parser('a', help='a help')
parser_a.add_argument('bar', type=int, help='bar help')
# create the parser for the "b" command
parser_b = subparsers.add_parser('b', help='b help')
parser_b.add_argument('--baz', choices='XYZ', help='baz help')
subparsers_b = parser_b.add_subparsers(help='parser b sub commands')

parser_c = subparsers_b.add_parser('c', help='c help')
parser_c.add_argument('qux', type=str, help='qux help')

# parse some argument lists
args = parser.parse_args()
print(args)
args = parser.parse_args()
print(args)
