#Import tkinter for python GUI
import tkinter as tk
#import random for random number generator
import random as rand

#Class to keep track of the condition ordering
class Condition_Order():
    #Constructor class to create empty list
    def __init__(self):
        self.condition_list = list()
    #Add condition 1 to the list
    def add_condition_1(self):
        self.condition_list.append(1)
    #Add condition 2 to the list
    def add_condition_2(self):
        self.condition_list.append(2)
    #Add condition 3 to the list
    def add_condition_3(self):
        self.condition_list.append(3)
    #Add condition 4 to the list
    def add_condition_4(self):
        self.condition_list.append(4)
    #Add condition 5 to the list
    def add_condition_5(self):
        self.condition_list.append(5)
    #Add condition 6 to the list
    def add_condition_6(self):
        self.condition_list.append(6)
    #Add one of each condition to the list in a psuedo-random order
    def add_all_conditions_at_random(self):
        #Initiallize a list of all possible conditions
        condition_list = [1, 2, 3, 4, 5, 6]
        #loop until all conitions are chosen
        while(len(condition_list) != 0):
            #get the current number of conitions remaining to choose from
            conditions_remaining = len(condition_list)
            #get a random condition from the selection list
            rand_condition_index = rand.randint(0, conditions_remaining-1)
            rand_condition = condition_list[rand_condition_index]
            #append the psuedo-randomly obtained condition to the experiment's condition list
            self.condition_list.append(rand_condition)
            #delete the selected condition from the condition selection list
            del condition_list[rand_condition_index]
    #Get the current condition list
    def get_condition_list(self):
        return(self.condition_list)


#Experimenter chooses the order of tests to present to the subject
def condition_select_window():
    #Instatiate a condition order class
    condition = Condition_Order()
    
    #Instantiate a window
    window = tk.Tk()

    #Instatiate Frame 1
    frame1 = tk.Frame(master=window)
    #display a title in frame 1
    title = tk.Label(master = frame1, text="Welcome to the Condition Selection Window")
    title.pack()
    #place in frame 1
    frame1.pack()

    #Instantiate Frame 2
    frame2 = tk.Frame(master=window)
    #Instantiate frame 3 (sub-frame)
    frame3 = tk.Frame(master=frame2)
    #Create 6 buttons for the 6 conditions
    btn_c1 = tk.Button(master = frame3, text="Condition 1", command = condition.add_condition_1)
    btn_c1.pack()
    btn_c2 = tk.Button(master = frame3, text="Condition 2", command = condition.add_condition_2)
    btn_c2.pack()
    btn_c3 = tk.Button(master = frame3, text="Condition 3", command = condition.add_condition_3)
    btn_c3.pack()
    btn_c4 = tk.Button(master = frame3, text="Condition 4", command = condition.add_condition_4)
    btn_c4.pack()
    btn_c5 = tk.Button(master = frame3, text="Condition 5", command = condition.add_condition_5)
    btn_c5.pack()
    btn_c6 = tk.Button(master = frame3, text="Condition 6", command = condition.add_condition_6)
    btn_c6.pack()
    btn_rand = tk.Button(master = frame3, text="One of Each Pseudo-Random Condition Ordering", command = condition.add_all_conditions_at_random)
    btn_rand.pack()
    #place in frame 3
    frame3.pack(side=tk.LEFT)
    #Instantiate Frame 4 (sub-frame)
    frame4 = tk.Frame(master=frame2)
    #Create a text box to put ordering options
    condition_order_print = tk.Label(master = frame4, text="Current List of Condition Orderings:")
    condition_order_print.pack()
    #place in frame4
    frame4.pack(side=tk.RIGHT)
    #place in frame 2
    frame2.pack()

    #Instantiate Frame 5
    frame5 = tk.Frame(master=window)
    #Create a submit button to close the window
    btn_submit = tk.Button(master=frame5, text="Submit", command=window.destroy)
    btn_submit.pack()
    #place in frame5
    frame5.pack()
    
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

    #return the conition ordering object
    return(condition)