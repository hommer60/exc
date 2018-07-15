import sys
from .argparser import parse_args

def main():
    """ Parses command line arguments execute
        subcommand if valid params were passed """
    args = parse_args(sys.argv[1:])
    if hasattr(args, "func"):
        args.func(args)

if __name__ == "__main__":
    main()