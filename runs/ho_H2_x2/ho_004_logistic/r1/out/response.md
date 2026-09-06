# Run summary for ho_004_logistic

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 293,
  "n_events": 153,
  "or_exposure": 2.255531090674604,
  "or_ci_low": 1.39111921642914,
  "or_ci_high": 3.6570701065136997,
  "p_exposure": 0.0009711871419276334,
  "or_age": 1.0192946657856494
}

## Plan
1. Load data.csv. 2. Apply exclusions in order: (a) age between 18 and 80 inclusive; (b) drop rows with missing biomass or bmi. 3. Code treatment as 1=fertilised,0=unfertilised. 4. Fit logistic regression: event ~ treatment + age + bmi, MLE (statsmodels Logit/GLM binomial), no penalization. 5. Compute n_model = number of rows in model, n_events = sum(event==1) among those rows. 6. Compute OR = exp(coef) for treatment and age, Wald 95% CI = exp(coef +/- 1.96*se), two-sided p-value from model. 7. Print all as JSON.
