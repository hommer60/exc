def valid_matching(directory, matching):
    """ Verifies that each match
        satisfies the two constraints """
    if len(matching) != len(directory):
        return False
    for [giver, recipient] in matching:
        if giver == recipient or directory[giver] == recipient:
            return False
    return True

def directory_builder(num_people, num_couples):
    """ Creates a directory composed of num_people
        guests with num_couples couples """
    directory = {}
    num_added = 0
    while num_added < num_people:
        if num_added < (num_couples * 2) - 1:
            directory[num_added] = num_added + 1
            directory[num_added + 1] = num_added
            num_added += 2
        else:
            directory[num_added] = None
            num_added += 1
    return directory
