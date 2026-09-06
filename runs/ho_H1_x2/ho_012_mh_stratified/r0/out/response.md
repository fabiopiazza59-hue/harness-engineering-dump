# Run summary for ho_012_mh_stratified

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_total": 445,
  "n_exposed": 223,
  "or_crude": 2.472192513368984,
  "or_mh": 2.500371270751079,
  "or_mh_ci_low": 1.7048032099066308,
  "or_mh_ci_high": 3.6672012671420107,
  "mh_chi2": 21.432116859945058,
  "mh_p": 3.665790509810307e-06,
  "or_site1": 1.6607142857142858
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (identical on every column), keep first occurrence. 3. Replace -999 sentinel values with NaN across all columns. 4. Filter to age between 18 and 80 inclusive (drop missing age or out of range). 5. Normalize program: strip whitespace, lowercase. 6. Define exposed = program=='tutoring', unexposed = program=='standard' (drop any other/missing program values). 7. Drop rows missing event or site (needed for MH). 8. n_total = count of analysis sample; n_exposed = count of exposed. 9. Build crude 2x2 table (exposed/unexposed x event/no event), compute crude OR = (a*d)/(b*c). 10. Stratify by site (1-4), build 2x2 tables per site, compute Mantel-Haenszel pooled OR = sum(a_i*d_i/n_i) / sum(b_i*c_i/n_i). 11. Compute MH OR 95% CI using Robins-Breslow-Greenland (RBG) variance formula for log(OR_MH). 12. Compute MH chi-square with continuity correction: sum(a_i) - sum(E_i) formula, corrected by 0.5, divided by sum(Var_i) (Mantel-Haenszel test statistic), then p-value from chi2 with df=1. 13. Compute site 1 specific OR = (a1*d1)/(b1*c1). 14. Print all claims as JSON.
