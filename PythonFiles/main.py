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

        #First open the file with all the previously gathered data
        try:
            dataframe_Tau = pd.read_csv(f"../{csv_filename}_test_data_Tau.csv", header=0)
        #If the file does not exist, create a new data file
        except:
            header_Tau = ["person", "game", "trial", "decision", "reward", "state"]
            dataframe_Tau = pd.DataFrame(dict(), columns=header_Tau)
        
        #Create a list of dataframes to add additional trials to
        df_Tau_list = list()
        #append the previos data to the list
        df_Tau_list.append(dataframe_Tau)
        #Loop through each condition
        condition_list = condition_order_object.get_condition_list()
        for i in range(len(condition_list)):
            #Get the results of the condition and append them to the dataframe list
            dataframe_Tau = experiment.run_test(subject_ID=subject_information_object.get_ID(), test_number=i+1, condition=condition_list[i])
            #append dataframe into list
            df_Tau_list.append(dataframe_Tau)
        #Concatinate all the new dataframes into a single instance
        dataframe_Tau = pd.concat(df_Tau_list)
        #Write the data to the Tau model csv
        dataframe_Tau.to_csv(f"../{csv_filename}_test_data_Tau.csv", index=False)
        #Lastly, drop the "state" column and add the data to the Win-Stay;Lose-Shift (WSLS) model csv
        dataframe_WSLS = dataframe_Tau.drop(columns=["state"])
        dataframe_WSLS.to_csv(f"../{csv_filename}_test_data_WSLS.csv", index=False)

        #At this point, the subject data has been saved, so save the subject information as well
        #First open the file with all the previously gathered data
        try:
            dataframe_subject = pd.read_csv(f"../{csv_filename}_subject_info.csv", header=0)
        #If the file does not exist, create a new data file
        except:
            header_subject = ["id", "age", "sex"]
            dataframe_subject = pd.DataFrame(dict(), columns=header_subject)
        #Then create a dataframe of the new subject information
        dataframe_new_subject = pd.DataFrame(subject_information_object.get_all_info())
        #Next, concatinate all the new dataframes to the old one
        df_subject_list = [dataframe_subject, dataframe_new_subject]
        dataframe_Tau = pd.concat(df_subject_list)
        #Lastly, write the dataframe into the csv
        dataframe_Tau.to_csv(f"../{csv_filename}_subject_info.csv", index=False)


#Run the main program when executed as the main file
if(__name__ == "__main__"):
    main()