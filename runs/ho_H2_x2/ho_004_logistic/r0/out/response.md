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
1. Load data.csv. 2. Apply exclusions in order: (a) keep only plots with age between 18 and 80 inclusive; (b) drop rows with missing biomass or bmi. 3. Recode treatment into binary exposure (1=fertilised,0=unfertilised). 4. Fit logistic regression: event ~ exposure + age + bmi using statsmodels Logit (ML, no penalization). 5. Extract n_model (nobs), n_events (sum of event==1 in modelled data). 6. Compute OR = exp(coef) for exposure and age, Wald 95% CI = exp(coef +/- 1.96*se) using statsmodels conf_int (which uses z-based Wald CI by default). 7. p-value for exposure from model summary (two-sided Wald test). 8. Print JSON with all claims. Save as analysis.py, run, verify sane values, then submit.
