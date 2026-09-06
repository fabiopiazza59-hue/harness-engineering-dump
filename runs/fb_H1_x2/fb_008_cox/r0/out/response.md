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
1. Load data.csv. 2. Drop exact duplicate rows (all columns identical), keep first. 3. Replace -999 with NaN in all numeric columns. 4. Normalize treatment: strip whitespace, lowercase. 5. Filter age between 18 and 80 inclusive. 6. Compute follow-up days = last_contact_date - enrol_date. 7. Exclude records with zero follow-up. 8. Administrative censoring at 730 days: if followup>730, set followup=730 and event=0. 9. Drop rows with missing age, event, followup, treatment needed for Cox model (complete case). 10. Code exposure: fertilised=1, unfertilised=0 based on normalized treatment. 11. Fit Cox PH model (lifelines CoxPHFitter, breslow ties method) with covariates exposure and age, duration=followup, event=event. 12. Extract n_model (n used in model), n_events (sum event==1), median_followup_days (median of followup column analysed), hr_exposure=exp(coef), CI via exp(coef +/- 1.96*se), p-value from model, hr_age=exp(coef_age). 13. Print JSON with all claims.
