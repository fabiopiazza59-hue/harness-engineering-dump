# Run summary for fb_005_anova

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_low": 62,
  "mean_low": 629.7161290322582,
  "n_middle": 62,
  "mean_middle": 698.2838709677418,
  "n_high": 62,
  "mean_high": 752.6741935483872,
  "f_stat": 42.334380123965964,
  "p_value": 7.746157286596403e-16,
  "eta_squared": 0.3163191706402577
}

## Plan
1. Load data.csv. 2. Exclude age<18 or age>80. 3. Exclude missing rt_ms. 4. Compute overall mean and sample SD (n-1) of rt_ms on remaining data; remove outliers >3 SD from mean. 5. On this analysis sample, compute tertile cutpoints (33.3%,66.7%) of baseline using quantile method; assign low/middle/high groups with values equal to a cutpoint going to lower group. 6. Compute n and mean rt_ms per group. 7. One-way ANOVA across 3 groups on rt_ms; get F, p. 8. eta_squared = SS_between/SS_total. 9. Output JSON.
