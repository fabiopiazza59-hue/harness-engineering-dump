# Run summary for ho_004_logistic

Status: success
Reason: verification gate passed
Steps: 5; scripts: 1; gate attempts: 1; compactions: 0

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
1. Load data.csv. 2. Apply exclusion: age between 18 and 80 inclusive. 3. Apply exclusion: drop rows with missing biomass or bmi. 4. Recode treatment to exposure=1 if fertilised else 0. 5. Fit logistic regression: event ~ exposure + age + bmi, using statsmodels Logit (ML, no penalization). 6. Compute n_model = number of rows used in model, n_events = sum of event among those rows. 7. Compute OR = exp(coef) for exposure and age, Wald 95% CI = exp(coef +- 1.96*SE) using statsmodels conf_int (which uses the correct alpha=0.05 t/z based CI), p-value from model summary. 8. Print JSON with all claim slots.
