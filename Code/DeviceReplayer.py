import customtkinter as ctk
import keyboard as kb
from DeviceFunctions import MouseFunctions, KeyboardFunctions
from ReplayQueue import replayQueue

# Creating recording mouse and keyboard objects
clicker = MouseFunctions()
board = KeyboardFunctions()
q = replayQueue()

# Appearance settings
ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("system")
app = ctk.CTk()
app.geometry("380x420")
app.resizable(False, False)
app.title("Keyboard and Mouse Replayer")

# App layout + Frames (Buttons and extras at bottom)
title = ctk.CTkLabel(app, text = "Harrison's Keyboard and Mouse Replayer")
title.grid(row = 0, rowspan = 1, columnspan = 6, pady = 8)

tabs = ctk.CTkTabview(app, width = 360, height = 330)
tabs.grid(row = 1, column = 2, padx = 8)
tabs.add("Mouse Controls")
tabs.add("Keyboard Controls")
tabs.add("Queue")
tabs.add("Settings")

mouseFrame = tabs.tab("Mouse Controls")
mRecordFrame = ctk.CTkFrame(mouseFrame, fg_color= "#3b3b3b")
mRecordFrame.grid(row = 0, padx = 8, pady = 8)
mReplayFrame = ctk.CTkFrame(mouseFrame, fg_color= "#3b3b3b")
mReplayFrame.grid(row = 1, padx = 8, pady = 8)
mDeleteFrame = ctk.CTkFrame(mouseFrame, fg_color= "#3b3b3b")
mDeleteFrame.grid(row = 2, padx = 8, pady = 8)

kbFrame = tabs.tab("Keyboard Controls")
kbRecordFrame = ctk.CTkFrame(kbFrame, fg_color= "#3b3b3b")
kbRecordFrame.grid(row = 0, padx = 8, pady = 0)
kbReplayFrame = ctk.CTkFrame(kbFrame, fg_color= "#3b3b3b")
kbReplayFrame.grid(row = 1, padx = 8, pady = 0)
kbDeleteFrame = ctk.CTkFrame(kbFrame, fg_color= "#3b3b3b")
kbDeleteFrame.grid(row = 2, padx = 8, pady = 0)

queueFrame = tabs.tab("Queue")
qDelayFrame = ctk.CTkFrame(queueFrame)
qDelayFrame.place(x = 8, y = 54)
scrollFrame = ctk.CTkScrollableFrame(queueFrame, width = 80, fg_color= "#3b3b3b")
scrollFrame.place(x = 240, y = 8)

settingsTab = tabs.tab("Settings")
changeKeyFrame = ctk.CTkFrame(settingsTab, width = 333, height = 46, fg_color= "#3b3b3b")
changeKeyFrame.grid(row = 0, column = 0, padx = 8, pady = 8)
sDelayFrame = ctk.CTkFrame(settingsTab, width = 333, height = 46, fg_color= "#3b3b3b")
sDelayFrame.grid(row = 1, column = 0, padx = 8, pady = 8)


textFrame = ctk.CTkFrame(app, border_width= 1, fg_color= "#3b3b3b")
textFrame.grid(row = 2, columnspan = 6, pady = 7)

"=================================================================================================="

# DEVICE METHODS

# Sets button to stop recording
def changeStop():
    detailer.configure(text = "Press any single key.")
    app.update()
    newKey = kb.read_key()
    clicker.stopKey = str(newKey)
    board.stopKey = str(newKey)
    detailer.configure(text = "Stop key changed to \'" + clicker.stopKey + '\'')

# Sets a delay for replays
def setDelay():
    if(not delayEntry.get().isdigit()):
        detailer.configure(text = "Enter valid delay in seconds")
    else:
        clicker.delay = int(delayEntry.get())
        board.delay = int(delayEntry.get())
        detailer.configure(text = "Delay set to " + str(delayEntry.get()) + " seconds")

# Sets delay for each replay or the start only
def delayEach():
    clicker.perLoop = delayEachCheck.get()
    board.perLoop = delayEachCheck.get()

# METHODS FOR QUEUE

# Plays queue in order
def playQueue():
    if (q.getString() == "Empty Queue"):
        detailer.configure(text = "The queue is empty")
    else:
        detailer.configure(text = "Queue playing now...")
        app.update()
        q.replay()
        detailer.configure(text = "Replay complete.")

# Empties the queue; indirect to clarify only the clear queue was used, not the clear records
def emptyQueue(indirect = False):
    q.clear()
    scrollQueue.configure(text = q.getString())
    if (not indirect):
        detailer.configure(text = "Queue has been cleared")

# Sets a delay for the start of queue
def setQDelay():
    if(not delayQEntry.get().isdigit()):
        detailer.configure(text = "Enter valid delay in seconds")
    else:
        q.delayQ = int(delayQEntry.get())
        detailer.configure(text = "Queue delay set to " + str(q.delayQ) + " seconds")

# METHODS FOR MOUSE
    
# Button function to start recording mouse
def mRecord(action = "RECORD"):
    change = False
    if (clicker.choice == ""):
        change = True
    detailer.configure(text = "Recording mouse. Press \'" + clicker.stopKey + "\' to stop...")
    app.update()
    clicker.appendChoice(mNameEntry.get())
    clicker.pickAction(action)
    mReplayOptionMenu.configure(values = clicker.choices)
    mDeleteOptionMenu.configure(values = clicker.choices)
    detailer.configure(text = "Recording stopped.")
    if (change):
        newChoice = clicker.choices[0]
        mReplayOptionMenu.set(newChoice)
        clicker.choice = newChoice
        mDeleteOptionMenu.set(newChoice)
        clicker.delChoice = newChoice

# Button function to clear mouse records
def mClear(action = "CLEAR", indirect = False):
    if(not indirect):
        detailer.configure(text = "Mouse records have been cleared.")

    # Resetting to default values
    clicker.pickAction(action)
    mReplayOptionMenu.configure(values = clicker.choices)
    mDeleteOptionMenu.configure(values = clicker.choices)
    mReplayOptionMenu.set("Replay record")
    mDeleteOptionMenu.set("Delete record")
    clicker.choice = ""
    clicker.delChoice = ""
    emptyQueue(True)

# Button function to replay mouse choice a number of times
def mReplay(action = "REPLAY"):

    # Checks for num of repeats
    if (mRepeatsEntry.get() == ""):
        clicker.repeats = 1
        if(len(clicker.choices) == 0):
            detailer.configure(text = "There are no records.")
        else:
            detailer.configure(text = "Replaying mouse...")
            app.update()
            clicker.pickAction(action)
            detailer.configure(text = "Replay complete.")
    else:
        if(mRepeatsEntry.get().isdigit()):
            clicker.repeats = int(mRepeatsEntry.get())
            if(len(clicker.choices) == 0):
                detailer.configure(text = "There are no records.")
            else:
                detailer.configure(text = "Replaying mouse...")
                app.update()
                clicker.pickAction(action)
                detailer.configure(text = "Replay complete.")
        else:
            detailer.configure(text = "Invalid number of repeats.")

# Button function to add mouse choice and repeats to queue
def mEnqueue():
    if(clicker.choice == ""):
        detailer.configure(text = "No record selected.")
    else:

        # Implement number of repeats
        if (mRepeatsEntry.get() == ''):
            clicker.repeats = 1
        elif(mRepeatsEntry.get().isdigit()):
            clicker.repeats = int(mRepeatsEntry.get())
        else:
            detailer.configure(text = "Invalid number of repeats.")

        # Adds to queue
        q.enqueue([clicker, clicker.choice, clicker.repeats])
        scrollQueue.configure(text = q.getString())
        detailer.configure(text = "Added to queue.")

# Button function to delete mouse elChoice
def mDelete():
    if(len(clicker.choices) == 0):
        detailer.configure(text = "There are no records.")
    
    else:
        detailer.configure(text = "Selected mouse record deleted.")
        clicker.delRecord()
        mReplayOptionMenu.configure(values = clicker.choices)
        mDeleteOptionMenu.configure(values = clicker.choices)
        if (len(clicker.choices) == 0):
            mClear("CLEAR", True)
        else:
            if (clicker.choice == clicker.delChoice):
                clicker.choice = clicker.choices[0]
                mReplayOptionMenu.set(clicker.choices[0])
            mDeleteOptionMenu.set(clicker.choices[0])
            clicker.delChoice = clicker.choices[0]

    emptyQueue(True)

# Menu function to update mouse choice
def mOptions(choice):
    clicker.choice = choice

# Menu function to update mouse delChoice
def mDelOptions(choice):
    clicker.delChoice = choice
    
# METHODS FOR KEYBOARD
    
# Button function to start recording keyboard
def kbRecord(action = "RECORD"):
    change = False
    if (board.choice == ""):
        change = True
    detailer.configure(text = "Recording Keyboard. Press \'" + board.stopKey + "\' to stop...")
    app.update()
    board.appendChoice(kbNameEntry.get())
    board.pickAction(action)
    kbReplayOptionMenu.configure(values = board.choices)
    kbDeleteOptionMenu.configure(values = board.choices)
    detailer.configure(text = "Recording stopped.")
    if (change):
        newChoice = board.choices[0]
        kbReplayOptionMenu.set(newChoice)
        board.choice = newChoice
        kbDeleteOptionMenu.set(newChoice)
        board.delChoice = newChoice

# Clears keyboard records and sets default values; indirect helps delete function reset to default values
def kbClear(action = "CLEAR", indirect = False):
    if (not indirect):
        detailer.configure(text = "Keyboard records have been cleared.")

    # Resetting values
    board.pickAction(action)
    kbReplayOptionMenu.configure(values = board.choices)
    kbDeleteOptionMenu.configure(values = board.choices)
    kbReplayOptionMenu.set("Replay record")
    kbDeleteOptionMenu.set("Delete record")
    kbReplayOptionMenu.set("Replay record")
    kbDeleteOptionMenu.set("Delete record")
    board.choice = ""
    board.delChoice = ""
    emptyQueue(True)

# Button functin to replay keyboard choice a number of times
def kbReplay(action = "REPLAY"):

    # Checks for num of repeats
    if (kbRepeatsEntry.get() == ''):
        board.repeats = 1
        if(len(board.choices) == 0):
            detailer.configure(text = "There are no records.")
        else:
            detailer.configure(text = "Replaying keyboard...")
            app.update()
            board.pickAction(action)
            detailer.configure(text = "Replay complete.")
    else:
        if(kbRepeatsEntry.get().isdigit()):
            board.repeats = int(kbRepeatsEntry.get())
            if(len(board.choices) == 0):
                detailer.configure(text = "There are no records.")
            else:
                detailer.configure(text = "Replaying keyboard...")
                app.update()
                board.pickAction(action)
                detailer.configure(text = "Replay complete.")
        else:
            detailer.configure(text = "Invalid number of repeats.")

# Button function to add keyboard choice and repeats to queue
def kbEnqueue():
    if(board.choice == ""):
        detailer.configure(text = "No record selected.")
    else:

        # Implements number of repeats
        if (kbRepeatsEntry.get() == ''):
            board.repeats = 1;
        elif(kbRepeatsEntry.get().isdigit()):
            board.repeats = int(kbRepeatsEntry.get())
        else:
            detailer.configure(text = "Invalid number of repeats.")

        # Adds to queue
        q.enqueue([board, board.choice, board.repeats])
        scrollQueue.configure(text = q.getString())
        detailer.configure(text = "Added to queue.")

# Button function to delete keyboard delChoice
def kbDelete():
    if(len(board.choices) == 0):
        detailer.configure(text = "There are no records")
    
    else:
        detailer.configure(text = "Selected mouse record deleted.")
        board.delRecord()
        kbReplayOptionMenu.configure(values = board.choices)
        kbDeleteOptionMenu.configure(values = board.choices)
        if (len(board.choices) == 0):
            kbClear("CLEAR", True)
        else:
            if(board.choice == clicker.delChoice):
                board.choice = board.choices[0]
                kbReplayOptionMenu.set(board.choices[0])
            kbDeleteOptionMenu.set(board.choices[0])
            board.delChoice = board.choices[0]

    emptyQueue(True)

# Menu function to update keyboard choice
def kbOptions(choice):
    board.choice = choice

# Menu function to update keyboard delChoice
def kbDelOptions(choice):
    board.delChoice = choice

"======================================================================================================"

# Mouse interface
mRecordButton = ctk.CTkButton(mRecordFrame, text = "Record Mouse", command = mRecord, width = 150, height = 30)
mRecordButton.grid(row = 0, column = 3, padx = 8, pady = 8)

mNameEntry = ctk.CTkEntry(mRecordFrame, placeholder_text= "Label mouse recording", width = 150, height = 30)
mNameEntry.grid(row = 0, column = 1, padx = 8, pady = 8)

mReplayOptionMenu = ctk.CTkOptionMenu(mReplayFrame, values = clicker.choices, command = mOptions, width = 150, height = 30)
mReplayOptionMenu.grid(row = 0, column = 1, padx = 8, pady = 8)

mRepeatsEntry = ctk.CTkEntry(mReplayFrame, placeholder_text = "Number of repeats", width = 150, height = 30)
mRepeatsEntry.grid(row = 1, column = 1, padx = 8, pady = 8)

mReplayButton = ctk.CTkButton(mReplayFrame, text = "Replay Mouse", command = mReplay, width = 150, height = 30)
mReplayButton.grid(row = 0, column = 2, padx = 8, pady = 8)

mEnqueueButton = ctk.CTkButton(mReplayFrame, text = "Add to Queue", command = mEnqueue, width = 150, height = 30)
mEnqueueButton.grid(row = 1, column = 2, padx = 8, pady = 8)

mDeleteOptionMenu = ctk.CTkOptionMenu(mDeleteFrame, values = clicker.choices, command = mDelOptions, width = 150, height = 30)
mDeleteOptionMenu.grid(row = 0, column = 1, padx = 8, pady = 8)

mDeleteButton = ctk.CTkButton(mDeleteFrame, text = "Delete Mouse Record", command = mDelete, width = 150, height = 30)
mDeleteButton.grid(row = 0, column = 2, padx = 8, pady = 8)

mClearButton = ctk.CTkButton(mDeleteFrame, text = "Clear Mouse Records", command = mClear, width = 150, height = 30)
mClearButton.grid(row = 1, column = 2, padx = 8, pady = 8)

# Keyboard interface
kbRecordButton = ctk.CTkButton(kbRecordFrame, text = "Record Keyboard", command = kbRecord, width = 150, height = 30)
kbRecordButton.grid(row = 0, column = 1, padx = 8, pady = 8)

kbNameEntry = ctk.CTkEntry(kbRecordFrame, placeholder_text= "Label keyboard recording", width = 150, height = 30)
kbNameEntry.grid(row = 0, column = 0, padx = 8, pady = 8)

kbReplayOptionMenu = ctk.CTkOptionMenu(kbReplayFrame, values = board.choices, command = kbOptions, width = 150, height = 30)
kbReplayOptionMenu.grid(row = 0, column = 0, padx = 8, pady = 8)

kbRepeatsEntry = ctk.CTkEntry(kbReplayFrame, placeholder_text = "Number of repeats", width = 150, height = 30)
kbRepeatsEntry.grid(row = 1, column = 0, padx = 8, pady = 8)

kbReplayButton = ctk.CTkButton(kbReplayFrame, text = "Replay Keyboard", command = kbReplay, width = 150, height = 30)
kbReplayButton.grid(row = 0, column = 1, padx = 8, pady = 8)

kbEnqueueButton = ctk.CTkButton(kbReplayFrame, text = "Add to Queue", command = kbEnqueue, width = 150, height = 30)
kbEnqueueButton.grid(row = 1, column = 1, padx = 8, pady = 8)

kbDeleteOptionMenu = ctk.CTkOptionMenu(kbDeleteFrame, values = board.choices, command = kbDelOptions, width = 150, height = 30)
kbDeleteOptionMenu.grid(row = 0, column = 0, padx = 8, pady = 8)

kbDeleteButton = ctk.CTkButton(kbDeleteFrame, text = "Delete Keyboard Record", command = kbDelete, width = 150, height = 30)
kbDeleteButton.grid(row = 0, column = 1, padx = 8, pady = 8)

kbClearButton = ctk.CTkButton(kbDeleteFrame, text = "Clear Keyboard Records", command = kbClear, width = 150, height = 30)
kbClearButton.grid(row = 1, column = 1, padx = 8, pady = 8)

# Queue interface
playQueueButton = ctk.CTkButton(queueFrame, text = "Play Queue", command = playQueue, width = 100, height = 30)
playQueueButton.place(x = 132, y = 18)

delayQEntry = ctk.CTkEntry(qDelayFrame, placeholder_text= "Delay seconds", width = 100, height = 30)
delayQEntry.grid(row = 0, column = 0, padx = 8, pady = 8)

delayQButton = ctk.CTkButton(qDelayFrame, text  = "Delay Queue", command = setQDelay, width = 100, height = 30)
delayQButton.grid(row = 0, column = 1, padx = 8, pady = 8)

emptyQueueButton = ctk.CTkButton(queueFrame, text = "Clear Queue", command = emptyQueue, width = 100, height = 30)
emptyQueueButton.place(x = 132, y = 108)

scrollQueue = ctk.CTkLabel(scrollFrame, text = q.getString())
scrollQueue.grid()

# Settings interface
changeKeyButton = ctk.CTkButton(changeKeyFrame, text = "Change Stop Button", command = changeStop, width = 150, height = 30)
changeKeyButton.place(x = 175, y = 8)

delayEntry = ctk.CTkEntry(sDelayFrame, placeholder_text= "Delay seconds", width = 150, height = 30)
delayEntry.grid(row = 1, column = 0, padx = 8, pady = 8)

delayButton = ctk.CTkButton(sDelayFrame, text  = "Set Delay", command = setDelay, width = 150, height = 30)
delayButton.grid(row = 1, column = 1, padx = 8, pady = 8)

delayEachCheck = ctk.CTkCheckBox(sDelayFrame, text= "Delay Loops", command = delayEach, onvalue = True, offvalue= False)
delayEachCheck.grid(row = 2, column = 0, padx = 8, pady = 8)

# Textbox interface
detailer = ctk.CTkLabel(textFrame, text = "Thanks for checking me out!")
detailer.pack(padx = 16, pady = 1)

"=================================================================================================="

if(len(clicker.choices) == 0):
    mReplayOptionMenu.set("Replay record")
    mDeleteOptionMenu.set("Delete record")
if(len(board.choices) == 0):
    kbReplayOptionMenu.set("Replay record")
    kbDeleteOptionMenu.set("Delete record")
    
app.mainloop()