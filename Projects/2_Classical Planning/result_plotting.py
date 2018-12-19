# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# constants
PROBLEMS = ["Air Cargo Problem 1",
            "Air Cargo Problem 2",
            "Air Cargo Problem 3",
            "Air Cargo Problem 4"]
SEARCHES = ["breadth_first_search", 
            'depth_first_graph_search', 
            'uniform_cost_search',
            'greedy_best_first_graph_search-h_unmet_goals',
            'greedy_best_first_graph_search-h_pg_levelsum',
            'greedy_best_first_graph_search-h_pg_maxlevel',
            'greedy_best_first_graph_search-h_pg_setlevel',
            'astar_search-h_unmet_goals',
            'astar_search-h_pg_levelsum',
            'astar_search-h_pg_maxlevel',
            'astar_search-h_pg_setlevel'
            ]


# load data frame
df_search= pd.DataFrame()
df_search["AlgName"]= SEARCHES
df_search["Alg"]= [i+1 for i in range(11)]
df= pd.read_csv("Summary.csv")


df_all= df.merge(df_search, left_on='Alg', right_on='Alg', how= 'outer')
df_all= df_all.sort_values(["Problem","Alg"])


#%% Nodes vs Actions
dfs= df.sort_values(by=["Actions"])
plt.figure()
plt.plot(dfs.Actions, dfs.NewNodes, 'o')
plt.xlabel("Number of Actions")
plt.ylabel("Number of New Nodes")


boxplot= df.boxplot(column=["NewNodes"], by=["Actions"])


sns.catplot(x="Actions", y="NewNodes", hue="Alg", kind="point", data=df)

#%% Time vs Number of Actions
plt.figure()
plt.plot(df.Actions, df.ElapsedTime, 'o')
plt.xlabel("Number of Actions")
plt.ylabel("Elapsed Time")


boxplot= df.boxplot(column=["ElapsedTime"], by=["Actions"])


sns.catplot(x="Actions", y="ElapsedTime", hue="Alg", kind="point", data=df)

#%% Length of Plans
sns.catplot(x="AlgName", y="PlanLength", hue="Problem", data=df_all, kind='bar')
plt.xticks(rotation=75, fontsize= 10)
plt.xlabel("Algorithm")
plt.ylabel("Plan Length")
ax= plt.gca()
ax.set_position([0.1, 0.4, 0.8, 0.55])

sns.catplot(x="Problem", y="PlanLength", hue="AlgName", data=df_all, kind='bar')
plt.xlabel("Problem")
plt.ylabel("Plan Length")

