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
1. Load data.csv. 2. Drop exact duplicate rows (identical on every column), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive (drop missing age or out of range). 5. Normalise program: strip whitespace, lowercase; map 'coaching'->1, 'waitlist'->0. 6. Compute follow-up days = last_contact_date - enrol_date. 7. Censor at 730 days: if followup>730, set followup=730 and event=0; exclude records with followup==0. 8. Drop rows missing age, program, event, followup. 9. Fit Cox PH model (lifelines CoxPHFitter, breslow ties) with covariates program(exposure) and age. 10. Extract n_model, n_events, median followup, HR exposure + CI + p, HR age. Print JSON.
