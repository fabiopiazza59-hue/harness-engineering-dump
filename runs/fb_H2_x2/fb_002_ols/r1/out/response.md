# Run summary for fb_002_ols

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 224,
  "coef_exposure": 28.94434618911196,
  "se_exposure": 13.121287181633466,
  "p_exposure": 0.028430010983004742,
  "coef_age": 2.334822792963563,
  "r_squared": 0.306150043523141,
  "adj_r_squared": 0.29347698495735364
}

## Plan
1. Load data.csv. 2. Apply exclusions in order: (a) keep only rows with age between 18 and 80 inclusive; (b) drop rows with missing biomass or bmi (complete-case). 3. Code treatment as exposure: 1 if fertilised, 0 if unfertilised (check treatment column values). 4. Fit OLS: biomass ~ exposure + age + bmi + baseline, with conventional (non-robust) SEs. 5. Extract n (nobs), coef and se/p for exposure, coef for age, r2, adj r2. 6. Print JSON with all claim ids. 7. Save as analysis.py, verify, submit.
