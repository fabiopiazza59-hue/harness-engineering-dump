# Run summary for fb_008_cox

Status: success
Reason: verification gate passed
Steps: 5; scripts: 2; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 404,
  "n_events": 250,
  "median_followup_days": 285.0,
  "hr_exposure": 1.4768294487428384,
  "hr_ci_low": 1.150940590527385,
  "hr_ci_high": 1.8949937456586565,
  "p_exposure": 0.002175548899268953,
  "hr_age": 1.006049424889128
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (identical on all columns), keep first occurrence. 3. Replace -999 with NaN across all columns. 4. Filter to age between 18 and 80 inclusive (drop missing age). 5. Normalize treatment: strip whitespace, lowercase; map to exposure 1=fertilised,0=unfertilised (drop unrecognized/missing). 6. Compute follow-up days = last_contact_date - enrol_date. 7. Exclude records with zero follow-up. 8. Administrative censoring at 730 days: if follow-up>730, set to 730 and event=0; else keep event as is (event must be 0/1, missing event treated as missing->exclude?). 9. Fit Cox PH model (lifelines CoxPHFactor with Breslow ties) with covariates: exposure (0/1) and age. 10. Extract n (rows in model), n_events (sum event after censoring), median follow-up (median of the censored duration column), HR exposure = exp(coef), 95% CI via 1.96*se, p-value, HR age = exp(coef_age). 11. Print JSON with all claim slots.
