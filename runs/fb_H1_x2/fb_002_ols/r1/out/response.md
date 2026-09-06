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
1. Load data.csv (243 rows expected). 2. Apply exclusions in order: (a) keep only plots with age between 18 and 80 inclusive; (b) drop rows with missing biomass or bmi (complete-case). 3. Recode treatment into exposure variable: 1 = fertilised, 0 = unfertilised. 4. Fit OLS: biomass ~ exposure + age + bmi + baseline, using conventional (non-robust) standard errors, on original scale covariates. 5. Extract: n_model = number of obs used in model; coef_exposure, se_exposure, p_exposure = coefficient/SE/p-value for exposure variable; coef_age = coefficient for age; r_squared, adj_r_squared from model. 6. Print all as JSON. 7. Save script as analysis.py and write claims.json.
