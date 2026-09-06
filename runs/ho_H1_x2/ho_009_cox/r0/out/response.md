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
1. Load data.csv (424 records expected).
2. Remove exact duplicate rows (identical on every column), keep first occurrence.
3. Replace -999 sentinel values with NaN across all columns.
4. Filter age to 18-80 inclusive (drop missing age too since inclusive bounds require known age).
5. Normalise program: strip whitespace, lowercase; map to exposure 1=tutoring,0=standard; drop other labels.
6. Compute follow-up days = last_contact_date - enrol_date.
7. Exclude records with zero follow-up.
8. Administrative censoring at 730 days: if followup>730, set followup=730 and event=0 (censored); else use as-is with actual event indicator.
9. Drop missing event/age/program/followup rows (complete case for Cox model variables).
10. Fit Cox PH model (lifelines CoxPHFitter with Breslow ties) with covariates exposure(program) and age, outcome duration=followup_days, event=event.
11. Extract n_model (n used in model), n_events (sum event after censoring), median_followup_days (median of followup all analysed records after censoring), hr_exposure & CI & p from model summary (exp(coef), exp(coef lower/upper 95%), p), hr_age similarly.
12. Print JSON with all claims mapped.
