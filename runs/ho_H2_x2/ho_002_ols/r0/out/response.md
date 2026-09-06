# Run summary for ho_002_ols

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 244,
  "coef_exposure": -0.09314589487782465,
  "se_exposure": 0.013871194024011099,
  "p_exposure": 1.3585645644354348e-10,
  "coef_age": -0.007154834352790379,
  "r_squared": 0.38967408543198656,
  "adj_r_squared": 0.3794594257739444
}

## Plan
1. Load data.csv. 2. Exclude participants with age outside [18,80]. 3. Exclude rows with missing rt_ms or bmi. 4. Compute mean and sample SD (ddof=1) of rt_ms on remaining data; remove observations with |rt_ms - mean| > 3*SD. 5. Set rt_ms values <1 to 1, then log-transform (natural log) to get log_rt. 6. Code condition: caffeine=1, placebo=0. 7. Standardize continuous covariates age, bmi, baseline (mean 0, sample SD 1) using the analysis sample. 8. Fit OLS: log_rt ~ exposure + age_std + bmi_std + baseline_std, with intercept, non-robust (standard) SE. 9. Extract n_model, coef_exposure, se_exposure, p_exposure, coef_age, r_squared, adj_r_squared. 10. Print JSON with all claims as last line of stdout.
