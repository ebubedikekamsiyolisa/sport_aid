# matplotlib - > line, bar and scatter plot
# seaborn - correlation heatmap
# bokeh ->browser-based plot
# plotly -> dashboard, web apps
# pandas

import pandas as pd

# score = [50, 60, 90,55]
# s = pd.Series(score, index=["Maths", "Eng", "Phy", "Chm"])
# print(s)

data = {
    "Name":["Tinubu", "Obi","Atiku"],
    "Age": [40,60,34],
    "score":[300,430,900]
}
df = pd.DataFrame(data)
print(df["Name"][0])