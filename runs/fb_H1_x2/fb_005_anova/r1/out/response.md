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
1. Load data.csv. 2. Exclude participants with age <18 or >80. 3. Exclude rows with missing rt_ms. 4. Compute overall mean and sample SD (n-1) of rt_ms on remaining data; remove rows where rt_ms is more than 3 SD from mean (outliers). 5. On resulting analysis sample, compute tertile cutpoints (1st and 2nd tertile, i.e. 33.33% and 66.67% quantiles) of baseline. 6. Assign group: low if baseline <= cut1, middle if cut1 < baseline <= cut2, high if baseline > cut2 (values equal to cutpoint go to lower group). 7. Compute n and mean rt_ms per group. 8. Run one-way ANOVA (scipy.stats.f_oneway) on rt_ms across 3 groups; get F and p. 9. Compute eta squared = SS_between/SS_total. 10. Print all as JSON.
