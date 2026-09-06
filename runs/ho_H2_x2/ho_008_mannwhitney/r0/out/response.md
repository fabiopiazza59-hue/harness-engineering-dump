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
1. Load data.csv. 2. Drop exact duplicate rows (all columns identical), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive. 5. Normalize diet: strip whitespace, lowercase. 6. Drop rows with missing glucose_fu. 7. Split into mediterranean and usual groups based on normalized diet. 8. Compute n for each group. 9. Compute median glucose_fu for each group. 10. Compute median_diff = median_mediterranean - median_usual. 11. Run scipy.stats.mannwhitneyu with alternative='two-sided', use_continuity=True, method='asymptotic' on (mediterranean, usual) - report U for mediterranean group (first arg). 12. Compute p-value from that test. 13. Compute rank_biserial = 1 - 2*U/(n1*n2) where n1=n_mediterranean, n2=n_usual. 14. Save all as claims JSON.
