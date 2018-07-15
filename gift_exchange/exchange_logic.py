import random

def valid_exchange(directory):
    """Verifies if any valid set of matches can
       exist given the current state of the directory"""
    ## All three people need to be singles
    if len(directory) == 3:
        num_singles = len([None for partner in directory.values() if partner == None])
        return num_singles == 3
    ## Both people should be singles
    elif len(directory) == 2:
        return None in directory.values()
    elif len(directory) <= 1:
        return False
    else:
        return True

def run_exchange(directory):
    """Executes algorithm described in README to create
       a list of valid matches"""
    guests = list(directory.keys())
    num_guests = len(guests)
    conflicting_matches = []
    valid_matches = []
    random.shuffle(guests)
    ## Initially assign everyone to give a gift to the person
    ## to their "right" (i -> i + 1) so that no one has themselves
    ## A conflicting match is when someone is matched with their partner
    for i in range(num_guests):
        giver = guests[i]
        recipient = guests[0] if i == num_guests - 1 else guests[i + 1]
        if directory[giver] == recipient:
            conflicting_matches.append([giver, recipient])
        else:
            valid_matches.append([giver, recipient])
    num_conflicts = len(conflicting_matches)
    while num_conflicts > 0:
        ## Choose a valid match and swap gift givers to fix
        if num_conflicts == 1:
            [invalid_g, invalid_r] = conflicting_matches.pop()
            for [valid_g, valid_r] in valid_matches:
                if valid_g != invalid_r and invalid_g != valid_r:
                    valid_matches.remove([valid_g, valid_r])
                    valid_matches.append([valid_g, invalid_r])
                    valid_matches.append([invalid_g, valid_r])
                    break
            num_conflicts -= 1
        ## Swap the people involved in two conflicting matches
        else:
            [invalid_g1, invalid_r1] = conflicting_matches.pop()
            [invalid_g2, invalid_r2] = conflicting_matches.pop()
            valid_matches.append([invalid_g1, invalid_r2])
            valid_matches.append([invalid_g2, invalid_r1])
            num_conflicts -= 2
    return valid_matches