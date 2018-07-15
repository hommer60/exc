# Gift Exchange CLI

Gift exchange command-line interface built with Python

#### Setup:

1. From the root directory run `python setup.py install` to create the executable `gift_exchange`
2. Run `gift_exchange <command>` with one of the valid commands listed below 
3. To run tests, run `python setup.py test`

#### Valid Commands:
- `gift_exchange register <your_name> [-p partner_name]`: register yourself and your partner (if specified) to the gift exchange
- `gift_exchange guests`: display the list of guests who have already registered
- `gift_exchange exchange`: execute the gift exchange and view the results of the matchings
- `gift_exchange reset`: delete the current guest directory 
- `gift_exchange import <file_name>`: import a tab delimited *.txt file into the guest directory (more info below)

#####File import:
Added feature to support large guest lists to examine performance. Importing a guest list will overwrite the current guest list. Use the command listed above with a valid txt file with formatted as:
`unique_name\tunique_partner_name\nunique_name\n...`

See `example_guest_list.txt` for an example. 

### Architecture Overview

- All command-line argument parsing is handled in `gift_exchange/argparser.py` with the help of Python's `argparse` module.
- Valid commands are routed to respective command handlers implemented in `gift_exchange/commands.py`.
- The list of registered guests (referred to as the 'directory' throughout the src code) is maintained by a dictionary object saved as a pickle file.

##### Gift Exchange Algorithm:
1. Randomly shuffle list of guests and pair each guest with the person to their right such that no one is paired with themselves.
2. This may result in conflicting pairs (someone is paired with their partner) in which case:
if there is more than one conflicting pair, continually pick two of the conflicting pairs, swap the gift givers, and add both pairs to the list of valid pairs.
3. If one conflicting pair still remains, search the space of valid pairs and choose the first one that doesn't conflict with the pair and swap the gift givers.

##### Possible Improvements:
- Add database integration to allow multiple gift exchanges to be easily managed.
- Store the list of couple and single attendees in some kind of bidirectional dict and set respectively. Currently, there is redundancy as both the person who registered and their partner are stored as keys in the directory dict to allow for easier access.
- Additional commands that add permissions to the "admin" and to the "guests" respectively.
- Allow one to update their registration as currenlt the whole directory needs to be reset for that to happen
