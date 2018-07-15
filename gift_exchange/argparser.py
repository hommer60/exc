import argparse
import sys
from .commands import register, guests, reset, exchange, import_file

REGISTER_DESC = "Register yourself in the gift exchange"
RESET_DESC = "Clear the current guest list -- be careful!"
GUESTS_DESC = "Print the current guestlist"
IMPORT_DESC = "Import a guestlist using a tab delimited .txt file - see example_guest_list.txt"
EXCHANGE_DESC = "Execute the gift exchange and show the results"

def parse_args(args):
    """ Create an argument parser and add various subcommands
        that route to the respective command function
    """
    parser = argparse.ArgumentParser(description="A Gift Exchange Program!")
    subparsers = parser.add_subparsers(title="Subcommands", dest="command")

    ## Add Register Subcommand
    parser_register = subparsers.add_parser("register", description=REGISTER_DESC)
    parser_register.add_argument("name", nargs="+")
    parser_register.add_argument("-p", "--partner", nargs="+", help="Register your partner as well")
    parser_register.set_defaults(func=register)
    
    ## Add Guestlist Subcommand
    parser_guests = subparsers.add_parser("guests", description=GUESTS_DESC)
    parser_guests.set_defaults(func=guests)

    ## Add Reset Subcommand
    parser_reset = subparsers.add_parser("reset", description=RESET_DESC)
    parser_reset.set_defaults(func=reset)

    ## Add Exchange Subcommand
    parser_exchange = subparsers.add_parser("exchange", description=EXCHANGE_DESC)
    parser_exchange.set_defaults(func=exchange)

    ## Add Import Subcommand
    parser_import = subparsers.add_parser("import", description=IMPORT_DESC)
    parser_import.add_argument("filename")
    parser_import.set_defaults(func=import_file)

    ## No Subcommands given
    if len(args) == 0:
        parser.print_help(sys.stderr)
        sys.exit(2)
    return parser.parse_args(args)