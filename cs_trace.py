import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
df2=pd.read_csv("F:/DeepAuc_paper/New_result_deep_04_02_2019/Original/cs-trace.csv")
df2.describe()
df2.sort_values(['Mechanisms'], inplace=True)
print(df2.head())
troughput1=df2[['Mechanisms','Type','Packets']]
troughput_group1=troughput1.groupby(['Mechanisms','Type']).sum().sort_values('Packets')
troughput_group1.unstack().plot(kind='bar',stacked=True, width=0.2)
plt.ylabel('Total packets', fontsize=12)
plt.xlabel('Congestion control mechanisms', fontsize=12)
plt.legend(loc='upper left', fancybox=True, title='',fontsize = 12)
plt.xticks(fontsize = 12, rotation=0)
plt.yticks(fontsize = 12)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.grid(color='gray')
plt.show()
