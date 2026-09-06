# Run summary for ho_008_ols

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 212,
  "coef_exposure": -56.365688738124845,
  "se_exposure": 13.610313189370553,
  "p_exposure": 5.0264957099630194e-05,
  "coef_age": -3.6167552688389213,
  "r_squared": 0.3570553934723337,
  "adj_r_squared": 0.34463134310464927
}

## Plan
1. Load data.csv. 2. Apply exclusions in order: keep age between 18 and 80 inclusive; drop rows with missing rt_ms or bmi (complete-case). 3. Code exposure: condition==caffeine -> 1, placebo -> 0. 4. Fit OLS: rt_ms ~ exposure + age + bmi + baseline, using conventional (non-robust) SE. 5. Extract n_model (nobs), coef_exposure, se_exposure, p_exposure for exposure var, coef_age, r_squared, adj_r_squared. 6. Print JSON with all claims.
