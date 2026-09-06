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
1. Load data.csv (204 rows expected).
2. Exclude participants with age <18 or >80.
3. Exclude participants with missing rt_ms.
4. Compute overall mean and sample SD (n-1) of rt_ms on remaining sample; remove rows where rt_ms is more than 3 SD from that mean (outlier removal based on overall sample stats, applied after prior exclusions).
5. Split into placebo and caffeine groups by condition.
6. Compute n, mean, sd (n-1) for each group.
7. Compute mean_diff = mean_caffeine - mean_placebo.
8. Run Welch's t-test (unequal variances), two-sided, on rt_ms between caffeine and placebo groups -> t_stat, p_value.
9. Compute pooled SD = sqrt(((n1-1)*sd1^2+(n2-1)*sd2^2)/(n1+n2-2)), cohens_d = mean_diff/pooled_sd.
10. Print all claims as JSON.
