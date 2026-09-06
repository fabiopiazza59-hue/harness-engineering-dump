# Run summary for fb_008_ols

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 322,
  "coef_exposure": 63.638147625621656,
  "se_exposure": 8.876205336801274,
  "p_exposure": 5.327989641369345e-12,
  "coef_age": -0.22162164667140907,
  "r_squared": 0.43914089103928156,
  "adj_r_squared": 0.43206380449088133
}

## Plan
1. Load data.csv. 2. Apply age filter 18-80 inclusive. 3. Drop rows with missing savings or bmi (complete-case). 4. Compute mean/sd of savings on remaining data; remove rows where |savings-mean|>3*sd (sample sd, n-1). 5. Code program as exposure: 1 if 'coaching', 0 if 'none'. 6. Fit OLS: savings ~ exposure + age + bmi + baseline, with intercept, non-robust SE. 7. Extract n_model, coef_exposure, se_exposure, p_exposure, coef_age, r_squared, adj_r_squared. 8. Print JSON.
