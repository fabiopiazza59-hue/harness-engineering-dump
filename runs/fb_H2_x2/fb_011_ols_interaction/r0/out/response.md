# Run summary for fb_011_ols_interaction

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 385,
  "coef_exposure": 4.693808312857147,
  "se_exposure_hc3": 1.1304348887854232,
  "p_exposure": 3.29273185640977e-05,
  "coef_interaction": -0.14538262430726343,
  "p_interaction": 0.08094265137155644,
  "coef_bmi": 0.8105836063805563,
  "r_squared": 0.16174519891102634
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (all columns identical), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive. 5. Drop rows missing math_score, weight_kg, or height_cm. 6. Compute BMI = weight_kg / (height_cm/100)^2; exclude BMI <15 or >50. 7. Recode program to exposure: 1 if tutoring, 0 if standard (need to check unique values in program column - free text). 8. Center age at mean of analysis sample. 9. Create interaction = exposure * age_centered. 10. Fit OLS: math_score ~ exposure + age_centered + interaction + bmi, HC3 robust SE. 11. Extract n, coef_exposure, se_exposure_hc3, p_exposure, coef_interaction, p_interaction, coef_bmi, r_squared. 12. Print as JSON.
