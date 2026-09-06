# Run summary for fb_004_logistic

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 161,
  "n_events": 59,
  "or_exposure": 0.34611422507808903,
  "or_ci_low": 0.16402088710743384,
  "or_ci_high": 0.7303646438818502,
  "p_exposure": 0.005358818793801879,
  "or_age": 1.0228231287726104
}

## Plan
1. Load data.csv. 2. Apply exclusions in order: (a) keep age between 18 and 80 inclusive; (b) drop rows with missing glucose_fu or bmi. 3. Recode diet: mediterranean=1, usual=0. 4. Fit logistic regression: event ~ diet + age + bmi using statsmodels GLM binomial (MLE, no penalization). 5. n_model = number of rows in model; n_events = sum of event==1 among those rows. 6. Compute OR = exp(coef) for diet and age; Wald 95% CI = exp(coef +/- 1.96*se) (use statsmodels conf_int default alpha=0.05). 7. p_exposure = p-value for diet coefficient. 8. Print all claims as JSON.
