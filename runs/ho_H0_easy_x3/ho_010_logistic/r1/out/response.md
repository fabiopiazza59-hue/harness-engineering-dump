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
1. Load data.csv. 2. Apply exclusions in order: (a) keep age between 18 and 80 inclusive; (b) drop rows with missing savings or bmi (complete-case). 3. Recode program: 1 for coaching, 0 for none (based on 'program' column values, likely 'coaching'/'none' strings). 4. Fit logistic regression: event ~ program + age + bmi using statsmodels Logit (ML, no penalization). 5. n_model = number of rows in model; n_events = sum of event==1 among those rows. 6. Extract OR for program = exp(coef), Wald CI = exp(coef +/- 1.96*se) (use statsmodels default conf_int which uses normal approx). 7. p_exposure = p-value for program coefficient from Wald test. 8. or_age = exp(coef_age). 9. Print all as JSON.
