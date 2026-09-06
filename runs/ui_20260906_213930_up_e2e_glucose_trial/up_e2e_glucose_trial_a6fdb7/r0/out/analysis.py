import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
n_total_collected = len(df)

# exclusion 1: age 18-80 inclusive
df1 = df[(df['age']>=18) & (df['age']<=80)]

# exclusion 2: missing glucose_fu
df2 = df1[df1['glucose_fu'].notna()]

# exclusion 3: outliers >3 SD from overall mean (on remaining data)
mean_all = df2['glucose_fu'].mean()
sd_all = df2['glucose_fu'].std(ddof=1)
df3 = df2[np.abs(df2['glucose_fu'] - mean_all) <= 3*sd_all]

usual = df3[df3['diet']=='usual']['glucose_fu']
med = df3[df3['diet']=='mediterranean']['glucose_fu']

n_usual = len(usual)
n_mediterranean = len(med)

mean_glucose_usual = usual.mean()
mean_glucose_mediterranean = med.mean()
sd_glucose_mediterranean = med.std(ddof=1)
sd_glucose_usual = usual.std(ddof=1)

mean_difference = mean_glucose_mediterranean - mean_glucose_usual

t_stat, p_val = stats.ttest_ind(med, usual, equal_var=True)

pooled_sd = np.sqrt(((n_usual-1)*sd_glucose_usual**2 + (n_mediterranean-1)*sd_glucose_mediterranean**2) / (n_usual+n_mediterranean-2))
cohens_d = mean_difference / pooled_sd

claims = {
 'n_total_collected': n_total_collected,
 'n_usual': n_usual,
 'n_mediterranean': n_mediterranean,
 'mean_glucose_usual': mean_glucose_usual,
 'mean_glucose_mediterranean': mean_glucose_mediterranean,
 'sd_glucose_mediterranean': sd_glucose_mediterranean,
 'mean_difference': mean_difference,
 't_statistic': t_stat,
 'p_value': p_val,
 'cohens_d': cohens_d
}
print(json.dumps(claims))
