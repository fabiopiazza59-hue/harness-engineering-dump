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
  "p_exposure": 0.001053498680615439,
  "hr_age": 1.0212162835402492
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (all columns identical), keep first occurrence. 3. Replace -999 sentinel values with NaN across all columns. 4. Filter to age between 18 and 80 inclusive (drop missing age too since range check fails on NaN). 5. Normalize program: strip whitespace, lowercase; map to exposure: 1='coaching', 0='waitlist' (drop other/unknown labels if any). 6. Compute follow-up days = last_contact_date - enrol_date. 7. Exclude records with zero follow-up. 8. Administrative censoring at 730 days: if followup>730, set followup=730 and event=0 (censored); else keep event as is. 9. Drop rows with missing age, program, event, followup, or other needed covariates (complete case). 10. Fit Cox PH model (lifelines CoxPHFitter) with covariates exposure (program) and age, Breslow ties method. 11. Extract n_model (# rows used), n_events (sum event after censoring), median follow-up (median of followup column), hr_exposure = exp(coef), 95% CI via lifelines summary (Wald, z=1.96), p-value for exposure, hr_age = exp(coef age). 12. Print JSON with all claims.
