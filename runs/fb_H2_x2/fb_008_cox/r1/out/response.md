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
  "p_exposure": 0.0021755488992689642,
  "hr_age": 1.006049424889128
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (identical on every column), keep first occurrence. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive. 5. Normalize treatment: strip whitespace, lowercase. 6. Compute follow-up days = last_contact_date - enrol_date. 7. Exclude records with zero follow-up. 8. Administratively censor at 730 days: if followup>730, set followup=730 and event=0. 9. Drop rows with missing age, treatment, event, followup after exclusions (complete case for model variables). 10. Code exposure: 1=fertilised,0=unfertilised based on normalized treatment. 11. Fit Cox PH model (Breslow ties) with exposure and age as covariates using lifelines. 12. Extract n_model (n used in model), n_events (sum event after censoring), median_followup_days (median of followup in analysed sample), hr_exposure, hr_ci_low, hr_ci_high, p_exposure, hr_age. 13. Print JSON with these values.
