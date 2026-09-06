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
1. Load data.csv. 2. Drop exact duplicate rows (identical on all columns), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age between 18-80 inclusive (drop missing age too). 5. Normalize program: strip whitespace, lowercase; map coaching=1, waitlist=0. 6. Compute followup_days = last_contact_date - enrol_date. 7. Exclude records with followup_days==0. 8. Censor followup_days>730 at 730, set event=0 for those. 9. Drop missing event/age/program rows (complete case). 10. Fit Cox PH model (lifelines CoxPHFitter with Breslow ties) with covariates program, age; event column, duration column. 11. Extract n_model (n used), n_events (sum of event after censoring), median_followup_days, hr_exposure=exp(coef program), CI via exp(coef +-1.96*se), p-value, hr_age=exp(coef age). Print JSON.
