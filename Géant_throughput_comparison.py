import matplotlib.pyplot as plt
from pylab import *
from matplotlib import style
import matplotlib.colors as clrs
#from bokeh.charts import BoxPlot, output_file, show
#style.use('ggplot')
import numpy as np
import pandas as pd
import seaborn as sns
import pandas as pd
#from bokeh.charts import TimeSeries, show, output_file
DeepAuC = pd.read_csv(
        "F:/DeepAuc_paper/New_result_deep_04_02_2019/Original/rate-trace_GEANT2_DeepAuC_05_02_2019.csv")
MIRCC = pd.read_csv(
    "F:/DeepAuc_paper/New_result_deep_04_02_2019/Original/rate-trace_GEANT2_mircc_05_02_2019.csv")
NCFCC = pd.read_csv(
        "F:/DeepAuc_paper/New_result_deep_04_02_2019/Original/rate-trace_GEANT2_NCFCC_05_02_2019.csv")

xyvalues = pd.DataFrame(dict(
    DeepAuC=DeepAuC['DeepAuC'],
    NCFCC=NCFCC['NCFCC'],
    MIRCC=MIRCC['MIRCC']))
print(xyvalues)
xyvalues1=xyvalues.rolling(window=10, center=True).mean()
xyvalues1.plot(linewidth=3.0)
plt.xlim(10, 360)
plt.ylim(-10, 550)
plt.ylabel(' Throughput (Kbps)', fontsize=12)
plt.xlabel('Time (Second)', fontsize=12)
plt.xticks(fontsize = 12) # work on current fig
plt.yticks(fontsize = 12) # work on current fig
plt.legend(loc='upper left', fancybox=True, title='',fontsize = 12)
plt.ticklabel_format( style='sci', axis='y', scilimits=(0,0))
plt.grid(color='gray')
plt.show()
