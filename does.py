import random
import timeit

def run_exchange(directory):
    start = timeit.default_timer()
    matches = []
    if not valid_exchange(directory):
        print("Sorry, not enough guests have signed up yet to execute a valid gift exchange")
    else:
        participants = list(directory.keys())
        givers = participants.copy()
        recipients = participants.copy()
        rounds = [0] * len(participants)
        print(len(rounds))
        cur_round = 0
        while cur_round < len(participants):
            if rounds[cur_round] == 6 and cur_round != 0:
                for i in range(len(rounds)):
                    if i >= cur_round:
                        rounds[i] = 0
                cur_round = cur_round - 1
                [removed_g, removed_r] = matches.pop()
                givers.append(removed_g)
                recipients.append(removed_r)
            giver = random.choice(givers)
            recipient = random.choice(recipients)
            #print(cur_round)
            if giver != recipient and directory[giver] != recipient:
                recipients.remove(recipient)
                givers.remove(giver)
                matches.append([giver, recipient])
                cur_round += 1
            else:
                rounds[cur_round] += 1
    end = timeit.default_timer()
    diff = end - start
    return matches, end

def run_exchange_bad(directory):
    start = timeit.default_timer()
    matches = []
    if not valid_exchange(directory):
        print("Sorry, not enough guests have signed up yet to execute a valid gift exchange")
    else:
        participants = list(directory.keys())
        givers = participants.copy()
        recipients = participants.copy()
        while len(givers) > 0 and len(recipients) > 0:
            giver = random.choice(givers)
            recipient = random.choice(recipients)
            if giver != recipient and directory[giver] != recipient:
                recipients.remove(recipient)
                givers.remove(giver)
                matches.append([giver, recipient])
            else:
                givers = participants.copy()
                recipients = participants.copy()
    end = timeit.default_timer()
    diff = end - start
    return matches, diff

def run_exchange2(directory):
    matches = []
    if not valid_exchange(directory):
        print("Sorry, not enough guests have signed up yet to execute a valid gift exchange")
    else:
        participants = list(directory.keys())
        givers = participants.copy()
        recipients = participants.copy()
        cur_saved = None
        fixed = False
        while len(givers) > 0 and len(recipients) > 0:
            if fixed == True and cur_saved != None:
                recipients.append(cur_saved)
                cur_saved = None
            giver = random.choice(givers)
            recipient = random.choice(recipients)
            if giver == directory[giver]:
                recipients.remove(directory[giver])
                cur_saved = directory[giver]
                fixed = False
            elif giver != recipient:
                fixed = True
                givers.remove(giver)
                recipients.remove(recipient)
                matches.append([giver, recipient])
    return matches

def run_exchange_good(directory):
    start = timeit.default_timer()
    participants = list(directory.keys())
    random.shuffle(participants)
    initial_matches = []
    conflicting_matches = []
    valid_matches = []
    start = timeit.default_timer()
    for i in range(len(participants)):
        giver = participants[i]
        if i == (len(participants) - 1):
            recipient = participants[0]
        else:
            recipient = participants[i + 1]
        initial_matches.append([giver, recipient])
    for [giver, recipient] in initial_matches:
        if directory[giver] == recipient:
            conflicting_matches.append([giver, recipient])
        else:
            valid_matches.append([giver, recipient])
    if len(conflicting_matches) == 1:
        [invalid_g, invalid_r] = conflicting_matches[0]
        [valid_g, valid_r] = random.choice(valid_matches)
        valid_matches.remove([valid_g, valid_r])
        valid_matches.append([valid_g, invalid_r])
        valid_matches.append([invalid_g, valid_r])
    else:
        for i in range(len(conflicting_matches)):
            [g1, r1] = conflicting_matches[i]
            [g2, r2] = conflicting_matches[0] if i == (len(conflicting_matches) - 1) else conflicting_matches[i + 1]
            valid_matches.append([g1, r2])
            valid_matches.append([g2, r1])
    end = timeit.default_timer()
    diff = end - start
    return valid_matches, diff

pairs = {'omar' : None, 'james' : 'john', 'john' : 'james', 'mike' : None}

matches, time = run_exchange_good(pairs)
for match in matches:
    print(match[0] + " will give a gift to " + match[1])