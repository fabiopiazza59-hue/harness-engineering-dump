# Run summary for ho_009_cox

Status: success
Reason: verification gate passed
Steps: 6; scripts: 3; gate attempts: 1; compactions: 0

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
1. Load data.csv. 2. Drop exact duplicate rows (all columns identical), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age to [18,80] inclusive (drop missing/out-of-range age). 5. Normalize program: strip whitespace, lowercase; map to exposure 1=tutoring,0=standard. 6. Compute followup_days = last_contact_date - enrol_date (in days). 7. Exclude records with followup_days==0. 8. Administrative censoring at 730 days: if followup_days>730, set followup_days=730 and event=0 (censored); else keep event as is. 9. Fit Cox PH model (lifelines CoxPHFitter, breslow ties) with covariates exposure (program) and age, duration=followup_days, event=event_after_censoring. 10. Extract n_model (n used in model), n_events (sum of event column after censoring), median_followup_days (median of followup_days after censoring, all analysed records), hr_exposure = exp(coef), CI via se*1.96, p-value from model summary, hr_age = exp(coef_age). 11. Print JSON with all claims.
