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
1. Load data.csv. 2. Apply age filter: keep age between 18 and 80 inclusive. 3. Drop rows with missing biomass or bmi. 4. Code treatment as 1=fertilised,0=unfertilised. 5. Fit OLS: biomass ~ treatment + age + bmi + baseline, non-robust SEs. 6. Extract n, coef_exposure (treatment), se_exposure, p_exposure, coef_age, r_squared, adj_r_squared. 7. Print JSON.
