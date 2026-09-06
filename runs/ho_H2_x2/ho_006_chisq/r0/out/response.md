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
1. Load data.csv. 2. Exclude patients with age outside [18,80] inclusive. 3. Exclude patients with missing sbp_12w. 4. Group by arm (control vs treatment). 5. Compute n per group, events per group (event==1), proportions. 6. Compute risk ratio = prop_treatment/prop_control. 7. Build 2x2 contingency table (arm x event) and run scipy.stats.chi2_contingency with correction=False. 8. Extract chi2 stat and p-value. 9. Print all claims as JSON.
