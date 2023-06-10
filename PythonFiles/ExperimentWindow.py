#Import tkinter for python GUI
import tkinter as tk
#Import pandas for data organization
import pandas as pd
#Import random for random number generator
import random as rand
#import os for getting image files from relative path on the os
import os

#class to store the selections made by the subject
class Test_Selection():
    #Constructor for test selection
    def __init__(self, subject_ID, test_condition, num_trials=15):
        self.subject_ID = subject_ID
        self.test_condition = test_condition
        self.num_trials = num_trials
        self.current_trial = 1
        self.red_correct = 0
        self.red_total = 0
        self.blue_correct = 0
        self.blue_total = 0
        self.test_dataframe = pd.DataFrame(dict(), columns=["person", "game", "trial", "decision", "reward", "state"])

    #getter function to return subject_ID
    def get_subject_ID(self):
        return(self.subject_ID)
    #getter function to return test_condition
    def get_test_condition(self):
        return(self.test_condition)
    #getter function to return the number of total trials
    def get_num_trials(self):
        return(self.num_trials)
    #getter function to return the current trial
    def get_current_trial(self):
        return(self.current_trial)
    #getter function to return red_correct
    def get_red_correct(self):
        return(self.red_correct)
    #getter function to return red fails
    def get_red_fails(self):
        return(self.red_total - self.red_correct)
    #getter function to return red_total
    def get_red_total(self):
        return(self.red_total)
    #getter function to return blue_correct
    def get_blue_correct(self):
        return(self.blue_correct)
    #getter function to return blue fails
    def get_blue_fails(self):
        return(self.blue_total - self.blue_correct)
    #getter function to return blue_total
    def get_blue_total(self):
        return(self.blue_total)
    #get the current state of the selection
    def get_state(self):
        red_correct = self.get_red_correct()
        red_fails = self.get_red_fails()
        blue_correct = self.get_blue_correct()
        blue_fails = self.get_blue_fails()
        #State 1: corrects and fails are the same 
        if(red_correct == blue_correct and red_fails == blue_fails):
            return(1)
        #State 2: left(red) option better than the right(blue); more correct and less fails than the right
        elif(red_correct >= blue_correct and red_fails <= blue_fails):
            return(2)
        #State 3: left(red) option is worse than the right(blue); less correct and more fails than the right
        elif(red_correct <= blue_correct and red_fails >= blue_fails):
            return(3)
        #State 4: exploration of left (red) option; fewer correct and fewer fails than the right
        elif(red_correct < blue_correct and red_fails < blue_fails):
            return(4)
        #State 5: exploit the left(red) option; more correct and more fails than the right
        elif(red_correct > blue_correct and red_fails > blue_fails):
            return(5)
    #get to total money earned thus far
    def get_money_earned(self):
        money_gained = 20*(self.get_red_correct() + self.get_blue_correct())
        money_lost = 5*(self.get_red_fails() + self.get_blue_fails())
        return(money_gained - money_lost)
    
    #reward for red (left/red = 0)
    def apply_red_reward(self):
        #Get the state of the option
        state = self.get_state()
        #add to increment based on selection condition
        self.red_correct += 1
        self.red_total += 1
        #Add selection to the dataframe
        data_row = [self.subject_ID, self.test_condition, self.current_trial, 0, 1, state]
        self.test_dataframe.loc[len(self.test_dataframe)] = data_row
        #increment trial number
        self.current_trial += 1
    #reward for blue (right/blue = 1)
    def apply_blue_reward(self):
        #Get the state of the option
        state = self.get_state()
        #add to increment based on selection condition
        self.blue_correct += 1
        self.blue_total += 1
        #Add selection to the dataframe
        data_row = [self.subject_ID, self.test_condition, self.current_trial, 1, 1, state]
        self.test_dataframe.loc[len(self.test_dataframe)] = data_row
        #increment trial number
        self.current_trial += 1
    #punishment for red (left/red = 0)
    def apply_red_punishment(self):
        #Get the state of the option
        state = self.get_state()
        #add to increment based on selection condition
        self.red_total += 1
        #Add selection to the dataframe
        data_row = [self.subject_ID, self.test_condition, self.current_trial, 0, 0, state]
        self.test_dataframe.loc[len(self.test_dataframe)] = data_row
        #increment trial number
        self.current_trial += 1
    #punishment for blue (right/blue = 1)
    def apply_blue_punishment(self):
        #Get the state of the option
        state = self.get_state()
        #add to increment based on selection condition
        self.blue_total += 1
        #Add selection to the dataframe
        data_row = [self.subject_ID, self.test_condition, self.current_trial, 1, 0, state]
        self.test_dataframe.loc[len(self.test_dataframe)] = data_row
        #increment trial number
        self.current_trial += 1


def run_test(subject_ID, test_number, condition):
    #Instantiate a test selection object
    test_data = Test_Selection(subject_ID, condition)

    #Pseudo-Randomly determine the better team (reference team such that the other team has 1-p probabilty of winning)
    better_team = int(rand.random() + 0.5) #will result in either 0 or 1 (rounded random decimal)

    #Create an instance of a window
    window = tk.Tk()
    #Name the window
    window.title("Testing Window")

    #Instatiate Frame 1
    frame1 = tk.Frame(master=window)
    #display a title in frame 1
    title = tk.Label(master = frame1, text=f"Welcome, Subject {subject_ID}, to the Testing Window (Test #{test_number})")
    title.pack()
    #place in frame 1
    frame1.pack()

    #Instatiate Frame 2
    frame2 = tk.Frame(master=window)
    #Define function for what happens to the left(red) button when it is pressed
    def red_btn_selected():
        #Mathematically determine the probabilty of the better team as a function of the condition
        p = 1.0 - 0.1*(test_data.get_test_condition()-1)
        #If red(team 0) is the worse team, then use 1-p for the probability
        if(better_team != 0):
            p = 1.0 - p
        #Get the random number to be used for this choice
        r = rand.random()
        #As long as r is below the probabilty threshold, then the choice ends in a reward
        if(r < p):
            test_data.apply_red_reward()
        #for probability threshold exceeded, apply the punishment
        else:
            test_data.apply_red_punishment()
    #Display button for left side (red team)
    red_btn = tk.Button(master=frame2, text="Select the Red Team", background="#e85a5a", command=red_btn_selected)
    red_btn.pack(side=tk.LEFT)
    #Instantiate frame 2_1
    frame2_1 = tk.Frame(master=frame2)
    #Define all central information for the test
    trial_label = tk.Label(master = frame2_1, text=f"Trial: {test_data.get_current_trial()}/{test_data.get_num_trials()}")
    trial_label.pack(side=tk.TOP)
    red_score_label = tk.Label(master = frame2_1, text=f"Red Selection: {test_data.get_red_correct()}/{test_data.get_red_total()}")
    red_score_label.pack(side=tk.LEFT)
    blue_score_label = tk.Label(master = frame2_1, text=f"Blue Selection: {test_data.get_blue_correct()}/{test_data.get_blue_total()}")
    blue_score_label.pack(side=tk.RIGHT)
    money_earned_label = tk.Label(master = frame2_1, text=f"Total Earnings: ${test_data.get_money_earned()}")
    money_earned_label.pack(side=tk.TOP)
    



    global_file_path = os.path.dirname(os.path.realpath(__file__))
    graphic = tk.PhotoImage(file=f"{global_file_path}\..\Images\Test_Screen_Layout-Draft.png")
    graphic = graphic.subsample(2, 2)
    graphic_disply = tk.Label(master = frame2_1, image=graphic)
    graphic_disply.pack(side=tk.BOTTOM)





    #place in frame 2_1
    frame2_1.pack(side=tk.LEFT)
    #Define function for what happens to the right(blue) button when it is pressed
    def blue_btn_selected():
        #Mathematically determine the probabilty of the better team as a function of the condition
        p = 1.0 - 0.1*(test_data.get_test_condition()-1)
        #If blue(team 1) is the worse team, then use 1-p for the probability
        if(better_team != 1):
            p = 1.0 - p
        #Get the random number to be used for this choice
        r = rand.random()
        #As long as r is below the probabilty threshold, then the choice ends in a reward
        if(r < p):
            test_data.apply_blue_reward()
        #for probability threshold exceeded, apply the punishment
        else:
            test_data.apply_blue_punishment()
    #Display button for left side (red team)
    blue_btn = tk.Button(master=frame2, text="Select the Blue Team", background="#5469d6", command=blue_btn_selected)
    blue_btn.pack(side=tk.LEFT)
    #place in frame 2
    frame2.pack()
    
    #allow for execution until the window has closed
    try:
        #Get the current trial to look for changes
        curr_trial = 1
        #loop until the window has closed
        while("normal" == window.state()):
            #Check to see if the list has been updated recently
            if(curr_trial != test_data.get_current_trial()):
                #update the current trial variable
                curr_trial = test_data.get_current_trial()
                #update the text to show new values
                trial_label.config(text=f"Trial: {test_data.get_current_trial()}/{test_data.get_num_trials()}")
                red_score_label.config(text=f"Red Selection: {test_data.get_red_correct()}/{test_data.get_red_total()}")
                blue_score_label.config(text=f"Blue Selection: {test_data.get_blue_correct()}/{test_data.get_blue_total()}")
                money_earned_label.config(text=f"Total Earnings: ${test_data.get_money_earned()}")
            #update the window to show any new conitions added
            window.update_idletasks()
            window.update()
    #exception to catch error when checking window after closing
    except:
        pass

    #Create two dataframes: the test data and the last question to return