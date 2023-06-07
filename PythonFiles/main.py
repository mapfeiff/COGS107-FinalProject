#Import python files for each window (+needed information)
import ConditionSelectWindow as condition
import SubjectInformationWindow as subject
import ExperimentWindow as experiment
#Import tkinter for python GUI
import tkinter as tk
#Import pandas for data organization
import pandas as pd

#Main function to run experiment
def main():
    #Get the condition ordering
    condition_order_object = condition.condition_select_window()
    
    #Get the subject information
    subject_information_object = subject.subject_information_window()
    
    #Check to see if the subject gave their consent
    if(subject_information_object.get_consent() == False):
        #If consent not given, then display message on window and halt experiment
        window = tk.Tk()
        greeting = tk.Label(master = window, text="Consent not given! Experiment Halted...")
        greeting.pack()
        window.mainloop()
    elif(subject_information_object.get_understanding() == False):
        #If understanding not confirmed, then display message on window and halt experiment
        window = tk.Tk()
        greeting = tk.Label(master = window, text="Understanding not confirmed! Experiment Halted...")
        greeting.pack()
        window.mainloop()

    #If consent is given and the subject gives confirmation of understanding, then the experiment can be run
    else:
        #First, decide if the subject is an the experimenter, AI, or human (rule: the experimenter uses ID 0 and AI is given a negative ID which is then converted to a positive ID)
        #Experimenter ID given
        if(subject_information_object.get_ID() < 0):
            #The subject is the experimenter, saved data should only be used for system testing
            csv_filename = "ai_test_data.csv"
        #AI ID given
        elif(subject_information_object.get_ID() < 0):
            #The subject is AI, data will go to the AI specific csv
            csv_filename = "ai_test_data.csv"
            #We will also convert the ID to a positive number
            id = subject_information_object.get_ID()
            subject_information_object.set_ID(-id)
        #Human ID given
        else:
            #The subject is natural (human), data will go into the human specific csv
            csv_filename = "human_test_data.csv"

        #First open the file ith all the previously gathered data
        try:
            dataframe = pd.read_csv(f"../{csv_filename}", header=0)
        #If the file does not exist, create a new data file
        except:
            header = ["person", "game", "trial", "decision", "reward"]
            dataframe = pd.DataFrame(dict(), columns=header)
        
        #Create a list of dataframes add additional trials to
        df_list = list()
        #append the dataframe with all the previous data to the list
        df_list.append(dataframe)
        #Loop through each condition
        condition_list = condition_order_object.get_condition_list()
        for i in range(len(condition_list)):
            #Get the results of the condition and append them to the dataframe list
            dataframe = experiment.run_test(subject_ID=subject_information_object.get_ID(), test_number=i+1, condition=condition_list[i])
            #append dataframe into list
            df_list.append(dataframe)
        #Concatinate all the dataframes into a single instance
        dataframe = pd.concat(df_list)
        #Write the data to the csv
        dataframe.to_csv(f"../{csv_filename}", index=False)


#Run the main program when executed as the main file
if(__name__ == "__main__"):
    main()