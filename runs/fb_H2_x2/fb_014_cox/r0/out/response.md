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
  "p_exposure": 0.0005974441906388961,
  "hr_age": 1.034470674978907
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (identical on all columns), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive (drop missing age). 5. Normalise condition: strip whitespace, lowercase. 6. Compute follow-up days = last_contact_date - enrol_date. 7. Censor at 730 days: if followup>730, set to 730 and event=0. 8. Exclude records with followup==0. 9. Build exposure variable: 1 if condition=='caffeine', 0 if condition=='placebo' (drop other/missing labels). 10. Drop missing age/event/followup rows for Cox model. 11. Fit Cox PH model (lifelines CoxPHFitter, breslow ties) with exposure and age as covariates. 12. Extract HR (exp(coef)), 95% CI via z=1.96, p-value for exposure; HR for age. 13. Compute n_model = number of rows in model, n_events = sum(event), median_followup_days = median of followup time after censoring. Print all as JSON.
