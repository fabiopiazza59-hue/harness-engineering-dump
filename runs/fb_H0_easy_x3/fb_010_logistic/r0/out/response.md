# Run summary for fb_010_logistic

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 207,
  "n_events": 115,
  "or_exposure": 1.8396254487841754,
  "or_ci_low": 1.0408764113641809,
  "or_ci_high": 3.2513195177312078,
  "p_exposure": 0.035918984633736606,
  "or_age": 1.007347508204559
}

## Plan
1. Load data.csv. 2. Apply age filter: keep 18<=age<=80. 3. Drop rows with missing savings or bmi (complete-case). 4. Recode program to binary: coaching=1, none=0. 5. Fit logistic regression: event ~ program + age + bmi using statsmodels Logit (MLE, no penalty). 6. Extract n_model (nobs), n_events (sum of event==1 in model sample). 7. Compute OR for program = exp(coef), Wald 95% CI = exp(coef +/- 1.96*se), p-value from Wald test (statsmodels default). 8. Compute OR for age = exp(coef_age). 9. Print all as JSON.
