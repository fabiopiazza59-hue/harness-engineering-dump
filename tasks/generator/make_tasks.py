#!/usr/bin/env python3
"""Generate synthetic 'reproduce a published analysis' tasks.

Each task is a small study: a dataset, a paper describing the methods (with a results
section whose numbers are withheld from the harness), a list of claim slots, and a
ground truth computed by a reference analysis.

Usage:
    python tasks/generator/make_tasks.py --split dev --n 3 --seed 101
    python tasks/generator/make_tasks.py --split feedback --n 10 --seed 202
    python tasks/generator/make_tasks.py --split heldout --n 10 --seed 303

Harness-visible files go to tasks/<split>/<task_id>/.
Truth and full paper go to evalkit/truth/<split>/<task_id>/.
"""
from __future__ import annotations

import argparse
import json
import random
import shutil
import textwrap
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]

# --------------------------------------------------------------------------------------
# Tolerances per claim type (see docs/PROTOCOL.md section 2)
# --------------------------------------------------------------------------------------
TOL = {
    "count": {"abs": 0, "rel": 0},
    "mean": {"abs": 0.01, "rel": 0.01},
    "sd": {"abs": 0.01, "rel": 0.02},
    "diff": {"abs": 0.01, "rel": 0.02},
    "stat": {"abs": 0.01, "rel": 0.02},
    "pvalue": {"abs": 0.002, "rel": 0.05},
    "effect": {"abs": 0.005, "rel": 0.02},
    "coef": {"abs": 0.005, "rel": 0.02},
    "se": {"abs": 0.005, "rel": 0.03},
    "ratio": {"abs": 0.01, "rel": 0.02},
    "ci": {"abs": 0.01, "rel": 0.03},
    "r2": {"abs": 0.01, "rel": 0.02},
    "corr": {"abs": 0.01, "rel": 0.02},
    "prop": {"abs": 0.005, "rel": 0.02},
}

THEMES = [
    dict(field="clinical", unit="patients", outcome="systolic blood pressure (mmHg) at 12 weeks",
         outcome_col="sbp_12w", group_col="arm", groups=("control", "treatment"),
         exposure="assignment to the treatment arm", setting="a two-arm randomised trial of an antihypertensive regimen"),
    dict(field="education", unit="students", outcome="end-of-year mathematics score (0-100)",
         outcome_col="math_score", group_col="program", groups=("standard", "tutoring"),
         exposure="enrolment in the peer-tutoring program", setting="a cohort study of a peer-tutoring program in secondary schools"),
    dict(field="ecology", unit="plots", outcome="above-ground biomass (g/m^2)",
         outcome_col="biomass", group_col="treatment", groups=("unfertilised", "fertilised"),
         exposure="nitrogen fertilisation", setting="a field experiment on nitrogen fertilisation in grassland plots"),
    dict(field="psychology", unit="participants", outcome="reaction time (ms) on the Stroop task",
         outcome_col="rt_ms", group_col="condition", groups=("placebo", "caffeine"),
         exposure="caffeine administration", setting="a laboratory study of caffeine and attention"),
    dict(field="economics", unit="households", outcome="monthly savings (USD)",
         outcome_col="savings", group_col="program", groups=("waitlist", "coaching"),
         exposure="participation in the financial coaching program", setting="an evaluation of a household financial coaching program"),
    dict(field="nutrition", unit="participants", outcome="fasting glucose (mg/dL) at follow-up",
         outcome_col="glucose_fu", group_col="diet", groups=("usual", "mediterranean"),
         exposure="the Mediterranean diet intervention", setting="a dietary intervention study on fasting glucose"),
]

COVARIATES = [
    dict(col="age", label="age in years", kind="cont", gen=lambda rng, n: rng.normal(45, 12, n).round(0)),
    dict(col="sex", label="sex (0 = female, 1 = male)", kind="bin", gen=lambda rng, n: rng.integers(0, 2, n)),
    dict(col="bmi", label="body-mass index (kg/m^2)", kind="cont", gen=lambda rng, n: rng.normal(26, 4, n).round(1)),
    dict(col="baseline", label="baseline value of the outcome on the same scale", kind="cont", gen=None),
    dict(col="site", label="study site identifier (1-4)", kind="cat", gen=lambda rng, n: rng.integers(1, 5, n)),
]


def fmt(x, nd=2):
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    return f"{x:.{nd}f}"


def fmt_p(p):
    return "< 0.001" if p < 0.001 else f"= {p:.3f}"


class Study:
    """One synthetic study. Builds data, runs reference analysis, writes paper."""

    def __init__(self, seed: int, task_id: str, analysis: str, difficulty: int):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.pyrng = random.Random(seed)
        self.task_id = task_id
        self.analysis = analysis
        self.difficulty = difficulty
        self.theme = self.pyrng.choice(THEMES)
        self.claims: list[dict] = []
        self.results_sentences: list[str] = []  # with {id} placeholders
        self.methods_paragraphs: list[str] = []
        self.wrinkles: list[str] = []
        self.ref_code_lines: list[str] = []
        self.df: pd.DataFrame | None = None
        self.columns_doc: list[tuple[str, str]] = []

    # ---------------------------------------------------------------- data
    def make_data(self):
        t = self.theme
        n = int(self.rng.integers(180, 420))
        df = pd.DataFrame({"id": np.arange(1, n + 1)})
        for cov in COVARIATES[:4]:
            if cov["col"] == "baseline":
                continue
            df[cov["col"]] = cov["gen"](self.rng, n)
            self.columns_doc.append((cov["col"], cov["label"]))
        if self.difficulty >= 2:
            df["site"] = COVARIATES[4]["gen"](self.rng, n)
            self.columns_doc.append(("site", COVARIATES[4]["label"]))
        # group / exposure
        df[t["group_col"]] = self.rng.choice(list(t["groups"]), n)
        self.columns_doc.append((t["group_col"], f"study group: {t['groups'][0]} or {t['groups'][1]}"))
        # baseline and outcome with a real effect
        base_mu, base_sd = {
            "sbp_12w": (140, 12), "math_score": (62, 12), "biomass": (420, 90),
            "rt_ms": (720, 90), "savings": (310, 110), "glucose_fu": (104, 12),
        }[t["outcome_col"]]
        df["baseline"] = self.rng.normal(base_mu, base_sd, n).round(1)
        self.columns_doc.append(("baseline", COVARIATES[3]["label"]))
        eff = float(self.rng.uniform(0.25, 0.7)) * base_sd
        sign = -1 if t["outcome_col"] in ("sbp_12w", "rt_ms", "glucose_fu") else 1
        grp = (df[t["group_col"]] == t["groups"][1]).astype(float)
        noise = self.rng.normal(0, base_sd * 0.8, n)
        age_eff = float(self.rng.uniform(-0.6, 0.6)) * base_sd / 12
        df[t["outcome_col"]] = (
            0.55 * df["baseline"] + 0.45 * base_mu + sign * eff * grp
            + age_eff * (df["age"] - 45) + noise
        ).round(1)
        self.columns_doc.append((t["outcome_col"], t["outcome"]))
        # binary outcome for logistic / chi-square
        lin = -0.2 + sign * 0.9 * grp + 0.03 * (df["age"] - 45) + 0.5 * (df["bmi"] - 26) / 4
        pr = 1 / (1 + np.exp(-lin))
        df["event"] = (self.rng.uniform(size=n) < pr).astype(int)
        self.columns_doc.append(("event", "binary clinical or study event at follow-up (1 = yes)"))
        # missingness
        miss_rate = 0.03 + 0.03 * self.difficulty
        for col in ["bmi", t["outcome_col"]]:
            m = self.rng.uniform(size=n) < miss_rate
            df.loc[m, col] = np.nan
        # a few outliers in the outcome
        k = int(self.rng.integers(2, 5))
        idx = self.rng.choice(n, k, replace=False)
        df.loc[idx, t["outcome_col"]] = df[t["outcome_col"]].mean() + self.rng.choice([-1, 1], k) * base_sd * self.rng.uniform(4.5, 7, k)
        # a few under-age / over-age rows
        idx = self.rng.choice(n, int(self.rng.integers(4, 12)), replace=False)
        df.loc[idx, "age"] = self.rng.choice([15, 16, 17, 81, 84, 88], len(idx))
        self.df = df

    # --------------------------------------------------------- preprocessing
    def preprocess(self) -> pd.DataFrame:
        """Apply the exclusion and transformation rules; record them in methods text."""
        t = self.theme
        df = self.df.copy()
        code = ["import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm",
                "df = pd.read_csv('data.csv')"]
        rules = []
        lo, hi = 18, 80
        df = df[(df["age"] >= lo) & (df["age"] <= hi)]
        code.append(f"df = df[(df['age'] >= {lo}) & (df['age'] <= {hi})]")
        rules.append(f"Only {t['unit']} aged {lo} to {hi} years inclusive were included in the analysis.")
        ycol = t["outcome_col"]
        needed = [ycol]
        if self.analysis in ("ols", "logistic"):
            needed = needed + ["bmi"]
        df = df.dropna(subset=needed)
        code.append(f"df = df.dropna(subset={needed!r})")
        rules.append(f"{self.theme['unit'].capitalize()} with missing values for {', '.join(needed)} were excluded (complete-case analysis).")
        if self.difficulty >= 1 and self.analysis in ("ttest", "ols", "anova", "correlation"):
            mu, sd = df[ycol].mean(), df[ycol].std(ddof=1)
            keep = (df[ycol] - mu).abs() <= 3 * sd
            df = df[keep]
            code.append(f"mu, sd = df['{ycol}'].mean(), df['{ycol}'].std(ddof=1)")
            code.append(f"df = df[(df['{ycol}'] - mu).abs() <= 3 * sd]")
            rules.append(f"After the exclusions above, observations whose {t['outcome']} lay more than three sample standard deviations from the overall mean were treated as outliers and removed.")
            self.wrinkles.append("outlier_3sd")
        if self.difficulty >= 2 and self.analysis in ("ols", "correlation"):
            df = df.assign(log_outcome=np.log(df[ycol].clip(lower=1)))
            code.append(f"df = df.assign(log_outcome=np.log(df['{ycol}'].clip(lower=1)))")
            rules.append(f"Because the distribution of {t['outcome']} was right-skewed, it was natural-log transformed before modelling (values below 1 were set to 1 before transformation).")
            self.wrinkles.append("log_outcome")
        self.methods_paragraphs.append(" ".join(rules))
        self.ref_code_lines = code
        return df

    # ------------------------------------------------------------ analyses
    def add_claim(self, cid, desc, value, ctype):
        self.claims.append({"id": cid, "description": desc, "type": ctype,
                            "value": float(value) if ctype != "count" else int(value)})

    def run_ttest(self, df):
        t = self.theme
        g0, g1 = t["groups"]
        ycol = t["outcome_col"]
        welch = self.pyrng.random() < 0.5
        a = df.loc[df[t["group_col"]] == g0, ycol]
        b = df.loc[df[t["group_col"]] == g1, ycol]
        res = st.ttest_ind(b, a, equal_var=not welch)
        sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
        d = (b.mean() - a.mean()) / sp
        self.methods_paragraphs.append(
            f"The primary analysis compared the mean {t['outcome']} between the {g1} and {g0} groups using "
            f"{'an unpaired Welch t-test (unequal variances)' if welch else 'an unpaired Student t-test assuming equal variances'}, two-sided. "
            f"Group means and sample standard deviations (n - 1 denominator) are reported. The mean difference is reported as {g1} minus {g0}. "
            f"Cohen's d was computed as the mean difference divided by the pooled standard deviation.")
        self.add_claim("n_" + g0, f"Number of {t['unit']} in the {g0} group included in the primary analysis", len(a), "count")
        self.add_claim("n_" + g1, f"Number of {t['unit']} in the {g1} group included in the primary analysis", len(b), "count")
        self.add_claim("mean_" + g0, f"Mean {t['outcome']} in the {g0} group", a.mean(), "mean")
        self.add_claim("mean_" + g1, f"Mean {t['outcome']} in the {g1} group", b.mean(), "mean")
        self.add_claim("sd_" + g1, f"Sample standard deviation of {t['outcome']} in the {g1} group", b.std(ddof=1), "sd")
        self.add_claim("mean_diff", f"Mean difference in {t['outcome']} ({g1} minus {g0})", b.mean() - a.mean(), "diff")
        self.add_claim("t_stat", "t statistic of the primary between-group test", res.statistic, "stat")
        self.add_claim("p_value", "Two-sided p-value of the primary between-group test", res.pvalue, "pvalue")
        self.add_claim("cohens_d", "Cohen's d (pooled SD) for the between-group difference", d, "effect")
        self.results_sentences.append(
            f"The primary analysis included {{n_{g0}}} {t['unit']} in the {g0} group and {{n_{g1}}} in the {g1} group. "
            f"Mean {t['outcome']} was {{mean_{g0}}} in the {g0} group and {{mean_{g1}}} (SD {{sd_{g1}}}) in the {g1} group, "
            f"a difference of {{mean_diff}} (t = {{t_stat}}, p {{p_value}}; Cohen's d = {{cohens_d}}).")
        self.ref_code_lines += [
            f"a = df.loc[df['{t['group_col']}'] == '{g0}', '{ycol}']",
            f"b = df.loc[df['{t['group_col']}'] == '{g1}', '{ycol}']",
            f"res = st.ttest_ind(b, a, equal_var={not welch})",
            "sp = np.sqrt(((len(a)-1)*a.var(ddof=1) + (len(b)-1)*b.var(ddof=1)) / (len(a)+len(b)-2))",
            "out = {" + f"'n_{g0}': len(a), 'n_{g1}': len(b), 'mean_{g0}': a.mean(), 'mean_{g1}': b.mean(), 'sd_{g1}': b.std(ddof=1),"
            " 'mean_diff': b.mean()-a.mean(), 't_stat': res.statistic, 'p_value': res.pvalue, 'cohens_d': (b.mean()-a.mean())/sp}",
        ]

    def run_ols(self, df):
        t = self.theme
        g0, g1 = t["groups"]
        ycol = "log_outcome" if "log_outcome" in df.columns else t["outcome_col"]
        covs = ["age", "bmi", "baseline"]
        standardize = self.difficulty >= 2 and self.pyrng.random() < 0.6
        X = pd.DataFrame({"exposure": (df[t["group_col"]] == g1).astype(float)})
        for c in covs:
            X[c] = (df[c] - df[c].mean()) / df[c].std(ddof=1) if standardize else df[c]
        X = sm.add_constant(X)
        model = sm.OLS(df[ycol], X).fit()
        self.methods_paragraphs.append(
            f"The association between {t['exposure']} and {'the log-transformed ' if ycol == 'log_outcome' else ''}{t['outcome']} was estimated with an ordinary least squares linear regression "
            f"adjusted for age, body-mass index and the baseline value. The exposure was coded 1 for {g1} and 0 for {g0}. "
            + ("Continuous covariates were standardised (mean 0, sample SD 1) before entering the model. " if standardize else "Covariates were entered on their original scale. ")
            + "Conventional (non-robust) standard errors are reported.")
        if standardize:
            self.wrinkles.append("standardized_covariates")
        self.add_claim("n_model", f"Number of {t['unit']} included in the regression model", int(model.nobs), "count")
        self.add_claim("coef_exposure", f"Adjusted regression coefficient for {t['exposure']}", model.params["exposure"], "coef")
        self.add_claim("se_exposure", "Standard error of the exposure coefficient", model.bse["exposure"], "se")
        self.add_claim("p_exposure", "Two-sided p-value for the exposure coefficient", model.pvalues["exposure"], "pvalue")
        self.add_claim("coef_age", "Adjusted regression coefficient for age (as entered in the model)", model.params["age"], "coef")
        self.add_claim("r_squared", "R squared of the model", model.rsquared, "r2")
        self.add_claim("adj_r_squared", "Adjusted R squared of the model", model.rsquared_adj, "r2")
        self.results_sentences.append(
            f"The adjusted model included {{n_model}} {t['unit']}. {t['exposure'].capitalize()} was associated with a change of {{coef_exposure}} "
            f"(SE {{se_exposure}}, p {{p_exposure}}) in {'log ' if ycol == 'log_outcome' else ''}{t['outcome']}; the coefficient for age was {{coef_age}}. "
            f"The model explained R^2 = {{r_squared}} (adjusted R^2 = {{adj_r_squared}}) of the variance.")
        self.ref_code_lines += [
            f"X = pd.DataFrame({{'exposure': (df['{t['group_col']}'] == '{g1}').astype(float)}})",
            f"for c in {covs!r}:",
            "    X[c] = (df[c]-df[c].mean())/df[c].std(ddof=1)" if standardize else "    X[c] = df[c]",
            "X = sm.add_constant(X)",
            f"m = sm.OLS(df['{ycol}'], X).fit()",
            "out = {'n_model': int(m.nobs), 'coef_exposure': m.params['exposure'], 'se_exposure': m.bse['exposure'], 'p_exposure': m.pvalues['exposure'],"
            " 'coef_age': m.params['age'], 'r_squared': m.rsquared, 'adj_r_squared': m.rsquared_adj}",
        ]

    def run_correlation(self, df):
        t = self.theme
        ycol = "log_outcome" if "log_outcome" in df.columns else t["outcome_col"]
        spearman = self.pyrng.random() < 0.4
        x = df["baseline"]
        y = df[ycol]
        r, p = (st.spearmanr(x, y) if spearman else st.pearsonr(x, y))
        g1 = t["groups"][1]
        sub = df[df[t["group_col"]] == g1]
        r_sub, p_sub = (st.spearmanr(sub["baseline"], sub[ycol]) if spearman else st.pearsonr(sub["baseline"], sub[ycol]))
        name = "Spearman rank correlation" if spearman else "Pearson product-moment correlation"
        self.methods_paragraphs.append(
            f"The relationship between the baseline value and {'the log-transformed ' if ycol == 'log_outcome' else ''}{t['outcome']} was quantified with the {name} coefficient, "
            f"first in the full analysis sample and then within the {g1} group only. Two-sided p-values are reported.")
        self.add_claim("n_all", f"Number of {t['unit']} in the full correlation analysis", len(df), "count")
        self.add_claim("r_all", f"{name} coefficient in the full sample", r, "corr")
        self.add_claim("p_all", "Two-sided p-value of the full-sample correlation", p, "pvalue")
        self.add_claim("n_" + g1, f"Number of {t['unit']} in the {g1} group correlation analysis", len(sub), "count")
        self.add_claim("r_" + g1, f"{name} coefficient within the {g1} group", r_sub, "corr")
        self.results_sentences.append(
            f"Across all {{n_all}} {t['unit']}, the baseline value correlated with the outcome (r = {{r_all}}, p {{p_all}}). "
            f"Within the {g1} group (n = {{n_{g1}}}) the correlation was r = {{r_{g1}}}.")
        fn = "st.spearmanr" if spearman else "st.pearsonr"
        self.ref_code_lines += [
            f"r, p = {fn}(df['baseline'], df['{ycol}'])",
            f"sub = df[df['{t['group_col']}'] == '{g1}']",
            f"r2, p2 = {fn}(sub['baseline'], sub['{ycol}'])",
            f"out = {{'n_all': len(df), 'r_all': r, 'p_all': p, 'n_{g1}': len(sub), 'r_{g1}': r2}}",
        ]

    def run_logistic(self, df):
        t = self.theme
        g0, g1 = t["groups"]
        X = pd.DataFrame({"exposure": (df[t["group_col"]] == g1).astype(float), "age": df["age"], "bmi": df["bmi"]})
        X = sm.add_constant(X)
        model = sm.Logit(df["event"], X).fit(disp=0)
        ci = model.conf_int().loc["exposure"]
        self.methods_paragraphs.append(
            f"The odds of the study event were modelled with a maximum-likelihood logistic regression (no penalisation) with {t['exposure']} "
            f"(coded 1 for {g1}, 0 for {g0}), age and body-mass index as predictors. Odds ratios with Wald 95% confidence intervals are reported.")
        self.add_claim("n_model", f"Number of {t['unit']} in the logistic model", int(model.nobs), "count")
        self.add_claim("n_events", "Number of study events among modelled participants", int(df["event"].sum()), "count")
        self.add_claim("or_exposure", f"Adjusted odds ratio for {t['exposure']}", float(np.exp(model.params["exposure"])), "ratio")
        self.add_claim("or_ci_low", "Lower bound of the 95% CI of the exposure odds ratio", float(np.exp(ci[0])), "ci")
        self.add_claim("or_ci_high", "Upper bound of the 95% CI of the exposure odds ratio", float(np.exp(ci[1])), "ci")
        self.add_claim("p_exposure", "Two-sided p-value for the exposure term", model.pvalues["exposure"], "pvalue")
        self.add_claim("or_age", "Adjusted odds ratio per one-year increase in age", float(np.exp(model.params["age"])), "ratio")
        self.results_sentences.append(
            f"Among {{n_model}} {t['unit']} there were {{n_events}} events. {t['exposure'].capitalize()} was associated with an adjusted odds ratio of {{or_exposure}} "
            f"(95% CI {{or_ci_low}} to {{or_ci_high}}, p {{p_exposure}}); the odds ratio per year of age was {{or_age}}.")
        self.ref_code_lines += [
            f"X = sm.add_constant(pd.DataFrame({{'exposure': (df['{t['group_col']}'] == '{g1}').astype(float), 'age': df['age'], 'bmi': df['bmi']}}))",
            "m = sm.Logit(df['event'], X).fit(disp=0)",
            "ci = m.conf_int().loc['exposure']",
            "out = {'n_model': int(m.nobs), 'n_events': int(df['event'].sum()), 'or_exposure': float(np.exp(m.params['exposure'])),"
            " 'or_ci_low': float(np.exp(ci[0])), 'or_ci_high': float(np.exp(ci[1])), 'p_exposure': m.pvalues['exposure'], 'or_age': float(np.exp(m.params['age']))}",
        ]

    def run_anova(self, df):
        t = self.theme
        ycol = t["outcome_col"]
        # three groups: tertiles of baseline (a realistic derived grouping)
        q = df["baseline"].quantile([1 / 3, 2 / 3]).values
        df = df.assign(tertile=np.where(df["baseline"] <= q[0], "low", np.where(df["baseline"] <= q[1], "middle", "high")))
        groups = [df.loc[df["tertile"] == k, ycol] for k in ("low", "middle", "high")]
        f, p = st.f_oneway(*groups)
        grand = df[ycol].mean()
        ss_between = sum(len(g) * (g.mean() - grand) ** 2 for g in groups)
        ss_total = ((df[ycol] - grand) ** 2).sum()
        eta = ss_between / ss_total
        self.methods_paragraphs.append(
            f"{t['unit'].capitalize()} were divided into three groups (low, middle, high) by tertiles of the baseline value, using the first and second tertile "
            f"cut-points of the analysis sample (values equal to a cut-point were assigned to the lower group). Mean {t['outcome']} was compared across the three groups "
            f"with a one-way analysis of variance; eta squared was computed as the between-group sum of squares divided by the total sum of squares.")
        self.wrinkles.append("derived_tertiles")
        for k, g in zip(("low", "middle", "high"), groups):
            self.add_claim(f"n_{k}", f"Number of {t['unit']} in the {k} baseline tertile group", len(g), "count")
            self.add_claim(f"mean_{k}", f"Mean {t['outcome']} in the {k} tertile group", g.mean(), "mean")
        self.add_claim("f_stat", "F statistic of the one-way ANOVA", f, "stat")
        self.add_claim("p_value", "p-value of the one-way ANOVA", p, "pvalue")
        self.add_claim("eta_squared", "Eta squared of the group factor", eta, "effect")
        self.results_sentences.append(
            f"The low, middle and high tertile groups comprised {{n_low}}, {{n_middle}} and {{n_high}} {t['unit']}, with mean {t['outcome']} of {{mean_low}}, {{mean_middle}} and {{mean_high}} respectively "
            f"(F = {{f_stat}}, p {{p_value}}, eta^2 = {{eta_squared}}).")
        self.ref_code_lines += [
            "q = df['baseline'].quantile([1/3, 2/3]).values",
            "df = df.assign(tertile=np.where(df['baseline'] <= q[0], 'low', np.where(df['baseline'] <= q[1], 'middle', 'high')))",
            f"groups = [df.loc[df['tertile'] == k, '{ycol}'] for k in ('low', 'middle', 'high')]",
            "f, p = st.f_oneway(*groups)",
            f"grand = df['{ycol}'].mean()",
            "ssb = sum(len(g)*(g.mean()-grand)**2 for g in groups)",
            f"sst = ((df['{ycol}']-grand)**2).sum()",
            "out = {'n_low': len(groups[0]), 'n_middle': len(groups[1]), 'n_high': len(groups[2]), 'mean_low': groups[0].mean(), 'mean_middle': groups[1].mean(),"
            " 'mean_high': groups[2].mean(), 'f_stat': f, 'p_value': p, 'eta_squared': ssb/sst}",
        ]

    def run_chisq(self, df):
        t = self.theme
        g0, g1 = t["groups"]
        tab = pd.crosstab(df[t["group_col"]], df["event"]).reindex(index=[g0, g1], columns=[0, 1]).fillna(0)
        chi2, p, dof, _ = st.chi2_contingency(tab.values, correction=False)
        p0 = tab.loc[g0, 1] / tab.loc[g0].sum()
        p1 = tab.loc[g1, 1] / tab.loc[g1].sum()
        rr = p1 / p0
        self.methods_paragraphs.append(
            f"The proportion of {t['unit']} with the study event was compared between the {g1} and {g0} groups with a Pearson chi-square test of independence "
            f"without continuity correction. The risk ratio is reported as the event proportion in the {g1} group divided by that in the {g0} group.")
        self.add_claim("n_" + g0, f"Number of {t['unit']} in the {g0} group", int(tab.loc[g0].sum()), "count")
        self.add_claim("n_" + g1, f"Number of {t['unit']} in the {g1} group", int(tab.loc[g1].sum()), "count")
        self.add_claim("events_" + g1, f"Number of events in the {g1} group", int(tab.loc[g1, 1]), "count")
        self.add_claim("prop_" + g0, f"Proportion with the event in the {g0} group", p0, "prop")
        self.add_claim("prop_" + g1, f"Proportion with the event in the {g1} group", p1, "prop")
        self.add_claim("risk_ratio", f"Risk ratio ({g1} over {g0})", rr, "ratio")
        self.add_claim("chi2_stat", "Pearson chi-square statistic (no continuity correction)", chi2, "stat")
        self.add_claim("p_value", "p-value of the chi-square test", p, "pvalue")
        self.results_sentences.append(
            f"Of {{n_{g1}}} {t['unit']} in the {g1} group, {{events_{g1}}} experienced the event (proportion {{prop_{g1}}}) compared with a proportion of {{prop_{g0}}} among the {{n_{g0}}} in the {g0} group "
            f"(risk ratio {{risk_ratio}}; chi-square = {{chi2_stat}}, p {{p_value}}).")
        self.ref_code_lines += [
            f"tab = pd.crosstab(df['{t['group_col']}'], df['event']).reindex(index=['{g0}', '{g1}'], columns=[0, 1]).fillna(0)",
            "chi2, p, dof, _ = st.chi2_contingency(tab.values, correction=False)",
            f"p0 = tab.loc['{g0}', 1] / tab.loc['{g0}'].sum(); p1 = tab.loc['{g1}', 1] / tab.loc['{g1}'].sum()",
            f"out = {{'n_{g0}': int(tab.loc['{g0}'].sum()), 'n_{g1}': int(tab.loc['{g1}'].sum()), 'events_{g1}': int(tab.loc['{g1}', 1]), 'prop_{g0}': p0, 'prop_{g1}': p1,"
            " 'risk_ratio': p1/p0, 'chi2_stat': chi2, 'p_value': p}",
        ]

    # --------------------------------------------------------------- paper
    def render(self, redacted: bool) -> str:
        t = self.theme
        title = {
            "ttest": f"Effect of {t['exposure']} on {t['outcome'].split(' (')[0]}: {t['setting'].split(' of ')[0]}",
            "ols": f"Adjusted association between {t['exposure']} and {t['outcome'].split(' (')[0]}",
            "correlation": f"Baseline values predict {t['outcome'].split(' (')[0]}: a correlational analysis",
            "logistic": f"Predictors of the study event in {t['setting']}",
            "anova": f"{t['outcome'].split(' (')[0].capitalize()} across baseline tertiles",
            "chisq": f"Event rates by group in {t['setting']}",
        }[self.analysis]
        values = {c["id"]: self._fmt_claim(c) for c in self.claims}
        if redacted:
            values = {k: "[value withheld]" for k in values}
            results = " ".join(self.results_sentences).format(**values)
            results_note = ("\n\nNumeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; "
                            "each slot id appears where the value would be reported.")
            slots = "\n".join(f"- `{c['id']}`: {c['description']}" for c in self.claims)
            results = " ".join(self.results_sentences).format(**{k: f"[{k}]" for k in values}) + results_note + "\n\nClaim slots:\n" + slots
        else:
            results = " ".join(self.results_sentences).format(**values)
        intro = (f"We report {t['setting']}. The primary question was whether {t['exposure']} is associated with {t['outcome']}. "
                 f"The dataset accompanying this report (data.csv) contains one row per {t['unit'][:-1]} and is described in the data dictionary.")
        methods = "\n\n".join([
            f"**Participants and data.** Data were collected for {len(self.df)} {t['unit']}. Each record contains the variables listed in the data dictionary. "
            f"Group membership is recorded in the column `{t['group_col']}`.",
            "**Exclusion criteria and preprocessing.** " + self.methods_paragraphs[0],
            "**Statistical analysis.** " + self.methods_paragraphs[1] + " All analyses were performed on the analysis sample defined above. "
            "Statistics were computed with standard scientific software; no random resampling was used.",
        ])
        abstract = (f"Background: {t['setting'].capitalize()}. Methods: {self.methods_paragraphs[1].split('.')[0]}. "
                    f"Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.")
        discussion = ("The analysis followed the pre-specified plan described in the Methods. Limitations include the observational "
                      "nature of some comparisons and the exclusion of records with missing values.")
        return "\n\n".join([f"# {title}", "## Abstract", abstract, "## Introduction", intro, "## Methods", methods,
                            "## Results", results, "## Discussion", discussion]) + "\n"

    def _fmt_claim(self, c):
        v = c["value"]
        if c["type"] == "count":
            return str(int(v))
        if c["type"] == "pvalue":
            return fmt_p(v)
        if c["type"] in ("prop", "corr", "r2", "effect"):
            return f"{v:.3f}"
        return f"{v:.2f}"

    # ------------------------------------------------------------------ io
    def write(self, split: str):
        task_dir = ROOT / "tasks" / split / self.task_id
        truth_dir = ROOT / "evalkit" / "truth" / split / self.task_id
        for d in (task_dir, truth_dir):
            if d.exists():
                shutil.rmtree(d)
            d.mkdir(parents=True)
        self.df.to_csv(task_dir / "data.csv", index=False)
        dictionary = "# Data dictionary for data.csv\n\n" + "\n".join(f"- `{c}`: {d}" for c, d in [("id", "record identifier")] + self.columns_doc)
        (task_dir / "data_dictionary.md").write_text(dictionary + "\n")
        (task_dir / "paper_methods.md").write_text(self.render(redacted=True))
        full_md = self.render(redacted=False)
        (truth_dir / "paper_full.md").write_text(full_md)
        write_pdf(full_md, truth_dir / "paper.pdf")
        task = {
            "task_id": self.task_id,
            "family": "reproduce_analysis",
            "title": full_md.splitlines()[0].lstrip("# "),
            "instructions": (
                "Reproduce the analysis described in paper_methods.md using data.csv. Follow the Methods section exactly "
                "(exclusions, transformations, test choice, coding of variables). Produce a numeric value for every claim slot "
                "listed under 'claims'. Write claims.json with {\"claims\": [{\"id\": ..., \"value\": <number>}, ...]} and analysis.py, "
                "a standalone script that, when run from the task directory, recomputes the claims from data.csv and prints them as a "
                "single JSON object {\"<id>\": <number>, ...} on stdout."
            ),
            "paper_view": "paper_methods.md",
            "data_files": ["data.csv"],
            "data_dictionary": "data_dictionary.md",
            "claims": [{"id": c["id"], "description": c["description"], "type": c["type"]} for c in self.claims],
            "output": {"claims_file": "claims.json", "analysis_script": "analysis.py"},
        }
        (task_dir / "task.json").write_text(json.dumps(task, indent=2) + "\n")
        truth = {
            "task_id": self.task_id, "analysis": self.analysis, "difficulty": self.difficulty,
            "wrinkles": self.wrinkles, "seed": self.seed, "theme": self.theme["field"],
            "claims": [{"id": c["id"], "value": c["value"], "type": c["type"], "tolerance": TOL[c["type"]]} for c in self.claims],
        }
        (truth_dir / "truth.json").write_text(json.dumps(truth, indent=2) + "\n")
        ref = "\n".join(self.ref_code_lines) + "\nprint(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))\n"
        (truth_dir / "reference_analysis.py").write_text(ref)
        return task_dir, truth_dir

    def build(self):
        self.make_data()
        df = self.preprocess()
        getattr(self, "run_" + self.analysis)(df)


def write_pdf(markdown: str, path: Path):
    """Render simple markdown to a paginated PDF with PyMuPDF's Story."""
    import html
    import pymupdf
    parts = []
    for block in markdown.split("\n\n"):
        b = block.strip()
        if not b:
            continue
        if b.startswith("# "):
            parts.append(f"<h1>{html.escape(b[2:])}</h1>")
        elif b.startswith("## "):
            parts.append(f"<h2>{html.escape(b[3:])}</h2>")
        else:
            txt = html.escape(b).replace("**", "")
            parts.append(f"<p>{txt}</p>")
    body = "".join(parts)
    story = pymupdf.Story(html=f"<body style='font-family: serif; font-size: 10pt'>{body}</body>")
    writer = pymupdf.DocumentWriter(str(path))
    mediabox = pymupdf.paper_rect("a4")
    where = mediabox + (50, 50, -50, -60)
    more = True
    while more:
        dev = writer.begin_page(mediabox)
        more, _ = story.place(where)
        story.draw(dev)
        writer.end_page()
    writer.close()


ANALYSES = ["ttest", "ols", "correlation", "logistic", "anova", "chisq"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", required=True, choices=["dev", "feedback", "heldout", "extra"])
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--prefix", default=None)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    prefix = args.prefix or {"dev": "dev", "feedback": "fb", "heldout": "ho", "extra": "ex"}[args.split]
    manifest = []
    shuffled = ANALYSES[:]
    rng.shuffle(shuffled)
    for i in range(args.n):
        analysis = ANALYSES[i % len(ANALYSES)] if args.n >= len(ANALYSES) else shuffled[i % len(ANALYSES)]
        difficulty = rng.choice([0, 1, 1, 2, 2])
        seed = args.seed * 1000 + i
        task_id = f"{prefix}_{i + 1:03d}_{analysis}"
        s = Study(seed, task_id, analysis, difficulty)
        s.build()
        task_dir, truth_dir = s.write(args.split)
        # self-check: reference script reproduces truth
        import subprocess
        out = subprocess.run(["python3", str(truth_dir / "reference_analysis.py")], cwd=task_dir, capture_output=True, text=True, timeout=120)
        got = json.loads(out.stdout.strip().splitlines()[-1])
        for c in s.claims:
            assert abs(got[c["id"]] - c["value"]) < 1e-6, (task_id, c["id"], got[c["id"]], c["value"])
        manifest.append({"task_id": task_id, "analysis": analysis, "difficulty": difficulty, "n_claims": len(s.claims), "wrinkles": s.wrinkles})
        print(f"{task_id}: difficulty={difficulty} claims={len(s.claims)} wrinkles={s.wrinkles}")
    (ROOT / "tasks" / args.split / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
