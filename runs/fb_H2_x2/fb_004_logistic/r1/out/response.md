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
1. Load data.csv. 2. Apply exclusions in order: (a) age between 18 and 80 inclusive; (b) drop rows missing glucose_fu or bmi. 3. Code diet as 1=mediterranean,0=usual. 4. Fit logistic regression event ~ diet + age + bmi via statsmodels Logit (ML, no penalization). 5. n_model = model n obs; n_events = sum(event) among modelled. 6. or_exposure = exp(coef_diet); CI = exp(coef +/- 1.96*se) Wald; p_exposure = model p-value for diet. 7. or_age = exp(coef_age). 8. Print JSON with all claims.
