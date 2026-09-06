# Run summary for fb_014_cox

Status: success
Reason: verification gate passed
Steps: 6; scripts: 3; gate attempts: 1; compactions: 0

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
1. Load data.csv (225 records). 2. Remove exact duplicate rows (identical on all columns), keep first occurrence. 3. Replace -999 with NaN across all columns. 4. Restrict to age between 18 and 80 inclusive. 5. Normalize condition: strip whitespace, lowercase. 6. Compute followup_days = last_contact_date - enrol_date. 7. Exclude records with followup_days == 0. 8. Administrative censoring at 730 days: if followup_days > 730, set followup_days=730 and event=0 (censored). 9. Recode condition to exposure: caffeine=1, placebo=0 (drop other/missing labels). 10. Fit Cox PH model (lifelines CoxPHFataset, breslow ties) with covariates exposure and age, outcome (followup_days, event). 11. Extract n_model (# rows in model / with complete covariates), n_events (sum of event after censoring), median_followup_days (median of followup_days in analysed sample), hr_exposure = exp(coef), CI via se*1.96, p-value for exposure, hr_age = exp(coef_age). 12. Print all as JSON.
