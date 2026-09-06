#!/usr/bin/env python3
"""Hard tier of synthetic reproduce-analysis tasks: messier data and less common analyses.

Wrinkles: sentinel-coded missing values, duplicated records, inconsistent category labels,
derived variables (BMI from height/weight, follow-up time from dates), administrative
censoring, robust standard errors, interaction terms, multiple-testing correction,
stratified tables. Analyses: paired, mannwhitney, ols_interaction, cox, multi_bh, mh_stratified.

    python tasks/generator/make_hard_tasks.py --split feedback --n 10 --seed 505 --start-index 7
"""
from __future__ import annotations

import argparse
import json
import random
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_tasks import ROOT, Study, THEMES, TOL  # noqa: E402


def messy_labels(rng, values, variants):
    out = []
    for v in values:
        r = rng.random()
        if r < 0.15:
            out.append(v.capitalize())
        elif r < 0.25:
            out.append(v.upper())
        elif r < 0.35:
            out.append(v + " ")
        elif r < 0.42:
            out.append(" " + v)
        else:
            out.append(v)
    return out


class HardStudy(Study):
    def make_data(self):
        t = self.theme
        rng = self.rng
        n = int(rng.integers(220, 460))
        df = pd.DataFrame({"id": np.arange(1, n + 1)})
        df["age"] = rng.normal(48, 13, n).round(0)
        df["sex"] = rng.integers(0, 2, n)
        df["height_cm"] = rng.normal(170, 9, n).round(1)
        df["weight_kg"] = (df["height_cm"] / 100) ** 2 * rng.normal(26, 4, n)
        df["weight_kg"] = df["weight_kg"].round(1)
        df["site"] = rng.integers(1, 5, n)
        g0, g1 = t["groups"]
        raw_group = rng.choice([g0, g1], n)
        df[t["group_col"]] = messy_labels(rng, raw_group, None) if self.analysis in ("mannwhitney", "mh_stratified", "cox") else raw_group
        base_mu, base_sd = {"sbp_12w": (140, 12), "math_score": (62, 12), "biomass": (420, 90), "rt_ms": (720, 90),
                            "savings": (310, 110), "glucose_fu": (104, 12)}[t["outcome_col"]]
        sign = -1 if t["outcome_col"] in ("sbp_12w", "rt_ms", "glucose_fu") else 1
        grp = (raw_group == g1).astype(float)
        eff = float(rng.uniform(0.3, 0.7)) * base_sd
        bmi_true = df["weight_kg"] / (df["height_cm"] / 100) ** 2
        df["baseline"] = rng.normal(base_mu, base_sd, n).round(1)
        age_slope = float(rng.uniform(-0.5, 0.5)) * base_sd / 13
        inter = float(rng.uniform(-0.4, 0.4)) * base_sd / 13
        df[t["outcome_col"]] = (0.55 * df["baseline"] + 0.45 * base_mu + sign * eff * grp + age_slope * (df["age"] - 48)
                                + inter * grp * (df["age"] - 48) + 0.8 * (bmi_true - 26) + rng.normal(0, base_sd * 0.75, n)).round(1)
        # paired outcome (post) for paired analyses
        df[t["outcome_col"] + "_post"] = (df[t["outcome_col"]] + sign * float(rng.uniform(0.2, 0.5)) * base_sd + rng.normal(0, base_sd * 0.5, n)).round(1)
        # binary event and survival-style dates
        lin = -0.3 + sign * 0.8 * grp + 0.03 * (df["age"] - 48) + 0.1 * (bmi_true - 26)
        pr = 1 / (1 + np.exp(-lin))
        df["event"] = (rng.uniform(size=n) < pr).astype(int)
        start = pd.Timestamp("2019-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D")
        hazard = np.exp(sign * 0.6 * grp + 0.02 * (df["age"] - 48))
        tt = rng.exponential(600 / hazard).round(0).astype(int) + 1
        df["enrol_date"] = start.strftime("%Y-%m-%d")
        df["last_contact_date"] = (start + pd.to_timedelta(tt, unit="D")).strftime("%Y-%m-%d")
        df["event"] = np.where(tt <= 1000, (rng.uniform(size=n) < 0.75).astype(int), 0) if self.analysis == "cox" else df["event"]
        # biomarkers for multiple-comparison tasks
        for k in range(1, 7):
            rho = [0.45, 0.05, -0.3, 0.02, 0.18, -0.04][k - 1]
            z = (df[t["outcome_col"]] - df[t["outcome_col"]].mean()) / df[t["outcome_col"]].std()
            df[f"biomarker_{k}"] = (rho * z + np.sqrt(max(1e-6, 1 - rho ** 2)) * rng.normal(size=n)).round(3)
        # sentinel-coded missing values (-999) in a few numeric columns
        for col in [t["outcome_col"], t["outcome_col"] + "_post", "weight_kg", "biomarker_2"]:
            m = rng.uniform(size=n) < 0.04
            df.loc[m, col] = -999
        # under/over-age rows
        idx = rng.choice(n, int(rng.integers(5, 12)), replace=False)
        df.loc[idx, "age"] = rng.choice([15, 16, 17, 82, 85, 90], len(idx))
        # duplicated records (exact copies appended)
        dups = df.sample(int(rng.integers(4, 9)), random_state=int(self.seed % 1000))
        df = pd.concat([df, dups], ignore_index=True).sample(frac=1, random_state=int(self.seed % 997)).reset_index(drop=True)
        self.columns_doc = [("age", "age in years"), ("sex", "sex (0 = female, 1 = male)"), ("height_cm", "height in centimetres"),
                            ("weight_kg", "weight in kilograms"), ("site", "study site identifier (1-4)"),
                            (t["group_col"], f"study group: {g0} or {g1} (free-text entry)"), ("baseline", "baseline value of the outcome"),
                            (t["outcome_col"], t["outcome"]), (t["outcome_col"] + "_post", t["outcome"] + " at the second assessment"),
                            ("event", "binary study event (1 = yes)"), ("enrol_date", "enrolment date (YYYY-MM-DD)"),
                            ("last_contact_date", "date of event or last contact (YYYY-MM-DD)"),
                            ("biomarker_1..biomarker_6", "six standardised biomarker levels")]
        self.df = df

    def preprocess(self) -> pd.DataFrame:
        t = self.theme
        df = self.df.copy()
        ycol = t["outcome_col"]
        code = ["import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm",
                "from statsmodels.stats.multitest import multipletests",
                "df = pd.read_csv('data.csv')",
                "df = df.drop_duplicates(keep='first')",
                "df = df.replace(-999, np.nan)",
                "df = df[(df['age'] >= 18) & (df['age'] <= 80)]"]
        df = df.drop_duplicates(keep="first").replace(-999, np.nan)
        df = df[(df["age"] >= 18) & (df["age"] <= 80)]
        rules = ["Exact duplicate records (identical on every column) were removed, keeping the first occurrence.",
                 "The value -999 denotes a missing measurement and was treated as missing.",
                 f"Only {t['unit']} aged 18 to 80 years inclusive were analysed."]
        if self.analysis in ("mannwhitney", "mh_stratified", "cox"):
            df[t["group_col"]] = df[t["group_col"]].str.strip().str.lower()
            code.append(f"df['{t['group_col']}'] = df['{t['group_col']}'].str.strip().str.lower()")
            rules.append(f"Group labels in `{t['group_col']}` were entered free-text and were normalised by trimming whitespace and lower-casing before use.")
            self.wrinkles.append("messy_labels")
        self.wrinkles += ["duplicates", "sentinel_missing"]
        needed = {"paired": [ycol, ycol + "_post"], "mannwhitney": [ycol], "ols_interaction": [ycol, "weight_kg", "height_cm"],
                  "cox": [], "multi_bh": [ycol] + [f"biomarker_{k}" for k in range(1, 7)], "mh_stratified": []}[self.analysis]
        if needed:
            df = df.dropna(subset=needed)
            code.append(f"df = df.dropna(subset={needed!r})")
            rules.append(f"Records with missing {', '.join(needed)} were excluded (complete-case analysis).")
        self.methods_paragraphs.append(" ".join(rules))
        self.ref_code_lines = code
        return df

    # ------------------------------------------------------------ analyses
    def run_paired(self, df):
        t = self.theme
        y0, y1 = t["outcome_col"], t["outcome_col"] + "_post"
        wilcoxon = self.pyrng.random() < 0.4
        d = df[y1] - df[y0]
        if wilcoxon:
            res = st.wilcoxon(df[y1], df[y0], zero_method="wilcox", correction=False, method="approx")
            stat_name, stat_val = "w_stat", res.statistic
            test_txt = "a Wilcoxon signed-rank test (two-sided, normal approximation without continuity correction, zero differences discarded)"
        else:
            res = st.ttest_rel(df[y1], df[y0])
            stat_name, stat_val = "t_stat", res.statistic
            test_txt = "a paired t-test (two-sided)"
        pct = ((df[y1] - df[y0]) / df[y0] * 100)
        self.methods_paragraphs.append(
            f"The change in {t['outcome']} from the first to the second assessment was tested with {test_txt}. The mean change is the mean of "
            f"(second minus first) over analysed {t['unit']}; its standard deviation is the sample SD of the paired differences. Cohen's dz is the mean change "
            f"divided by the SD of the differences. Percent change was computed per {t['unit'][:-1]} as (second - first) / first x 100 and then averaged.")
        self.wrinkles.append("wilcoxon" if wilcoxon else "paired_t")
        self.add_claim("n_pairs", f"Number of {t['unit']} with both assessments in the analysis", len(df), "count")
        self.add_claim("mean_first", f"Mean {t['outcome']} at the first assessment", df[y0].mean(), "mean")
        self.add_claim("mean_second", "Mean at the second assessment", df[y1].mean(), "mean")
        self.add_claim("mean_change", "Mean change (second minus first)", d.mean(), "diff")
        self.add_claim("sd_change", "Sample SD of the paired differences", d.std(ddof=1), "sd")
        self.add_claim(stat_name, "Test statistic of the paired test", stat_val, "stat")
        self.add_claim("p_value", "Two-sided p-value of the paired test", res.pvalue, "pvalue")
        self.add_claim("cohens_dz", "Cohen's dz", d.mean() / d.std(ddof=1), "effect")
        self.add_claim("mean_pct_change", "Mean per-subject percent change", pct.mean(), "diff")
        self.results_sentences.append(
            f"Among {{n_pairs}} {t['unit']} the mean value changed from {{mean_first}} to {{mean_second}}, a mean change of {{mean_change}} (SD {{sd_change}}; "
            f"statistic = {{{stat_name}}}, p {{p_value}}; dz = {{cohens_dz}}); the mean percent change was {{mean_pct_change}}%.")
        self.ref_code_lines += [
            f"d = df['{y1}'] - df['{y0}']",
            (f"res = st.wilcoxon(df['{y1}'], df['{y0}'], zero_method='wilcox', correction=False, method='approx')" if wilcoxon
             else f"res = st.ttest_rel(df['{y1}'], df['{y0}'])"),
            f"pct = (df['{y1}'] - df['{y0}']) / df['{y0}'] * 100",
            "out = {'n_pairs': len(df), " + f"'mean_first': df['{y0}'].mean(), 'mean_second': df['{y1}'].mean(), 'mean_change': d.mean(), 'sd_change': d.std(ddof=1), "
            f"'{stat_name}': res.statistic, 'p_value': res.pvalue, 'cohens_dz': d.mean()/d.std(ddof=1), 'mean_pct_change': pct.mean()}}",
        ]

    def run_mannwhitney(self, df):
        t = self.theme
        g0, g1 = t["groups"]
        ycol = t["outcome_col"]
        a = df.loc[df[t["group_col"]] == g0, ycol]
        b = df.loc[df[t["group_col"]] == g1, ycol]
        res = st.mannwhitneyu(b, a, alternative="two-sided", method="asymptotic", use_continuity=True)
        rb = 1 - 2 * res.statistic / (len(a) * len(b))
        self.methods_paragraphs.append(
            f"{t['outcome'].capitalize()} was compared between the {g1} and {g0} groups with a two-sided Mann-Whitney U test (asymptotic method with continuity correction). "
            f"The U statistic is reported for the {g1} group. The rank-biserial correlation was computed as 1 - 2U/(n1 n2). Medians and the difference in medians ({g1} minus {g0}) are reported.")
        self.add_claim("n_" + g0, f"Number of {t['unit']} in the {g0} group", len(a), "count")
        self.add_claim("n_" + g1, f"Number of {t['unit']} in the {g1} group", len(b), "count")
        self.add_claim("median_" + g0, f"Median {t['outcome']} in the {g0} group", a.median(), "mean")
        self.add_claim("median_" + g1, f"Median {t['outcome']} in the {g1} group", b.median(), "mean")
        self.add_claim("median_diff", f"Difference in medians ({g1} minus {g0})", b.median() - a.median(), "diff")
        self.add_claim("u_stat", f"Mann-Whitney U statistic for the {g1} group", res.statistic, "stat")
        self.add_claim("p_value", "Two-sided p-value", res.pvalue, "pvalue")
        self.add_claim("rank_biserial", "Rank-biserial correlation 1 - 2U/(n1 n2)", rb, "effect")
        self.results_sentences.append(
            f"The {g1} group (n = {{n_{g1}}}, median {{median_{g1}}}) differed from the {g0} group (n = {{n_{g0}}}, median {{median_{g0}}}); the difference in medians was {{median_diff}} "
            f"(U = {{u_stat}}, p {{p_value}}, rank-biserial r = {{rank_biserial}}).")
        self.ref_code_lines += [
            f"a = df.loc[df['{t['group_col']}'] == '{g0}', '{ycol}']; b = df.loc[df['{t['group_col']}'] == '{g1}', '{ycol}']",
            "res = st.mannwhitneyu(b, a, alternative='two-sided', method='asymptotic', use_continuity=True)",
            f"out = {{'n_{g0}': len(a), 'n_{g1}': len(b), 'median_{g0}': a.median(), 'median_{g1}': b.median(), 'median_diff': b.median()-a.median(), "
            "'u_stat': res.statistic, 'p_value': res.pvalue, 'rank_biserial': 1 - 2*res.statistic/(len(a)*len(b))}",
        ]

    def run_ols_interaction(self, df):
        t = self.theme
        g0, g1 = t["groups"]
        ycol = t["outcome_col"]
        df = df.assign(bmi=df["weight_kg"] / (df["height_cm"] / 100) ** 2)
        df = df[(df["bmi"] >= 15) & (df["bmi"] <= 50)]
        df = df.assign(age_c=df["age"] - df["age"].mean(), exposure=(df[t["group_col"]] == g1).astype(float))
        df = df.assign(inter=df["exposure"] * df["age_c"])
        X = sm.add_constant(df[["exposure", "age_c", "inter", "bmi"]])
        m = sm.OLS(df[ycol], X).fit(cov_type="HC3")
        self.methods_paragraphs.append(
            f"Body-mass index was derived as weight in kg divided by height in metres squared, and {t['unit']} with an implausible BMI (below 15 or above 50) were excluded. "
            f"Age was centred at the mean of the analysis sample. {t['outcome'].capitalize()} was regressed on {t['exposure']} (1 = {g1}, 0 = {g0}), centred age, "
            f"their product (interaction), and BMI, using ordinary least squares with heteroskedasticity-robust (HC3) standard errors. R squared is the ordinary R squared.")
        self.wrinkles += ["derived_bmi", "centred_age", "hc3"]
        self.add_claim("n_model", "Number of records in the model", int(m.nobs), "count")
        self.add_claim("coef_exposure", "Coefficient of the exposure (at mean age)", m.params["exposure"], "coef")
        self.add_claim("se_exposure_hc3", "HC3 robust standard error of the exposure coefficient", m.bse["exposure"], "se")
        self.add_claim("p_exposure", "p-value of the exposure coefficient (HC3)", m.pvalues["exposure"], "pvalue")
        self.add_claim("coef_interaction", "Coefficient of the exposure x centred-age interaction", m.params["inter"], "coef")
        self.add_claim("p_interaction", "p-value of the interaction term (HC3)", m.pvalues["inter"], "pvalue")
        self.add_claim("coef_bmi", "Coefficient of BMI", m.params["bmi"], "coef")
        self.add_claim("r_squared", "R squared", m.rsquared, "r2")
        self.results_sentences.append(
            f"In the {{n_model}} records analysed, the exposure coefficient was {{coef_exposure}} (HC3 SE {{se_exposure_hc3}}, p {{p_exposure}}); the interaction with centred age was "
            f"{{coef_interaction}} (p {{p_interaction}}) and the BMI coefficient {{coef_bmi}} (R^2 = {{r_squared}}).")
        self.ref_code_lines += [
            "df = df.assign(bmi=df['weight_kg'] / (df['height_cm']/100)**2)",
            "df = df[(df['bmi'] >= 15) & (df['bmi'] <= 50)]",
            f"df = df.assign(age_c=df['age'] - df['age'].mean(), exposure=(df['{t['group_col']}'] == '{g1}').astype(float))",
            "df = df.assign(inter=df['exposure']*df['age_c'])",
            "X = sm.add_constant(df[['exposure', 'age_c', 'inter', 'bmi']])",
            f"m = sm.OLS(df['{ycol}'], X).fit(cov_type='HC3')",
            "out = {'n_model': int(m.nobs), 'coef_exposure': m.params['exposure'], 'se_exposure_hc3': m.bse['exposure'], 'p_exposure': m.pvalues['exposure'], "
            "'coef_interaction': m.params['inter'], 'p_interaction': m.pvalues['inter'], 'coef_bmi': m.params['bmi'], 'r_squared': m.rsquared}",
        ]

    def run_cox(self, df):
        t = self.theme
        g0, g1 = t["groups"]
        d0 = pd.to_datetime(df["enrol_date"])
        d1 = pd.to_datetime(df["last_contact_date"])
        time_days = (d1 - d0).dt.days.astype(float)
        event = df["event"].astype(int).copy()
        cens = 730
        event = np.where(time_days > cens, 0, event)
        time_days = np.minimum(time_days, cens)
        df = df.assign(time=time_days, ev=event, exposure=(df[t["group_col"]] == g1).astype(float))
        df = df[df["time"] > 0]
        X = df[["exposure", "age"]]
        m = sm.PHReg(df["time"], X, status=df["ev"], ties="breslow").fit()
        s = m.summary().tables[1]
        hr = float(np.exp(m.params[0]))
        ci = np.exp(m.params[0] + np.array([-1, 1]) * 1.959963984540054 * m.bse[0])
        self.methods_paragraphs.append(
            f"Follow-up time in days was computed from the enrolment date to the date of event or last contact. Follow-up was administratively censored at {cens} days: "
            f"{t['unit']} with longer follow-up were censored at {cens} days and counted as event-free, and records with zero follow-up were excluded. "
            f"The hazard of the study event was modelled with a Cox proportional-hazards model with {t['exposure']} (1 = {g1}, 0 = {g0}) and age (years) as covariates, "
            f"using the Breslow method for ties. Hazard ratios with Wald 95% confidence intervals (z = 1.96) are reported.")
        self.wrinkles += ["dates_to_time", "admin_censoring", "breslow"]
        self.add_claim("n_model", f"Number of {t['unit']} in the Cox model", int(len(df)), "count")
        self.add_claim("n_events", "Number of events after censoring", int(df["ev"].sum()), "count")
        self.add_claim("median_followup_days", "Median follow-up time in days (all analysed records, after censoring)", float(df["time"].median()), "mean")
        self.add_claim("hr_exposure", "Hazard ratio for the exposure", hr, "ratio")
        self.add_claim("hr_ci_low", "Lower 95% CI of the exposure hazard ratio", float(ci[0]), "ci")
        self.add_claim("hr_ci_high", "Upper 95% CI of the exposure hazard ratio", float(ci[1]), "ci")
        self.add_claim("p_exposure", "p-value of the exposure term", float(m.pvalues[0]), "pvalue")
        self.add_claim("hr_age", "Hazard ratio per year of age", float(np.exp(m.params[1])), "ratio")
        self.results_sentences.append(
            f"Of {{n_model}} {t['unit']} (median follow-up {{median_followup_days}} days), {{n_events}} had an event. The exposure hazard ratio was {{hr_exposure}} "
            f"(95% CI {{hr_ci_low}} to {{hr_ci_high}}, p {{p_exposure}}); the hazard ratio per year of age was {{hr_age}}.")
        self.ref_code_lines += [
            "t0 = pd.to_datetime(df['enrol_date']); t1 = pd.to_datetime(df['last_contact_date'])",
            "tm = (t1 - t0).dt.days.astype(float); ev = df['event'].astype(int)",
            f"ev = np.where(tm > {cens}, 0, ev); tm = np.minimum(tm, {cens})",
            f"df = df.assign(time=tm, ev=ev, exposure=(df['{t['group_col']}'] == '{g1}').astype(float)); df = df[df['time'] > 0]",
            "m = sm.PHReg(df['time'], df[['exposure', 'age']], status=df['ev'], ties='breslow').fit()",
            "ci = np.exp(m.params[0] + np.array([-1, 1]) * 1.959963984540054 * m.bse[0])",
            "out = {'n_model': int(len(df)), 'n_events': int(df['ev'].sum()), 'median_followup_days': float(df['time'].median()), 'hr_exposure': float(np.exp(m.params[0])), "
            "'hr_ci_low': float(ci[0]), 'hr_ci_high': float(ci[1]), 'p_exposure': float(m.pvalues[0]), 'hr_age': float(np.exp(m.params[1]))}",
        ]

    def run_multi_bh(self, df):
        t = self.theme
        ycol = t["outcome_col"]
        cols = [f"biomarker_{k}" for k in range(1, 7)]
        rs, ps = [], []
        for c in cols:
            r, p = st.pearsonr(df[c], df[ycol])
            rs.append(r)
            ps.append(p)
        rej, padj, _, _ = multipletests(ps, alpha=0.05, method="fdr_bh")
        strongest = max(range(6), key=lambda i: abs(rs[i]))
        self.methods_paragraphs.append(
            f"Each of the six biomarkers was correlated with {t['outcome']} using Pearson correlation (two-sided). The six p-values were adjusted for multiple testing with the "
            f"Benjamini-Hochberg false-discovery-rate procedure; associations with adjusted p < 0.05 were declared significant. The strongest association is the biomarker with the largest absolute correlation.")
        self.wrinkles += ["bh_correction"]
        self.add_claim("n_analysed", f"Number of {t['unit']} with all biomarkers and the outcome", len(df), "count")
        self.add_claim("r_biomarker_1", "Pearson r of biomarker_1 with the outcome", rs[0], "corr")
        self.add_claim("p_adj_biomarker_1", "BH-adjusted p-value for biomarker_1", padj[0], "pvalue")
        self.add_claim("r_biomarker_3", "Pearson r of biomarker_3 with the outcome", rs[2], "corr")
        self.add_claim("p_adj_biomarker_3", "BH-adjusted p-value for biomarker_3", padj[2], "pvalue")
        self.add_claim("p_adj_biomarker_5", "BH-adjusted p-value for biomarker_5", padj[4], "pvalue")
        self.add_claim("n_significant_adj", "Number of biomarkers significant after BH adjustment (adjusted p < 0.05)", int(rej.sum()), "count")
        self.add_claim("r_strongest", "Signed Pearson r of the biomarker with the largest absolute correlation", rs[strongest], "corr")
        self.results_sentences.append(
            f"Among {{n_analysed}} {t['unit']}, biomarker_1 correlated with the outcome (r = {{r_biomarker_1}}, adjusted p {{p_adj_biomarker_1}}), as did biomarker_3 (r = {{r_biomarker_3}}, "
            f"adjusted p {{p_adj_biomarker_3}}); the adjusted p for biomarker_5 was {{p_adj_biomarker_5}}. In total {{n_significant_adj}} biomarkers remained significant after adjustment; "
            f"the strongest association had r = {{r_strongest}}.")
        self.ref_code_lines += [
            f"cols = [f'biomarker_{{k}}' for k in range(1, 7)]",
            f"rp = [st.pearsonr(df[c], df['{ycol}']) for c in cols]; rs = [x[0] for x in rp]; ps = [x[1] for x in rp]",
            "rej, padj, _, _ = multipletests(ps, alpha=0.05, method='fdr_bh')",
            "strongest = max(range(6), key=lambda i: abs(rs[i]))",
            "out = {'n_analysed': len(df), 'r_biomarker_1': rs[0], 'p_adj_biomarker_1': padj[0], 'r_biomarker_3': rs[2], 'p_adj_biomarker_3': padj[2], "
            "'p_adj_biomarker_5': padj[4], 'n_significant_adj': int(rej.sum()), 'r_strongest': rs[strongest]}",
        ]

    def run_mh_stratified(self, df):
        t = self.theme
        g0, g1 = t["groups"]
        df = df.assign(exposure=(df[t["group_col"]] == g1).astype(int))
        tables = []
        for s in sorted(df["site"].unique()):
            sub = df[df["site"] == s]
            tab = pd.crosstab(sub["exposure"], sub["event"]).reindex(index=[1, 0], columns=[1, 0]).fillna(0).values
            tables.append(tab)
        stt = sm.stats.StratifiedTable(tables)
        or_mh = float(stt.oddsratio_pooled)
        ci = stt.oddsratio_pooled_confint(alpha=0.05)
        test = stt.test_null_odds(correction=True)
        crude = pd.crosstab(df["exposure"], df["event"]).reindex(index=[1, 0], columns=[1, 0]).fillna(0).values
        or_crude = (crude[0, 0] * crude[1, 1]) / (crude[0, 1] * crude[1, 0])
        s1 = tables[0]
        or_site1 = (s1[0, 0] * s1[1, 1]) / (s1[0, 1] * s1[1, 0])
        self.methods_paragraphs.append(
            f"The association between {t['exposure']} (exposed = {g1}) and the study event was summarised with the crude odds ratio and with the Mantel-Haenszel odds ratio pooled across "
            f"the four study sites (2x2 tables ordered exposed/unexposed by event/no event), with its 95% confidence interval, and the Mantel-Haenszel chi-square test with continuity correction. "
            f"The site-specific odds ratio for site 1 is also reported.")
        self.wrinkles += ["mantel_haenszel"]
        self.add_claim("n_total", f"Number of {t['unit']} analysed", len(df), "count")
        self.add_claim("n_exposed", f"Number in the {g1} (exposed) group", int(df["exposure"].sum()), "count")
        self.add_claim("or_crude", "Crude odds ratio (exposed vs unexposed)", float(or_crude), "ratio")
        self.add_claim("or_mh", "Mantel-Haenszel pooled odds ratio across sites", or_mh, "ratio")
        self.add_claim("or_mh_ci_low", "Lower 95% CI of the MH odds ratio", float(ci[0]), "ci")
        self.add_claim("or_mh_ci_high", "Upper 95% CI of the MH odds ratio", float(ci[1]), "ci")
        self.add_claim("mh_chi2", "Mantel-Haenszel chi-square statistic (continuity corrected)", float(test.statistic), "stat")
        self.add_claim("mh_p", "p-value of the Mantel-Haenszel test", float(test.pvalue), "pvalue")
        self.add_claim("or_site1", "Odds ratio within site 1", float(or_site1), "ratio")
        self.results_sentences.append(
            f"Among {{n_total}} {t['unit']} ({{n_exposed}} exposed) the crude odds ratio was {{or_crude}} and the Mantel-Haenszel odds ratio pooled over sites was {{or_mh}} "
            f"(95% CI {{or_mh_ci_low}} to {{or_mh_ci_high}}; MH chi-square = {{mh_chi2}}, p {{mh_p}}). Within site 1 the odds ratio was {{or_site1}}.")
        self.ref_code_lines += [
            f"df = df.assign(exposure=(df['{t['group_col']}'] == '{g1}').astype(int))",
            "tables = [pd.crosstab(df[df['site']==s]['exposure'], df[df['site']==s]['event']).reindex(index=[1,0], columns=[1,0]).fillna(0).values for s in sorted(df['site'].unique())]",
            "stt = sm.stats.StratifiedTable(tables); ci = stt.oddsratio_pooled_confint(alpha=0.05); test = stt.test_null_odds(correction=True)",
            "crude = pd.crosstab(df['exposure'], df['event']).reindex(index=[1,0], columns=[1,0]).fillna(0).values",
            "s1 = tables[0]",
            "out = {'n_total': len(df), 'n_exposed': int(df['exposure'].sum()), 'or_crude': float((crude[0,0]*crude[1,1])/(crude[0,1]*crude[1,0])), 'or_mh': float(stt.oddsratio_pooled), "
            "'or_mh_ci_low': float(ci[0]), 'or_mh_ci_high': float(ci[1]), 'mh_chi2': float(test.statistic), 'mh_p': float(test.pvalue), 'or_site1': float((s1[0,0]*s1[1,1])/(s1[0,1]*s1[1,0]))}",
        ]

    def render(self, redacted: bool) -> str:
        t = self.theme
        title = {
            "paired": f"Within-{t['unit'][:-1]} change in {t['outcome'].split(' (')[0]} between two assessments",
            "mannwhitney": f"Distribution-free comparison of {t['outcome'].split(' (')[0]} by group",
            "ols_interaction": f"Does age modify the effect of {t['exposure']} on {t['outcome'].split(' (')[0]}?",
            "cox": f"Time to the study event by {t['exposure']}: a survival analysis",
            "multi_bh": f"Biomarker correlates of {t['outcome'].split(' (')[0]} with false-discovery-rate control",
            "mh_stratified": f"Site-stratified association between {t['exposure']} and the study event",
        }[self.analysis]
        values = {c["id"]: self._fmt_claim(c) for c in self.claims}
        if redacted:
            results = " ".join(self.results_sentences).format(**{k: f"[{k}]" for k in values})
            results += ("\n\nNumeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; "
                        "each slot id appears where the value would be reported.\n\nClaim slots:\n" + "\n".join(f"- `{c['id']}`: {c['description']}" for c in self.claims))
        else:
            results = " ".join(self.results_sentences).format(**values)
        intro = (f"We report {t['setting']}. The primary question concerns {t['exposure']} and {t['outcome']}. The accompanying dataset (data.csv) contains one row per "
                 f"{t['unit'][:-1]}-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.")
        methods = "\n\n".join([
            f"**Participants and data.** The export contains {len(self.df)} records. Variables are listed in the data dictionary. Group membership is recorded in `{t['group_col']}`.",
            "**Data cleaning and exclusions.** " + self.methods_paragraphs[0],
            "**Statistical analysis.** " + self.methods_paragraphs[1] + " All analyses used the cleaned analysis sample; no random resampling was used.",
        ])
        abstract = (f"Background: {t['setting'].capitalize()}. Methods: {self.methods_paragraphs[1].split('. ')[0]}. Results: see the Results section. "
                    f"Conclusion: the findings are discussed in the context of the analysis sample.")
        discussion = "The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values."
        return "\n\n".join([f"# {title}", "## Abstract", abstract, "## Introduction", intro, "## Methods", methods, "## Results", results, "## Discussion", discussion]) + "\n"


HARD = ["paired", "mannwhitney", "ols_interaction", "cox", "multi_bh", "mh_stratified"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--start-index", type=int, default=1)
    ap.add_argument("--prefix", default=None)
    a = ap.parse_args()
    prefix = a.prefix or {"dev": "dev", "feedback": "fb", "heldout": "ho", "extra": "ex"}[a.split]
    manifest_path = ROOT / "tasks" / a.split / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    rng = random.Random(a.seed)
    order = HARD[:]
    rng.shuffle(order)
    for i in range(a.n):
        analysis = order[i % len(HARD)]
        seed = a.seed * 1000 + i
        task_id = f"{prefix}_{a.start_index + i:03d}_{analysis}"
        s = HardStudy(seed, task_id, analysis, difficulty=3)
        s.build()
        task_dir, truth_dir = s.write(a.split)
        out = subprocess.run(["python3", str(truth_dir / "reference_analysis.py")], cwd=task_dir, capture_output=True, text=True, timeout=180)
        assert out.returncode == 0, (task_id, out.stderr[-500:])
        got = json.loads(out.stdout.strip().splitlines()[-1])
        for c in s.claims:
            assert abs(got[c["id"]] - c["value"]) < 1e-6, (task_id, c["id"], got[c["id"]], c["value"])
        manifest.append({"task_id": task_id, "analysis": analysis, "difficulty": 3, "n_claims": len(s.claims), "wrinkles": s.wrinkles})
        print(f"{task_id}: claims={len(s.claims)} wrinkles={s.wrinkles}")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
