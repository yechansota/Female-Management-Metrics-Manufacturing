# **Reinterpreting Women's Leadership Metrics** 

### *Are We Correctly Measuring the 'Female Share of Management'?*
<p align="center">
  <strong>The Two Faces of Women's Managerial Representation in Manufacturing — Analyzing the Illusion Between Absolute Share and Relative Odds</strong><br>
  <em>EEO-1 · QWI · QCEW  |  CBSA × NAICS-3  |  2022–2023 main cross-section, 2015–2021 comparison  |  2,779 local labor markets</em><br>
</p>

---


Yechan Kim <yechansota@gmail.com>
8:58 AM (15 minutes ago)
to me

### **Project Motivation**

When organizations, researchers, and policymakers assess women's representation in management, they typically begin with one number: the percentage of managers who are women. This measure is widely used because it is easy to understand and appears in both workforce disclosures and academic research.
 
However, this statistic answers only one question: **what share of management positions are held by women?**
It does not answer a different and equally important question: **how likely is an employed woman to hold a management position relative to an employed man?**
 
Because the first measure mechanically rises when more women enter the workforce, the two measures can move in opposite directions. Women's share of management can increase even while women's relative managerial representation declines.

Manufacturing is where this matters most directly. First- and mid-level managers — production supervisors, shift leads, area managers — are the entry point to every tier above them. If women do not reach that tier in proportion to their presence on the floor, there is no pipeline further up.

This project asks a single question of the EEOC's own data: **in U.S. manufacturing, do the absolute share and the relative odds tell the same story?** They do not.

This study compares local industry cells at one point in time. It does not track individual employees, promotions, or career transitions. The results therefore describe a pattern in workforce composition, not the effect of adding more women to a workplace.

| Measure | Coefficient on female share of the workforce |
|---|---:|
| Women's **share of** management | **+0.297*** |
| Women's **odds of holding** management, relative to men in the same cell | **−1.175*** |

Neither number is wrong. They answer different questions, and reporting practice overwhelmingly uses the first.

The divergence survives a fixed-margin randomization test, five weighting schemes, industry and city influence checks, and a comparison of industries *within* the same labor market. **It does not survive disclosure suppression intact.** Once the cells the EEOC withholds are bounded, the sign of the relative measure is no longer identified — and a specific, low-cost change to the release rule would restore it.

---

### **1. The Divergence**
<img width="1680" height="1160" alt="fig1_counts_rise" src="https://github.com/user-attachments/assets/3f802d2d-a50d-401e-a4c8-382d28a91a31" />
<img width="1680" height="1160" alt="fig2_odds_fall" src="https://github.com/user-attachments/assets/c0e1ed3c-f0e5-441a-b08c-c8e8799da97d" />

**Figures 1 and 2. The same cells, read two ways.** Each point is the average of one-twelfth of the 2,779 metropolitan-area × manufacturing-subsector cells, ordered by the female share of that cell's workforce.

On the left, women's share of mid-management rises steadily with their share of the workforce. This reproduces the established finding — Taylor, Buck, Bloch and Turgeon (2019) reached it with 195,534 EEO-1 workplaces from 1980–2005 — and it is the measure most workforce reporting relies on.

On the right, the same cells are measured as women's odds of holding management relative to men's, after absorbing industry and region. Now the line falls. It drops steeply until female share reaches about a quarter, then flattens; there is no upturn. Error bars are 95% intervals, and the dashed line marks parity.

Where there are more women, there are **more** women managers — and **fewer women managers per woman**.

---

### **2. Where the Divergence Comes From**

<img width="1680" height="1160" alt="fig3_decomposition" src="https://github.com/user-attachments/assets/6ea0b651-6b10-483f-b3a2-8012d086fbbd" />


**Figure 3. Positions are reallocated, not removed.** The odds ratio is split into its two components: the share of employed women who hold management, and the share of employed men who do.

As female share rises, women's management rate **falls** (−0.833) while men's **rises** (+0.221). The overall managerial layer does not thin: management intensity is flat (−0.090, p = 0.21). That rules out the most obvious structural explanation — that female-intensive industries simply have flatter hierarchies. The positions exist; they are allocated differently by sex.

**What this means in practice.** A ten-point increase in female share goes with an 11% reduction in women's relative odds. Across the interquartile range (0.21 to 0.37) it is 16%: women's management rate moves from 8.7% to 7.7% while men's moves from 10.1% to 10.5%. In a median cell employing 254 women, that is roughly **22 versus 19.5 women in mid-management**. The illustration holds female employment fixed while moving the share, so it describes the cross-sectional association, not the effect of adding women.

---

### **3. How Confident to Be**

<img width="1680" height="1160" alt="fig4_estimand_bounds" src="https://github.com/user-attachments/assets/f5b427c3-9740-4566-955a-0a3b891e3063" />

**Figure 4. Direction is stable; magnitude is not.** Five weighting schemes are shown, each answering a different question — the average local industry cell (unweighted, −1.175), the average worker (−0.606), the average woman (−0.519), the average managerial position (−0.421), and large cells only (−0.418). All are negative. Their magnitudes span a factor of three, and the association is strongest in small markets.

The shaded bands are the sharp worst-case bounds under suppression, discussed in Section 5. The darker band holds at a continuity correction of 0.5 and stays below zero; the lighter band, at 0.25, **crosses zero**.

This is why the claims here are about direction and shape, never about effect size.

---

### **4. Testing Whether the Arithmetic Produces It**

<img width="1680" height="1160" alt="fig5_randomization" src="https://github.com/user-attachments/assets/e4cee523-e0cc-4239-bf60-df5e4b7d67b5" />


**Figure 5. The observed slope sits far outside anything chance produces.** The odds ratio and the female share are computed from the same cell counts, so the obvious objection is that the arithmetic alone generates a negative slope.

EEO-1 cells are administrative enumerations, not survey samples, so the right null is a randomization over the observed table. In every cell, female, male, manager and non-manager totals are held fixed and only the association between sex and management status is removed by hypergeometric resampling. The female share — the regressor — is therefore untouched.

Across repeated randomizations the slope centres on zero, with a 95% range of [−0.150, +0.142]. The observed coefficient is **−1.175**, about fifteen null standard deviations away. A stricter null that imposes one constant gender gap everywhere gives the same answer. The observed relationship requires the odds ratio itself to vary with female share.

**Every other threat tested:**

| Challenge | Test | Result |
|---|---|---|
| **Is it a local labor market confounder?** | Industry and CBSA fixed effects together, comparing industries *within* the same labor market. Every market-level factor drops out. | **−0.999** (t = −5.76) against −1.114 on the same sample. About 90% survives. |
| Does the continuity correction create it? | Uncorrected estimate; correction shift by female-share bin. | The observed sample has no zero cells, so the headline uses **no correction**. The correction accounts for 4% of the coefficient. |
| Is it driven by one industry or city? | Leave-one-industry-out; leave-one-CBSA-out over the 20 largest. | [−1.254, −1.094] and [−1.240, −1.165]. |
| Is the t-statistic a clustering artefact? | Homoskedastic, CBSA- and industry-clustered, wild cluster bootstrap over 21 industries. | SEs rise up to 1.9×; bootstrap p < 0.001. |
| Are the fixed effects dead weight? | Joint F-tests. | Industry F = 11.9, region F = 7.7, both p < 0.0001. |
| Is the design numerically stable? | Condition number, VIF, standardized refit. | Condition number 164, or 14 with fixed effects absorbed; VIF ≤ 1.37. |
| Is measurement error behind the OLS gap? | Two instruments, Anderson–Rubin, Conley-style sensitivity. | AR set [−2.24, −1.62], but both instruments plausibly violate exclusion. **Reported as sensitivity only.** |
| Would a panel identify a causal effect? | Variance decomposition first. | The regressor moves **4.9%** within cells over seven years. Not estimated. |

---

### **5. What the Published Data Cannot Tell Us**

<img width="1680" height="1160" alt="fig7_suppression" src="https://github.com/user-attachments/assets/3107fc1e-af16-4e6f-9900-a10b89a6f573" />

**Figure 6. Suppression falls where the answer matters most.** The EEOC withholds any count below three. In cells under 250 employees, 63% have the female mid-management count withheld; above 1,000 employees, almost none do. Figure 4 already showed that the association is strongest in small markets — so the data are thinnest exactly where the signal is largest.

Because the rule is deterministic, a selection model has no exclusion restriction to work with. Bounds are the right tool, and because OLS is linear in the outcome, the sharp bounds follow in closed form — equivalent to searching all 3²⁷⁵ admissible assignments of the withheld counts. The 275 suppressed cells carry **12.2%** of the estimation weight.

| Continuity correction | Current rule | True zeros flagged separately |
|---|---|---|
| 0 | lower bound diverges | **[−1.46, −0.67]** |
| 0.25 | [−2.01, **+0.35**] | **[−1.47, −0.78]** |
| 0.5 | [−1.86, −0.08] | [−1.48, −0.87] |
| 1.0 | [−1.76, −0.48] | [−1.51, −1.01] |

Under the current rule the sign is **not identified** at small corrections. Publishing the [0, 2] bounds would add nothing — they are already implied by the rule, and these bounds are computed from them. What cannot be recovered is whether a withheld count is zero or one-to-two, and it is the zero case that drives the lower bound to minus infinity.

**Flagging true zeros separately closes the set.** The sign becomes identified at every correction, the set narrows roughly threefold, and the dependence on the correction largely disappears.

---

### **6. Data Integrity Audit**

<img width="1680" height="1160" alt="fig6_regime_break" src="https://github.com/user-attachments/assets/bf39693b-5333-4d97-9142-41759f3c8871" />


**Figure 7. A filing-regime break, not an economic one.** Employees per EEO-1 reporting unit in manufacturing CBSA cells hold near 233 from 2015 to 2021, then fall to about 113 in 2022 and stay there. No economic event halves plant size in a year. The EEOC consolidated its establishment report types, discontinued the Type 6 establishment list, and barred PEO aggregate filing — so the reporting unit itself changed.

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
| 9 | Specification search: outcome, geography and sample split were revised after seeing results. | Stated plainly. The randomization test and the bounds are the defences, not the 2015–2021 estimate. |

---

### **7. Full Results**

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

Fixed effects: NAICS-3 and Census region, except J3 (NAICS-3 and CBSA); the 2015–2021 regime adds year. Standard errors clustered by CBSA. Complete output in `results_log.txt`.

**On precision.** Panel I1 reports t = −22.6. That is not evidence of certainty. These are cell means, so individual heterogeneity has been averaged away and the t-statistic is mechanically large. Aggregation shrinks variance and leaves bias untouched. The randomization test and the bounds carry the argument, not the p-values.

**How this started.** The project was designed around a monopsony mechanism: where workers have fewer employers to move between, women should fare worse. External mobility from QWI has no relationship with managerial representation in any specification. That test is kept in Panel I rather than deleted.

---

### **What the Data Support, and What They Do Not**

**Supported.** A cross-sectional ecological association between the female share of a local industry workforce and women's relative managerial representation odds, at the CBSA × NAICS-3 level, in the observed cells.

**Not supported.** Promotion, advancement, backlash, or any individual-level transition. These are stock distributions, not flows. The term used throughout is *representation odds*, not *access*. Kanter's tokenism and the Blalock–Yoder group-threat model both predict change at a threshold; this is a cross-section and tests neither.

**Not identified.** The magnitude, which ranges from −0.42 to −2.24 across estimands and specifications — and, under the current suppression rule, the sign.

**Unexplained.** Establishment size is the second-strongest predictor (−0.14 to −0.17), stable across the filing regimes, but it shrinks by 36% in large cells, so part of it is selection. No mechanism is proposed.

---

### **Figure Guide**

| Figure | File | Shows | Section |
|---|---|---|---|
| 1 | `fig1_counts_rise.png` | Women's share of management rises with female share | 1 |
| 2 | `fig2_odds_fall.png` | Women's relative odds of management fall with female share | 1 |
| 3 | `fig3_decomposition.png` | Management rate by sex; overall intensity flat | 2 |
| 4 | `fig4_estimand_bounds.png` | Five estimands against the suppression bounds | 3 |
| 5 | `fig5_randomization.png` | Fixed-margin randomization null versus observed | 4 |
| 6 | `fig7_suppression.png` | Share of cells withheld, by cell size | 5 |
| 7 | `fig6_regime_break.png` | Employees per reporting unit, 2015–2023 | 6 |

---

### **Repository Contents**

| File | Description |
|---|---|
| `Gender_Management_Gap.py` | Analysis, Panels A–J. Writes `results_log.txt`. Runs from the shipped data alone. |
| `make_figures.py` | Builds all seven figures. Independent of the analysis script. |
| `build_dataset.py` | Source pipeline from raw EEO-1, QWI, QCEW and OMB files. |
| `gender_mgmt_cbsa_2023.csv.zip` | Main cross-section: 2,779 observed cells plus 275 carrying suppression bounds. |
| `gender_mgmt_panel_2015_2021.csv.zip` | 2015–2021 comparison panel, 12,764 cell-years. |
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

---

**Sean (Yechan) Kim** · M.S. Analytics, Georgia Institute of Technology
