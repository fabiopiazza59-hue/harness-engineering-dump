# Run summary for ho_014_mannwhitney

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_unfertilised": 120,
  "n_fertilised": 121,
  "median_unfertilised": 419.5,
  "median_fertilised": 475.9,
  "median_diff": 56.39999999999998,
  "u_stat": 9670.5,
  "p_value": 8.441766954014353e-06,
  "rank_biserial": -0.3320247933884297
}

## Plan
1. Load data.csv (268 records). 2. Remove exact duplicate rows (identical on every column), keep first occurrence. 3. Replace -999 sentinel values with NaN across relevant columns (especially biomass). 4. Filter to age between 18 and 80 inclusive. 5. Normalise treatment: strip whitespace, lower-case. 6. Exclude rows with missing biomass (complete-case). 7. Split into fertilised vs unfertilised groups based on normalised treatment. 8. Compute n per group, median biomass per group, median_diff = median_fertilised - median_unfertilised. 9. Run two-sided Mann-Whitney U test (scipy.stats.mannwhitneyu, use_continuity=True, alternative='two-sided', method='asymptotic'); report U for fertilised group (need to set correct group order in mannwhitneyu(fertilised, unfertilised) so that returned U corresponds to fertilised group per scipy convention: U1 for first sample). 10. Compute rank-biserial = 1 - 2*U/(n1*n2) where U is for fertilised group, n1=n_fertilised, n2=n_unfertilised. 11. Output JSON with all claim slots. 12. Save as analysis.py, verify counts and value ranges before submission.
