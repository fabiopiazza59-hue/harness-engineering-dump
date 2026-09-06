# Run summary for dev_001_logistic

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 322,
  "n_events": 112,
  "or_exposure": 0.4436901330231654,
  "or_ci_low": 0.2688040028052041,
  "or_ci_high": 0.7323586408226764,
  "p_exposure": 0.0014820504660406628,
  "or_age": 1.0344346251043577
}

## Plan
1. Load data.csv. 2. Apply exclusions in order: (a) keep only age between 18 and 80 inclusive; (b) drop rows with missing sbp_12w or bmi (complete-case). 3. Code arm as 1=treatment,0=control. 4. Fit logistic regression: event ~ arm + age + bmi, using statsmodels Logit (ML, no penalization). 5. Compute n_model = number of rows in model; n_events = sum of event among those rows. 6. Compute OR for arm = exp(coef), Wald 95% CI = exp(coef +/- 1.96*se) (use statsmodels conf_int default z-based), p-value from Wald test. 7. Compute OR per year age = exp(coef_age). 8. Output JSON with all claims.
