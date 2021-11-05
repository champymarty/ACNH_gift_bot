import pickle
import os

class Data:
    USER_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "user_file.bin")
    USER_MAPPING_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "user_mapping_file.bin")

    def __init__(self):
        self.usersID = set()
        self.usersID_mapping = {} # match -> giver
        self.loadData()

    def saveData(self):
        with open(Data.USER_FILE,'wb') as f:
            pickle.dump(self.usersID, f)
        with open(Data.USER_MAPPING_FILE,'wb') as f:
            pickle.dump(self.usersID_mapping, f)

    def loadData(self):
        if os.path.isfile(Data.USER_FILE):
            with open(Data.USER_FILE,'rb') as f:
                self.usersID = pickle.load(f)
        if os.path.isfile(Data.USER_MAPPING_FILE):
            with open(Data.USER_MAPPING_FILE,'rb') as f:
                self.usersID_mapping = pickle.load(f)