# Run summary for fb_015_mh_stratified

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_total": 307,
  "n_exposed": 164,
  "or_crude": 0.5713033313851549,
  "or_mh": 0.5574900665452579,
  "or_mh_ci_low": 0.34434453898523265,
  "or_mh_ci_high": 0.9025703593631398,
  "mh_chi2": 5.143501328634977,
  "mh_p": 0.023333542804517826,
  "or_site1": 1.0178571428571428
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (identical on all columns), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive. 5. Normalize diet: strip whitespace, lowercase. 6. Drop rows with missing diet, event, or site (needed for analysis). 7. Define exposed = diet=='mediterranean'. 8. Compute n_total, n_exposed. 9. Build crude 2x2 table (exposed/unexposed x event/no event), compute crude OR. 10. Stratify by site (1-4), build 2x2 tables per site, compute Mantel-Haenszel OR, CI (Robins-Breslow-Day or standard MH CI formula), MH chi-square with continuity correction, p-value. 11. Compute OR for site 1 alone from its 2x2 table. 12. Output all claims as JSON.
