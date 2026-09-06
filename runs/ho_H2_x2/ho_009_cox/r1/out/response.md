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
1. Load data.csv (424 rows expected). 2. Remove exact duplicate rows (identical on every column), keep first occurrence. 3. Replace -999 with NaN across all columns (sentinel missing). 4. Filter to age between 18 and 80 inclusive (drop missing age too). 5. Normalize program: strip whitespace, lowercase; map to 1=tutoring,0=standard (drop unrecognized/missing). 6. Compute followup_days = last_contact_date - enrol_date (parse dates). 7. Exclude records with followup_days == 0. 8. Censor followup at 730 days: if followup>730, set to 730 and event=0 (censored). 9. Drop rows with missing age, event, program, followup after cleaning (complete case for model variables). 10. Fit Cox PH model (lifelines CoxPHFitter, breslow ties) with covariates program(exposure) and age; duration=followup_days, event=event. 11. Extract n_model (n used in model), n_events (sum of event after censoring), median_followup_days (median of followup after censoring, all analysed records), hr_exposure=exp(coef), 95% CI via se (Wald, z=1.96), p-value for exposure, hr_age=exp(coef_age). 12. Print JSON with all claims as last line of stdout.
