def registration_logic(directory, name, partner):
    old_partner = None
    if name in directory:
        print("You've already been registered for the gift exchange")
        old_partner = directory[name]
    else:
        print("Great, we've added you to the gift exchange!")
        directory[name] = old_partner
    if partner:
        if partner in directory:
            print("The partner you specified is already registered")
            if directory[partner] != name:
                print("And they registered as a couple with someone else...")
                return
        if current_partner and current_partner != partner:
            update = input("You have already registered as a couple with someone else, would you like to update your partner? [Y/n]\n")
            update = update.lower()
            if update == 'y' or update == 'yes':
                print("Your partner has been updated to " + partner)
                directory[name] = partner
                directory[partner] = name
                directory[current_partner] = None
                return
            else:
                print("Ok, your partner will remain " + current_partner)
                return
        else:
            print("Your partner has been added to the gift exchange!")
            directory[name] = partner
            directory[partner] = name 
            return 