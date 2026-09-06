# Run summary for ho_001_ttest

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_placebo": 89,
  "n_caffeine": 90,
  "mean_placebo": 706.9932584269662,
  "mean_caffeine": 682.9911111111111,
  "sd_caffeine": 99.26045824891838,
  "mean_diff": -24.002147315855154,
  "t_stat": -1.601365191318443,
  "p_value": 0.11108100293042009,
  "cohens_d": -0.23941371382337256
}

## Plan
1. Load data.csv. 2. Apply exclusions in order: (a) keep age between 18 and 80 inclusive; (b) drop rows with missing rt_ms; (c) compute overall mean and sample SD (n-1) of rt_ms on remaining data, remove rows where rt_ms is more than 3 SD from that mean. 3. Split by condition into placebo and caffeine groups. 4. Compute n, mean, sample SD (n-1) per group. 5. Compute mean_diff = mean_caffeine - mean_placebo. 6. Welch's t-test (unequal variances), two-sided, via scipy.stats.ttest_ind(equal_var=False) -> t_stat, p_value. 7. Cohen's d = mean_diff / pooled_sd, pooled_sd = sqrt(((n1-1)*sd1^2+(n2-1)*sd2^2)/(n1+n2-2)). 8. Print all claims as JSON.
