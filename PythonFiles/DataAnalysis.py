import pandas as pd
import matplotlib.pyplot as plt
import os

global_file_path = os.path.dirname(os.path.realpath(__file__))

filename = f"{global_file_path}\\..\\Data\\Final_Bet\\human_test_data_FinalBet.csv"
#filename = f"{global_file_path}\\..\\Data\\Final_Bet\\ai_test_data_FinalBet.csv"

dataframe = pd.read_csv(filename, header=0)

dataframe = dataframe.sort_values(["ID","Condition"])

subject_finalBet_dataframe = dataframe.groupby("ID")

specific_id_list = [1, 2, 3, 4, 5, 6, 7, 8] #All subjects
#specific_id_list = [1] #High-risk, dynamic betting
#specific_id_list = [5] #low-risk, dynamic betting
#specific_id_list = [4] #low-risk, static betting
#specific_id_list = [2, 3, 6, 7, 8] #high-risk, static betting
color = ["red", "orange", "yellow", "green", "blue", "cyan", "purple", "violet"]
for id, group_dataframe in subject_finalBet_dataframe:
    if(id not in set(specific_id_list)):
        continue
    group_dataframe = group_dataframe.drop(["Better_Team","Total_Winnings","Chosen_Team","Final_Bet"], axis="columns")
    p_diff = (100 - 10*(group_dataframe["Condition"] - 1)) - (0 + 10*(group_dataframe["Condition"] - 1))
    prop_bet = group_dataframe["Proportion"]
    plt.plot(p_diff, prop_bet, label=id, c=color[id-1])


plt.title("Human Test Results: Final Bet Proportion vs Team Probability Difference")
#plt.title("Human Subjects Final Bet: High-Risk and Static Betting")
#plt.title("ChatGPT Test Results: Final Bet Proportion vs Team Probability Difference")

plt.legend(loc="upper left")
plt.xlabel("Probability Difference Between Teams")
plt.ylabel("Proportion Bet")

plt.show()