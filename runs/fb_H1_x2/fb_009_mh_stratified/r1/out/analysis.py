import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('data.csv')
# 2. remove exact duplicates
df = df.drop_duplicates(keep='first')
# 3. replace -999 sentinel with NaN across all columns
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)
# 4. filter age 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]
# 5. normalize diet
df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()
# 6. drop rows missing age, diet, event, site
df = df.dropna(subset=['age','diet_norm','event','site'])

df['exposed'] = df['diet_norm']=='mediterranean'

n_total = len(df)
n_exposed = int(df['exposed'].sum())

# crude OR: exposed vs unexposed, event vs no event
a = ((df['exposed']) & (df['event']==1)).sum()
b = ((df['exposed']) & (df['event']==0)).sum()
c = ((~df['exposed']) & (df['event']==1)).sum()
d = ((~df['exposed']) & (df['event']==0)).sum()
or_crude = (a*d)/(b*c)

print('table', a,b,c,d)

sites = sorted(df['site'].unique())
num_sum = 0.0
den_sum = 0.0
var_num = 0.0  # for Robins-Breslow-Day-Greenland variance
P_sum=0.0
Q_sum=0.0
R_sum=0.0
S_sum=0.0
O_minus_E_sum = 0.0
var_sum = 0.0
site_ors = {}
for s in sites:
    sub = df[df['site']==s]
    a_i = ((sub['exposed']) & (sub['event']==1)).sum()
    b_i = ((sub['exposed']) & (sub['event']==0)).sum()
    c_i = ((~sub['exposed']) & (sub['event']==1)).sum()
    d_i = ((~sub['exposed']) & (sub['event']==0)).sum()
    n_i = a_i+b_i+c_i+d_i
    if n_i==0:
        continue
    num_sum += (a_i*d_i)/n_i
    den_sum += (b_i*c_i)/n_i
    if (b_i*c_i)!=0 and (a_i*d_i)!=0:
        site_ors[s] = (a_i*d_i)/(b_i*c_i)
    else:
        site_ors[s] = np.nan
    # MH chi-square components
    E_i = (a_i+b_i)*(a_i+c_i)/n_i
    V_i = (a_i+b_i)*(c_i+d_i)*(a_i+c_i)*(b_i+d_i)/(n_i**2*(n_i-1)) if n_i>1 else 0
    O_minus_E_sum += (a_i - E_i)
    var_sum += V_i
    # Robins-Breslow-Greenland variance for OR
    P_i = (a_i+d_i)/n_i
    Q_i = (b_i+c_i)/n_i
    R_i = a_i*d_i/n_i
    S_i = b_i*c_i/n_i
    P_sum += P_i*R_i
    Q_sum += (P_i*S_i + Q_i*R_i)
    S_sum += Q_i*S_i

or_mh = num_sum/den_sum

# Robins-Breslow-Greenland variance of ln(OR_mh)
var_ln_or = P_sum/(2*num_sum**2) + Q_sum/(2*num_sum*den_sum) + S_sum/(2*den_sum**2)
se_ln_or = np.sqrt(var_ln_or)
ci_low = np.exp(np.log(or_mh) - 1.96*se_ln_or)
ci_high = np.exp(np.log(or_mh) + 1.96*se_ln_or)

# MH chi-square with continuity correction
mh_chi2 = (abs(O_minus_E_sum)-0.5)**2 / var_sum
mh_p = 1 - stats.chi2.cdf(mh_chi2, df=1)

or_site1 = site_ors[1]

result = {
 'n_total': n_total,
 'n_exposed': n_exposed,
 'or_crude': or_crude,
 'or_mh': or_mh,
 'or_mh_ci_low': ci_low,
 'or_mh_ci_high': ci_high,
 'mh_chi2': mh_chi2,
 'mh_p': mh_p,
 'or_site1': or_site1
}
import json
print(json.dumps(result))
