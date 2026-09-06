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
1. Load data.csv (expect 303 records). 2. Remove exact duplicate rows (identical on every column), keep first occurrence. 3. Replace -999 with NaN across all columns. 4. Normalize `program` by trimming whitespace and lower-casing. 5. Filter to age between 18 and 80 inclusive (drop missing age or out-of-range). 6. Compute follow-up days = last_contact_date - enrol_date. 7. Exclude records with zero follow-up. 8. Administrative censoring at 730 days: if follow-up > 730, set to 730 and event=0 (censored); else keep original event and time. 9. Drop rows with missing values needed for model (age, program, event, followup). 10. Code exposure: program=='coaching' -> 1, 'waitlist' -> 0 (drop other/missing labels). 11. Fit Cox PH model (lifelines CoxPHFitter, breslow ties) with covariates exposure (coaching) and age, duration=followup days, event=event. 12. Extract n_model (n used in model), n_events (sum event==1 in analysed data), median_followup_days (median of followup time all analysed records), hr_exposure = exp(coef), CI via exp(coef +/- 1.96*se), p-value (Wald), hr_age = exp(coef_age). 13. Print JSON with all claims.
