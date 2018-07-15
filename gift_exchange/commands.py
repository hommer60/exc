from .utils import load_directory, save_directory, delete_directory, create_directory
from .exchange_logic import run_exchange, valid_exchange

def exchange(args):
    """ Execute the exchange if the directory has 
        enough people """
    directory = load_directory()
    if not directory:
        print("No one has registered for the gift exchange yet :(")
    elif not valid_exchange(directory):
        print("Sorry, not enough guests have signed up yet to execute a valid gift exchange")
    else:
        matches = run_exchange(directory)
        for match in matches:
            print(match[0] + " will give a gift to " + match[1])

def register(args):
    """ Registers someone as a guest and potentially their partner
        as well, if neither of them are already registered """
    directory = load_directory()
    if not directory:
        directory = create_directory()
    name = " ".join(args.name)
    partner = " ".join(args.partner) if args.partner else None
    if name in directory:
        print(directory)
        print(name)
        print("You've already been registered for the gift exchange")
        return
    else:
        if partner:
            if partner in directory:
                print("""The partner you specified is already registered...\n
                Try registering just yourself or with a different partner""")
                return
            else:
                directory[name] = partner
                directory[partner] = name
                print("Great, we've added you and your partner to the gift exchange!")
        else:
            directory[name] = None
            print("Great, we've added you to the gift exchange!")
    save_directory(directory)

def reset(args):
    """ Deletes the currently saved directory if there is one """
    directory = load_directory()
    if not directory:
        print("The directory is already empty")
    else:
        delete_directory()
        print("### Directory Deleted")

def guests(args):
    """ Prints the guests currently registered if there are any """
    directory = load_directory()
    if not directory:
        print("No one has registered for the gift exchange yet :(")
    else:
        partners_printed = []
        for guest in list(directory.keys()):
            if not directory[guest]:
                print(guest + " is bringing no one")
            else:
                if guest not in partners_printed:
                    partner = directory[guest]
                    print(guest + " is bringing " + partner)
                    partners_printed.append(partner)

def import_file(args):
    """ Deletes the current directory and imports a new one
        if a valid file is specified """
    filename = args.filename
    if not filename.lower().endswith(".txt"):
        print("Must provide a .txt file, take a look at example_guest_list.txt for an example")
        return
    try:
        with open(filename, "r") as f:
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
        print("The specified file does not exist!")

