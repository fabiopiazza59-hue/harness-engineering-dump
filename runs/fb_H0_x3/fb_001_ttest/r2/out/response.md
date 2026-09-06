# Run summary for fb_001_ttest

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_usual": 108,
  "n_mediterranean": 108,
  "mean_usual": 105.03240740740742,
  "mean_mediterranean": 100.92129629629629,
  "sd_mediterranean": 10.722489693154255,
  "mean_diff": -4.1111111111111285,
  "t_stat": -2.660960768781127,
  "p_value": 0.00838948917866922,
  "cohens_d": -0.36211089494876725
}

## Plan
1. Load data.csv. 2. Exclude participants with age <18 or >80. 3. Exclude participants with missing glucose_fu (complete-case). 4. Compute overall mean and sample SD (n-1) of glucose_fu on remaining data; remove observations >3 SD from overall mean (outliers). 5. Split into usual and mediterranean groups by diet column. 6. Compute n, mean, sample SD (n-1) for each group. 7. Compute mean_diff = mean(mediterranean) - mean(usual). 8. Run Welch's t-test (unequal variances), two-sided, scipy.stats.ttest_ind(equal_var=False). 9. Compute pooled SD = sqrt(((n1-1)*sd1^2+(n2-1)*sd2^2)/(n1+n2-2)) and Cohen's d = mean_diff/pooled_sd. 10. Output all claim values as JSON.
