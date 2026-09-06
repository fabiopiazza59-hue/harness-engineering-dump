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
1. Load data.csv (225 records expected).
2. Remove exact duplicate rows (identical on every column), keep first occurrence.
3. Replace -999 sentinel values with NaN across all columns.
4. Filter age to [18,80] inclusive (drop missing age or out of range).
5. Normalize condition: strip whitespace, lowercase.
6. Compute follow-up days = last_contact_date - enrol_date (in days).
7. Censor follow-up at 730 days: if followup>730, set to 730 and event=0.
8. Exclude records with followup==0.
9. Build exposure variable: 1 if condition=='caffeine', 0 if condition=='placebo' (drop other/missing labels).
10. Fit Cox PH model (lifelines CoxPHFitter, breslow ties) with covariates exposure and age, outcome (followup, event).
11. Extract n_model (n used in fit), n_events (sum event after censoring), median_followup_days (median of followup among analysed sample), hr_exposure = exp(coef), 95% CI via exp(coef +/- 1.96*se), p-value (Wald), hr_age = exp(coef_age).
12. Print JSON with all claim slots.
13. Save as analysis.py, run, verify counts, submit.
