# Run summary for ho_013_multi_bh

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_analysed": 271,
  "r_biomarker_1": 0.4870554486770405,
  "p_adj_biomarker_1": 9.009457135971509e-17,
  "r_biomarker_3": -0.2868025042169946,
  "p_adj_biomarker_3": 4.7416054188900804e-06,
  "p_adj_biomarker_5": 0.004345390491568552,
  "n_significant_adj": 4,
  "r_strongest": 0.4870554486770405
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (identical on every column), keep first occurrence. 3. Replace -999 with NaN across all columns (sentinel missing). 4. Filter age between 18 and 80 inclusive. 5. Drop rows with missing any of sbp_12w, biomarker_1..6 (complete-case). 6. n_analysed = resulting row count. 7. For each biomarker_1..6, compute Pearson r and p-value vs sbp_12w (two-sided). 8. Apply BH FDR correction across the 6 p-values -> adjusted p-values. 9. Extract r_biomarker_1, p_adj_biomarker_1, r_biomarker_3, p_adj_biomarker_3, p_adj_biomarker_5. 10. n_significant_adj = count of adjusted p < 0.05. 11. r_strongest = signed r of biomarker with max abs(r). 12. Print JSON with all claims.
