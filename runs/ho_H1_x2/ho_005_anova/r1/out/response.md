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
1. Load data.csv. 2. Exclude participants with age outside [18,80]. 3. Exclude participants with missing glucose_fu. 4. Compute overall mean and sample SD (n-1) of glucose_fu on remaining sample; remove outliers where |glucose_fu - mean| > 3*SD. 5. Compute tertile cutpoints (33.3%, 66.7%) of baseline on this final analysis sample; assign group: low if baseline <= q1, middle if q1 < baseline <= q2, high if baseline > q2. 6. Compute n and mean glucose_fu per group. 7. One-way ANOVA (scipy.stats.f_oneway) across three groups on glucose_fu. 8. Eta squared = SS_between/SS_total. 9. Output all as JSON.
