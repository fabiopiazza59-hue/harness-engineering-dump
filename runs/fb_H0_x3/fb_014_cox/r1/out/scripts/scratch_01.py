import pandas as pd, numpy as np
from lifelines import CoxPHFitter
import json

df = pd.read_csv('data.csv')
print(df['condition'].unique())
print(df.shape)
df2 = df.drop_duplicates(keep='first')
print(df2.shape)
