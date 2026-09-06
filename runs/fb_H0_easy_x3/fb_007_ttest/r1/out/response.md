# Run summary for fb_007_ttest

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_placebo": 102,
  "n_caffeine": 91,
  "mean_placebo": 723.5480392156862,
  "mean_caffeine": 700.5274725274725,
  "sd_caffeine": 88.174864226256,
  "mean_diff": -23.020566688213762,
  "t_stat": -1.8756869708520303,
  "p_value": 0.062280512718236994,
  "cohens_d": -0.2716809645898705
}

## Plan
1. Load data.csv (226 rows expected). 2. Exclude participants with age <18 or >80. 3. Exclude participants with missing rt_ms. 4. Compute overall mean and sample SD of rt_ms on remaining data; remove observations with |rt_ms - mean| > 3*SD (outliers). 5. Split into placebo and caffeine groups by condition. 6. Compute n, mean, sample SD (n-1) for each group. 7. Compute mean_diff = mean_caffeine - mean_placebo. 8. Run Welch's t-test (unequal variances), two-sided, on rt_ms between caffeine and placebo. 9. Compute Cohen's d = mean_diff / pooled_SD, where pooled SD = sqrt(((n1-1)*sd1^2+(n2-1)*sd2^2)/(n1+n2-2)). 10. Output all claim values as JSON.
