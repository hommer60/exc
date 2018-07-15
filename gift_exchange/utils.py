import pickle
import os 

DIRECTORY_PATH = "directory/directory.pickle"

def load_directory():
    ## Load directory if it exists
    try:
        directory = pickle.load(open(DIRECTORY_PATH, "rb"))
        return directory
    except (OSError, IOError) as e:
        pass

def create_directory():
    directory = dict()
    pickle.dump(directory, open(DIRECTORY_PATH, "wb")) 
    return directory

def save_directory(directory):
    pickle.dump(directory, open(DIRECTORY_PATH, "wb"))

def delete_directory():
    try:
        os.remove(DIRECTORY_PATH)
    except OSError:
        pass