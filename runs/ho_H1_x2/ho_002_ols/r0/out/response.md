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
1. Load data.csv. 2. Exclude participants with age <18 or >80. 3. Exclude rows with missing rt_ms or bmi (complete-case on these two vars). 4. Clip rt_ms values below 1 to 1, then compute outlier removal: compute mean and sample SD of rt_ms (after clipping) over remaining data, remove rows where rt_ms is more than 3 SD from mean. 5. Log-transform rt_ms (natural log) to get outcome. 6. Code condition as exposure: 1=caffeine,0=placebo. 7. Standardize continuous covariates age, bmi, baseline (mean0, sd1 sample SD) before entering model. 8. Fit OLS: log_rt ~ exposure + age_std + bmi_std + baseline_std, with intercept. Use conventional (non-robust) SE. 9. Extract n_model, coef_exposure, se_exposure, p_exposure, coef_age, r_squared, adj_r_squared. 10. Print JSON with all slots.
