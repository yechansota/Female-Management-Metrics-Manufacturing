# Technical Documentation

## Reinterpreting Women's Leadership Metrics: Are We Correctly Measuring the 'Female Share of Management'?

*The Two Faces of Women's Managerial Representation in Manufacturing — Analyzing the Illusion Between Absolute Share and Relative Odds*

**Version**: 3.3 — adds Panel K (job-ladder position, EEO-1 job categories) and Panel L (independent replication in the ACS via IPUMS USA); the decomposition is now reported as source-dependent. 3.2 — resampling p-values reported as draw counts with their resolution; every number in this document is now printed by `Gender_Management_Gap.py`; code reference rebuilt for Panels A–J. 3.1 added Panel J (data consistency, fixed-effect joint tests, CBSA within-market comparison, conditioning, economic magnitude). 3.0 superseded v2.0: The binomial placebo is replaced by
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

### 2.4 American Community Survey (IPUMS USA)

- **Extract**: ACS 1-year 2022, 2023, 2024; fixed-width, rectangular, positions from the
  extract's own codebook (`YEAR` 1–4, `STATEFIP` 55–56, `MET2013` 57–61, `PERWT` 79–88 with
  two implied decimals, `SEX` 89, `AGE` 90–92, `EMPSTATD` 94–95, `CLASSWKRD` 97–98,
  `OCCSOC` 99–104, `INDNAICS` 105–112). A layout inferred before the codebook arrived was
  checked against it: 20 of 20 variables match.
- **Filters**: `EMPSTATD` ∈ {10, 12} (civilian employed), `CLASSWKRD` ∈ {22, 23} (private
  wage and salary), `INDNAICS` 311–339. 300,881 workers.
- **Managers**: (a) SOC 11 excluding chief executives (`1110XX`), plus first-line supervisors
  (major groups 33–53 whose minor group begins with 1); (b) SOC 11 excluding chief executives.
- **Geography**: `MET2013` is the metro area of **residence**, assigned to each public-use
  area by majority population; metros with match error of 15% or more are not coded, and
  areas under 100,000 people cannot be identified. Montana, South Dakota and Vermont have no
  usable metro in the manufacturing extract. 264 metros present, 178 in usable cells.
- **Shipped as aggregates**: `acs_mfg_cells_2022_2024.csv` holds metro × NAICS-3 × year
  weighted and unweighted counts by sex and manager status, plus Σw and Σw² for the
  weighting design effect. No person-level records are redistributed.
- **Citation**: Ruggles, S., Flood, S., Sobek, M., Backman, D., Cooper, G., Rivera Drew, J. A.,
  Richards, S., Rodgers, R., Schroeder, J., and Williams, K. C. W. *IPUMS USA: Version 16.0*
  [dataset]. Minneapolis, MN: IPUMS, 2025. https://doi.org/10.18128/D010.V16.0

### 2.5 CBSA Delineation

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
shift is systematically larger in low-female cells (+0.045 in the lowest
female-share sextile, where the median cell has 8 female managers, versus
+0.014 in the highest, with 30), which is the direction that would inflate the
result, but it accounts for roughly 4% of the coefficient (Panel E). The bounds in §8.3 are the one place a correction
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
| central hypergeometric, no association (200 draws) | −0.004 | [−0.150, +0.142] |
| noncentral, constant odds ratio ψ = 0.842 (100 draws) | −0.015 | [−0.183, +0.135] |
| **observed** | **−1.175** | — |

No draw is as extreme in either: 0 of 200 (p < 0.005) and 0 of 100 (p < 0.010).
A resampling p-value cannot be smaller than one over the number of draws, so
these are stated as counts rather than as p ≈ 0. The observed coefficient lies
about fifteen null standard deviations from the central null's mean. The second null is the stronger one: a world in which women
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
opposite direction from women's. Two qualifications follow in §8.10 and §8.11:
much of the reallocation reflects where women and men sit in the job ladder, and
the ACS shows a growing — not flat — managerial layer.

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

**Counterfactual release rule.** Publishing the [0, 2] bounds would add nothing:
they are already implied by the rule, and the sharp bounds above are computed
from them. What cannot be recovered is whether a withheld count is zero or one
to two, and it is the zero case that drives the lower bound to minus infinity as
the correction goes to zero. Re-solving with the admissible set restricted to
{1, 2} — as if the agency flagged true zeros separately:

| Correction | Current rule | True zeros flagged | Width, flagged |
|---:|---|---|---:|
| c = 0 | lower bound diverges | [−1.462, −0.669] | 0.79 |
| c = 0.25 | [−2.007, +0.350] | [−1.470, −0.782] | 0.69 |
| c = 0.50 | [−1.858, −0.077] | [−1.481, −0.872] | 0.61 |
| c = 1.00 | [−1.757, −0.481] | [−1.509, −1.007] | 0.50 |

The sign becomes identified at every correction, the set narrows two-and-a-half
to three-and-a-half times, and dependence on the correction largely disappears.

### 8.4 Inference and influence (Panel F)

| SE | se | t |
|---|---:|---:|
| homoskedastic | 0.092 | −12.75 |
| cluster: CBSA | 0.160 | −7.35 |
| cluster: NAICS-3 | 0.174 | −6.74 |
| wild cluster bootstrap, 21 industries | — | 0 of 499 draws as extreme (p < 0.002) |

Two-way clustering is not used: the industry dimension has 21 clusters, too few
for the Cameron–Gelbach–Miller asymptotics, so the bootstrap is used instead.
Leave-one-industry-out spans [−1.254, −1.094]; leave-one-CBSA-out over the 20
largest spans [−1.240, −1.165]. Across sequential controls — fixed effects only,
then adding employment, establishment size, management intensity and mobility —
the coefficient stays between −1.213 and −1.175.

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

### 8.10 Job-ladder position (Panel K)

EEO-1 reports eight non-management categories by sex. Suppression is heavy in some
(female counts published for 53.5% of cells in craft, 58.3% in technicians, 17.0% in
service), so each test runs on the cells it needs and is compared with the main
specification on those same cells.

| Share working as operatives or laborers | Women | Men |
|---|---:|---:|
| low female-share tercile | 42.1% | 52.6% |
| middle | 50.1% | 52.9% |
| high female-share tercile | 51.4% | 52.3% |

| Test | Same-cell main | Test | Reduction | n |
|---|---:|---:|---:|---:|
| + each sex's floor share | −0.928 | −0.517 (t = −4.46) | 44% | 2,006 |
| + floor and skilled-pipeline shares | −0.707 | −0.223 (t = −2.20) | 68% | 1,027 |
| managers per professionals + technicians + craft | −0.832 | −0.413 (t = −3.02) | 50% | 1,136 |
| managers per operatives + laborers | −0.928 | −1.446 (t = −5.37) | — | 2,006 |

In male-dominated cells the women present are disproportionately off the floor, closer
to management; that position accounts for roughly half to two-thirds of the
association. The remainder is negative in every version. Job-ladder position may be
one of the channels through which the gap arises, so the controlled coefficient is a
split of the association, not an estimate of a direct effect. The cells with published
category detail are larger than average, which is why the same-cell baselines are
already smaller than −1.175.

### 8.11 Independent replication: ACS (Panel L)

Cells: metro (residence) × NAICS-3, pooled 2022–2024; usable if at least 50
respondents and at least 3 female and 3 male managers. 937 cells in 178 metros,
median 136 respondents. Controls: log group employment; fixed effects for NAICS-3 and
Census region (by metro); SEs clustered by metro.

| Outcome | Manager def. (a) | Manager def. (b) |
|---|---:|---:|
| women's share of managers | **+0.748** (t = 12.37) | — |
| relative log odds | **−1.599** (t = −4.16) | −2.007 (t = −5.26) |
| female management rate | −0.494 (t = −1.90) | −0.375 (t = −1.31) |
| male management rate | +0.759 (t = 4.18) | +1.332 (t = 5.53) |
| overall management intensity | +0.435 (t = 2.87) | +0.913 (t = 4.56) |

Robustness of the relative measure: inverse-variance weighted −0.970 (t = −3.41);
employment-weighted −1.087 (t = −3.56); cells with 100+ respondents −0.878
(t = −2.15); 200+ respondents −0.597 (t = −0.98, n = 301); 2024 alone −1.307
(t = −2.14), with the absolute share +0.783 (t = 7.90).

**The decomposition is source-dependent.** Both sources show relative odds falling,
men's rate rising and no shrinking of the managerial layer. Women's rate falls
clearly only in EEO-1; in the ACS the layer grows, more so under definition (b), so
the difference is not an artefact of including supervisors. The data cannot say
which source's decomposition is right.

**Cell-level agreement.** In 788 cells present in both sources the correlations are
0.698 (female share of workforce), 0.390 (female share of managers) and 0.118
(relative log odds). With a median weighting design effect of 1.61 per cell, sampling
noise is about 99% of the cross-cell variance of the ACS log odds, capping any
correlation near 0.09 (59% and 0.64 if the weights are ignored). The weak agreement
is therefore what noise alone produces; the sources are comparable only in aggregate.
Household clustering is not included in the design effect and would raise it further.

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
| Managerial layer is flat where female share is higher | v3 | **Qualified.** Holds in EEO-1; in the ACS the layer grows (§8.11). |
| Positions are allocated differently by sex | v3 | **Qualified.** Half to two-thirds reflects job-ladder position (§8.10). |
| `ln_estab_size` awaiting a theory | v1 | **Still open**; carries a selection component: it shrinks 35% in large cells (Panel J6). |

---

## 10. Code Reference

```
Gender_Management_Gap.py            -> results_log.txt
├── absorb()      — alternating-projections fixed-effect demeaning
├── fit()         — OLS on absorbed data, CBSA-clustered SE, optional weights
├── resample_p()  — resampling p-values reported as counts, with resolution
├── log_odds()    — log odds ratio, optional continuity correction
├── Panel A  — relative representation odds (main)
├── Panel B  — absolute share; replication of prior literature
├── Panel C  — decomposition: female rate, male rate, management intensity
├── Panel D  — estimand and scale: weighting schemes, minimum cell size
├── Panel E  — fixed-margin randomization; continuity-correction checks
├── Panel F  — SEs, wild cluster bootstrap, sequential controls, influence
├── Panel G  — sharp worst-case bounds; true-zero counterfactual
├── Panel H  — measurement-error sensitivity: 2SLS, Anderson-Rubin, Conley
├── Panel I  — 2015-2021 regime, variance decomposition, mobility test
├── Panel J  — consistency, FE joint tests, CBSA FE, conditioning,
│              economic magnitude, establishment-size check
├── Panel K  — job-ladder position from the eight EEO-1 job categories
└── Panel L  — ACS replication, decomposition, robustness, cell-level agreement

make_figures.py                     -> fig1 ... fig7
└── one standalone figure per file, fixed 8.4 x 5.8 in canvas

build_dataset.py                    -> the two shipped CSVs
├── parse_eeo1()   — XLSX -> CBSA x NAICS-3, level filter, suppression flags
├── build_qwi()    — chunked read, status masking, quarterly -> annual
├── build_qcew()   — zip streaming, agglvl 45, private ownership
├── build_acs()    — IPUMS fixed-width -> metro x NAICS-3 x year aggregates
├── anchor_match() — vintage-robust CBSA name -> code
└── assemble()     — merge, derive, bound, write
```

Dependencies: `pandas`, `numpy`, `scipy`, `statsmodels`; `matplotlib` for the
figures only. Optional
`python-calamine` accelerates EEO-1 XLSX reads roughly sevenfold.

---

## 11. Known Limitations

1. **Cross-sectional ecological association.** No promotion, transition or
   behavioural mechanism is identified, and the panel cannot repair this (§8.6).
2. **The sign is not identified** once suppressed cells are bounded at small
   continuity corrections (§8.3). This is a property of the published data.
3. **The magnitude is not identified.** Estimates span about −0.40 to −2.31
   across estimands, instruments and filing regimes (§6, §8.5, Panel I).
4. **Precision is not evidence.** These are cell means; aggregation shrinks
   variance and leaves bias intact.
5. **Specification search.** Outcome, geographic unit and sample split were all
   revised after seeing results. The randomization test and the bounds are the
   defenses; the regime-1 estimate is not, because the samples overlap.
6. **Markets with one or two covered employers** are removed by EEOC primary
   suppression before publication, so the mobility test is not fully powered
   against the thinnest markets — where its theory applies most.
7. **`ln_estab_size` carries a selection component** and has no mechanism attached.
8. **The decomposition differs by source.** Women's rate falls clearly only in
   EEO-1; the ACS shows a growing managerial layer driven by men's rate.
9. **ACS groups are almost entirely noise individually** and ACS metros are places
   of residence; the two sources are comparable only in aggregate, and neither
   supports claims about particular metro areas.
10. **The job-ladder split is not a direct effect.** Job position may be a channel
   of the gap, and the tests run only where category detail is published.
11. **No causal language is warranted** anywhere in this repository.
