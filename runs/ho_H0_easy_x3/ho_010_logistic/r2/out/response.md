# Run summary for ho_010_logistic

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 275,
  "n_events": 162,
  "or_exposure": 2.771350178647144,
  "or_ci_low": 1.6626466763890246,
  "or_ci_high": 4.619370983477976,
  "p_exposure": 9.218650401753427e-05,
  "or_age": 1.0272316527751124
}

## Plan
1. Load data.csv. 2. Apply exclusions in order: (a) keep only age between 18 and 80 inclusive; (b) drop rows with missing savings or bmi (complete-case). 3. Code program as 1=coaching, 0=none. 4. Fit logistic regression: event ~ program + age + bmi, using MLE (statsmodels Logit, no penalization). 5. Compute n_model = number of rows in model, n_events = sum of event==1 among those. 6. Extract OR for program = exp(coef), Wald 95% CI = exp(coef +/- 1.96*se) (or statsmodels default CI), p-value for program coef. 7. OR per year age = exp(coef_age). 8. Print all claims as JSON.
