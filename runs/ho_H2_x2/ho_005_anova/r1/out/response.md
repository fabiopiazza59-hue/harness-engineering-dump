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
1. Load data.csv. 2. Exclude participants with age <18 or >80. 3. Exclude participants with missing glucose_fu. 4. Compute overall mean and sample SD (n-1) of glucose_fu on remaining sample; remove observations >3 SD from mean (outliers). 5. On this final analysis sample, compute tertile cut-points of baseline (33.3% and 66.7% percentiles) using the analysis sample. 6. Assign group: low if baseline <= 1st tercile cutpoint, middle if baseline <= 2nd tercile cutpoint (and > 1st), high if baseline > 2nd tercile cutpoint. 7. Compute n and mean glucose_fu per group. 8. One-way ANOVA (scipy.stats.f_oneway) across three groups on glucose_fu. 9. Compute eta squared = SS_between/SS_total. 10. Output all claims as JSON.
