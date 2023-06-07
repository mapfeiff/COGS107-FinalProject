#Import tkinter for python GUI
import tkinter as tk
#import random for random number generator
import random as rand

#class to store the selections made by the subject
class Test_Selection():
    def __init__(self):
        self.subject_ID = None
        self.test_condition = None


def run_test(subject_ID, test_number, condition):
    #Create an instance of a window
    window = tk.Tk()
    #Name the window
    window.title("Testing Window")

    #Instatiate Frame 1
    frame1 = tk.Frame(master=window)
    #display a title in frame 1
    title = tk.Label(master = frame1, text=f"Welcome, Subject {subject_ID}, to the Testing Window (Test #{i+1})")
    title.pack()
    #place in frame 1
    frame1.pack()
    #...
    #...
    #...
    #allow for execution until the window has closed
    try:
        #copy the current instance of the condition ordering
        curr_condition_ordering = condition.get_condition_list().copy()
        #loop until the window has closed
        while("normal" == window.state()):
            #Check to see if the list has been updated recently
            if(curr_condition_ordering != condition.get_condition_list()):
                #If a change has been made, get the difference in length and update the current instance of the list
                prev_len = len(curr_condition_ordering)
                curr_condition_ordering = condition.get_condition_list().copy()
                curr_len = len(curr_condition_ordering)
                #Loop through the added conditions
                for i in range(prev_len, curr_len):
                    #add a new text line to the window representing the condition number
                    condition_order_print = tk.Label(master = frame4, text=f"Condition {curr_condition_ordering[i]}")
                    condition_order_print.pack()
                    frame4.pack(side=tk.RIGHT)
            #update the window to show any new conitions added
            window.update_idletasks()
            window.update()
    #exception to catch error when checking window after closing
    except:
        pass
    
    #Create a 