# Run summary for ho_008_mannwhitney

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_usual": 192,
  "n_mediterranean": 202,
  "median_usual": 105.35,
  "median_mediterranean": 96.6,
  "median_diff": -8.75,
  "u_stat": 13059.0,
  "p_value": 2.087096990227714e-08,
  "rank_biserial": 0.32657797029702973
}

## Plan
1. Load data.csv. 2. Drop exact duplicate rows (identical on all columns), keep first. 3. Replace -999 with NaN across all columns (sentinel for missing). 4. Filter age between 18 and 80 inclusive (drop missing/out-of-range age). 5. Normalize diet: strip whitespace, lowercase. 6. Drop rows with missing glucose_fu. 7. Keep only rows where diet in {'usual','mediterranean'} (after normalization). 8. Compute n per group, median glucose_fu per group. 9. median_diff = median_mediterranean - median_usual. 10. Mann-Whitney U test two-sided, asymptotic with continuity correction (scipy.stats.mannwhitneyu with method='asymptotic', use_continuity=True), alternative='two-sided'. 11. u_stat = U for mediterranean group (need to set order so U corresponds to mediterranean as sample x). 12. rank_biserial = 1 - 2*U/(n1*n2) using n1=n_mediterranean, n2=n_usual. 13. Print all claims as JSON.
