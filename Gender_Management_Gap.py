"""
================================================================================
 Reinterpreting Women's Leadership Metrics:
 Are We Correctly Measuring the 'Female Share of Management'?
 The Two Faces of Women's Managerial Representation in Manufacturing
 Sean (Yechan) Kim  |  Georgia Tech OMSA
--------------------------------------------------------------------------------
 Reproduces results_log.txt (Panels A-L) from the two shipped datasets. Figures are built
 separately by make_figures.py. No raw federal files, no network access.

     python Gender_Management_Gap.py

 Requires : pandas, numpy, scipy, statsmodels
 Runtime  : ~4 minutes (randomization, bootstrap and the AR grid dominate)

 ESTIMAND. The unweighted specification answers: in the average local
 industry cell, how does women's relative managerial representation vary with
 women's share of that cell's workforce? It is NOT a worker-level national
 relationship. Weighted alternatives, which answer different questions, are
 reported in Panel D and differ in magnitude by a factor of about three.
================================================================================
"""
import zipfile, warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats
warnings.filterwarnings("ignore")

CROSS_SECTION, PANEL = "gender_mgmt_cbsa_2023.csv", "gender_mgmt_panel_2015_2021.csv"
ACS_CELLS = "acs_mfg_cells_2022_2024.csv"   # IPUMS USA ACS, aggregated to metro x industry x year
TAU      = 3      # EEOC suppression threshold, recovered empirically
REPS_RND = 200    # fixed-margin randomization replications
REPS_WCB = 499    # wild cluster bootstrap replications
LOG, rng = [], np.random.default_rng(11)


def load(name):
    try:
        return pd.read_csv(name, dtype={"naics3": str, "cbsa_code": str})
    except FileNotFoundError:
        with zipfile.ZipFile(name + ".zip") as z, z.open(name) as fh:
            return pd.read_csv(fh, dtype={"naics3": str, "cbsa_code": str})


def P(m=""):
    LOG.append(m); print(m)


def absorb(df, cols, w=None, fes=("naics3", "region"), it=40):
    """Alternating-projections demeaning; w gives weighted group means."""
    X = df[cols].astype(float).copy()
    ww = np.ones(len(df)) if w is None else df[w].astype(float).values
    for _ in range(it):
        for fe in fes:
            num = pd.DataFrame(X.values * ww[:, None], index=df.index).groupby(
                df[fe].values).transform("sum").values
            den = pd.Series(ww, index=df.index).groupby(df[fe].values).transform("sum").values
            X = X - pd.DataFrame(num / den[:, None], index=X.index, columns=X.columns)
    return X


def fit(df, rhs, outcome, label="", w=None, fe=("naics3", "region"), quiet=False):
    Z = absorb(df, [outcome] + list(rhs), w=w, fes=fe).dropna()
    Z = Z[np.isfinite(Z).all(axis=1)]
    X, y = sm.add_constant(Z[list(rhs)]), Z[outcome]
    ww = df.loc[Z.index, w].astype(float) if w else None
    m = (sm.WLS(y, X, weights=ww) if w else sm.OLS(y, X)).fit(
        cov_type="cluster", cov_kwds={"groups": df.loc[Z.index, "cbsa_code"]})
    if not quiet:
        P(f"\n{label}\n  outcome={outcome}  n={int(m.nobs):,}  "
          f"clusters={df.loc[Z.index,'cbsa_code'].nunique():,}  R2(within)={m.rsquared:.4f}")
        for v in rhs:
            b, se, p = m.params[v], m.bse[v], m.pvalues[v]
            star = "***" if p < .01 else "**" if p < .05 else "*" if p < .1 else ""
            P(f"    {v:<16} {b:>+10.4f}  se {se:.4f}  t {b/se:>+7.2f}  p {p:.4g} {star}")
    return m


def resample_p(k, n):
    """A resampling p-value cannot be smaller than 1/n; report the count."""
    return (f"{k} of {n} draws as extreme (p < {1/n:.3f})" if k == 0
            else f"{k} of {n} draws as extreme (p = {k/n:.3f})")


def log_odds(mid_f, df, c=0.0):
    f1, f0 = mid_f + c, df.emp_f - mid_f + c
    m1 = (df.mid_tot - mid_f) + c
    m0 = (df.emp - df.emp_f) - (df.mid_tot - mid_f) + c
    return np.log((f1 / f0) / (m1 / m0))


# ------------------------------------------------------------------- inputs
full = load(CROSS_SECTION)
full["region"] = full.region.fillna("MultiState")
a   = full[full.in_sample == 1].copy()
bnd = full[full.bounded == 1].copy()
r1  = load(PANEL); r1["region"] = r1.region.fillna("MultiState"); r1["yr"] = r1.year.astype(str)

a["y"] = log_odds(a.mid_f, a)                       # no continuity correction: no zero cells
a["rate_f"] = np.log(a.mid_f / a.emp_f)
a["rate_m"] = np.log((a.mid_tot - a.mid_f) / (a.emp - a.emp_f))
a["mgmt_int"] = np.log(a.mid_tot / a.emp)
a["prec"] = 1 / (1/a.mid_f + 1/(a.emp_f - a.mid_f)
                 + 1/(a.mid_tot - a.mid_f) + 1/((a.emp - a.emp_f) - (a.mid_tot - a.mid_f)))
a = a[np.isfinite(a.y) & np.isfinite(a.prec)].copy()
r1["y"] = log_odds(r1.mid_f, r1); r1 = r1[np.isfinite(r1.y)]

P("=" * 80)
P("REINTERPRETING WOMEN'S LEADERSHIP METRICS")
P("Absolute share vs relative odds of women's managerial representation, U.S. manufacturing")
P("EEO-1 2022-2023 main cross-section; 2015-2021 comparison under a different filing regime")
P("Cross-sectional ecological association. No causal interpretation is warranted.")
P("=" * 80)
P(f"\n[ESTIMAND] unweighted = the average CBSA x NAICS-3 cell (see Panel D)")
P(f"[SAMPLE]   {len(a):,} cells, {a.cbsa_code.nunique():,} CBSAs, {a.naics3.nunique()} subsectors")
P(f"[BOUNDED]  {len(bnd):,} cells suppressed, counts known to lie in [0,{TAU-1}]")
P(f"[OUTCOME]  ln_theta, no continuity correction; zero-female-manager cells: {(a.mid_f==0).sum()}")
P(f"           mean {a.y.mean():+.3f}  sd {a.y.std():.3f}  below parity {(a.y<0).mean()*100:.1f}%")

RHS = ["fem_share", "ln_emp", "ln_estab_size"]

P("\n" + "-"*80); P("PANEL A  RELATIVE REPRESENTATION ODDS"); P("-"*80)
fit(a, RHS, "y", "A1  main specification, unweighted")
fit(a, ["fem_share_eeo1", "ln_emp", "ln_estab_size"], "y", "A2  female share measured from EEO-1")

P("\n" + "-"*80); P("PANEL B  ABSOLUTE SHARE  (the divergence)"); P("-"*80)
fit(a, RHS, "mid_fem_share", "B1  women's share OF management")
fit(r1, ["fem_share_eeo1", "ln_emp", "ln_estab_size"], "mid_fem_share",
    "B2  regime 1, same specification", fe=("naics3", "region", "yr"))

P("\n" + "-"*80); P("PANEL C  DECOMPOSITION  (what actually moves)"); P("-"*80)
bf = fit(a, RHS, "rate_f", "C1  log female management rate  (F mgr / F employed)").params.fem_share
bm = fit(a, RHS, "rate_m", "C2  log male   management rate  (M mgr / M employed)").params.fem_share
fit(a, RHS, "mgmt_int", "C3  log overall management intensity  (all mgr / all employed)")
P(f"\n  female rate {bf:+.4f} minus male rate {bm:+.4f} = {bf-bm:+.4f}, "
  f"against the direct odds estimate {fit(a,RHS,'y',quiet=True).params.fem_share:+.4f}")
P("  The managerial layer does not thin. Positions are reallocated, not removed.")

P("\n" + "-"*80); P("PANEL D  ESTIMAND AND SCALE  (different questions, not robustness)"); P("-"*80)
for w, lbl in [(None, "unweighted: the average local industry cell"),
               ("emp", "employment-weighted: the average worker"),
               ("emp_f", "female-employment-weighted: the average woman"),
               ("mid_tot", "manager-weighted: the average managerial position"),
               ("prec", "inverse-variance weighted: precision")]:
    m = fit(a, RHS, "y", w=w, quiet=True)
    P(f"  {lbl:<48} b={m.params.fem_share:+8.4f} se={m.bse.fem_share:.4f}")
P("")
for k in [10, 20, 50, 100, 200]:
    m = fit(a[a.mid_tot >= k], RHS, "y", quiet=True)
    P(f"  minimum mid-management headcount >= {k:<13} b={m.params.fem_share:+8.4f} "
      f"se={m.bse.fem_share:.4f}  n={int(m.nobs):,}")
P("  Sign is stable; magnitude spans roughly -0.4 to -1.2. Headline claims are")
P("  about direction and shape, not about effect size.")

P("\n" + "-"*80); P("PANEL E  FIXED-MARGIN RANDOMIZATION"); P("-"*80)
N = a.emp.round().astype(int).values; K = a.mid_tot.round().astype(int).values
n = a.emp_f.round().astype(int).values
ok = (N > 0) & (K > 0) & (K < N) & (n > 0) & (n < N)
s, Ns, Ks, ns = a[ok].copy(), N[ok], K[ok], n[ok]
obs = fit(s, RHS, "y", quiet=True).params.fem_share


def randomize(psi, reps):
    out = []
    for _ in range(reps):
        fm = (rng.hypergeometric(ns, Ns - ns, Ks) if psi == 1
              else stats.nchypergeom_fisher.rvs(Ns, ns, Ks, psi, random_state=rng))
        d = s.copy()
        d["ysim"] = np.log(((fm + .5) / (ns - fm + .5))
                           / (((Ks - fm) + .5) / ((Ns - ns) - (Ks - fm) + .5)))
        out.append(fit(d, RHS, "ysim", quiet=True).params.fem_share)
    return np.array(out)

P("  All four cell margins are held fixed; only the sex-management association is")
P("  removed. EEO-1 cells are administrative enumerations, not samples, so this")
P("  randomization -- not a binomial sampling model -- is the correct null.")
psi = float(np.exp(s.y.mean()))
for lbl, v in [("central hypergeometric (no association)", randomize(1.0, REPS_RND)),
               (f"noncentral, constant odds ratio psi={psi:.3f}",
                randomize(psi, max(REPS_RND // 2, 100)))]:
    P(f"  {lbl:<46} null mean {v.mean():+.4f}  sd {v.std():.4f}  "
      f"[{np.quantile(v,.025):+.4f}, {np.quantile(v,.975):+.4f}]")
    P(f"  {'':<46} {resample_p(int((v <= obs).sum()), len(v))}")
P(f"  {'OBSERVED':<46} {obs:+.4f}")
P("\n  continuity-correction sensitivity (point estimate):")
for c in [0.0, 0.25, 0.5, 1.0]:
    d = a.copy(); d["yc"] = log_odds(d.mid_f, d, c)
    P(f"    c={c:<5} b={fit(d, RHS, 'yc', quiet=True).params.fem_share:+.4f}")
P("\n  Haldane shift (c=0.5 minus c=0) by female-share sextile:")
hs = a.assign(shift=log_odds(a.mid_f, a, 0.5) - a.y)
for _, row in hs.groupby(pd.qcut(hs.fem_share, 6)).agg(
        fem=("fem_share", "mean"), shift=("shift", "mean"),
        med=("mid_f", "median")).iterrows():
    P(f"    female share {row.fem:.3f}  shift {row['shift']:+.4f}  "
      f"median female managers {row.med:.0f}")
P("  The shift is larger where female managers are few, which is the direction")
P("  that would inflate the slope; the headline therefore uses no correction.")

P("\n" + "-"*80); P("PANEL F  INFERENCE AND INFLUENCE"); P("-"*80)
Z = absorb(a, ["y"] + RHS); X, y = sm.add_constant(Z[RHS]), Z.y
for lbl, kw in [("homoskedastic", {}),
                ("cluster: CBSA", {"cov_type": "cluster", "cov_kwds": {"groups": a.cbsa_code}}),
                ("cluster: NAICS-3 (21 clusters)",
                 {"cov_type": "cluster", "cov_kwds": {"groups": a.naics3}})]:
    r = sm.OLS(y, X).fit(**kw)
    P(f"  {lbl:<34} b={r.params.fem_share:+.4f} se={r.bse.fem_share:.4f} "
      f"t={r.tvalues.fem_share:+.2f} p={r.pvalues.fem_share:.3g}")
rr = sm.OLS(y, X.drop(columns="fem_share")).fit()
t0 = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": a.naics3}).tvalues.fem_share
ts = []
for _ in range(REPS_WCB):
    wm = dict(zip(sorted(a.naics3.unique()), rng.choice([-1, 1], size=a.naics3.nunique())))
    ts.append(sm.OLS(rr.fittedvalues + rr.resid * a.naics3.map(wm).values, X).fit(
        cov_type="cluster", cov_kwds={"groups": a.naics3}).tvalues.fem_share)
P(f"  wild cluster bootstrap over 21 industries: "
  f"{resample_p(int((np.abs(ts) >= abs(t0)).sum()), len(ts))}")
P("  coefficient across sequential controls:")
for cols, lbl in [(["fem_share"], "fixed effects only"),
                  (["fem_share", "ln_emp"], "+ ln_emp"),
                  (RHS, "+ ln_estab_size"),
                  (RHS + ["mgmt_intensity"], "+ mgmt_intensity"),
                  (RHS + ["mgmt_intensity", "sep_rate_all"], "+ mobility")]:
    dd = a.dropna(subset=["y"] + cols)
    P(f"    {lbl:<22} b={fit(dd, cols, 'y', quiet=True).params.fem_share:+.4f}  n={len(dd):,}")
li = sorted((fit(a[a.naics3 != j], RHS, "y", quiet=True).params.fem_share, j)
            for j in a.naics3.unique())
P(f"  leave-one-industry-out: [{li[0][0]:+.4f} (drop {li[0][1]}), "
  f"{li[-1][0]:+.4f} (drop {li[-1][1]})]")
lc = [fit(a[a.cbsa_code != c], RHS, "y", quiet=True).params.fem_share
      for c in a.cbsa_code.value_counts().head(20).index]
P(f"  leave-one-CBSA-out, 20 largest: [{min(lc):+.4f}, {max(lc):+.4f}]")

P("\n" + "-"*80); P("PANEL G  SHARP WORST-CASE BOUNDS UNDER SUPPRESSION"); P("-"*80)
P("  Suppression is a deterministic threshold rule, so a selection model with an")
P("  exclusion restriction is inapplicable. OLS is linear in y, so the exact")
P("  bounds follow in closed form from the FWL weights -- equivalent to searching")
P(f"  all 3^{len(bnd)} admissible assignments.")
P("  Bounds require a continuity correction: a suppressed cell may truly hold zero")
P("  female managers, at which the uncorrected statistic diverges.")
BOUNDS = {}
for c in [0.25, 0.5, 1.0]:
    d = full.dropna(subset=["fem_share", "ln_emp", "ln_estab_size", "emp_f", "mid_tot", "emp"]).copy()
    Zb = absorb(d, RHS)
    C2 = sm.add_constant(Zb[["ln_emp", "ln_estab_size"]])
    xt = np.asarray(Zb.fem_share) - C2 @ np.linalg.lstsq(C2, Zb.fem_share, rcond=None)[0]
    cw = xt / (xt @ xt)
    b = d.bounded.values.astype(bool)
    yo = np.where(b, 0.0, log_odds(d.mid_f, d, c))
    lo = log_odds(pd.Series(np.zeros(len(d)), index=d.index), d, c).values
    hi = log_odds(np.minimum(np.minimum(TAU - 1, d.emp_f), d.mid_tot), d, c).values
    base = np.sum(cw[~b] * yo[~b])
    lo_b, hi_b, cb = lo[b], hi[b], cw[b]
    bmin = base + np.sum(np.where(cb > 0, cb * lo_b, cb * hi_b))
    bmax = base + np.sum(np.where(cb > 0, cb * hi_b, cb * lo_b))
    BOUNDS[c] = (bmin, bmax)
    P(f"    c={c:<5} sharp set [{bmin:+.4f}, {bmax:+.4f}]  width {bmax-bmin:.4f}"
      + ("   <-- sign NOT identified" if bmax > 0 else ""))
P("  The sign of the coefficient is not identified once suppressed cells are")
P("  bounded and the correction is small. This is a property of the published")
P("  data, not of the estimator.")
P(f"  Cells where TOTAL1_2 is also suppressed hold at most {TAU-1} managers in total,")
P("  so the mid_tot>=10 filter excludes them by construction, not by convenience.")

P("\n  Counterfactual release rule: flag true zeros separately from counts of 1-2.")
P("  Publishing the [0,2] bounds would add nothing -- they are already implied by")
P("  the rule. What cannot be recovered is whether a withheld count is 0 or 1-2,")
P("  and the zero case is what makes the lower bound diverge as c -> 0.")
for c in [0.0, 0.25, 0.5, 1.0]:
    cc = c if c > 0 else 1e-12
    d = full.dropna(subset=["fem_share", "ln_emp", "ln_estab_size", "emp_f", "mid_tot", "emp"]).copy()
    Zb = absorb(d, RHS)
    C2 = sm.add_constant(Zb[["ln_emp", "ln_estab_size"]])
    xt = np.asarray(Zb.fem_share) - C2 @ np.linalg.lstsq(C2, Zb.fem_share, rcond=None)[0]
    cw = xt / (xt @ xt)
    b = d.bounded.values.astype(bool)
    yo = np.where(b, 0.0, log_odds(d.mid_f, d, cc))
    lo = log_odds(pd.Series(np.ones(len(d)), index=d.index), d, cc).values
    hi = log_odds(np.minimum(np.minimum(TAU - 1, d.emp_f), d.mid_tot), d, cc).values
    base = np.sum(cw[~b] * yo[~b]); cb = cw[b]
    bmin = base + np.sum(np.where(cb > 0, cb * lo[b], cb * hi[b]))
    bmax = base + np.sum(np.where(cb > 0, cb * hi[b], cb * lo[b]))
    cur = "diverges" if c == 0 else f"[{BOUNDS[c][0]:+.4f}, {BOUNDS[c][1]:+.4f}]" if c in BOUNDS else "  --"
    P(f"    c={c:<5} current {cur:<22}  zeros flagged [{bmin:+.4f}, {bmax:+.4f}]  "
      f"width {bmax-bmin:.4f}")
P("  With zeros flagged the sign is identified at every correction, the set narrows")
P("  roughly threefold, and dependence on the correction largely disappears.")

P("\n" + "-"*80); P("PANEL H  MEASUREMENT-ERROR SENSITIVITY  (not causal identification)"); P("-"*80)
lag = (r1.groupby(["cbsa_code", "naics3"], as_index=False).fem_share_eeo1
         .mean().rename(columns={"fem_share_eeo1": "fem_lag"}))
d = a.merge(lag, on=["cbsa_code", "naics3"], how="left").dropna(
    subset=["y", "fem_share_eeo1", "fem_share", "fem_lag", "ln_emp", "ln_estab_size"])
Z = absorb(d, ["y", "fem_share_eeo1", "fem_share", "fem_lag", "ln_emp", "ln_estab_size"])
C2 = sm.add_constant(Z[["ln_emp", "ln_estab_size"]])
res = lambda v: np.asarray(sm.OLS(Z[v], C2).fit().resid)
yt, xt, zq, zl = res("y"), res("fem_share_eeo1"), res("fem_share"), res("fem_lag")
cl = d.cbsa_code.values
P(f"  n={len(d):,}  clusters={d.cbsa_code.nunique():,}")
for lbl, ZZ in [("QWI female share", [zq]), ("lagged EEO-1 2015-21", [zl]), ("both", [zq, zl])]:
    M = sm.add_constant(np.column_stack(ZZ))
    s1 = sm.OLS(xt, M).fit(cov_type="cluster", cov_kwds={"groups": cl})
    s2 = sm.OLS(yt, sm.add_constant(sm.OLS(xt, M).fit().fittedvalues)).fit(
        cov_type="cluster", cov_kwds={"groups": cl})
    F = float(s1.f_test(np.eye(len(s1.params))[1:]).fvalue)
    P(f"  {lbl:<22} first-stage F={F:>8,.1f}   2SLS b={s2.params[1]:+.4f} (se {s2.bse[1]:.4f})")
M = sm.add_constant(np.column_stack([zq, zl]))
keep = [b for b in np.arange(-4, 2.001, 0.02)
        if float(sm.OLS(yt - b*xt, M).fit(cov_type="cluster", cov_kwds={"groups": cl})
                 .f_test(np.eye(3)[1:]).pvalue) > 0.05]
P(f"  Anderson-Rubin 95% set: [{min(keep):+.3f}, {max(keep):+.3f}]")
for lbl, z in [("QWI", zq), ("lagged", zl)]:
    pi = sm.OLS(xt, sm.add_constant(z)).fit().params[1]
    rf = sm.OLS(yt, sm.add_constant(z)).fit().params[1]
    P(f"  {lbl:<8} first stage {pi:+.4f}  reduced form {rf:+.4f}  "
      f"direct effect reaching b=-0.50 needs {abs((rf+0.5*pi)/rf)*100:.0f}% of the reduced form")
P("  first-stage coefficient on the QWI instrument across control sets:")
for cols, lbl in [([], "fixed effects only"), (["ln_emp"], "+ ln_emp"),
                  (["ln_emp", "ln_estab_size"], "+ ln_estab_size"),
                  (["ln_emp", "ln_estab_size", "mgmt_intensity"], "+ mgmt_intensity")]:
    Zc = absorb(d, ["fem_share_eeo1", "fem_share"] + cols)
    CC = sm.add_constant(Zc[cols]) if cols else np.ones((len(Zc), 1))
    xr = np.asarray(sm.OLS(Zc.fem_share_eeo1, CC).fit().resid)
    zr = np.asarray(sm.OLS(Zc.fem_share, CC).fit().resid)
    P(f"    {lbl:<20} pi={sm.OLS(xr, sm.add_constant(zr)).fit().params[1]:+.4f}")
P("  Both instruments plausibly violate the exclusion restriction through the same")
P("  persistent local industry structure, so the overidentification test has little")
P("  power against it. These results bound measurement error only.")

P("\n" + "-"*80); P("PANEL I  REGIME 1, AND WHAT IS NOT ESTIMATED"); P("-"*80)
fit(r1, ["fem_share_eeo1", "ln_emp", "ln_estab_size"], "y",
    "I1  regime 1, 2015-2021 (76.5% cell overlap; a different filing regime, not an independent sample)",
    fe=("naics3", "region", "yr"))
r1["cell"] = r1.cbsa_code.astype(str) + "|" + r1.naics3.astype(str)
for v in ["y", "fem_share_eeo1"]:
    wi = (r1[v] - r1.groupby("cell")[v].transform("mean")).var() / r1[v].var()
    P(f"    within-cell variance share, {v:<18} {wi*100:.1f}%")
bal = r1.groupby("cell").year.nunique()
P(f"    cells observed in all 7 years: {(bal == 7).sum():,} of {len(bal):,} "
  f"({(bal == 7).mean()*100:.1f}%)")
P("    The regressor moves 4.9% within cells, so no cell fixed-effects estimator")
P("    is reported: it would remove the signal and keep the noise.")
m = fit(a, ["sep_rate_all"] + RHS, "y", quiet=True)
P(f"\n  Pre-specified test, retained for the record: external mobility "
  f"b={m.params.sep_rate_all:+.4f} (p={m.pvalues.sep_rate_all:.3f}). "
  f"The monopsony hypothesis this project began with is not supported.")


P("\n" + "-"*80)
P("PANEL J  VALIDITY, SPECIFICATION AND SCALE")
P("-"*80)

P("\n  J1  internal consistency of the EEO-1 counts (full frame, observed + bounded)")
fr = full.copy()
for lbl, bad in [("female managers > female employed", fr.mid_f > fr.emp_f),
                 ("all managers > all employed", fr.mid_tot > fr.emp),
                 ("female managers > all managers", fr.mid_f > fr.mid_tot),
                 ("female employed > all employed", fr.emp_f > fr.emp),
                 ("male managers > male employed", (fr.mid_tot - fr.mid_f) > (fr.emp - fr.emp_f)),
                 ("derived male managers < 0", (fr.mid_tot - fr.mid_f) < 0),
                 ("derived male employed < 0", (fr.emp - fr.emp_f) < 0)]:
    P(f"    {lbl:<36} violations: {int(bad.sum())}")
mi = a.mid_tot / a.emp
P(f"    management intensity: median {mi.median():.3f}, p1 {mi.quantile(.01):.3f}, "
  f"p99 {mi.quantile(.99):.3f}")

P("\n  J2  joint significance of the fixed effects")
base = "y ~ fem_share + ln_emp + ln_estab_size"
m_full = smf.ols(base + " + C(naics3) + C(region)", a).fit()
for lbl, frm in [("industry (20 indicators)", base + " + C(region)"),
                 ("region (4 indicators)", base + " + C(naics3)")]:
    r_ = smf.ols(frm, a).fit()
    q = r_.df_resid - m_full.df_resid
    F = ((r_.ssr - m_full.ssr) / q) / (m_full.ssr / m_full.df_resid)
    P(f"    {lbl:<26} F={F:6.2f}  df=({int(q)},{int(m_full.df_resid)})  "
      f"p={1 - stats.f.cdf(F, q, m_full.df_resid):.3g}   "
      f"fem_share without it {r_.params.fem_share:+.4f}")
P("    Both sets are jointly significant; neither is dead weight.")

P("\n  J3  CBSA fixed effects: comparing industries WITHIN the same labor market")
cnt = a.groupby("cbsa_code").size()
ns = a[a.cbsa_code.map(cnt) >= 2].copy()
P(f"    singleton CBSAs dropped {int((cnt == 1).sum())}; "
  f"{len(ns):,} cells in {ns.cbsa_code.nunique()} CBSAs remain")
for fes, lbl in [(("naics3", "region"), "industry + region (main spec, same sample)"),
                 (("cbsa_code",), "CBSA"),
                 (("naics3", "cbsa_code"), "industry + CBSA, two-way")]:
    m_ = fit(ns, RHS, "y", fe=fes, quiet=True)
    P(f"    {lbl:<44} b={m_.params.fem_share:+.4f}  se={m_.bse.fem_share:.4f}  "
      f"t={m_.tvalues.fem_share:+.2f}")
wv = absorb(ns, ["fem_share"], fes=("naics3", "cbsa_code")).fem_share.var() / ns.fem_share.var()
P(f"    within-(industry+CBSA) share of female-share variance: {wv*100:.1f}%")
P("    Every market-level confounder is absorbed. About 90% of the association")
P("    survives the within-market comparison; about 10% runs through market-level")
P("    factors. Singletons are disproportionately small markets, where Panel D")
P("    shows the association is strongest, so this is kept as a robustness check.")

P("\n  J4  numerical stability")
Xc = a[RHS].astype(float)
Xd = pd.get_dummies(a[["naics3", "region"]], drop_first=True).astype(float)
Xs = (Xc - Xc.mean()) / Xc.std()
P(f"    condition number: raw {np.linalg.cond(sm.add_constant(pd.concat([Xc, Xd], axis=1)).values):,.1f}"
  f" | standardized {np.linalg.cond(sm.add_constant(pd.concat([Xs, Xd], axis=1)).values):,.1f}"
  f" | fixed effects absorbed "
  f"{np.linalg.cond(sm.add_constant(absorb(a, RHS)).values):,.1f}")
V = sm.add_constant(Xc).values
P("    VIF " + "  ".join(f"{c} {variance_inflation_factor(V, i):.3f}"
                           for i, c in enumerate(RHS, 1)))
ms = smf.ols("y ~ fz + ez + sz + C(naics3) + C(region)",
             a.assign(fz=Xs.fem_share, ez=Xs.ln_emp, sz=Xs.ln_estab_size)).fit()
P(f"    standardized refit: t {ms.tvalues.fz:+.2f} vs raw {m_full.tvalues.fem_share:+.2f}; "
  f"R2 {ms.rsquared:.4f} vs {m_full.rsquared:.4f} (homoskedastic, dummies)")
P(f"    standardized coefficient: 1 SD of female share ({Xc.fem_share.std():.3f}) "
  f"shifts ln_theta by {ms.params.fz:+.4f}")

P("\n  J5  economic magnitude of the main coefficient")
b0 = fit(a, RHS, "y", quiet=True).params.fem_share
q10, q25, q75, q90 = a.fem_share.quantile([.10, .25, .75, .90])
P(f"    female share  p10 {q10:.3f}  p25 {q25:.3f}  p75 {q75:.3f}  p90 {q90:.3f}")
for lo, hi, lbl in [(0, .10, "+10 percentage points"), (q25, q75, "p25 -> p75"),
                    (q10, q90, "p10 -> p90")]:
    dl = b0 * (hi - lo)
    P(f"    {lbl:<22} odds ratio x {np.exp(dl):.3f}  ({(np.exp(dl)-1)*100:+.1f}%)")
bf_ = fit(a, RHS, "rate_f", quiet=True).params.fem_share
bm_ = fit(a, RHS, "rate_m", quiet=True).params.fem_share
rf0 = (a.mid_f / a.emp_f).median()
rm0 = ((a.mid_tot - a.mid_f) / (a.emp - a.emp_f)).median()
kf, km = np.exp(bf_ * (q75 - q25)), np.exp(bm_ * (q75 - q25))
P(f"    median management rate: women {rf0*100:.2f}%, men {rm0*100:.2f}%")
P(f"    across the IQR: women {rf0*100:.2f}% -> {rf0*kf*100:.2f}%, "
  f"men {rm0*100:.2f}% -> {rm0*km*100:.2f}%")
ef = a.emp_f.median()
P(f"    illustration, median cell ({ef:.0f} women employed): "
  f"{ef*rf0:.1f} -> {ef*rf0*kf:.1f} women in mid-management")
P("    The illustration holds female employment fixed while moving the share;")
P("    it describes the cross-sectional association, not a predicted effect.")

P("\n  J6  establishment size: artefact or selection?")
e_all = fit(a, RHS, "y", quiet=True).params.ln_estab_size
e_big = fit(a[a.emp >= a.emp.median()], RHS, "y", quiet=True).params.ln_estab_size
e_r1 = fit(r1, ["fem_share_eeo1", "ln_emp", "ln_estab_size"], "y", quiet=True,
           fe=("naics3", "region", "yr")).params.ln_estab_size
P(f"    full sample {e_all:+.4f} | 2015-2021 regime {e_r1:+.4f} | "
  f"large cells only (employment >= median) {e_big:+.4f}")
P(f"    stable across the filing regimes despite a 2x change in reporting-unit size,")
P(f"    so not purely a reporting artefact; shrinks {(1 - e_big/e_all)*100:.0f}% in large cells,")
P("    so part of it is selection. No mechanism is proposed.")


# ============================================================ Panel K
P("\n" + "-"*80)
P("PANEL K  JOB-LADDER POSITION  (is the gap about where each sex sits in the plant?)")
P("-"*80)
JOBS = ["prof", "tech", "sales", "admin", "craft", "oper", "labor", "serv"]
for j in JOBS:
    a[f"{j}_m"] = a[f"{j}_tot"] - a[f"{j}_f"]
P("  EEO-1 also reports professionals, technicians, sales, administrative support,")
P("  craft, operatives, laborers and service workers by sex. Small counts in")
P("  these categories are suppressed, so each test runs on the cells where the")
P("  categories it needs are published, and is compared with the main")
P("  specification ON THE SAME CELLS.")
for j, nm in zip(JOBS, ["professionals", "technicians", "sales", "admin support",
                        "craft", "operatives", "laborers", "service"]):
    P(f"    female count published, {nm:<14} {a[f'{j}_f'].notna().mean()*100:5.1f}% of cells")
fl = a.dropna(subset=["oper_f", "labor_f", "oper_tot", "labor_tot"]).copy()
fl["w_floor"] = (fl.oper_f + fl.labor_f) / fl.emp_f
fl["m_floor"] = (fl.oper_m + fl.labor_m) / (fl.emp - fl.emp_f)
P("\n  share of each sex working as operatives or laborers (the production floor):")
for k, g in fl.groupby(pd.qcut(fl.fem_share, 3, labels=["low female share", "middle", "high female share"])):
    P(f"    {k:<18} women {g.w_floor.median()*100:5.1f}%   men {g.m_floor.median()*100:5.1f}%   cells {len(g):,}")
P("  In male-dominated cells the women present are less often on the floor than")
P("  men -- more often in office and technical roles closer to management.")
P("\n  K1  controlling for where each sex sits")
b0 = fit(fl, RHS, "y", quiet=True); b1 = fit(fl, RHS + ["w_floor", "m_floor"], "y", quiet=True)
P(f"    same cells, main specification              b={b0.params.fem_share:+.4f}  n={int(b0.nobs):,}")
P(f"    + women's and men's floor shares            b={b1.params.fem_share:+.4f}  t={b1.tvalues.fem_share:+.2f}"
  f"   ({(1-b1.params.fem_share/b0.params.fem_share)*100:.0f}% of the coefficient)")
sk = a.dropna(subset=["prof_f", "tech_f", "craft_f", "oper_f", "labor_f"]).copy()
sk["w_floor"] = (sk.oper_f + sk.labor_f) / sk.emp_f
sk["m_floor"] = (sk.oper_m + sk.labor_m) / (sk.emp - sk.emp_f)
sk["w_skill"] = (sk.prof_f + sk.tech_f + sk.craft_f) / sk.emp_f
sk["m_skill"] = (sk.prof_m + sk.tech_m + sk.craft_m) / (sk.emp - sk.emp_f)
b0 = fit(sk, RHS, "y", quiet=True)
b1 = fit(sk, RHS + ["w_floor", "m_floor", "w_skill", "m_skill"], "y", quiet=True)
P(f"    same cells, main specification              b={b0.params.fem_share:+.4f}  n={int(b0.nobs):,}")
P(f"    + floor and skilled-pipeline shares         b={b1.params.fem_share:+.4f}  t={b1.tvalues.fem_share:+.2f}"
  f"   ({(1-b1.params.fem_share/b0.params.fem_share)*100:.0f}% of the coefficient)")
P("\n  K2  comparing managers only with the tier immediately below")
for cats, lbl in [(["prof", "tech", "craft"], "professionals + technicians + craft"),
                  (["oper", "labor"], "operatives + laborers")]:
    dk = a.dropna(subset=[f"{c}_f" for c in cats] + [f"{c}_tot" for c in cats]).copy()
    Fp = sum(dk[f"{c}_f"] for c in cats); Mp = sum(dk[f"{c}_m"] for c in cats)
    dk["yp"] = np.log((dk.mid_f / Fp) / ((dk.mid_tot - dk.mid_f) / Mp))
    dk = dk[np.isfinite(dk.yp)]
    mp = fit(dk, RHS, "yp", quiet=True); mb = fit(dk, RHS, "y", quiet=True)
    P(f"    managers per {lbl:<36} b={mp.params.fem_share:+.4f}  t={mp.tvalues.fem_share:+.2f}"
      f"   same cells, main {mb.params.fem_share:+.4f}  n={int(mp.nobs):,}")
P("  Roughly half to two-thirds of the association is accounted for by where women")
P("  and men sit in the job ladder; a smaller remainder is negative in every test.")
P("  Job-ladder position may itself be part of how the gap arises, so the controlled")
P("  coefficient splits the association rather than isolating a 'true' effect.")

# ============================================================ Panel L
P("\n" + "-"*80)
P("PANEL L  A SECOND, INDEPENDENT SOURCE: ACS 2022-2024 (IPUMS USA)")
P("-"*80)
acs = load(ACS_CELLS)
num = ["n", "sum_w", "sum_w2", "F", "M", "Fm_a", "Mm_a", "Fm_b", "Mm_b",
       "nF", "nM", "nFm_a", "nMm_a", "nFm_b", "nMm_b"]


def acs_cells(df, k):
    g = df.groupby(["met2013", "naics3", "region"], as_index=False)[num].sum()
    g["cbsa_code"] = g.met2013.astype(str)
    g["Fm"], g["Mm"] = g[f"Fm_{k}"], g[f"Mm_{k}"]
    g["nFm"], g["nMm"] = g[f"nFm_{k}"], g[f"nMm_{k}"]
    g["nFo"], g["nMo"] = g.nF - g.nFm, g.nM - g.nMm
    g["fem_share"] = g.F / (g.F + g.M)
    g["mgmt_fem_share"] = g.Fm / (g.Fm + g.Mm)
    g["y"] = np.log((g.Fm / (g.F - g.Fm)) / (g.Mm / (g.M - g.Mm)))
    g["rate_f"], g["rate_m"] = np.log(g.Fm / g.F), np.log(g.Mm / g.M)
    g["mgmt_int"] = np.log((g.Fm + g.Mm) / (g.F + g.M))
    g["ln_emp"] = np.log(g.F + g.M)
    g["prec"] = 1 / (1/g.nFm + 1/g.nMm + 1/g.nFo + 1/g.nMo)
    g["deff"] = g.n * g.sum_w2 / g.sum_w**2
    g["wt_emp"] = g.F + g.M
    return g


def usable(g, nmin=50):
    return g[(g.n >= nmin) & (g.nFm >= 3) & (g.nMm >= 3) & (g.nFo > 0) & (g.nMo > 0)
             & np.isfinite(g.y)].copy()


RA = ["fem_share", "ln_emp"]      # ACS has no establishment size
LA = usable(acs_cells(acs, "a"))
P("  Census survey of individuals: not subject to the EEOC suppression rule, the")
P("  100-employee threshold, or employer job classification. Private wage and")
P("  salary workers, employed, in manufacturing. Metro is place of RESIDENCE.")
P("  Manager = management occupations (SOC 11, chief executives excluded) plus")
P("  first-line supervisors, to mirror EEO-1 first/mid-level management.")
P(f"  usable cells (>=50 respondents, >=3 female and >=3 male managers): {len(LA):,} "
  f"in {LA.met2013.nunique()} metros; median {LA.n.median():.0f} respondents per cell")


def L(df, yv, lbl, w=None):
    m_ = fit(df, RA, yv, w=w, quiet=True)
    P(f"    {lbl:<50} b={m_.params.fem_share:+.4f}  se={m_.bse.fem_share:.4f}  "
      f"t={m_.tvalues.fem_share:+.2f}  n={int(m_.nobs):,}")
    return m_

P("\n  L1  the divergence  (EEO-1: absolute +0.297, relative -1.175)")
L(LA, "mgmt_fem_share", "absolute: women's share of managers")
L(LA, "y", "relative: log odds, women vs men")
P("\n  L2  decomposition")
for mgr, lbl in [("a", "management + first-line supervisors"), ("b", "management occupations only")]:
    G = LA if mgr == "a" else usable(acs_cells(acs, "b"))
    P(f"    manager definition: {lbl}  ({len(G):,} cells)")
    for yv, nm in [("y", "relative log odds"), ("rate_f", "female management rate"),
                   ("rate_m", "male management rate"), ("mgmt_int", "overall management intensity")]:
        L(G, yv, "  " + nm)
P("  Common to both sources: relative odds fall, men's management rate rises, and")
P("  the managerial layer does not shrink. Women's rate falls clearly only in EEO-1;")
P("  in ACS the management layer grows. The decomposition is source-dependent.")
P("\n  L3  robustness of the relative measure")
L(LA, "y", "inverse-variance weighted", w="prec")
L(LA, "y", "employment-weighted", w="wt_emp")
for k in (100, 200):
    L(usable(acs_cells(acs, "a"), k), "y", f"cells with >= {k} respondents")
A24 = usable(acs_cells(acs[acs.year == 2024], "a"))
L(A24, "y", "2024 alone, relative")
L(A24, "mgmt_fem_share", "2024 alone, absolute")
P("\n  L4  can the two sources be compared cell by cell?")
ee = a.assign(met2013=pd.to_numeric(a.cbsa_code, errors="coerce"))
jn = LA.merge(ee[["met2013", "naics3", "fem_share_eeo1", "mid_fem_share", "y"]]
              .rename(columns={"y": "y_eeo", "mid_fem_share": "mgmt_share_eeo"}),
              on=["met2013", "naics3"], how="inner")
P(f"    cells present in both: {len(jn):,}")
P(f"    correlation, female share of workforce    {jn.fem_share.corr(jn.fem_share_eeo1):.3f}")
P(f"    correlation, female share of managers     {jn.mgmt_fem_share.corr(jn.mgmt_share_eeo):.3f}")
P(f"    correlation, relative log odds            {jn.y.corr(jn.y_eeo):.3f}")
tv = LA.y.var()
for lbl, sv in [("ignoring the survey weights", (1 / LA.prec).mean()),
                ("with the weighting design effect", (LA.deff / LA.prec).mean())]:
    rel = max(1 - sv / tv, 0)
    P(f"    sampling noise, {lbl:<33} {min(sv/tv, 1)*100:4.0f}% of cell variance; "
      f"correlation ceiling {np.sqrt(rel):.2f}")
P(f"    median weighting design effect per cell: {LA.deff.median():.2f}")
P("  Individual ACS cells are almost entirely sampling noise, so the weak cell-level")
P("  agreement is what noise alone would produce. The two sources can be compared")
P("  only in aggregate, where they agree on direction. The household-clustering")
P("  component is not included; it would add noise, not remove it.")

with open("results_log.txt", "w") as fh:
    fh.write("\n".join(LOG) + "\n")
print("\nwrote results_log.txt")
