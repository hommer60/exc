import sys
import os
import argparse
import pickle
import random

def load_directory():
    ## Load directory if it exists or create a new one
    try:
        directory = pickle.load(open('memory.pickle', 'rb'))
    except (OSError, IOError) as e:
        directory = dict()
        pickle.dump(directory, open("memory.pickle", "wb")) 
    print(directory)
    return directory

def save_directory(directory):
    pickle.dump(directory, open("memory.pickle", "wb"))

def delete_directory():
    try:
        os.remove("memory.pickle")
    except OSError:
        pass

def register(args):
    directory = load_directory()
    name = ' '.join(args.name)
    partner = ' '.join(args.partner) if args.partner else None
    if name in directory:
        print("You've already been registered for the gift exchange")
        return
    else:
        if partner:
            if partner in directory:
                print("The partner you specified is already registered...\nTry registering just yourself or with a different partner")
                return
            else:
                directory[name] = partner
                directory[partner] = name
                print("Great, we've added you and your partner to the gift exchange!")
        else:
            directory[name] = None
            print("Great, we've added you to the gift exchange!")
    save_directory(directory)
          

def exchange(args):
    directory = load_directory()
    if not directory:
        print("No one has registered for the gift exchange yet :(")
    else:
        matches = run_exchange(directory)
        for match in matches:
            print(match[0] + " will give a gift to " + match[1])

def valid_exchange(directory):
    if len(directory) == 3:
        num_singles = len([None for partner in directory.values() if partner == None])
        return num_singles > 1
    elif len(directory) == 2:
        return None in directory.values()
    else:
        return True

def run_exchange(directory):
    matches = []
    if not valid_exchange(directory):
        print("Sorry, not enough guests have signed up yet to execute a valid gift exchange")
    else:
        participants = list(directory.keys())
        givers = participants.copy()
        recipients = participants.copy()
        print(participants)
        while len(givers) > 0 and len(recipients) > 0:
            giver = random.choice(givers)
            recipient = random.choice(recipients)
            if giver != recipient and directory[giver] != recipient:
                recipients.remove(recipient)
                givers.remove(giver)
                matches.append([participant, recipient])
    return matches


def reset(args):
    confirmation = input("Are you sure you want to delete the current directory? [Y/N]\n")
    confirmation = confirmation.lower()
    if confirmation == 'yes' or confirmation == 'y':
        delete_directory()
        print('### Directory Deleted')

def guests(args):
    directory = load_directory()
    if not directory:
        print("No one has registered for the gift exchange yet :(")
    else:
        for person, partner in directory.items():
            print(person, partner)

def import_list(args):
    return 1
   

def main():
    parser = argparse.ArgumentParser(description = "A Gift Exchange Program!")
    subparsers = parser.add_subparsers(title='Subcommands', description='valid subcommands', dest='command')
    ## ADD Register SubCommand
    parser_register = subparsers.add_parser('register', description='Register yourself in the gift exchange')
    parser_register.add_argument('name', nargs='+')
    parser_register.add_argument('-p', '--partner', nargs='+', metavar = 'partner_name', help = 'Register your partner as well')
    parser_register.set_defaults(func=register)
    ## ADD Guestlist SubCommand
    parser_guests = subparsers.add_parser('guests', description='Print the current guestlist')
    parser_guests.set_defaults(func=guests)
    ## ADD Reset SubCommand
    parser_reset = subparsers.add_parser('reset', description='clears the current guest list -- be careful!')
    parser_reset.set_defaults(func=reset)
    ## ADD Exchange Subcommand
    parser_exchange = subparsers.add_parser('exchange', description='Execute the gift exchange and show the results')
    parser_exchange.set_defaults(func=exchange)
    ## ADD Import Subcommand
    parser_import = subparsers.add_parser('import', description='Import a guestlist using a csv - see the example file')
    parser_import.set_defaults(func=import_list)
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)

if __name__ == '__main__':
    main()