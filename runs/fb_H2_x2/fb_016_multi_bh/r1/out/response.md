# Run summary for fb_016_multi_bh

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_analysed": 344,
  "r_biomarker_1": 0.45475731660164226,
  "p_adj_biomarker_1": 3.501982336685894e-18,
  "r_biomarker_3": -0.32473696432571536,
  "p_adj_biomarker_3": 2.0612362737474602e-09,
  "p_adj_biomarker_5": 0.09436758685942508,
  "n_significant_adj": 2,
  "r_strongest": 0.45475731660164226
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (identical on every column), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive. 5. Drop rows missing any of rt_ms, biomarker_1..6 (complete case). 6. n_analysed = resulting row count. 7. For each biomarker_1..6, compute Pearson r and p-value vs rt_ms. 8. Apply BH FDR correction across the 6 p-values. 9. Extract r and adjusted p for biomarker_1, biomarker_3, biomarker_5. 10. n_significant_adj = count of adjusted p < 0.05. 11. r_strongest = signed r of biomarker with largest abs(r). 12. Print all as JSON.
