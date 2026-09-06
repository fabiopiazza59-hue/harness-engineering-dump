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
  "p_exposure": 0.0004795310868910274,
  "hr_age": 1.0185766648834829
}

## Plan
1. Load data.csv (424 records). 2. Remove exact duplicate rows (identical on all columns), keep first occurrence. 3. Replace -999 with NaN across all columns (sentinel missing). 4. Filter age to 18-80 inclusive (drop missing/out-of-range age). 5. Normalize program: strip whitespace, lowercase; map to 1=tutoring,0=standard (drop unrecognized labels if any). 6. Compute follow-up days = last_contact_date - enrol_date. 7. Exclude records with zero follow-up. 8. Administrative censoring at 730 days: if followup>730, set followup=730 and event=0 (censored); else keep original event status. 9. Fit Cox PH model (lifelines CoxPHFitter, Breslow ties) with covariates program(exposure) and age, duration=followup_days, event_col=event. 10. Extract n_model (# students in model), n_events (# events after censoring), median_followup_days (median of followup after censoring, all analysed records), hr_exposure = exp(coef_program), 95% CI via Wald (coef +/- 1.96*se), p-value for exposure, hr_age = exp(coef_age). 11. Print JSON with all claim ids.
