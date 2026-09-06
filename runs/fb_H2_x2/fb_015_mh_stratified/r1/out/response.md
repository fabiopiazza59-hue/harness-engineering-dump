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
1. Load data.csv. 2. Remove exact duplicate rows (all columns identical), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive (drop missing age too, since must be in range). 5. Normalize diet: strip whitespace, lowercase. 6. Define exposed = diet=='mediterranean', unexposed = diet=='usual' (drop other/missing categories). 7. Drop rows with missing event. 8. Compute n_total, n_exposed. 9. Build crude 2x2 table (exposed/unexposed x event/no event), compute crude OR = (a*d)/(b*c). 10. Stratify by site (1-4), build 2x2 tables per site, compute Mantel-Haenszel OR = sum(a_i*d_i/n_i) / sum(b_i*c_i/n_i). 11. Compute MH CI using Robins-Breslow-Greenland (RBG) variance formula, standard for MH OR CI. 12. Compute MH chi-square with continuity correction (standard Mantel-Haenszel test statistic). 13. Compute p-value from chi2 with df=1. 14. Compute OR for site 1 alone. 15. Print JSON of all claims.
