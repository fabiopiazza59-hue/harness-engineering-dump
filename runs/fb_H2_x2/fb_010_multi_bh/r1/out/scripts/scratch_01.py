import pandas as pd, numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18)&(df['age']<=80)]
cols = ['savings','biomarker_1','biomarker_2','biomarker_3','biomarker_4','biomarker_5','biomarker_6']
df = df.dropna(subset=cols)

n_analysed = len(df)

biomarkers = [f'biomarker_{i}' for i in range(1,7)]
results = {}
pvals = []
rvals = []
for b in biomarkers:
    r,p = stats.pearsonr(df[b], df['savings'])
    rvals.append(r)
    pvals.append(p)

reject, p_adj, _, _ = multipletests(pvals, method='fdr_bh')

results_dict = {b: {'r': r, 'p_adj': pa} for b,r,pa in zip(biomarkers, rvals, p_adj)}

n_significant_adj = int(sum(p_adj < 0.05))

abs_rs = [abs(r) for r in rvals]
idx_max = int(np.argmax(abs_rs))
r_strongest = rvals[idx_max]

out = {
 'n_analysed': n_analysed,
 'r_biomarker_1': results_dict['biomarker_1']['r'],
 'p_adj_biomarker_1': results_dict['biomarker_1']['p_adj'],
 'r_biomarker_3': results_dict['biomarker_3']['r'],
 'p_adj_biomarker_3': results_dict['biomarker_3']['p_adj'],
 'p_adj_biomarker_5': results_dict['biomarker_5']['p_adj'],
 'n_significant_adj': n_significant_adj,
 'r_strongest': r_strongest
}
print(json.dumps(out))
