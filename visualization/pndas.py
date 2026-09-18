import pandas as pd
# 1D series
ages = pd.Series([25, 30, 35, 40], index=['Alice', 'Bob', 'Charlie', 'Dave'])
print(ages)
print('-'*20)
# 2D series
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Dave'],
    'age': [25, 30, 35, 40],
    'city': ['Lagos', 'Abuja', 'Lagos', 'Kano'],
    'score': [88.5, 92.1, 79.4, 95.0]
})
print(df)
print(df['age'][1]) #display all the age