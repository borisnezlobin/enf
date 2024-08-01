import pandas as pd

# csv format:
# Time;f60_US_UT01;QI_US_UT01
# timestamp, deviation from base (in mHz), 0

df = pd.read_csv('US_UT01.csv')
BASE_HZ = 60

print(df.head())

deviations = df['f60_US_UT01'].divide(1000).add(BASE_HZ)[:86400]

# plot the data in the second column
import matplotlib.pyplot as plt
plt.plot(deviations)
# make the plotted line thinner
plt.setp(plt.gca().get_lines(), linewidth=1)

plt.show()