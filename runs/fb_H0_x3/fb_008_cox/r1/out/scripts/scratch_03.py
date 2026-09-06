import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

def run():
    df = pd.read_csv('data.csv')
    df = df.drop_duplicates(keep='first')
    df = df.replace(-999, np.nan)
    df = df[(df['age']>=18) & (df['age']<=80)]
    df['treatment_norm'] = df['treatment'].str.strip().str.lower()
    df['enrol_date'] = pd.to_datetime(df['enrol_date'])
    df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
    df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days
    df = df[df['followup'] != 0]
    df['event_cens'] = df['event']
    mask = df['followup']>730
    df.loc[mask, 'event_cens'] = 0
    df.loc[mask, 'followup'] = 730
    df['exposure'] = (df['treatment_norm']=='fertilised').astype(int)
    model_df = df.dropna(subset=['age','exposure','event_cens','followup','treatment_norm'])

    exog = model_df[['exposure','age']]
    model = PHReg(model_df['followup'], exog, status=model_df['event_cens'], ties='breslow')
    result = model.fit()

    z = 1.96
    coef_exp = result.params[0]
    se_exp = result.bse[0]
    hr_exp = np.exp(coef_exp)
    ci_low = np.exp(coef_exp - z*se_exp)
    ci_high = np.exp(coef_exp + z*se_exp)
    p_exp = result.pvalues[0]
    hr_age = np.exp(result.params[1])

    claims = {
        'n_model': int(len(model_df)),
        'n_events': int(model_df['event_cens'].sum()),
        'median_followup_days': float(model_df['followup'].median()),
        'hr_exposure': float(hr_exp),
        'hr_ci_low': float(ci_low),
        'hr_ci_high': float(ci_high),
        'p_exposure': float(p_exp),
        'hr_age': float(hr_age)
    }
    return claims

claims = run()
print(json.dumps(claims))
