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
1. Load data.csv. 2. Remove exact duplicate rows (all columns identical), keep first. 3. Replace -999 with NaN across relevant columns (age, biomass). 4. Filter age between 18 and 80 inclusive (drop missing age too since filter can't apply). 5. Normalize treatment: strip whitespace, lowercase. 6. Drop rows with missing biomass. 7. Split into fertilised/unfertilised groups based on normalized treatment values. 8. Compute n per group, median per group, median_diff = median_fert - median_unfert. 9. Run scipy.stats.mannwhitneyu with alternative='two-sided', method='asymptotic', use_continuity=True. 10. U stat reported for fertilised group (u_stat = U for fertilised as first arg). 11. rank_biserial = 1 - 2*U/(n1*n2) using n1=fertilised n, n2=unfertilised n. 12. Print all claims as JSON.
