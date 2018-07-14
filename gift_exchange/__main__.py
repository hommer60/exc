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
    elif not valid_exchange(directory):
        print("Sorry, not enough guests have signed up yet to execute a valid gift exchange")
    else:
        matches, _ = run_exchange_good(directory)
        for match in matches:
            print(match[0] + " will give a gift to " + match[1])
        print(res)

def valid_exchange(directory):
    if len(directory) == 3:
        num_singles = len([None for partner in directory.values() if partner == None])
        return num_singles > 1
    elif len(directory) == 2:
        return None in directory.values()
    else:
        return True

def valid_matching(directory, matching):
    for [giver, recipient] in matching:
        if giver == recipient or directory[giver] == recipient:
            return False
    return True

def run_exchange(directory):
    guests = list(directory.keys())
    num_guests = len(guests)
    random.shuffle(guests)
    conflicting_matches = []
    valid_matches = []
    for i in range(num_guests):
        giver = guests[i]
        recipient = guests[0] if i == num_guests - 1 else guests[i + 1]
        if directory[giver] == recipient:
            conflicting_matches.append([giver, recipient])
        else:
            valid_matches.append([giver, recipient])
    num_conflicts = len(conflicting_matches)
    if num_conflicts == 1:
        [invalid_g, invalid_r] = conflicting_matches[0]
        for [valid_g, valid_r] in valid_matches:
            if valid_g != invalid_r and invalid_g != valid_r:
                valid_matches.remove([valid_g, valid_r])
                valid_matches.append([valid_g, invalid_r])
                valid_matches.append([invalid_g, valid_r])
                break
    else:
        for i in range(num_conflicts):
            [g1, r1] = conflicting_matches[i]
            [g2, r2] = conflicting_matches[0] if i == num_conflicts - 1 else conflicting_matches[i + 1]
            valid_matches.append([g1, r2])
            valid_matches.append([g2, r1])
    return valid_matches


def test_perf(num_runs):
    directory = load_directory()
    results = {'Omar' : 0, 'Bad' : 0, 'Averill' : 0}
    print("OMAR")
    for i in range(num_runs):
        _, time = run_exchange(directory)
        print(time)
        results['Omar'] += time
    results['Omar'] = results['Omar'] / num_runs
    print("Bad")
    for i in range(num_runs):
        _, time = run_exchange_bad(directory)
        print(time)
        results['Bad'] += time
    results['Bad'] = results['Bad'] / num_runs
    return results

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

def import_file(args):
    filename = args.filename
    if not filename.lower().endswith('.txt'):
        print('Must provide a .txt file, see the example file....')
    try:
        with open(filename, 'r') as f:
            delete_directory()
            directory = {}
            for line in f:
                people = line.rstrip().split()
                if len(people) == 1:
                    directory[people[0]] = None
                else:
                    directory[people[0]] = people[1]
                    directory[people[1]] = people[0]
            save_directory(directory)
            print("Your guest list has been loaded")
    except IOError as e:
        print('The specified file does not exist!')
   

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
    parser_import = subparsers.add_parser('import', description='Import a guestlist using a tab delimited .txt file - see the example file')
    parser_import.add_argument('filename')
    parser_import.set_defaults(func=import_file)
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)

if __name__ == '__main__':
    main()