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
1. Load data.csv. 2. Exclude participants with age<18 or age>80. 3. Exclude participants with missing rt_ms. 4. Compute overall mean and sample SD (n-1) of rt_ms on remaining data; remove observations more than 3 SD from overall mean (outliers). 5. Split into placebo and caffeine groups by condition. 6. Compute n, mean, sample SD for each group. 7. Welch's t-test (two-sided, unequal variances) between caffeine and placebo rt_ms. 8. mean_diff = mean_caffeine - mean_placebo. 9. Cohen's d = mean_diff / pooled SD (pooled using n-1 weighting across both groups). 10. Output all claims as JSON.
