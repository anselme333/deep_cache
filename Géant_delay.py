import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
df1 = pd.read_csv("C:/Users/anselme/Google Drive/research/Simulation_Research/Journal5/simulation/delay.csv",
                  low_memory=False)
df1.describe()
print(df1.head())
df1['DeepAuc'] = df1['DeepAuc'].convert_objects(convert_numeric=True)
df1['MIRCC'] = df1['MIRCC'].convert_objects(convert_numeric=True)
df1['NCFCC'] = df1['NCFCC'].convert_objects(convert_numeric=True)
fig, ax = plt.subplots()
medianprops = dict(linestyle='-', linewidth=2, color='blue')
bp=df1.boxplot(column=['DeepAuc','MIRCC','NCFCC'], showbox=True, notch=True, patch_artist=True, showmeans=True,
               meanline=True,medianprops=medianprops, showfliers=False, return_type='dict')
## change color and linewidth of the whiskers
for whisker in bp['whiskers']:
    whisker.set(color='#228b22', linewidth=2)

## change color and linewidth of the caps
for cap in bp['caps']:
    cap.set(color='#228b22', linewidth=2)

## change color and linewidth of the medians
for median in bp['medians']:
    median.set(color='red', linewidth=2)
## change color and linewidth of the medians
for median in bp['means']:
    median.set(color='black', linewidth=2)

## change the style of fliers and their fill
for flier in bp['fliers']:
    flier.set(marker='o', color='yello', alpha=0.5)

plt.ylabel('Delay (second)', fontsize=18)
plt.xlabel('Congestion control mechanisms', fontsize=18)
plt.xticks(fontsize = 18) # work on current fig
plt.yticks(fontsize = 18) # work on current fig
ax.set_yscale('log')
plt.grid(color='gray')
plt.show()