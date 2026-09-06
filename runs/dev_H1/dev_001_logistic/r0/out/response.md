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
1. Load data.csv. 2. Apply exclusions in order: (a) age between 18 and 80 inclusive, (b) drop rows with missing sbp_12w or bmi. 3. Recode arm as 1=treatment,0=control (binary exposure). 4. Fit logistic regression: event ~ arm + age + bmi via statsmodels Logit (no penalization, MLE). 5. Compute n_model (n obs used), n_events (sum of event==1 in model sample). 6. Extract OR for arm = exp(coef), Wald 95% CI = exp(coef +/- 1.96*se) (statsmodels default uses normal z), p-value for arm term. 7. OR per year age = exp(coef_age). 8. Print JSON with all claims.
