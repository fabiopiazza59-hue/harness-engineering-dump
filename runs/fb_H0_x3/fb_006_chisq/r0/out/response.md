# Run summary for fb_006_chisq

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_unfertilised": 163,
  "n_fertilised": 135,
  "events_fertilised": 94,
  "prop_unfertilised": 0.4294478527607362,
  "prop_fertilised": 0.6962962962962963,
  "risk_ratio": 1.6213756613756614,
  "chi2_stat": 21.248013742781275,
  "p_value": 4.035283100798139e-06
}

## Plan
1. Load data.csv. 2. Apply exclusion: keep only rows with age between 18 and 80 inclusive. 3. Exclude rows with missing biomass (complete-case). 4. Group by treatment (fertilised vs unfertilised). 5. Compute n per group, events per group (sum of event==1), proportions. 6. Compute risk ratio = prop_fertilised/prop_unfertilised. 7. Chi-square test of independence (no continuity correction) via scipy.stats.chi2_contingency(correction=False) or pd.crosstab. 8. Print all claims as JSON.
