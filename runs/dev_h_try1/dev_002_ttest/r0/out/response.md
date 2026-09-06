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
1. Load data.csv. 2. Exclude age<18 or age>80. 3. Exclude missing glucose_fu. 4. Compute overall mean/SD of glucose_fu on remaining sample; remove rows where |glucose_fu-mean|>3*SD. 5. Split by diet into usual/mediterranean. 6. Compute n, mean, sample SD (ddof=1) for each group. 7. Mean diff = mediterranean - usual. 8. Run unpaired Student t-test (equal variances) two-sided via scipy.stats.ttest_ind. 9. Cohen's d = mean_diff / pooled_SD where pooled_SD = sqrt(((n1-1)*sd1^2+(n2-1)*sd2^2)/(n1+n2-2)). 10. Print JSON with all claim values.
