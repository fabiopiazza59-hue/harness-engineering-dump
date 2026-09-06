# Run summary for ho_013_multi_bh

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_analysed": 271,
  "r_biomarker_1": 0.4870554486770405,
  "p_adj_biomarker_1": 9.00945713597151e-17,
  "r_biomarker_3": -0.2868025042169946,
  "p_adj_biomarker_3": 4.7416054188900804e-06,
  "p_adj_biomarker_5": 0.0043453904915685525,
  "n_significant_adj": 4,
  "r_strongest": 0.4870554486770405
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (identical on every column), keep first occurrence. 3. Replace -999 with NaN across all columns (sentinel missing). 4. Filter age between 18 and 80 inclusive. 5. Drop rows with missing sbp_12w or any of biomarker_1..6 (complete-case). 6. n_analysed = resulting row count. 7. For each biomarker_i, compute Pearson r and two-sided p-value vs sbp_12w. 8. Apply BH FDR correction across the 6 p-values. 9. Extract r and adjusted p for biomarker_1, biomarker_3, biomarker_5. 10. Count biomarkers with adjusted p < 0.05 -> n_significant_adj. 11. Find biomarker with largest |r| -> r_strongest (signed). 12. Print all as JSON.
