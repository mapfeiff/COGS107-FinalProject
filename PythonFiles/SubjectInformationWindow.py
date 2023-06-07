#Import tkinter for python GUI
import tkinter as tk

#class to gather subject information
class Subject_Information():
    #Constructor to instantiate the ID and consent data members
    def __init__(self):
        self.ID = None
        self.age = None
        self.sex = None
        self.understanding = False
        self.consent = False
    
    #Set the ID for the subject
    def set_ID(self, id):
        self.ID = id
    #set the age for the subject
    def set_age(self, age):
        #raise exception for wrong input
        if(age <= 0):
            raise(Exception(f"Error: wrong input for the age paramter! Can only be positive number but wrote {age}"))
        self.age = age
    #set the sex for the subject
    def set_sex(self, sex):
        #set the letter to be captial
        sex = sex.upper()
        #raise exception for wrong input
        if(sex != "M" and sex != "F" and sex != "X"):
            raise(Exception(f"Error: wrong input for the sex paramter! Can only be (M, F, X) but wrote {sex}"))
        #set parameter
        self.sex = sex
    #Set the understanding for the subject
    def set_understanding(self, understanding):
        self.understanding = understanding
    #Set the consent for the subject
    def set_consent(self, consent):
        self.consent = consent
    
    #Get the ID of the subject
    def get_ID(self):
        return(self.ID)
    #Get the age of the subject
    def get_age(self):
        return(self.age)
    #Get the sex of the subject
    def get_sex(self):
        return(self.sex)
    #Get the understanding of the subject
    def get_understanding(self):
        return(self.understanding)
    #Get the consent of the subject
    def get_consent(self):
        return(self.consent)


#The subject provides information and agrees to the consent form
def subject_information_window():
    #Instatiate a condition order class
    subject = Subject_Information()
    
    #Instantiate a window
    window = tk.Tk()
    #Name the window
    window.title("Subject Information Window")

    #Instatiate Frame 1
    frame1 = tk.Frame(master=window)
    #display a title in frame 1
    title = tk.Label(master = frame1, text="Welcome to the Subject Information Window")
    title.pack()
    #place in frame 1
    frame1.pack()

    #Instatiate Frame 2
    frame2 = tk.Frame(master=window)
    #Instantiate Frame 2_1
    frame2_1 = tk.Frame(master=frame2)
    #display textbox to enter id
    ID_entry_label = tk.Label(master=frame2_1, text="Enter subject ID here:")
    ID_entry_label.pack(side=tk.LEFT)
    ID_entry = tk.Entry(master=frame2_1)
    ID_entry.pack(side=tk.RIGHT)
    #place in frame 2_1
    frame2_1.pack()
    #Instantiate Frame 2_2
    frame2_2 = tk.Frame(master=frame2)
    #display textbox to enter age
    age_entry_label = tk.Label(master=frame2_2, text="Enter age here:")
    age_entry_label.pack(side=tk.LEFT)
    age_entry = tk.Entry(master=frame2_2)
    age_entry.pack(side=tk.RIGHT)
    #place in frame 2_2
    frame2_2.pack()
    #Instantiate Frame 2_3
    frame2_3 = tk.Frame(master=frame2)
    #display textbox to enter sex
    sex_entry_label = tk.Label(master=frame2_3, text="Enter sex (M=male, F=female, or X=other/prefer not to say) here:")
    sex_entry_label.pack(side=tk.LEFT)
    sex_entry = tk.Entry(master=frame2_3)
    sex_entry.pack(side=tk.RIGHT)
    #place in frame 2_3
    frame2_3.pack()
    #place in frame 2
    frame2.pack()

    #Instantiate frame 3
    frame3 = tk.Frame(master=window)
    #display the experiment information to the subject
    top_space_label = tk.Label(master=frame3, text="")
    top_space_label.pack()
    experiment_information_label = tk.Label(master=frame3, text="Test informatio here pls")
    experiment_information_label.pack()
    bottom_space_label = tk.Label(master=frame3, text="")
    bottom_space_label.pack()
    #place in frame 3
    frame3.pack()

    #Instatiate frame 4
    frame4 = tk.Frame(master=window)
    #display checkbox for consent
    undertanding_checkbox_var = tk.IntVar()
    undertanding_check = tk.Checkbutton(master=frame4, text="I understand the details of the study.", variable=undertanding_checkbox_var)
    undertanding_check.pack()
    #display checkbox for consent
    consent_checkbox_var = tk.IntVar()
    consent_check = tk.Checkbutton(master=frame4, text="I hereby give my consent to participate in the study and use any data provided.", variable=consent_checkbox_var)
    consent_check.pack()
    #place in frame 4
    frame4.pack()

    #Instantiate Frame 5
    frame5 = tk.Frame(master=window)
    #define a function for what happens when the button is submitted (nested function allos us to use external variables)
    def submit_submission():
        #gather the data items from the window
        subject_ID = int(ID_entry.get())
        subject_age = int(age_entry.get())
        subject_sex = sex_entry.get()
        subject_understanding = bool(undertanding_checkbox_var.get())
        subject_consent = bool(consent_checkbox_var.get())
        #save the data inside the subject information object
        subject.set_ID(subject_ID)
        subject.set_age(subject_age)
        subject.set_sex(subject_sex)
        subject.set_understanding(subject_understanding)
        subject.set_consent(subject_consent)
        #close the window
        window.destroy()
    #Create a submit button to close the window
    btn_submit = tk.Button(master=frame5, text="Submit", command=submit_submission)
    btn_submit.pack()
    #place in frame 5
    frame5.pack()
    
    #execute the window (blocking function)
    window.mainloop()

    #return the subject information object
    return(subject)