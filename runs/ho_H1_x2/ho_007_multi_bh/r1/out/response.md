# Run summary for ho_007_multi_bh

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_analysed": 373,
  "r_biomarker_1": 0.5151716689332558,
  "p_adj_biomarker_1": 6.795760569079605e-26,
  "r_biomarker_3": -0.3301967368376184,
  "p_adj_biomarker_3": 1.844488072954684e-10,
  "p_adj_biomarker_5": 0.009969775767624933,
  "n_significant_adj": 5,
  "r_strongest": 0.5151716689332558
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (identical on every column), keep first. 3. Replace -999 with NaN across all columns (sentinel missing). 4. Filter age between 18 and 80 inclusive (drop missing age too). 5. Drop rows with missing sbp_12w or biomarker_1..6 (complete case). 6. n_analysed = resulting row count. 7. For each biomarker_1..6, compute Pearson r and two-sided p-value vs sbp_12w. 8. Apply BH FDR adjustment across the 6 p-values. 9. Extract r and adjusted p for biomarker_1, biomarker_3, biomarker_5. 10. Count biomarkers with adjusted p<0.05 -> n_significant_adj. 11. Find biomarker with max abs(r) -> r_strongest (signed). 12. Print JSON with all claims.
