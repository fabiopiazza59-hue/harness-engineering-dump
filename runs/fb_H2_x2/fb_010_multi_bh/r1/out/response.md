# Run summary for fb_010_multi_bh

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_analysed": 291,
  "r_biomarker_1": 0.49773822919901184,
  "p_adj_biomarker_1": 7.633757228942548e-19,
  "r_biomarker_3": -0.3178142009352862,
  "p_adj_biomarker_3": 8.943947025490594e-08,
  "p_adj_biomarker_5": 0.0004143740270936808,
  "n_significant_adj": 3,
  "r_strongest": 0.49773822919901184
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (all columns identical), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive. 5. Drop rows with missing savings or any of biomarker_1..6 (complete case). 6. n_analysed = resulting row count. 7. For each biomarker_i, compute Pearson r and p-value vs savings. 8. Apply BH adjustment across the 6 p-values (statsmodels multipletests method='fdr_bh'). 9. Extract r and adjusted p for biomarker_1, biomarker_3, biomarker_5. 10. n_significant_adj = count of adjusted p < 0.05. 11. r_strongest = signed r of biomarker with max abs(r). 12. Print JSON with all claims.
