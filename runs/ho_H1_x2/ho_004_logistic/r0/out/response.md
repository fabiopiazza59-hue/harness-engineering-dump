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
1. Load data.csv. 2. Apply exclusion: keep only age between 18 and 80 inclusive. 3. Drop rows with missing biomass or bmi (complete-case). 4. Code treatment as nitrogen exposure: 1=fertilised, 0=unfertilised. 5. Fit logistic regression: event ~ exposure + age + bmi, using statsmodels Logit (MLE, no penalisation). 6. Compute n_model = number of rows used in model; n_events = sum of event among those rows. 7. Compute OR = exp(coef) for exposure and age, Wald 95% CI = exp(coef +/- 1.96*se) (use statsmodels conf_int default alpha=0.05), p-value from model's summary (Wald test). 8. Print JSON with all claim slots as last line of stdout.
