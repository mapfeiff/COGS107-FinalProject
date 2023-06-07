# COGS 107 - Final Project - Bandit Problem Analysis
## Contents:
> These files contain the source code and data related to the bandit problem experiment. This is a 2 alternative, finite-horizon (15-choices) environment.
>
> The data in the files are as follows:
>> 1. <u>human-test-data_WSLS.csv</u>: WSLS Model formatted data using human test subjects
>>
>> 2. <u>human-test-data_Tau.csv</u>: Tau Model formatted data using human test subjects
>>
>> 3. <u>ai-test-data_WSLS.csv</u>: WSLS Model formatted data using artificial test subjects
>>
>> 4. <u>ai-test-data_Tau.csv</u>: Tau Model formatted data using artificial test subjects
>>
>> 5. <u>toy-test-data_WSLS.csv</u>: WSLS Model formatted data using no test subject (only used to ensure the system works properly)
>>
>> 6. <u>toy-test-data_Tau.csv</u>: Tau Model formatted data using no test subject (only used to ensure the system works properly)

## Requirements
> The complete list of requirements are in the requirement.txt file
>
> The main dependecies to have installed are as follows:
>> 1. pandas
>>
>> 2. tkinter
>
> If you have the requirements met on your system, you can directly run the ./main.py file directly instead of executing ./start-up.sh (the start-up will pip install all requirements via the "pip install -r requirements.txt" command)

## How to Run:
> 1. Create a python virtual environment (optional, but recommended since start-up will install some libraries)
>
> 2. Execute the start-up sequence by entering "./start-up.sh" in your environment's terminal (pip installation of all requirements part of start-up process)
>
> 3. Run through the experiment (ensure that you have and enter the proper subject ID that is given to you)
>
> 4. Lastly, after finishing all tests, execute the "./end-down.sh" command in your environment's terminal to anonymously save all data to github (anonymous pushing required for subject confidentiality)
>
> 5. Can now decide what to do with the files on your system (since all data is saved on github, you can either keep or delete them) 