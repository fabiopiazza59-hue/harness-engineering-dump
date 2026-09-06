# Run summary for dev_002_ttest

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_usual": 151,
  "n_mediterranean": 161,
  "mean_usual": 102.70132450331126,
  "mean_mediterranean": 98.29689440993788,
  "sd_mediterranean": 13.055125537314112,
  "mean_diff": -4.404430093373378,
  "t_stat": -2.9669917233423937,
  "p_value": 0.003241289877945753,
  "cohens_d": -0.3361183478602517
}

## Plan
1. Load data.csv. 2. Exclude participants with age <18 or >80. 3. Exclude missing glucose_fu. 4. Compute overall mean/SD of glucose_fu on remaining sample; remove outliers >3 SD from mean. 5. Split by diet group (usual vs mediterranean). 6. Compute n, mean, sample SD (ddof=1) for each group. 7. Compute mean_diff = mean_mediterranean - mean_usual. 8. Run Student's t-test (equal variances assumed), two-sided, get t_stat and p_value. 9. Compute pooled SD = sqrt(((n1-1)*sd1^2+(n2-1)*sd2^2)/(n1+n2-2)), Cohen's d = mean_diff/pooled_sd. 10. Print all claims as JSON.
