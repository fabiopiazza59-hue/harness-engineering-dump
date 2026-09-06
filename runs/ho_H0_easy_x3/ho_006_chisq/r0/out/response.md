# Run summary for ho_006_chisq

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_control": 168,
  "n_treatment": 130,
  "events_treatment": 38,
  "prop_control": 0.47619047619047616,
  "prop_treatment": 0.2923076923076923,
  "risk_ratio": 0.6138461538461539,
  "chi2_stat": 10.360877189351761,
  "p_value": 0.0012871402931461772
}

## Plan
1. Load data.csv. 2. Apply exclusion: keep only age between 18 and 80 inclusive. 3. Apply exclusion: drop rows with missing sbp_12w. 4. This is the analysis sample. 5. Split by arm (control vs treatment). 6. Compute n_control, n_treatment as group sizes. 7. Compute events_treatment = sum(event==1) in treatment group. 8. Compute prop_control = mean(event) in control, prop_treatment = mean(event) in treatment. 9. risk_ratio = prop_treatment/prop_control. 10. Build 2x2 contingency table (arm x event) and run scipy.stats.chi2_contingency with correction=False to get chi2_stat and p_value. 11. Print all claims as JSON.
