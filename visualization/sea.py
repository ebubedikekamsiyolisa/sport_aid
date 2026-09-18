import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
tips = pd.read_csv('C:/Users/USER/Desktop/records.csv') #load data set
# tips = sns.load_dataset()
sns.set_theme(style='whitegrid')
sns.boxplot(data=tips, x = 'day', y = 'Total bill', hue ='Gender')
plt.show()
