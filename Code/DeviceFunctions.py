import keyboard as kb
import mouse
import pickle
import os.path
import time

class DeviceFunctions:
    def __init__(self):
        self.repeats = 1
        self.stopKey = "esc"
        self.delay = 0
        self.perLoop = False
        self.choice = ""
        self.delChoice = ""
        self.choices = []

    # Checks if list contains a certain value
    def listContains(self, list, value):
        for element in list:
            if(value == element):
                return True
        return False

    # Returns a unique name by appending a digit
    def uniqueName(self, name, digits = -1):
        HIGHEST_DIGIT = 9

        # Recursively loops until unique name created
        if(not self.listContains(self.choices, name)):
            return str(name)
        
        # Adds number to end if it doesn't have one
        elif (not name[-1].isdigit()):
            return self.uniqueName(name + " 1")
        
        # Increments digits to deal with next place value
        elif (int(name[-digits]) == HIGHEST_DIGIT):
            return self.uniqueName(name[0:digits] + " " + str(int(name[digits:]) + 1), digits - 1)
        
        # Increments number at end
        else:
            return self.uniqueName(name[0:digits] + str(int(name[digits:]) + 1), digits)
        
        """
        # Recursively loops until unique name created
        if(not self.listContains(self.choices, name)):
            return str(name)
        
        # Adds number to end if it doesn't have one
        elif (not name[-1].isdigit()):
            return self.uniqueName(name + " 1")
        
        # Increments numbers at end and increases place value scope
        elif (name[-1] == 9):
            return self.uniqueName(name[0:-digits] + " " + str(int(name[-digits:]) + 1), digits + 1)

        # Increments numbers at end
        elif (not name[-digits].isdigit()):
            return self.uniqueName(name[0:-digits] + " " + str(int(name[-digits:]) + 1), digits)
        """

    # Rewrites choices file based on choices list
    def updateChoices(self):
        with open(self.choicesFile, "wb") as choices:
            pickle.dump(self.choices, choices)

    # Returns a record object based on given index
    def getEvents(self, index):
        with open(self.recordsFile, "rb") as record:

            # Iterates through unused records
            for i in range(0, index):
                pickle.load(record)

            return pickle.load(record)

    # Clears the record file and choices list
    def clearRecords(self):

        # Open file with wb to erase contents
        with open(self.recordsFile, "wb") as record:
            pass
        self.choices = []
        self.updateChoices()

    # Appends name to choices list
    def appendChoice(self, name = ""):
        if (name == ""):

            # Default name is the next number
            self.choices.append(str(len(self.choices) + 1))
        else:
            name = self.uniqueName(name)
            self.choices.append(name)
        self.updateChoices()

    # Deletes record set by delChoice
    def delRecord(self):
        index = self.choices.index(self.delChoice)
        del self.choices[index]

        # Rewriting files with new choices list
        with open(self.recordsFile, "wb") as record:
            for i in self.choices:
                pickle.dump(i, record)
        self.updateChoices()

class MouseFunctions(DeviceFunctions):
    def __init__(self):
        super().__init__()
        self.recordsFile = "save files\\mouseRecords.pkl"

        # Finding or creating the avaliable options based on choices file
        if (not os.path.isfile("save files\\mouseChoices.pkl")):
            self.choicesFile = "save files\\mouseChoices.pkl"
            with open(self.choicesFile, 'wb') as choices:
                pickle.dump(self.choices, choices)
        else:
            self.choicesFile = "save files\\mouseChoices.pkl"
            with open(self.choicesFile, "rb") as choices:
                self.choices = pickle.load(choices)
            if(not len(self.choices) == 0):
                self.choice = self.choices[0]
                self.delChoice = self.choices[0]

    # Records mouse actions as a list
    def record(self):
        actions = []

        # callback method for each hook event
        def appendEvent(event):
            actions.append(event)

        mouse.hook(appendEvent)

        # wait until key pressed
        kb.wait(self.stopKey)

        mouse.unhook(appendEvent)
        return actions
    
    # Performs selected actions for mouse
    def pickAction(self, action):

        # Record mouse and store in file
        if(action == "RECORD"):
            with open(self.recordsFile, "ab") as record:
                rec = self.record()
                pickle.dump(rec, record)
            self.updateChoices()

        # Replay selection and implements any delays
        elif(action == "REPLAY"):
            index = self.choices.index(str(self.choice))
            event = self.getEvents(index)

            # Checks for whether to delay each time or just the start
            if(not self.perLoop):
                time.sleep(self.delay)
                for i in range(self.repeats):
                    mouse.play(event)
            else:
                for i in range(self.repeats):
                    time.sleep(self.delay)
                    mouse.play(event)

        elif(action == "CLEAR"):
            super().clearRecords()

class KeyboardFunctions(DeviceFunctions):

    def __init__(self):
        super().__init__()
        self.recordsFile = "save files\\kbRecords.pkl"

        # Finding or creating the avaliable options based on choices file
        if (not os.path.isfile("save files\\kbChoices.pkl")):
            self.choicesFile = "save files\\kbChoices.pkl"
            with open(self.choicesFile, 'wb') as choices:
                pickle.dump(self.choices, choices)
        else:
            self.choicesFile = "save files\\kbChoices.pkl"
            with open(self.choicesFile, "rb") as choices:
                self.choices = pickle.load(choices)
            if(not len(self.choices) == 0):
                self.choice = self.choices[0]
                self.delChoice = self.choices[0]

    # Performs selected action for keyboard
    def pickAction(self, action):

        # Record keyboard and store in file
        if(action == "RECORD"):
            with open(self.recordsFile, "ab") as record:
                rec = kb.record(until = self.stopKey)
                pickle.dump(rec, record)
            self.updateChoices()

        # Replay selection and implements any delays
        elif(action == "REPLAY"):
            index = self.choices.index(str(self.choice))
            event = self.getEvents(index)

            # Checks for whether to delay each time or just the start
            if(not self.perLoop):
                time.sleep(self.delay)
                for i in range(self.repeats):
                    kb.play(event)
            else:
                for i in range(self.repeats):
                    time.sleep(self.delay)
                    kb.play(event)

        # Clears records
        elif(action == "CLEAR"):
            super().clearRecords()