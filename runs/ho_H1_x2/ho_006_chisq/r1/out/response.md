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
1. Load data.csv. 2. Apply exclusion: keep age between 18 and 80 inclusive. 3. Apply exclusion: drop rows with missing sbp_12w. 4. Compute group sizes n_control, n_treatment from arm column. 5. Compute events_treatment (sum of event in treatment group). 6. Compute prop_control and prop_treatment as mean of event in each group. 7. Compute risk_ratio = prop_treatment/prop_control. 8. Perform Pearson chi-square test of independence (2x2 table of arm x event) without continuity correction using scipy.stats.chi2_contingency(correction=False). 9. Extract chi2_stat and p_value. 10. Print all claims as JSON.
