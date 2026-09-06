import pandas as pd, numpy as np
from scipy.stats import chi2

df = pd.read_csv('data.csv')
# remove exact duplicates
df = df.drop_duplicates(keep='first')
# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age']>=18)&(df['age']<=80)]
# normalize diet
df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()
df = df[df['diet_norm'].isin(['mediterranean','usual'])]
# drop missing event or site
df = df.dropna(subset=['event','site'])

n_total = len(df)
n_exposed = (df['diet_norm']=='mediterranean').sum()

exposed = df['diet_norm']=='mediterranean'
event = df['event']==1

a = ((exposed) & (event)).sum()
b = ((exposed) & (~event)).sum()
c = ((~exposed) & (event)).sum()
d = ((~exposed) & (~event)).sum()
or_crude = (a*d)/(b*c)

sites = sorted(df['site'].unique())
num = 0.0
den = 0.0
PR_sum=0.0
PS_sum=0.0
QR_sum=0.0
QS_sum=0.0
R_sum=0.0
S_sum=0.0
sum_a=0.0
sum_Ea=0.0
sum_Va=0.0

site_ors = {}
for s in sites:
    sub = df[df['site']==s]
    ai = ((sub['diet_norm']=='mediterranean') & (sub['event']==1)).sum()
    bi = ((sub['diet_norm']=='mediterranean') & (sub['event']==0)).sum()
    ci = ((sub['diet_norm']=='usual') & (sub['event']==1)).sum()
    di = ((sub['diet_norm']=='usual') & (sub['event']==0)).sum()
    ni = ai+bi+ci+di
    if ni==0:
        continue
    num += ai*di/ni
    den += bi*ci/ni
    if s==1:
        or_site1 = (ai*di)/(bi*ci)
    # RBG variance components
    PR_sum += (ai+di)*(ai*di)/ni**2
    PS_sum += (ai+di)*(bi*ci)/ni**2
    QR_sum += (bi+ci)*(ai*di)/ni**2
    QS_sum += (bi+ci)*(bi*ci)/ni**2
    R_sum += ai*di/ni
    S_sum += bi*ci/ni
    # MH test statistics
    ni1 = ai+bi  # exposed total
    ni0 = ci+di  # unexposed total
    m1 = ai+ci   # event total
    m0 = bi+di
    Ea = ni1*m1/ni
    Va = ni1*ni0*m1*m0/(ni**2*(ni-1)) if ni>1 else 0
    sum_a += ai
    sum_Ea += Ea
    sum_Va += Va

or_mh = num/den

# RBG variance of ln(OR_mh)
var_ln_or = (PR_sum/(2*R_sum**2)) + (PS_sum*QR_sum + QS_sum*R_sum*S_sum... )
