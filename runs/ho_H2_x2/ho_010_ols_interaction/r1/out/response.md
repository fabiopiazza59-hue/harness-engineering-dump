# Run summary for ho_010_ols_interaction

Status: success
Reason: verification gate passed
Steps: 5; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_model": 401,
  "coef_exposure": -7.37880510859495,
  "se_exposure_hc3": 1.2143135025370693,
  "p_exposure": 1.2281565102439397e-09,
  "coef_interaction": -0.11528452671652002,
  "p_interaction": 0.2226173693562139,
  "coef_bmi": 0.5133464796205561,
  "r_squared": 0.12510349936102938
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (identical on every column), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age 18-80 inclusive. 5. Drop rows missing sbp_12w, weight_kg, height_cm. 6. Compute BMI = weight_kg/(height_cm/100)^2; exclude BMI<15 or >50. 7. Recode arm to binary exposure: treatment=1, control=0 (need to check actual values). 8. Center age at mean of analysis sample. 9. Create interaction = exposure*age_centered. 10. Fit OLS: sbp_12w ~ exposure + age_centered + interaction + bmi, HC3 robust SE. 11. Extract n, coef_exposure, se_exposure_hc3, p_exposure, coef_interaction, p_interaction, coef_bmi, r_squared. 12. Print JSON.
