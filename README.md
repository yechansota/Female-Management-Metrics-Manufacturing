# **Reinterpreting Women's Leadership Metrics**

### *Are We Correctly Measuring the 'Female Share of Management'?*
<p align="center">
  <strong>The Two Faces of Women's Managerial Representation in Manufacturing — Analyzing the Illusion Between Absolute Share and Relative Odds</strong><br>
  <em>EEO-1 · ACS · QWI · QCEW  |  CBSA × NAICS-3  |  2022–2023 main cross-section, 2015–2021 comparison  |  2,779 local labor markets</em><br>
</p>

---

### **Project Motivation**

When organizations, researchers, and policymakers assess women's representation in management, they typically begin with one number: the percentage of managers who are women. This measure is widely used because it is easy to understand and appears in both workforce disclosures and academic research.

However, this statistic answers only one question: **what share of management positions are held by women?**
It does not answer a different and equally important question: **how likely is an employed woman to hold a management position relative to an employed man?**

Because the first measure mechanically rises when more women enter the workforce, the two measures can move in opposite directions. Women's share of management can increase even while women's relative managerial representation declines.

Manufacturing is where this matters most directly. First- and mid-level managers — production supervisors, shift leads, area managers — are the entry point to every tier above them. If women do not reach that tier in proportion to their presence on the floor, there is no pipeline further up.

This project asks a single question of the EEOC's own data: **in U.S. manufacturing, do the absolute share and the relative odds tell the same story?** They do not.

This study compares local industry cells in a single cross-section (2022–2023). It does not track individual employees, promotions, or career transitions. The results therefore describe a pattern in workforce composition, not the effect of adding more women to a workplace.

| Measure | Coefficient on female share of the workforce |
|---|---:|
| Women's **share of** management | **+0.297*** |
| Women's **odds of holding** management, relative to men in the same cell | **−1.175*** |

Neither number is wrong. They answer different questions, and reporting practice overwhelmingly uses the first.

The divergence survives a fixed-margin randomization test, five alternative estimands, industry and city influence checks, a comparison of industries *within* the same labor market, and a second, independent data source — the Census Bureau's American Community Survey, including 2024 on its own. **It does not survive disclosure suppression intact.** Once the cells the EEOC withholds are bounded, the sign of the relative measure is no longer identified — and a specific, low-cost change to the release rule would restore it.

---

### **1. The Divergence**

<table><tr>
<td width="50%"><img width="100%" alt="fig1_counts_rise" src="https://github.com/user-attachments/assets/3f802d2d-a50d-401e-a4c8-382d28a91a31" /></td>
<td width="50%"><img width="100%" alt="fig2_odds_fall" src="https://github.com/user-attachments/assets/c0e1ed3c-f0e5-441a-b08c-c8e8799da97d" /></td>
</tr></table>

**Figures 1 and 2. The same cells, read two ways.** Each point is the average of one-twelfth of the 2,779 metropolitan-area × manufacturing-subsector cells, ordered by the female share of that cell's workforce.

On the left, women's share of mid-management rises steadily with their share of the workforce. This reproduces the established finding — Taylor, Buck, Bloch and Turgeon (2019) reached it with 195,534 EEO-1 workplaces from 1980–2005 — and it is the measure most workforce reporting relies on.

On the right, the same cells are measured as women's odds of holding management relative to men's, after absorbing industry and region. Now the line falls. It drops steeply up to a female share of about 0.20, sits near parity until about 0.27, then falls below parity and stays there; there is no upturn. Error bars are 95% intervals, and the dashed line marks parity.

Where there are more women, there are **more** women managers — and **fewer women managers per employed woman**.

---

### **2. Where the Divergence Comes From**

<p align="center"><img width="780" alt="fig3_decomposition" src="https://github.com/user-attachments/assets/6ea0b651-6b10-483f-b3a2-8012d086fbbd" /></p>

**Figure 3. Positions are reallocated, not removed.** The odds ratio is split into its two components: the share of employed women who hold management, and the share of employed men who do.

As female share rises, women's management rate **falls** (−0.833) while men's **rises** (+0.221). The overall managerial layer does not thin: management intensity is flat (−0.090, p = 0.21). That rules out the most obvious structural explanation — that female-intensive industries simply have flatter hierarchies.

**Part of the gap is about where people work in the plant.** EEO-1 also counts professionals, technicians, craft workers, operatives and laborers by sex. In male-dominated cells, the women who are there are less often on the production floor than men (42% versus 53%) — more often in office and technical roles closer to management. Where women are numerous, their job mix matches men's (51% versus 52%). Accounting for where each sex sits reduces the coefficient by 44% to 68%, and comparing managers only with the skilled tier directly below them halves it (−0.832 to −0.413, same cells). A smaller remainder is negative in every version. Because job-ladder position may itself be part of how the gap arises, this splits the association rather than isolating a "true" effect.

**The decomposition depends on the source.** In the ACS (Section 5), the managerial layer *grows* where female share is higher and men's rate carries most of the divergence; women's rate falls clearly only in EEO-1. What both sources agree on: relative odds fall, men's management rate rises, and manager roles do not shrink.

**What this means in practice.** A ten-point increase in female share goes with an 11% reduction in women's relative odds. Across the interquartile range (0.21 to 0.37) it is 16%: women's management rate moves from 8.7% to 7.7% while men's moves from 10.1% to 10.5%. In a median cell employing 254 women, that is roughly **22 versus 19.5 women in mid-management**. The illustration holds female employment fixed while moving the share, so it describes the cross-sectional association, not the effect of adding women.

---

### **3. How Confident to Be**

<p align="center"><img width="780" alt="fig4_estimand_bounds" src="https://github.com/user-attachments/assets/f5b427c3-9740-4566-955a-0a3b891e3063" /></p>

**Figure 4. Direction is stable; magnitude is not.** Five estimands are shown — four weighting choices and one size restriction — each answering a different question: the average local industry cell (unweighted, −1.175), the average worker (−0.606), the average woman (−0.519), the average managerial position (−0.421), and large cells only (−0.418). All are negative. Their magnitudes span a factor of three, and the association is strongest in small markets.

The shaded bands are the sharp worst-case bounds under suppression, discussed in Section 6. The darker band holds at a continuity correction of 0.5 and stays below zero; the lighter band, at 0.25, **crosses zero**.

This is why the claims here are about direction and shape, never about effect size.

---

### **4. Testing Whether the Arithmetic Produces It**

<p align="center"><img width="780" alt="fig5_randomization" src="https://github.com/user-attachments/assets/e4cee523-e0cc-4239-bf60-df5e4b7d67b5" /></p>

**Figure 5. The observed slope sits far outside anything chance produces.** The odds ratio and the female share are computed from the same cell counts, so the obvious objection is that the arithmetic alone generates a negative slope.

EEO-1 cells are administrative enumerations, not survey samples, so the right null is a randomization over the observed table. In every cell, female, male, manager and non-manager totals are held fixed and only the association between sex and management status is removed by hypergeometric resampling. The female share — the regressor — is therefore untouched.

Across 200 randomizations the slope centres on zero, with a 95% range of [−0.150, +0.142]. The observed coefficient is **−1.175**, about fifteen null standard deviations away, and no randomization comes close. A stricter null that imposes one constant gender gap everywhere gives the same answer. The observed relationship requires the odds ratio itself to vary with female share.

**Every other threat tested:**

| Challenge | Test | Result |
|---|---|---|
| **Is it a local labor market confounder?** | Industry and CBSA fixed effects together, comparing industries *within* the same labor market. Every market-level factor drops out. | **−0.999** (t = −5.76) against −1.114 on the same sample. About 90% survives. |
| **Is it specific to EEO-1?** | The same analysis in the Census ACS, 2022–2024, built from individual survey responses (Section 5). | Absolute **+0.748**, relative **−1.599**; 2024 alone −1.307. Same direction. |
| **Is it just job mix inside the plant?** | Control for each sex's share on the production floor and in skilled roles; compare managers with the tier directly below. | Coefficient falls 44%–68%; a smaller negative remainder in every version (Section 2). |
| Does the continuity correction create it? | Uncorrected estimate; correction shift by female-share bin. | The observed sample has no zero cells, so the headline uses **no correction**. The correction accounts for 4% of the coefficient. |
| Is it driven by one industry or city? | Leave-one-industry-out; leave-one-CBSA-out over the 20 largest. | [−1.254, −1.094] and [−1.240, −1.165]. |
| Is the t-statistic a clustering artefact? | Homoskedastic, CBSA- and industry-clustered, wild cluster bootstrap over 21 industries. | SEs rise up to 1.9×. None of 499 bootstrap draws is as extreme (p < 0.002). |
| Are the fixed effects dead weight? | Joint F-tests. | Industry F = 11.9, region F = 7.7, both p < 0.0001. |
| Is the design numerically stable? | Condition number, VIF, standardized refit. | Condition number 164, or 14 with fixed effects absorbed; VIF ≤ 1.37. |
| Is measurement error behind the OLS gap? | Two instruments, Anderson–Rubin, Conley-style sensitivity. | AR set [−2.24, −1.62], but both instruments plausibly violate exclusion. **Reported as sensitivity only.** |
| Would a panel identify a causal effect? | Variance decomposition first. | The regressor moves **4.9%** within cells over seven years. Not estimated. |

---

### **5. A Second, Independent Source**

Everything above comes from one dataset, so the obvious question is whether the pattern belongs to EEO-1 rather than to manufacturing. The American Community Survey asks workers directly. It is not subject to the EEOC's suppression rule, the 100-employee threshold, or employer job classification. The same analysis was rebuilt from IPUMS USA microdata for 2022–2024: private, employed wage and salary workers in manufacturing, grouped by metro area and industry — 937 groups in 178 metro areas, with a median of 136 respondents each. Managers are management occupations, excluding chief executives, plus first-line supervisors, to mirror EEO-1's first- and mid-level category.

| Measure | EEO-1, 2022–23 | ACS, 2022–24 | ACS, 2024 alone |
|---|---:|---:|---:|
| Women's share of managers | +0.297*** | **+0.748*** (t = 12.4) | +0.783*** |
| Women's relative odds of management | −1.175*** | **−1.599*** (t = −4.2) | −1.307** |

The same divergence appears in a different source, and it holds in 2024 by itself. It also survives inverse-variance weighting (−0.970), employment weighting (−1.087), and a stricter definition counting management occupations only (−2.007). In the largest groups (200+ respondents, 301 groups) the estimate is negative but not distinguishable from zero (−0.597, t = −0.98) — the same pattern as in EEO-1, where the association is weakest in large markets.

**The two sources cannot be compared group by group.** Across the 788 groups present in both, they agree on the female share of the workforce (correlation 0.70) but barely on the relative odds (0.12). Once the survey weights are accounted for, about 99% of the variation in an individual ACS group's estimate is sampling noise, which caps any possible correlation near 0.09. The weak agreement is what noise alone would produce. The sources can be compared only in aggregate, where they agree on direction. For the same reason, neither dataset supports claims about which particular metro area is worse.

Two differences remain in the definitions themselves: ACS metro areas are where people live, not where they work, and IPUMS assigns them from public-use areas, so three small-manufacturing states (Montana, South Dakota, Vermont) drop out.

---

### **6. What the Published Data Cannot Tell Us**

<p align="center"><img width="780" alt="fig7_suppression" src="https://github.com/user-attachments/assets/3107fc1e-af16-4e6f-9900-a10b89a6f573" /></p>

**Figure 6. Suppression falls where the answer matters most.** The EEOC withholds any count below three. In cells under 250 employees, 63% have the female mid-management count withheld; above 1,000 employees, only 1–2% do. Figure 4 already showed that the association is strongest in small markets — so the data are thinnest exactly where the signal is largest.

Because the rule is deterministic, a selection model has no exclusion restriction to work with. Bounds are the right tool, and because OLS is linear in the outcome, the sharp bounds follow in closed form — equivalent to searching all 3²⁷⁵ admissible assignments of the withheld counts. The 275 suppressed cells carry **12.2%** of the estimation weight.

| Continuity correction | Current rule | True zeros flagged separately |
|---|---|---|
| 0 | lower bound diverges | **[−1.46, −0.67]** |
| 0.25 | [−2.01, **+0.35**] | **[−1.47, −0.78]** |
| 0.5 | [−1.86, −0.08] | [−1.48, −0.87] |
| 1.0 | [−1.76, −0.48] | [−1.51, −1.01] |

Under the current rule the sign is **not identified** at small corrections. Publishing the [0, 2] bounds would add nothing — they are already implied by the rule, and these bounds are computed from them. What cannot be recovered is whether a withheld count is zero or one-to-two, and it is the zero case that drives the lower bound to minus infinity.

**Flagging true zeros separately closes the set.** The sign becomes identified at every correction, the set narrows two-and-a-half to three-and-a-half times, and the dependence on the correction largely disappears.

---

### **7. Data Integrity Audit**

<p align="center"><img width="780" alt="fig6_regime_break" src="https://github.com/user-attachments/assets/bf39693b-5333-4d97-9142-41759f3c8871" /></p>

**Figure 7. A filing-regime break, not an economic one.** Employees per EEO-1 reporting unit in manufacturing CBSA cells hold between 233 and 240 from 2015 to 2021, then fall to about 113 in 2022 and stay there. No economic event halves plant size in a year. The EEOC consolidated its establishment report types, discontinued the Type 6 establishment list, and barred PEO aggregate filing — so the reporting unit itself changed.

The main analysis therefore uses 2022–2023 only, and **no specification pools across the break**. The 2015–2021 files are used as a comparison under a different filing regime, not as an independent sample: 76.5% of cells appear in both.

| # | Problem | Resolution |
|---|---|---|
| 1 | Filing-regime break at 2022 (Figure 7). | Two regimes, estimated separately. |
| 2 | Ratios absorb the break imperfectly: matched cells show ΔR = −0.015 (p = 0.010) against a +0.004 within-regime benchmark. | Second-order, 4–13% of one SD. Reported. |
| 3 | The original outcome placed the regressor in its own denominator. | Replaced by the log odds ratio, and checked by randomization (Figure 5) rather than by argument. |
| 4 | EEO-1 publishes CBSA names on an older delineation vintage; exact matching reached 78.5%. | Anchor matching on leading city plus state: **98.4%**, zero collisions. |
| 5 | Executive tier: 86.6% suppressed, and executives are assigned to headquarters, not plants. | Not reported. The framing applies to first/mid-level management only. |
| 6 | Suppression is non-random (Figure 6). | Sharp bounds. Cells where the total manager count is also withheld hold at most two managers and fail the size filter by construction. |
| 7 | QCEW has no 3-digit detail for micropolitan areas, and its NAICS assignment differs from EEO-1's. | Demoted to a control. |
| 8 | Accounting consistency. | Seven identities checked in all 3,054 cells: **zero violations**. |
| 9 | ACS metro areas are places of residence assigned from public-use areas; three states drop out; individual ACS groups are mostly sampling noise. | Compared with EEO-1 only in aggregate. Group-level agreement reported with its noise ceiling (Section 5). |
| 10 | Specification search: outcome, geography and sample split were revised after seeing results. | Stated plainly. The randomization test and the bounds are the defences, not the 2015–2021 estimate. |

---

### **8. Full Results**

| Panel | Specification | Coefficient | n |
|---|---|---:|---:|
| **J3** | **robustness: industry + CBSA fixed effects, within-market comparison** | **−0.999*** (0.174)** | 2,630 |
| A1 | relative odds ~ female share, unweighted | −1.175*** (0.160) | 2,779 |
| **B1** | **absolute share of management ~ female share** | **+0.297*** (0.037)** | 2,779 |
| **C1** | **log female management rate** | **−0.833*** (0.146)** | 2,779 |
| **C2** | **log male management rate** | **+0.221*** (0.071)** | 2,779 |
| C3 | log overall management intensity | −0.090 (p = 0.21) | 2,779 |
| D | employment-weighted / manager-weighted | −0.606 / −0.421 | 2,779 |
| E | fixed-margin randomization null, 95% range | [−0.150, +0.142] | 2,779 |
| **G** | **sharp bounds, c = 0.5 / c = 0.25** | **[−1.86, −0.08] / [−2.01, +0.35]** | 3,054 |
| G | same, true zeros flagged, c = 0.25 | [−1.47, −0.78] | 3,054 |
| H | 2SLS, Anderson–Rubin set | [−2.24, −1.62] | 2,125 |
| I1 | 2015–2021 filing regime | −2.305*** (0.102) | 12,764 |
| I | pre-specified mobility (monopsony) test | −0.055 (p = 0.49) | 2,779 |
| J5 | economic magnitude, interquartile range of female share | odds ratio × 0.837 (−16%) | 2,779 |
| K1 | + floor and skilled-pipeline shares of each sex (same-cell main: −0.707) | −0.223** (t = −2.20) | 1,027 |
| K2 | managers per skilled tier below (same-cell main: −0.832) | −0.413*** (t = −3.02) | 1,136 |
| **L1** | **ACS 2022–2024, absolute / relative** | **+0.748*** / −1.599*** | 937 |
| L3 | ACS 2024 alone, relative | −1.307** (t = −2.14) | 331 |
| L4 | ACS–EEO-1 agreement on relative odds, group level (noise ceiling ≈ 0.09) | correlation 0.118 | 788 |

Fixed effects: NAICS-3 and Census region, except J3 (NAICS-3 and CBSA); the 2015–2021 regime adds year. Standard errors clustered by CBSA (EEO-1) or metro area (ACS). ACS models control for group size only; the survey has no establishment information. Complete output in `results_log.txt`.

**On precision.** Panel I1 reports t = −22.6. That is not evidence of certainty. These are cell means, so individual heterogeneity has been averaged away and the t-statistic is mechanically large. Aggregation shrinks variance and leaves bias untouched. The randomization test and the bounds carry the argument, not the p-values.

**How this started.** The project was designed around a monopsony mechanism: where workers have fewer employers to move between, women should fare worse. External mobility from QWI has no relationship with managerial representation in any specification. That test is kept in Panel I rather than deleted.

---

### **What the Data Support, and What They Do Not**

**Supported.** A cross-sectional ecological association between the female share of a local industry workforce and women's relative managerial representation odds, at the metro × industry level, in two independent sources. Roughly half to two-thirds of it reflects where women and men sit in the job ladder.

**Not supported.** Promotion, advancement, backlash, or any individual-level transition. These are stock distributions, not flows. The term used throughout is *representation odds*, not *access*. Kanter's tokenism and the Blalock–Yoder group-threat model both predict change at a threshold; this is a cross-section and tests neither.

**Not identified.** The magnitude, which ranges from about −0.40 to −2.31 across estimands, instruments and filing regimes — and, under the current suppression rule, the sign in EEO-1. Which component moves (women's rate or men's) also differs between sources, and neither source supports claims about individual metro areas.

**Unexplained.** Establishment size is the second-strongest predictor (−0.14 to −0.17), stable across the filing regimes, but it shrinks by 35% in large cells, so part of it is selection. No mechanism is proposed.

---

### **Figure Guide**

| Figure | File | Shows | Section |
|---|---|---|---|
| 1 | `fig1_counts_rise.png` | Women's share of management rises with female share | 1 |
| 2 | `fig2_odds_fall.png` | Women's relative odds of management fall with female share | 1 |
| 3 | `fig3_decomposition.png` | Management rate by sex; overall intensity flat | 2 |
| 4 | `fig4_estimand_bounds.png` | Five estimands against the suppression bounds | 3 |
| 5 | `fig5_randomization.png` | Fixed-margin randomization null versus observed | 4 |
| 6 | `fig7_suppression.png` | Share of cells withheld, by cell size | 6 |
| 7 | `fig6_regime_break.png` | Employees per reporting unit, 2015–2023 | 7 |

---

### **Repository Contents**

| File | Description |
|---|---|
| `Gender_Management_Gap.py` | Analysis, Panels A–L. Writes `results_log.txt`. Runs from the shipped data alone. |
| `make_figures.py` | Builds all seven figures. Independent of the analysis script. |
| `build_dataset.py` | Source pipeline from raw EEO-1, QWI, QCEW and OMB files. |
| `gender_mgmt_cbsa_2023.csv.zip` | Main cross-section: 2,779 observed cells plus 275 carrying suppression bounds. |
| `gender_mgmt_panel_2015_2021.csv.zip` | 2015–2021 comparison panel, 12,764 cell-years. |
| `acs_mfg_cells_2022_2024.csv.zip` | ACS metro × industry × year aggregates (weighted and unweighted counts). No person-level records. |
| `results_log.txt` | Complete regression output. |
| `fig1` … `fig7` `.png` | The seven figures above. |
| `Technical_Documentation.md` | Definitions, schemas, estimator, diagnostics, limitations, withdrawn claims. |
| `JSM_2027_Submission.md` | Abstract, section choice and submission checklist. |

```bash
pip install pandas numpy scipy statsmodels matplotlib
python Gender_Management_Gap.py   # -> results_log.txt  (about 4 minutes)
python make_figures.py            # -> fig1 ... fig7
```

---

### **Data Sources**

| Source | Provider | Use |
|---|---|---|
| EEO-1 Public Use File, 2015–2023 | U.S. EEOC | Outcome: sex × job category × NAICS-3 × geography |
| Quarterly Workforce Indicators, 2023 | U.S. Census Bureau, LEHD | Worker flows; independent female-share measure |
| QCEW Annual Averages, 2023 | U.S. Bureau of Labor Statistics | Coverage ratio, establishment density |
| CBSA Delineation File, July 2023 | U.S. OMB / Census Bureau | Geographic crosswalk |
| American Community Survey, 2022–2024 (IPUMS USA) | U.S. Census Bureau via IPUMS | Independent replication from individual responses |

ACS data: Steven Ruggles, Sarah Flood, Matthew Sobek, Daniel Backman, Grace Cooper, Julia A. Rivera Drew, Stephanie Richards, Renae Rodgers, Jonathan Schroeder, and Kari C.W. Williams. *IPUMS USA: Version 16.0* [dataset]. Minneapolis, MN: IPUMS, 2025. https://doi.org/10.18128/D010.V16.0

---

**Sean (Yechan) Kim** · M.S. Analytics, Georgia Institute of Technology
