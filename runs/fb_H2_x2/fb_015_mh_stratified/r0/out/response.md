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
1. Load data.csv. 2. Drop exact duplicate rows (all columns identical), keep first. 3. Replace -999 with NaN in all columns. 4. Filter age between 18 and 80 inclusive (drop missing age). 5. Normalize diet: strip whitespace, lowercase. 6. Define exposed = diet=='mediterranean', unexposed = diet=='usual' (drop other/missing values if any). 7. n_total = count of analysis sample (after exclusions, with valid diet and event and site). 8. n_exposed = count exposed. 9. Build crude 2x2 table (exposed/unexposed x event/no event), compute crude OR = (a*d)/(b*c). 10. Build stratified tables by site (1-4), compute MH pooled OR = sum(a_i*d_i/n_i)/sum(b_i*c_i/n_i). 11. Compute MH OR CI using Robins-Breslow-Greenland variance formula. 12. Compute MH chi-square with continuity correction (Mantel-Haenszel test statistic with 0.5 correction) and p-value from chi2 df=1. 13. Compute OR for site 1 alone. 14. Print JSON with all claims.
