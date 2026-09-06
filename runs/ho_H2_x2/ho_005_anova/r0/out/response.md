# Run summary for ho_005_anova

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_low": 75,
  "mean_low": 97.10666666666667,
  "n_middle": 76,
  "mean_middle": 99.62236842105264,
  "n_high": 73,
  "mean_high": 108.95205479452055,
  "f_stat": 18.838074156760843,
  "p_value": 2.7910371969175134e-08,
  "eta_squared": 0.14564987363217294
}

## Plan
1. Load data.csv. 2. Exclude participants with age <18 or >80. 3. Exclude participants with missing glucose_fu. 4. Compute overall mean and sample SD (n-1) of glucose_fu on remaining sample; remove observations with |glucose_fu - mean| > 3*SD (outliers). 5. On this analysis sample, compute tertile cutpoints (33rd and 66th percentile) of baseline value; assign group: low if baseline <= cut1, middle if cut1 < baseline <= cut2, high if baseline > cut2. 6. Compute n and mean glucose_fu per group. 7. Run one-way ANOVA (scipy.stats.f_oneway) on glucose_fu across 3 groups; get F, p. 8. Compute eta_squared = SS_between/SS_total. 9. Output JSON with all claims.
