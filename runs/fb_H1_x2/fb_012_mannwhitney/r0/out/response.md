# Run summary for fb_012_mannwhitney

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_waitlist": 204,
  "n_coaching": 207,
  "median_waitlist": 314.0,
  "median_coaching": 377.9,
  "median_diff": 63.89999999999998,
  "u_stat": 28388.0,
  "p_value": 1.534699155096575e-09,
  "rank_biserial": -0.34451075116036756
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (identical on every column), keep first. 3. Replace -999 with NaN across all columns (sentinel missing). 4. Filter age between 18 and 80 inclusive (drop missing age or out of range). 5. Normalise program: strip whitespace, lowercase. 6. Drop rows with missing savings (complete-case). 7. Subset into coaching and waitlist groups based on normalized program. 8. Compute n per group, median savings per group, median_diff = median_coaching - median_waitlist. 9. Run scipy.stats.mannwhitneyu(coaching, waitlist, alternative='two-sided', use_continuity=True, method='asymptotic') to get U statistic for coaching group and p-value. 10. Compute rank_biserial = 1 - 2*U/(n1*n2) where n1=n_coaching, n2=n_waitlist. 11. Print all as JSON.
