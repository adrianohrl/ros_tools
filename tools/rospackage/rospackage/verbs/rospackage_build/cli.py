from __future__ import print_function

def prepare_arguments(parser):
    parser.description = "Generates ..."
    # parser.add_argument()
    return parser

def argument_preprocessor(args):
    extras = {}
    # if '--strange-argument' in args:
    #     args.remove('-strange-argument')
    #     extras['strange_argument'] = True
    return args, extras

def main(options):
    # if not ok():
    #	return 1
    return 0