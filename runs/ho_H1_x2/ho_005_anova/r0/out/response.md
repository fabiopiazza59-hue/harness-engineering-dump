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
1. Load data.csv. 2. Exclude participants with age <18 or >80. 3. Exclude participants with missing glucose_fu. 4. Compute overall mean and sample SD (n-1) of glucose_fu on remaining sample; remove outliers >3 SD from mean (using abs(x-mean)>3*sd). 5. On this final analysis sample, compute tertile cut-points of baseline (33rd and 66th percentiles) - need to decide method (likely np.percentile with linear interpolation, using first and second tertile cut-points). 6. Assign group: low if baseline <= 1st tertile cutpoint, middle if > 1st and <= 2nd tertile cutpoint, high if > 2nd tertile cutpoint (values equal to cutpoint assigned to lower group). 7. Compute n and mean glucose_fu per group. 8. Run one-way ANOVA (scipy.stats.f_oneway) across three groups on glucose_fu. 9. Compute eta_squared = SS_between/SS_total. 10. Output all claims as JSON.
