import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')

# 1. drop exact duplicates
df = df.drop_duplicates(keep='first')

# 2. replace -999 sentinel with NaN in numeric columns
num_cols = df.select_dtypes(include=[np.number]).columns
df[num_cols] = df[num_cols].replace(-999, np.nan)

# 3. normalize treatment
df['treatment'] = df['treatment'].astype(str).str.strip().str.lower()

# 4. filter age 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

# 5. compute follow-up days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# 6. exclude zero followup
df = df[df['followup'] != 0]

# 7. administrative censoring at 730
mask = df['followup'] > 730
df.loc[mask, 'followup'] = 730
df.loc[mask, 'event'] = 0

# keep only rows with valid treatment labels
df = df[df['treatment'].isin(['fertilised','unfertilised'])]

# exposure coding
df['exposure'] = (df['treatment']=='fertilised').astype(int)

# complete case
model_df = df.dropna(subset=['age','event','followup','exposure']).copy()

n_model = len(model_df)
n_events = int(model_df['event'].sum())
median_followup = float(model_df['followup'].median())

exog = model_df[['exposure','age']].values
model = PHReg(model_df['followup'].values, exog, status=model_df['event'].values, ties='breslow')
result_fit = model.fit()

params = result_fit.params
se = result_fit.bse
pvals = result_fit.pvalues

hr_exposure = float(np.exp(params[0]))
hr_ci_low = float(np.exp(params[0] - 1.96*se[0]))
hr_ci_high = float(np.exp(params[0] + 1.96*se[0]))
p_exposure = float(pvals[0])
hr_age = float(np.exp(params[1]))

result = {
 'n_model': n_model,
 'n_events': n_events,
 'median_followup_days': median_followup,
 'hr_exposure': hr_exposure,
 'hr_ci_low': hr_ci_low,
 'hr_ci_high': hr_ci_high,
 'p_exposure': p_exposure,
 'hr_age': hr_age
}
print(json.dumps(result))
