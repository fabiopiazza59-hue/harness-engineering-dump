# Run summary for ho_015_cox

Status: success
Reason: verification gate passed
Steps: 5; scripts: 2; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 286,
  "n_events": 174,
  "median_followup_days": 304.5,
  "hr_exposure": 1.6567505762898334,
  "hr_ci_low": 1.224816609428381,
  "hr_ci_high": 2.2410068992432235,
  "p_exposure": 0.0010534986806155417,
  "hr_age": 1.0212162835402492
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (identical on every column), keep first. 3. Replace -999 sentinel values with NaN across all columns. 4. Filter to age 18-80 inclusive. 5. Normalize program: trim whitespace, lowercase. Map to binary: coaching=1, waitlist=0. 6. Compute followup_days = last_contact_date - enrol_date (in days). 7. Exclude records with followup_days == 0. 8. Administrative censoring at 730 days: if followup_days>730, set followup_days=730 and event=0 (censored); else keep as is. 9. Drop rows with missing values needed for model (age, program, event, followup_days). 10. Fit Cox PH model (lifelines CoxPHFitter) with covariates program (exposure) and age, duration=followup_days, event=event, ties method='breslow'. 11. Extract n_model (number of rows used), n_events (sum of event after censoring), median_followup_days (median of followup_days), hr_exposure = exp(coef_program), CI from Wald test (z=1.96), p_exposure, hr_age = exp(coef_age). 12. Print JSON with all claim ids.
