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
1. Load data.csv. 2. Apply exclusions in order: (a) keep only rows with age between 18 and 80 inclusive; (b) drop rows with missing biomass (complete-case). 3. Group by treatment column (fertilised vs unfertilised). 4. Compute n per group, events (sum of event==1) per group, proportions. 5. Compute risk ratio = prop_fertilised/prop_unfertilised. 6. Run scipy.stats.chi2_contingency with correction=False on 2x2 table (event yes/no x treatment) to get chi2 stat and p-value. 7. Print all claims as JSON.
