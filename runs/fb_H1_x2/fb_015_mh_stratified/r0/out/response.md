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
1. Load data.csv. 2. Drop exact duplicate rows (all columns identical), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive (drop missing age). 5. Normalize diet: strip whitespace, lowercase. 6. Define exposed = diet=='mediterranean', unexposed = diet=='usual' (drop other/missing diet values). 7. Drop missing event values. 8. n_total = count of analysis sample; n_exposed = count where exposed. 9. Build crude 2x2 table (exposed/unexposed x event/no event), compute crude OR = (a*d)/(b*c). 10. Build per-site 2x2 tables ordered exposed/unexposed by event/no event for site in 1..4, compute MH odds ratio = sum(a_i*d_i/n_i) / sum(b_i*c_i/n_i). 11. Compute MH OR variance (Robins-Breslow-Greenland) for 95% CI. 12. Compute MH chi-square with continuity correction: sum((|sum(a_i)-sum(E_i)| - 0.5)^2) / sum(Var_i) using hypergeometric moments per stratum. 13. Compute p-value from chi2 distribution df=1. 14. Compute site1 OR from site1 2x2 table using same a*d/(b*c) formula. 15. Print JSON with all claim slots.
