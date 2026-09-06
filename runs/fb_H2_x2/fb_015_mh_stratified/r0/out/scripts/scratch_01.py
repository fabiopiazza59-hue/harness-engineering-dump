code = '''
import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv("data.csv")

# drop exact duplicates
df = df.drop_duplicates(keep="first")

# replace -999 sentinel with NaN across all columns
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# age filter
df = df[(df["age"]>=18) & (df["age"]<=80)]

# normalize diet
df["diet_norm"] = df["diet"].astype(str).str.strip().str.lower()

# keep only mediterranean/usual
df = df[df["diet_norm"].isin(["mediterranean","usual"])]

# need event and site non-missing
df = df.dropna(subset=["event","site"])

n_total = len(df)
n_exposed = int((df["diet_norm"]=="mediterranean").sum())

exposed = df["diet_norm"]=="mediterranean"
event = df["event"]==1

a = int(((exposed) & (event)).sum())
b = int(((exposed) & (~event)).sum())
c = int(((~exposed) & (event)).sum())
d = int(((~exposed) & (~event)).sum())

or_crude = (a*d)/(b*c)

# stratify by site
sites = sorted(df["site"].dropna().unique())
num = 0.0
den = 0.0
var_sum = 0.0
P_sum = 0.0
Q_sum = 0.0
R_sum = 0.0
S_sum = 0.0
sum_ad_over_n = 0.0
sum_bc_over_n = 0.0

site1_or = None

for s in sites:
    sub = df[df["site"]==s]
    ex = sub["diet_norm"]=="mediterranean"
    ev = sub["event"]==1
    ai = int(((ex)&(ev)).sum())
    bi = int(((ex)&(~ev)).sum())
    ci = int(((~ex)&(ev)).sum())
    di = int(((~ex)&(~ev)).sum())
    ni = ai+bi+ci+di
    if ni==0:
        continue
    num += (ai*di)/ni
    den += (bi*ci)/ni
    # RBG variance components
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    Ri = (ai*di)/ni
    Si = (bi*ci)/ni
    P_sum += Pi*Ri
    Q_sum += Pi*Si + Qi*Ri
    R_sum += Ri
    S_sum += Si
    Q_sum2 = Qi*Si
    if s==sites[0]:
        if bi>0 and ci>0 and ai>0 and di>0:
            site1_or = (ai*di)/(bi*ci)
        else:
            site1_or = (ai*di)/(bi*ci) if bi*ci!=0 else np.nan

# recompute variance sums properly with second loop to include Qi*Si term correctly
P_sum = 0.0
Q_sum_num = 0.0
R_sum = 0.0
S_sum = 0.0
for s in sites:
    sub = df[df["site"]==s]
    ex = sub["diet_norm"]=="mediterranean"
    ev = sub["event"]==1
    ai = int(((ex)&(ev)).sum())
    bi = int(((ex)&(~ev)).sum())
    ci = int(((~ex)&(ev)).sum())
    di = int(((~ex)&(~ev)).sum())
    ni = ai+bi+ci+di
    if ni==0:
        continue
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    Ri = (ai*di)/ni
    Si = (bi*ci)/ni
    P_sum += Pi*Ri
    Q_sum_num += Pi*Si + Qi*Ri
    R_sum += Ri
    S_sum += Si

or_mh = num/den

var_log_or_mh = (P_sum/(2*R_sum**2)) + (Q_sum_num/(2*R_sum*S_sum)) + (S_sum*0)  # placeholder fix below
# proper RBG formula:
# Var(ln OR_MH) = sum(Pi*Ri)/(2*(sum Ri)^2) + sum(Pi*Si+Qi*Ri)/(2*sum Ri*sum Si) + sum(Qi*Si)/(2*(sum Si)^2)
QS_sum = 0.0
for s in sites:
    sub = df[df["site"]==s]
    ex = sub["diet_norm"]=="mediterranean"
    ev = sub["event"]==1
    ai = int(((ex)&(ev)).sum())
    bi = int(((ex)&(~ev)).sum())
    ci = int(((~ex)&(ev)).sum())
    di = int(((~ex)&(~ev)).sum())
    ni = ai+bi+ci+di
    if ni==0:
        continue
    Qi = (bi+ci)/ni
    Si = (bi*ci)/ni
    QS_sum += Qi*Si

var_log_or_mh = (P_sum/(2*R_sum**2)) + (Q_sum_num/(2*R_sum*S_sum)) + (QS_sum/(2*S_sum**2))
se_log = np.sqrt(var_log_or_mh)
log_or = np.log(or_mh)
ci_low = np.exp(log_or - 1.96*se_log)
ci_high = np.exp(log_or + 1.96*se_log)

# MH chi-square with continuity correction
sum_a = 0.0
sum_Ea = 0.0
sum_Va = 0.0
for s in sites:
    sub = df[df["site"]==s]
    ex = sub["diet_norm"]=="mediterranean"
    ev = sub["event"]==1
    ai = int(((ex)&(ev)).sum())
    bi = int(((ex)&(~ev)).sum())
    ci = int(((~ex)&(ev)).sum())
    di = int(((~ex)&(~ev)).sum())
    ni = ai+bi+ci+di
    if ni==0:
        continue
    row1 = ai+bi
    row2 = ci+di
    col1 = ai+ci
    col2 = bi+di
    Ea = row1*col1/ni
    Va = row1*row2*col1*col2/(ni**2*(ni-1)) if ni>1 else 0
    sum_a += ai
    sum_Ea += Ea
    sum_Va += Va

numerator = (abs(sum_a - sum_Ea) - 0.5)**2
mh_chi2 = numerator/sum_Va
mh_p = 1 - stats.chi2.cdf(mh_chi2, df=1)

# site 1 OR
site1 = sites[0]
sub1 = df[df["site"]==site1]
ex1 = sub1["diet_norm"]=="mediterranean"
ev1 = sub1["event"]==1
a1 = int(((ex1)&(ev1)).sum())
b1 = int(((ex1)&(~ev1)).sum())
c1 = int(((~ex1)&(ev1)).sum())
d1 = int(((~ex1)&(~ev1)).sum())
or_site1 = (a1*d1)/(b1*c1)

result = {
    "n_total": n_total,
    "n_exposed": n_exposed,
    "or_crude": or_crude,
    "or_mh": or_mh,
    "or_mh_ci_low": ci_low,
    "or_mh_ci_high": ci_high,
    "mh_chi2": mh_chi2,
    "mh_p": mh_p,
    "or_site1": or_site1,
}

import json
print(json.dumps(result))
'''
with open('analysis.py','w') as f:
    f.write(code)
import subprocess
r = subprocess.run(['python3','analysis.py'], capture_output=True, text=True, cwd='.')
print(r.stdout)
print(r.stderr)
