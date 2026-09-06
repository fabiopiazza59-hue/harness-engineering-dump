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
1. Load data.csv. 2. Remove exact duplicate rows (identical on all columns), keep first. 3. Replace -999 with NaN. 4. Filter age 18-80 inclusive (drop missing age or out of range). 5. Normalize diet: strip+lowercase. 6. Define exposed = diet=='mediterranean'. 7. n_total = count of analysis sample (need event and diet non-missing at least). 8. n_exposed = count exposed. 9. Build 2x2 table exposed/unexposed x event/no event (need event non-missing, drop missing event). 10. crude OR = (a*d)/(b*c) using standard 2x2 counts. 11. Stratify by site (1-4), compute MH pooled OR = sum(a_i*d_i/n_i)/sum(b_i*c_i/n_i). 12. MH OR CI via Robins-Breslow-Greenland variance formula. 13. MH chi-square with continuity correction (Cochran-Mantel-Haenszel test, corrected). 14. p-value from chi2 with df=1. 15. Site1 OR = a*d/(b*c) crude within site1 only. Print all as JSON.
