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
1. Load data.csv. 2. Exclude participants with age <18 or >80. 3. Exclude participants with missing rt_ms. 4. Compute overall mean and SD of rt_ms on remaining sample; remove observations where rt_ms is more than 3 SD from overall mean. 5. Split by condition (placebo vs caffeine). 6. Compute n, mean, sample SD (ddof=1) for each group. 7. Compute mean_diff = mean_caffeine - mean_placebo. 8. Welch t-test (scipy.stats.ttest_ind, equal_var=False), two-sided, report t_stat and p_value. 9. Compute pooled SD = sqrt(((n1-1)*sd1^2+(n2-1)*sd2^2)/(n1+n2-2)), cohens_d = mean_diff/pooled_sd. 10. Print JSON with all claim slots.
