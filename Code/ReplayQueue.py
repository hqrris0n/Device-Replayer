from DeviceFunctions import MouseFunctions, KeyboardFunctions
import time

class replayQueue():
    def __init__(self):
        self.line = [] # the queue itself
        self.names = [] # names of each action
        self.delayQ = 0

    # Add item to queue
    def enqueue(self, item):
        self.line.append(item)
        self.names.append(item[1] + " x " + str(item[2]))

    # Empty out the queue
    def clear(self):
        self.line = []
        self.names = []

    # Play the contents of queue
    def replay(self):
        time.sleep(self.delayQ)
        for action in self.line:
            device = action[0]
            device.repeats = action[2]
            device.choice = action[1]
            device.pickAction("REPLAY")

    # Return string based on state of queue
    def getString(self):
        if (len(self.names) == 0):
            return "Empty Queue"
        string = ""
        for name in self.names:
            string += name + "\n"
        return string