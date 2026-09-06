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
1. Load data.csv. 2. Drop exact duplicate rows (identical on every column), keep first. 3. Replace -999 with NaN across all columns (sentinel missing). 4. Filter age between 18 and 80 inclusive (drop missing age too since must be in range). 5. Normalize program: strip whitespace, lowercase. 6. Drop rows with missing savings. 7. Keep only rows where program is 'coaching' or 'waitlist' (drop others if any). 8. Compute n per group, median savings per group. 9. Run scipy.stats.mannwhitneyu(coaching, waitlist, alternative='two-sided', method='asymptotic', use_continuity=True) - U statistic reported for coaching group (that's the first argument). 10. Compute rank_biserial = 1 - 2*U/(n1*n2) where n1=n_coaching, n2=n_waitlist. 11. median_diff = median_coaching - median_waitlist. 12. Print JSON with all claims.
