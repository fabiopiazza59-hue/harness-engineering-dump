# Run summary for ho_007_multi_bh

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_analysed": 373,
  "r_biomarker_1": 0.5151716689332558,
  "p_adj_biomarker_1": 6.795760569079606e-26,
  "r_biomarker_3": -0.3301967368376184,
  "p_adj_biomarker_3": 1.8444880729546843e-10,
  "p_adj_biomarker_5": 0.009969775767624933,
  "n_significant_adj": 5,
  "r_strongest": 0.5151716689332558
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (all columns identical), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive. 5. Drop rows with missing sbp_12w or biomarker_1..6 (complete case). 6. n_analysed = resulting row count. 7. For each biomarker_1..6, compute Pearson r and p-value vs sbp_12w. 8. BH-adjust the 6 p-values (statsmodels multipletests method='fdr_bh'). 9. Extract r and adj p for biomarker_1, biomarker_3, biomarker_5. 10. n_significant_adj = count adj p < 0.05. 11. r_strongest = signed r of biomarker with max abs(r). 12. Print all claims as JSON.
