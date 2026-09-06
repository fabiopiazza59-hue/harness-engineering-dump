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
1. Load data.csv. 2. Remove exact duplicate rows (identical on all columns), keep first. 3. Replace -999 with NaN across relevant columns (age, glucose_fu, etc.). 4. Filter to age between 18 and 80 inclusive. 5. Normalize diet: strip whitespace, lowercase. 6. Drop rows with missing glucose_fu. 7. Subset to diet in {'usual','mediterranean'} groups. 8. Compute n per group, medians per group, median_diff = median_mediterranean - median_usual. 9. Run scipy.stats.mannwhitneyu with alternative='two-sided', method='asymptotic' (with continuity correction, which is default in asymptotic method), compute U statistic for mediterranean group (x=mediterranean sample). 10. Compute rank_biserial = 1 - 2*U/(n1*n2) where n1=n_mediterranean, n2=n_usual. 11. Print all claims as JSON.
