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
        self.better_team = None
        self.current_trial = 1
        self.red_correct = 0
        self.red_total = 0
        self.blue_correct = 0
        self.blue_total = 0
        self.chosen_team = None
        self.final_bet = None
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
    
    def set_better_team(self, better_team):
        #Handle any errors in setting the chosen team
        if(better_team != 0 and better_team != 1):
            raise(Exception("Invalid team number entered for better team!"))
        #Set the chosen team
        self.better_team = better_team
    def set_chosen_team(self, chosen_team):
        #Handle any errors in setting the chosen team
        if(chosen_team != 0 and chosen_team != 1):
            raise(Exception("Invalid team number entered for chosen team!"))
        #Set the chosen team
        self.chosen_team = chosen_team
    def set_final_bet(self, final_bet):
        #Handle any errors in setting the final bet
        if(final_bet < 0):
            raise(Exception("You cannot bet a negative amount! Please enter a non-negative number"))
        if(final_bet > max(self.get_money_earned(), 10)):
            raise(Exception("You cannot bet more than what you earned! Please enter a number at or below yout total earnings"))
        #Set the bet
        self.final_bet = final_bet
        

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
    test_data.set_better_team(better_team)

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
            
            #Check for end of trials
            if(test_data.get_current_trial() > test_data.get_num_trials()):
                #remove the center image to replace it with the final bet decision
                graphic_disply.destroy()
                
                #Create a frame to place for the final bet
                frame2_1_1 = tk.Frame(master=frame2_1)
                #Add in the final bet option
                final_bet_team = tk.Label(master=frame2_1_1, text="Please choose which team you think will be most likely to win:")
                final_bet_team.pack()
                options = ["===Choose a Team===", "Red Team", "Blue Team"]
                selection = tk.StringVar()
                selection.set("===Choose a Team===")
                dropdown = tk.OptionMenu(master=frame2_1_1, variable= selection, values=options)
                dropdown.pack()
                if(test_data.get_money_earned() < 10):
                    low_money_message = tk.Label(master=frame2_1_1, text=f"Note: Since you have earned less than $10, then lets assume you won $10 for the next question:")
                    low_money_message.pack()
                money_to_bet = test_data.get_money_earned()
                final_bet_money = tk.Label(master=frame2_1_1, text=f"From your total earnings (${money_to_bet}), how much of it would you bet that your chosen team will win?")
                final_bet_money.pack()
                bet_entry = tk.Entry(master=frame2_1_1)
                bet_entry.pack()
                #place in the frame
                frame2_1_1.pack()

                #Instantiate Frame 3
                frame3 = tk.Frame(master=window)
                #define a function for what happens when the button is submitted (nested function allos us to use external variables)
                def submit_submission():
                    #gather the data items from the window
                    team_select = selection.get()
                    final_bet = int(final_bet_money.get())
                    #Change the selected team into a number (0:red)/(1:blue)
                    if(team_select == "===Choose a Team==="):
                        raise(Exception("Team not selected for bet! Please choose a team..."))
                    elif(team_select == "Red Team"):
                        chosen_team = 0
                    elif(team_select == "Blue Team"):
                        chosen_team = 1
                    #For evenly matched team, have the winning team match the chosen team (for convienience of data analysis)
                    if(condition == 6):
                        better_team = chosen_team
                    #save the data inside the subject information object
                    test_data.set_better_team(better_team)
                    test_data.set_chosen_team(chosen_team)
                    test_data.set_final_bet(final_bet)
                    #close the window
                    window.destroy()
                #Create a submit button to close the window
                btn_submit = tk.Button(master=frame3, text="Submit", command=submit_submission)
                btn_submit.pack()
                #place in frame 3
                frame3.pack()
                
                #run the loop until the submit button has been pressed
                window.mainloop()


    #exception to catch error when checking window after closing
    except:
        pass

    #Create two dataframes: the test data and the last question to return