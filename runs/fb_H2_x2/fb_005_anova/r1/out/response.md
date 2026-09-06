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
  "eta_squared": 0.3163191706402576
}

## Plan
1. Load data.csv. 2. Exclude age not in [18,80]. 3. Exclude missing rt_ms. 4. Compute overall mean/sd of rt_ms on remaining sample; remove outliers >3 SD from mean (sample SD, ddof=1). 5. Compute tertile cutpoints (33.3%,66.7%) of baseline on analysis sample; assign low (<=cut1), middle (>cut1 & <=cut2), high (>cut2). 6. Compute n and mean rt_ms per group. 7. One-way ANOVA (scipy f_oneway) across groups; get F, p. 8. eta_squared = SS_between/SS_total. 9. Output JSON with all claims.
