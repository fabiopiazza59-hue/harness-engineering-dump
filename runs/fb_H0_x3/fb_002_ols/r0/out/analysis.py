import pandas as pd
import numpy as np
import statsmodels.api as sm
import json

df = pd.read_csv('data.csv')
# exclusion 1: age between 18 and 80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
# exclusion 2: drop missing biomass or bmi
df = df.dropna(subset=['biomass', 'bmi'])

df['exposure'] = (df['treatment'] == 'fertilised').astype(int)

X = df[['exposure', 'age', 'bmi', 'baseline']]
X = sm.add_constant(X)
y = df['biomass']

model = sm.OLS(y, X).fit()

result = {
 'n_model': int(model.nobs),
 'coef_exposure': model.params['exposure'],
 'se_exposure': model.bse['exposure'],
 'p_exposure': model.pvalues['exposure'],
 'coef_age': model.params['age'],
 'r_squared': model.rsquared,
 'adj_r_squared': model.rsquared_adj
}
print(json.dumps(result))
