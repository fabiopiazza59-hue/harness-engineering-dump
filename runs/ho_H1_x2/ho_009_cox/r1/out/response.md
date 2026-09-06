# Run summary for ho_009_cox

Status: success
Reason: verification gate passed
Steps: 5; scripts: 2; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 405,
  "n_events": 242,
  "median_followup_days": 282.0,
  "hr_exposure": 1.5779029477063051,
  "hr_ci_low": 1.221516116754938,
  "hr_ci_high": 2.0382684094210353,
  "p_exposure": 0.0004795310868910543,
  "hr_age": 1.0185766648834829
}

## Plan
1. Load data.csv (424 records expected). 2. Remove exact duplicate rows (identical on every column), keep first occurrence. 3. Replace -999 sentinel values with NaN across all columns. 4. Filter to age between 18 and 80 inclusive. 5. Normalize program: strip whitespace, lowercase; map to exposure variable tutoring=1, standard=0. 6. Compute follow-up days = last_contact_date - enrol_date. 7. Exclude records with zero follow-up. 8. Administratively censor at 730 days: if follow-up>730, set to 730 and event=0 (censored); else keep original event status. 9. Fit Cox PH model (lifelines CoxPHFitter, breslow ties) with covariates: exposure (program tutoring=1/0) and age. Drop rows with missing values in model variables (age, program, event, duration). 10. Report n_model = number of students in model, n_events = sum of event indicator after censoring, median_followup_days = median duration, hr_exposure = exp(coef) for exposure, CI via 1.96*SE Wald, p-value for exposure, hr_age = exp(coef) for age. 11. Print all claims as JSON.
