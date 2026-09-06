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
1. Load data.csv. 2. Remove exact duplicate rows (identical on every column), keep first occurrence. 3. Replace -999 with NaN across columns. 4. Filter age to [18,80] inclusive (drop missing age too). 5. Normalize treatment: strip whitespace, lowercase; map to exposure 1=fertilised,0=unfertilised. 6. Compute follow-up days = last_contact_date - enrol_date. 7. Exclude records with zero follow-up. 8. Administrative censoring at 730 days: if followup>730, set followup=730 and event=0; else keep event as is. 9. Drop rows with missing values needed for model (age, event, followup, treatment). 10. Fit Cox PH model (lifelines CoxPHFitter, breslow ties) with covariates: exposure (fertilised 0/1) and age. 11. Extract n (rows used), n_events (sum event after censoring), median follow-up (median of followup days across analysed sample), HR for exposure with 95% CI (Wald, z=1.96) and p-value, HR per year age. 12. Print JSON with all claim ids as last line of stdout.
