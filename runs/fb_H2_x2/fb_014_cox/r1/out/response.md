# Run summary for fb_014_cox

Status: success
Reason: verification gate passed
Steps: 5; scripts: 2; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 207,
  "n_events": 88,
  "median_followup_days": 484.0,
  "hr_exposure": 0.46931717029210945,
  "hr_ci_low": 0.304708508588407,
  "hr_ci_high": 0.7228501998561286,
  "p_exposure": 0.0005974441906388748,
  "hr_age": 1.034470674978907
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (all columns identical), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive (drop missing age too). 5. Normalize condition: strip whitespace, lowercase. 6. Compute followup_days = last_contact_date - enrol_date. 7. Exclude records with followup_days == 0. 8. Cap followup_days at 730, set event=0 for those censored at cap. 9. Build exposure variable: 1 if condition=='caffeine', 0 if 'placebo' (drop others/missing). 10. Fit CoxPH model (lifelines, Breslow ties) with covariates exposure and age. 11. Extract n_model, n_events, median followup, HR exposure with 95% CI (Wald), p-value, HR age. 12. Print JSON of all claims.
