# Technical Documentation

## Reinterpreting Women's Leadership Metrics: Are We Correctly Measuring the 'Female Share of Management'?

*The Two Faces of Women's Managerial Representation in Manufacturing — Analyzing the Illusion Between Absolute Share and Relative Odds*

**Version**: 3.1 — adds Panel J (data consistency, fixed-effect joint tests, CBSA within-market comparison, conditioning, economic magnitude). 3.0 superseded v2.0: The binomial placebo is replaced by
fixed-margin randomization, the suppression bounds are recomputed sharply and no
longer identify the sign, the continuity correction is dropped from the headline,
the estimand is stated explicitly, the instrumental-variable results are demoted
to measurement-error sensitivity, and "access" is replaced by "representation
odds" throughout.
**Author**: Sean (Yechan) Kim

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [Data Pipeline](#2-data-pipeline)
3. [Unit of Analysis](#3-unit-of-analysis)
4. [Outcome Construction](#4-outcome-construction)
5. [Treatment Construction](#5-treatment-construction)
6. [Estimator](#6-estimator)
7. [Sample Construction Cascade](#7-sample-construction-cascade)
8. [Identification Threats and Tests](#8-identification-threats-and-tests)
9. [Withdrawn Across Versions](#9-withdrawn-across-versions)
10. [Code Reference](#10-code-reference)
11. [Known Limitations](#11-known-limitations)

---

## 1. System Architecture

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Raw federal │ ->│  Crosswalk   │ ->│  Estimation  │ ->│  Adversarial │
│   sources    │   │  & merge     │   │   panels     │   │    audit     │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
      ↑                   ↑                  ↑                  ↑
  EEO-1 PUF          OMB CBSA          two regimes       placebo, IV,
  QWI (LEHD)         anchor match      absorbed FE       bounds, wild
  QCEW               bound suppressed  CBSA clusters     bootstrap
```

`build_dataset.py` performs the first two stages. `Gender_Management_Gap.py`
performs the last two and runs from the shipped CSVs alone.

---

## 2. Data Pipeline

### 2.1 EEO-1 Public Use File

- **Provider**: U.S. Equal Employment Opportunity Commission
- **Universe**: private employers with 100+ employees; federal contractors with 50+
- **Format**: one XLSX per year, 275 columns, aggregation levels stacked

| Column | Description |
|---|---|
| `Nation` … `County` | Six nested geography labels; a null means "aggregated over" |
| `NAICS2`, `NAICS3` | Industry codes, 2017 NAICS definitions |
| `Establishments` | Count of reporting units |
| `TOTAL10`, `MT10`, `FT10` | Total / male / female employment |
| `TOTAL1`, `MT1`, `FT1` | Executive and senior officials and managers |
| `TOTAL1_2`, `MT1_2`, `FT1_2` | First and mid-level officials and managers |
| `*` | Disclosure suppression flag |

**Level selection.** A CBSA × NAICS-3 row satisfies: `CBSA` not null, `County`
null, `NAICS3` not null. Filtering on `NAICS3` alone double-counts.

**`1_2` is job category 1.2, not `1+2`.** Verified arithmetically
(`TOTAL1 + TOTAL1_2 + TOTAL2…TOTAL9 = TOTAL10`) and against the PUF User Guide.

**Suppression threshold.** Recovered empirically: the smallest published value of
`FT1_2`, `FT1` and `TOTAL1_2` is **3** in every year, with counts of 3, 4 and 5
running smoothly (603 / 610 / 667). The cliff sits between 2 and 3. Suppressed
cells are therefore known to lie in **[0, 2]**, which is what makes bounds narrow.

**Filing-regime break.** Employees per reporting unit: 198–207 (2015–2021) → 50
(2022–2023). Establishments ×5.2. Cause: Type 6 establishment-list reports
discontinued, size-based non-headquarters report types consolidated, PEO
aggregate filing barred. No specification pools across this break.

### 2.2 Quarterly Workforce Indicators

- **Extract**: `geo_level=M`, `ind_level=3`, NAICS 311–339, `sex ∈ {0,1,2}`,
  `agegrp=A00`, firm characteristics not crossed, 2023 Q1–Q4
- **Status flags**: values masked to null unless the flag equals `1`; cells kept
  only where all four quarters are publishable

| Indicator | Use |
|---|---|
| `EmpS` | Stable (full-quarter) employment — denominator, and female share |
| `SepS`, `HirAS` | Stable separations and hires — flow numerators |
| `EarnS` | Stable earnings |

Do **not** cross sex with firm characteristics; it collapses most cells. Do not
substitute J2J: the NAICS-3 research release is state-level and is not crossed
with person demographics.

### 2.3 QCEW

`own_code=5`, `agglvl_code=45`, `area_fips` beginning with `C`. The area code is
`C` plus the first four digits of the CBSA code (`C1206` → `12060`).
Micropolitan areas carry no 3-digit industry detail, which is why QCEW is a
control rather than a denominator.

### 2.4 CBSA Delineation

`list1_2023.xlsx`, header on row 3. Supplies code, title and metro/micro flag.

---

## 3. Unit of Analysis

**CBSA × NAICS-3 subsector**: a metropolitan or micropolitan area crossed with
one of 21 manufacturing subsectors (311–316, 321–327, 331–337, 339).

County was rejected: 94.1% of female-executive cells are suppressed at county
level versus 86.6% at CBSA, and CBSA captures 35% more manufacturing employment.
CBSAs crossing state lines are retained; `region` is set to `MultiState` and
absorbed.

---

## 4. Outcome Construction

```
             ( FT1_2 + c ) / ( FT10 - FT1_2 + c )
ln_theta = ln ─────────────────────────────────────
             ( MT1_2 + c ) / ( MT10 - MT1_2 + c )
```

**The headline uses c = 0.** The estimation sample contains no cells with zero
female managers, so no correction is needed. Sensitivity: c = 0 gives −1.175,
c = 0.25 gives −1.200, c = 0.5 gives −1.224, c = 1.0 gives −1.266. The Haldane
shift is systematically larger in low-female cells (+0.045 versus +0.014 across
bins), which is the direction that would inflate the result, but it accounts for
roughly 4% of the coefficient. The bounds in §8.3 are the one place a correction
is unavoidable, because a suppressed cell may truly hold zero female managers.

**Naming.** The outcome is *relative managerial representation odds*, not
"access". Access implies an individual transition process; these are stock
distributions in a cross-section.

Zero is parity. Negative means women are less likely than men to hold a
management position conditional on employment in that market and subsector.
Zero-female-management cells in the estimation sample: 0, so the Haldane
correction is precautionary.

**Why not a ratio of shares.** The v1 outcome divided women's management share by
women's workforce share, placing the regressor in its own denominator. The odds
ratio is invariant to the marginal sex distribution. The two correlate at
r = 0.967, so the substantive result is unchanged — but only the odds ratio is
defensible, and invariance at the parameter level does not by itself rule out
correlated estimation noise. That is what the null simulation in §8 tests.

Secondary outcome: `mid_fem_share`, the absolute share, for literature comparison.

---

## 5. Treatment Construction

```
sep_rate  = Σ_q SepS  / mean_q EmpS
hire_rate = Σ_q HirAS / mean_q EmpS
```

`fem_share` is taken from QWI (`EmpS_f / (EmpS_f + EmpS_m)`) wherever available,
so that regressor and outcome come from independent measurement systems.
`fem_share_eeo1` is retained and reported alongside; §8 shows the gap between
them is attenuation, not shared-source bias.

---

## 6. Estimand and Estimator

**Estimand.** The unweighted specification answers: *in the average CBSA ×
NAICS-3 cell, how do women's relative managerial representation odds vary with
women's share of that cell's workforce?* It is not a worker-level national
relationship, and the title should not be read as one. Weighted alternatives
answer different questions and differ in magnitude by roughly a factor of three:

| Weight | Estimand | β |
|---|---|---:|
| none | the average local industry cell | −1.175 |
| total employment | the average manufacturing worker | −0.606 |
| female employment | the average woman | −0.519 |
| management headcount | the average managerial position | −0.421 |
| inverse variance | precision-weighted | −0.405 |

Minimum cell size attenuates it monotonically: β = −1.175 at `mid_tot ≥ 10`,
−0.851 at ≥ 50, −0.418 at ≥ 200. The association is strongest in small markets
and present but weaker in large ones.

**Economic magnitude (Panel J5).** Coefficients on a log-odds scale are not
interpretable on their own, so the main estimate is translated:

| Movement in female share | Odds ratio | Change |
|---|---:|---:|
| +10 percentage points | × 0.889 | −11.1% |
| p25 → p75 (0.214 → 0.365) | × 0.837 | −16.3% |
| p10 → p90 (0.161 → 0.433) | × 0.727 | −27.3% |

In rates, across the interquartile range women's management rate moves from
8.73% to 7.70% and men's from 10.11% to 10.45%. In a median cell employing 254
women this corresponds to about 22.2 versus 19.5 women in mid-management. The
illustration holds female employment fixed while varying the share and therefore
describes the cross-sectional association; it is not a predicted effect of adding
women to a workforce. Standardized: one standard deviation of female share
(0.117) shifts `ln_theta` by −0.137.


```
ln_theta_{cj} = β₁ fem_share_{cj} + β₂ ln_emp_{cj} + β₃ ln_estab_size_{cj}
                + μ_j + λ_r + ε_{cj}
```

- `μ_j` — NAICS-3 fixed effects. These absorb the industry-level confound that
  women in male-dominated heavy manufacturing are disproportionately in office
  and professional roles rather than on the line.
- `λ_r` — Census region, with `MultiState` as its own category.
- Fixed effects are absorbed by alternating within-group demeaning, so reported
  R² is a within-R².
- Standard errors clustered by CBSA (526 clusters). The industry dimension has
  only 21 clusters, so it is tested by wild cluster bootstrap rather than by a
  two-way cluster estimator, whose asymptotics are unreliable at that count.

---

## 7. Sample Construction Cascade

| Step | Filter | Cells |
|---|---|---:|
| 0 | EEO-1 regime-2 units (2022–23 average) | 3,841 |
| 1 | matched to a CBSA code | 3,781 |
| 2 | cell employment ≥ 50, QWI mobility observed, mid-management ≥ 10 | 3,054 |
| 3 | `FT1_2` published → **estimation sample** | **2,779** |
| 3′ | `FT1_2` suppressed, `TOTAL1_2` published → **bounded** | **275** |
| — | `TOTAL1_2` also suppressed (excluded; tested separately) | 15 |

Regime 1 applies the same size filters, yielding 12,764 cell-years across 538
CBSAs. **76.5% of regime-2 cells also appear in regime 1**; the two are the same
population under different filing rules.

---

## 8. Identification Threats and Tests

### 8.1 Fixed-margin randomization (Panel E)

EEO-1 cells are administrative enumerations, not survey samples. There is no
binomial sampling process to model, so the correct null is a randomization over
the observed table: hold all four margins fixed — female total, male total,
manager total, non-manager total — and remove only the sex-management
association by hypergeometric resampling. The regressor is then deterministic
and unchanged, so market composition, industry composition and managerial
opportunity structure are all preserved exactly.

| Null | Mean β | 95% range |
|---|---:|---|
| central hypergeometric, no association | −0.002 | [−0.161, +0.143] |
| noncentral, constant odds ratio ψ = 0.865 | −0.009 | [−0.177, +0.154] |
| **observed** | **−1.229** | — |

p < 0.0001 in both. The second null is the stronger one: a world in which women
are uniformly disadvantaged by the same factor everywhere, with only cell
composition varying, does not reproduce the slope. The observed relationship
therefore requires the odds ratio itself to vary with female share.

This replaces the binomial placebo used in v1–v2, which assumed a sampling
process that does not exist and drew the regressor from an independent source,
thereby bypassing the shared-count channel it was meant to test.

### 8.2 Decomposition (Panel C)

| Outcome | β |
|---|---:|
| log female management rate, F_mgr / F_employed | **−0.833*** |
| log male management rate, M_mgr / M_employed | **+0.221*** |
| log overall management intensity | −0.090 (p = 0.21) |
| log odds ratio (difference) | −1.175 |

The first two sum to −1.054 against a direct estimate of −1.175; the residual is
the odds denominators. The managerial layer does not thin, so an explanation
running through flatter hierarchies in female-intensive industries is ruled out.
Positions are reallocated rather than removed, and men's rate moves in the
opposite direction from women's.

### 8.3 Sharp worst-case bounds under suppression (Panel G)

Suppression is a deterministic threshold rule — the smallest published value of
`FT1_2`, `FT1` and `TOTAL1_2` is **3** in every year, with counts of 3, 4 and 5
running smoothly — so a selection model requires an exclusion restriction that
does not exist, and cell size affects the outcome directly. Bounds are the
correct tool.

Because OLS is linear in the outcome, β = Σ cᵢ yᵢ with FWL weights cᵢ that do not
depend on y. The outcome is monotone in the suppressed count, so assigning the
lower bound wherever cᵢ > 0 and the upper bound wherever cᵢ < 0 yields the exact
extremes. This is equivalent to searching all 3²⁷⁵ admissible assignments; the
vertex-and-median heuristic used in v2 was not sharp and understated the set on
both sides.

| Correction | Point estimate | Sharp set | Width |
|---:|---:|---|---:|
| c = 0.25 | −1.200 | **[−2.007, +0.350]** | 2.36 |
| c = 0.50 | −1.224 | [−1.858, −0.077] | 1.78 |
| c = 1.00 | −1.266 | [−1.757, −0.481] | 1.28 |

The 275 bounded cells carry 12.2% of the estimation weight. **The sign is not
identified**: it depends on the continuity correction, which cannot be set to
zero here because a suppressed cell may truly hold zero female managers. The v2
claim that the sign was identified is withdrawn.

Cells where `TOTAL1_2` is also suppressed hold at most two managers in total and
therefore fail the `mid_tot ≥ 10` filter by construction.

### 8.4 Inference and influence (Panel F)

| SE | se | t |
|---|---:|---:|
| homoskedastic | 0.090 | −13.1 |
| cluster: CBSA | 0.160 | −7.35 |
| cluster: NAICS-3 | 0.173 | −6.8 |
| wild cluster bootstrap, 21 industries | — | p < 0.001 |

Two-way clustering is not used: the industry dimension has 21 clusters, too few
for the Cameron–Gelbach–Miller asymptotics, so the bootstrap is used instead.
Leave-one-industry-out spans [−1.254, −1.094]; leave-one-CBSA-out over the 20
largest spans [−1.240, −1.165]. Coefficient stability across sequential controls
is within 0.05.

### 8.5 Measurement-error sensitivity, not identification (Panel H)

`fem_share_eeo1` instrumented by the QWI measure and by the 2015–21 lagged value.

| Instrument | First-stage π | First-stage F | Reduced form | 2SLS |
|---|---:|---:|---:|---:|
| QWI female share | +0.434 | 45.1 | −0.917 | −2.110 |
| lagged EEO-1 | +0.787 | 2,056 | −1.484 | −1.886 |
| both | — | 1,351 | — | −1.915 |

Anderson–Rubin 95% set: [−2.24, −1.62]. First-stage coefficients are unmoved by
the control sequence (+0.4385 → +0.4327).

**These do not establish validity.** Both instruments plausibly violate the
exclusion restriction through the same channel — persistent local industry
structure in which female-intensive production coexists with male-intensive
management — so the overidentification test has little power against it, and the
v2 reading of Sargan p = 0.21 as agreement between instruments is withdrawn. In
a Conley-style sensitivity, a direct effect worth 73–76% of the reduced form
moves the estimate to −0.50; 100% moves it to zero. The reduced form of the
lagged instrument on the outcome is itself −1.484 (t = −12.1), which is what such
a direct channel would look like.

### 8.6 Why no cell fixed effects (Panel I)

| Variable | within-cell share of variance |
|---|---:|
| `ln_theta` | 22.2% |
| `fem_share_eeo1` | **4.9%** |

Balanced cells: 1,019 of 2,758 (36.9%). At 4.9% within-variation a cell-FE
estimator removes signal and retains noise (Griliches–Hausman), producing an
estimate near zero with wide errors that cannot be distinguished from
attenuation. **Not estimated.** This also removes the basis for a shift-share
instrument, which needs panel variation to survive the industry fixed effects
already present.

### 8.7 Within-market comparison: CBSA fixed effects (Panel J3)

The main specification compares cells across labor markets within an industry.
A market-level confounder — local gender norms, educational composition,
urbanisation, female labor supply — could produce the association without any
industry-level relationship. Absorbing CBSA and industry jointly removes every
such factor, identifying the coefficient from industries with more versus fewer
women *inside the same market*.

| Fixed effects (2,630 cells, 377 CBSAs) | β | se | t |
|---|---:|---:|---:|
| industry + region (main, same sample) | −1.114 | 0.160 | −6.95 |
| CBSA only | −1.131 | 0.112 | −10.12 |
| **industry + CBSA** | **−0.999** | 0.174 | **−5.76** |

149 CBSAs contributing a single cell are dropped because a CBSA effect absorbs
them entirely. The regressor keeps 41.3% of its variance after both sets are
absorbed — enough to identify, in contrast to the 4.9% within-cell variation
that ruled out the panel design in §8.6. Roughly 90% of the association survives
the within-market comparison and roughly 10% runs through market-level factors.

This is kept as a robustness check rather than the main specification because
the dropped singletons are disproportionately small markets, where Panel D shows
the association is strongest, and dropping them would change the estimand.

### 8.8 Specification and numerical checks (Panels J1, J2, J4)

**Internal consistency.** Seven accounting identities are checked in every one of
the 3,054 cells — managers never exceed employment, female counts never exceed
totals, derived male counts are never negative. Zero violations. Management
intensity has median 0.097 and a 1st–99th percentile range of 0.040–0.232.

**Fixed effects.** Industry indicators are jointly significant (F = 11.91 on 20
and 2,751 df), as are region indicators (F = 7.68 on 4 df, p = 3.8 × 10⁻⁶).
Dropping industry moves the coefficient to −1.259, dropping region to −1.156.

**Conditioning.** Condition number 163.6 on the raw design, 22.6 standardized,
13.7 with fixed effects absorbed — all well below conventional warning levels.
VIFs are 1.014, 1.367 and 1.352. A standardized refit returns identical t and R²,
confirming that scale does not enter inference.

### 8.9 Ecological inference

The data support a cell-level association. They do not identify whether the same
woman is disadvantaged in promotion, whether female hiring concentrates in
entry-level occupations, whether male managers are hired externally, or whether
within-firm promotion rates differ by sex. Establishment- and firm-level
heterogeneity is aggregated away by construction.

---

## 9. Withdrawn Across Versions

| Claim | Version | Status |
|---|---|---|
| U-shaped relationship, quadratic `+3.377***` | v1 | **Withdrawn.** Binned means show saturation. The quadratic was driven by 2.5% of cells. |
| Regime 1 as an "independent sample" | v1 | **Corrected.** 76.5% cell overlap. |
| Kanter versus Blalock as testable here | v1 | **Withdrawn.** Both predict change at a threshold; this is a cross-section. |
| Suppression bias as "conservative" | v1 | **Corrected**, then superseded by sharp bounds. |
| Executive tier as a reported result | v1 | **Demoted.** |
| Cell fixed effects as the next step | v2 | **Withdrawn** on the variance decomposition. |
| Binomial placebo as the null | v2 | **Replaced** by fixed-margin randomization. |
| "Sign is identified" under suppression | v2 | **Withdrawn.** Sharp bounds admit a positive sign at c = 0.25. |
| IV as evidence against shared-source bias | v2 | **Demoted** to measurement-error sensitivity. |
| Sargan non-rejection as instrument agreement | v2 | **Withdrawn** on power grounds. |
| "Access to management" | v1–v2 | **Renamed** to representation odds. |
| `ln_estab_size` awaiting a theory | v1 | **Still open**; now known to carry a selection component (−36% in large cells). |

---

## 10. Code Reference

```
Gender_Management_Gap.py
├── absorb()   — alternating-projections FE demeaning
├── fit()      — OLS on absorbed data, CBSA-clustered SE
├── log_odds() — Haldane-corrected outcome
├── Panel A    — relative access; includes the failed mobility test
├── Panel B    — absolute share; literature replication
├── Panel C    — binned functional form
├── Panel D    — errors-in-variables 2SLS + Sargan
├── Panel E    — fixed-margin randomization
├── Panel F    — SE robustness + wild cluster bootstrap + stability
├── Panel G    — Manski bounds
└── Panel H    — regime 1 + variance decomposition

build_dataset.py
├── parse_eeo1()   — XLSX → CBSA × NAICS-3, level filter, suppression flags
├── build_qwi()    — chunked read, status masking, quarterly → annual
├── build_qcew()   — zip streaming, agglvl 45, private ownership
├── anchor_match() — vintage-robust CBSA name → code
└── assemble()     — merge, derive, bound, write
```

Dependencies: `pandas`, `numpy`, `scipy`, `statsmodels`, `matplotlib`. Optional
`python-calamine` accelerates EEO-1 XLSX reads roughly sevenfold.

---

## 11. Known Limitations

1. **Cross-sectional ecological association.** No promotion, transition or
   behavioural mechanism is identified, and the panel cannot repair this (§8.6).
2. **The sign is not identified** once suppressed cells are bounded at small
   continuity corrections (§8.3). This is a property of the published data.
3. **The magnitude is not identified.** Estimates span −0.42 to −2.24 across
   estimands and specifications (§6).
4. **Precision is not evidence.** These are cell means; aggregation shrinks
   variance and leaves bias intact.
5. **Specification search.** Outcome, geographic unit and sample split were all
   revised after seeing results. The randomization test and the bounds are the
   defenses; the regime-1 estimate is not, because the samples overlap.
6. **Markets with one or two covered employers** are removed by EEOC primary
   suppression before publication, so the mobility test is not fully powered
   against the thinnest markets — where its theory applies most.
7. **`ln_estab_size` carries a selection component** and has no mechanism attached.
8. **No causal language is warranted** anywhere in this repository.
