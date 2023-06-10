#Import python files for each window (+needed information)
import ConditionSelectWindow as condition
import SubjectInformationWindow as subject
import ExperimentWindow as experiment
#Import tkinter for python GUI
import tkinter as tk
#Import pandas for data organization
import pandas as pd

#function to get the dataframe from a file (or create a new one if the file doesnt exist)
def append_dataframe_to_csv(filename:str, dataframe):
    #First open the files with all the previously gathered data
    try:
        old_dataframe = pd.read_csv(filename, header=0)
    #If file does not exist, raise exception
    except:
        raise(Exception("File \"{filename}\" does not exist"))
    #Concatinate all the new dataframes into a single instance
    dataframe_Tau = pd.concat([old_dataframe, dataframe])
    #Write the data to the Tau model csv
    dataframe_Tau.to_csv(filename, index=False)

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
        window.title("Error Window")
        greeting = tk.Label(master = window, text="Consent not given! Experiment Halted...")
        greeting.pack()
        window.mainloop()
    elif(subject_information_object.get_understanding() == False):
        #If understanding not confirmed, then display message on window and halt experiment
        window = tk.Tk()
        window.title("Error Window")
        greeting = tk.Label(master = window, text="Understanding not confirmed! Experiment Halted...")
        greeting.pack()
        window.mainloop()

    #If consent is given and the subject gives confirmation of understanding, then the experiment can be run
    else:
        #First, decide if the subject is an the experimenter, AI, or human (rule: the experimenter uses ID 0 and AI is given a negative ID which is then converted to a positive ID)
        #Experimenter ID given
        if(subject_information_object.get_ID() == 0):
            #The subject is the experimenter, saved data should only be used for system testing
            csv_filename = "toy"
        #AI ID given
        elif(subject_information_object.get_ID() < 0):
            #The subject is AI, data will go to the AI specific csv
            csv_filename = "ai"
            #We will also convert the ID to a positive number
            id = subject_information_object.get_ID()
            subject_information_object.set_ID(-id)
        #Human ID given
        else:
            #The subject is natural (human), data will go into the human specific csv
            csv_filename = "human"
        
        #Loop through each condition
        condition_list = condition_order_object.get_condition_list()
        for i in range(len(condition_list)):
            #Get the results of the condition and append them to the dataframe list
            dataframe_Tau, dataframe_FinalBet = experiment.run_test(subject_ID=subject_information_object.get_ID(), test_number=i+1, condition=condition_list[i])
            
            #Append the tau data to the csv
            filename = f"../{csv_filename}_test_data_Tau_c{condition_list[i]}.csv"
            try:
                append_dataframe_to_csv(filename, dataframe_Tau)
            except:
                #If csv file does not exist, then create a new csv with only a header to add to
                header_Tau = ["person", "game", "trial", "decision", "reward", "state"]
                new_dataframe = pd.DataFrame(dict(), columns=header_Tau)
                new_dataframe.to_csv(filename, index=False)
                append_dataframe_to_csv(filename, dataframe_Tau)
            
            #Append the WSLS data to the csv
            filename = f"../{csv_filename}_test_data_WSLS_c{condition_list[i]}.csv"
            try:
                #WSLS data is simply the Tau data without the "state" column
                dataframe_WSLS = dataframe_Tau.drop("state", axis="columns")
                append_dataframe_to_csv(filename, dataframe_WSLS)
            except:
                #If csv file does not exist, then create a new csv with only a header to add to
                header_WSLS = ["person", "game", "trial", "decision", "reward"]
                new_dataframe = pd.DataFrame(dict(), columns=header_WSLS)
                new_dataframe.to_csv(filename, index=False)
                append_dataframe_to_csv(filename, dataframe_WSLS)
            
            #Append the final bet data to the csv
            filename = f"../{csv_filename}_test_data_FinalBet.csv"
            try:
                append_dataframe_to_csv(filename, dataframe_Tau)
            except:
                #If csv file does not exist, then create a new csv with only a header to add to
                header_FinalBet = ["ID", "Condition", "Better_Team", "Total_Winnings", "Chosen_Team", "Final_Bet", "Proportion"]
                new_dataframe = pd.DataFrame(dict(), columns=header_FinalBet)
                new_dataframe.to_csv(filename, index=False)
                append_dataframe_to_csv(filename, dataframe_FinalBet)

        #At this point, the subject data has been saved, so save the subject information as well
        filename = f"../{csv_filename}_subject_info.csv"
        #Gether the dataframe describing all relevent information about the subject
        dataframe_new_subject = pd.DataFrame(subject_information_object.get_all_info())
        #Append the subject dataframe to the csv
        try:
            append_dataframe_to_csv(filename, dataframe_new_subject)
        except:
            #If csv file does not exist, then create a new csv with only a header to add to
            header_subject = ["id", "age", "sex"]
            new_dataframe = pd.DataFrame(dict(), columns=header_subject)
            new_dataframe.to_csv(filename, index=False)
            append_dataframe_to_csv(filename, dataframe_new_subject)


#Run the main program when executed as the main file
if(__name__ == "__main__"):
    main()