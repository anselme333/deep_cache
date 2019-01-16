import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
df1 = pd.read_csv("C:/Users/anselme/Google Drive/research/Simulation_Research/Journal5/simulation/throughput_DCbC.csv",
                  low_memory=False)
df1.describe()
df1.sort_values(['Time'], inplace=True)
troughput1 = df1[['Time','Kilobytes']]
troughput_group1 = troughput1.groupby('Time').sum().sort_values('Kilobytes').reset_index()
#troughput_group1.unstack().plot(linewidth=4.0, title="", label='DCbC')

df2 = pd.read_csv("C:/Users/anselme/Google Drive/research/Simulation_Research/Journal5/simulation/throughput_MIRCC.csv",
                  low_memory=False)
df2.describe()
df2.sort_values(['Time'], inplace=True)
troughput2 = df2[['Time','Kilobytes']]
troughput_group2 = troughput2.groupby('Time').sum().sort_values('Kilobytes').reset_index()
print(troughput_group2.head(20))
#troughput_group2.unstack().plot(title="", linewidth=4.0, label='MIRCC')

df3 = pd.read_csv("C:/Users/anselme/Google Drive/research/Simulation_Research/Journal5/simulation/throughput_NCFCC.csv",
                  low_memory=False)
df3.describe()
df3.sort_values(['Time'], inplace=True)
troughput3 = df3[['Time','Kilobytes']]
troughput_group3 = troughput3.groupby('Time').sum().sort_values('Kilobytes').reset_index()
#ax = troughput_group3.unstack().plot(linewidth=4.0, title="", label='NCFCC')
plt.plot(troughput_group1['Kilobytes'], color='blue', linewidth=4.0, label='DeepAuc')
plt.plot(troughput_group2['Kilobytes'], linewidth=4.0, color='yellowgreen', label='MIRCC')
plt.plot(troughput_group3['Kilobytes'], linewidth=4.0, color='red', label='NCFCC')
#ax.set_xticklabels(troughput_group3.index)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.grid(color='gray')
plt.xlabel('Time', fontsize=18)
plt.ylabel('Throughput', fontsize=18)
plt.xlim(0,360)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.legend(title='', fontsize=18)
plt.show()
