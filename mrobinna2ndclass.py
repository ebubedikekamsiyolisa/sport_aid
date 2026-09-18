import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

tips = pd.read_csv("C:/Users/hp/OneDrive/Documents/alpha.csv")
sns.set_theme(style='whitegrid')
sns.boxplot(data=tips, x = 'Day',y = 'Total Bill',hue = 'Gender')
plt.show()