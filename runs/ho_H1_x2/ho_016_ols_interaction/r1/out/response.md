# Run summary for ho_016_ols_interaction

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 267,
  "coef_exposure": 58.933827069898044,
  "se_exposure_hc3": 12.178018270109126,
  "p_exposure": 1.3025723427478084e-06,
  "coef_interaction": 3.7537144062959786,
  "p_interaction": 0.00026096888724641277,
  "coef_bmi": -0.15650972961204868,
  "r_squared": 0.1897569008172647
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (all columns identical), keep first. 3. Replace -999 with NaN across relevant columns. 4. Filter age 18-80 inclusive. 5. Drop rows missing savings, weight_kg, height_cm. 6. Compute BMI = weight_kg/(height_cm/100)^2; exclude BMI <15 or >50. 7. Recode program to binary exposure: 1=coaching,0=waitlist (case-insensitive match). 8. Center age at mean of analysis sample. 9. Fit OLS: savings ~ exposure + age_c + exposure:age_c + BMI, HC3 robust SE. 10. Extract n, coef_exposure, se_exposure_hc3, p_exposure, coef_interaction, p_interaction, coef_bmi, r_squared. 11. Print JSON.
