# Run summary for fb_004_logistic

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 161,
  "n_events": 59,
  "or_exposure": 0.3461142250757604,
  "or_ci_low": 0.16402077528609071,
  "or_ci_high": 0.7303651417989179,
  "p_exposure": 0.005358860802361403,
  "or_age": 1.022823128772859
}

## Plan
1. Load data.csv. 2. Apply age filter: keep 18<=age<=80. 3. Drop rows with missing glucose_fu or bmi. 4. Code diet: mediterranean=1, usual=0. 5. Fit logistic regression event ~ diet + age + bmi using statsmodels Logit (ML, no penalty). 6. Compute n_model = n obs used, n_events = sum(event). 7. Compute OR = exp(coef) for diet and age, Wald 95% CI = exp(coef +/- 1.96*se) using statsmodels conf_int, p-value from model summary. 8. Print JSON with all claims.
