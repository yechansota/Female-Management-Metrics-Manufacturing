# JSM 2027 — Contributed Abstract Submission

**Submission window**: December 1, 2026 – February 1, 2027
**Decision**: approximately April 1, 2027
**Abstract editing reopens**: April 1 – May 31, 2027

---

## Submission Record

| Field | Entry |
|---|---|
| **Title** | Suppression Can Cost a Sign: Measuring Women's Managerial Representation in U.S. Manufacturing |
| **Primary sponsor** | ASA Section on **Government Statistics** |
| **Session subtype** | **Speed** (4-minute talk + e-poster) |
| **Alternate subtypes** | **Yes — check this box.** The committee cannot place every paper abstract; flexibility raises acceptance odds. |
| **Presenting author** | Sean (Yechan) Kim |
| **Affiliation** | Georgia Institute of Technology |
| **Email** | *confirm before submission* |
| **Co-authors** | none |
| **Keywords** | disclosure limitation; partial identification; public-use files; administrative data; measurement; workforce statistics |

**Why Government Statistics.** The statistical contribution is that a federal
agency's deterministic suppression threshold, not sampling error, is what
constrains inference — and that a specific, costless-to-implement change to the
release rule would restore identification. Disclosure avoidance and public-use
file quality are core GSS topics. Social Statistics is the natural second choice
but places the work against the full field of applied social science. Business &
Economic Statistics fits least: the result is measurement, not causal labor
economics.

**Why Speed.** The argument reduces to two figures and one interval. The
e-poster format (42-inch landscape display) suits an interactive presentation of
the identified set, and speed sessions are less oversubscribed than contributed
papers.

---

## Abstract — GSS version (submit this one)

**1175 characters including spaces. Limit is 1,200. No LaTeX, no special characters.**

```
Disclosure suppression in public-use files is usually treated as a loss of precision. We show it can cost identification of a sign. In EEOC EEO-1 Public Use Files across 2,779 metropolitan-area by NAICS-3 manufacturing cells in 2022-2023, two standard measures diverge: women's share of management rises with their share of the workforce (+0.30), while their odds of holding management relative to men fall (-1.17), as women's management rate declines, men's rises, and managerial intensity is unchanged. EEO-1 cells are administrative enumerations, not samples, so we test against a fixed-margin randomization null: the null interval is [-0.15, +0.14]. Counts below three are withheld, a deterministic rule with no exclusion restriction for selection models. Because OLS is linear in the outcome, sharp bounds follow in closed form. The 275 suppressed cells carry 12.2 percent of the estimation weight; the identified set is [-1.86, -0.08], admitting a positive sign under a weaker continuity correction. The sign is stable across weighting and specification but not under suppression. A flag separating true zeros from counts of one or two closes the set to [-1.47, -0.78].
```

---

## Abstract — Social Statistics alternate (do not submit alongside)

Only one primary sponsor may be named. This version exists for a later
submission elsewhere, should GSS decline. The hook moves from suppression to the
counts/odds divergence, the decomposition is promoted to its own sentence with
coefficients, and the closing recommendation addresses research practice rather
than agency practice — SSS attendees are data users, not data producers. The
suppression material is repositioned, not reduced: shortening it would shift the
headline onto the non-identification result.

**1155 characters including spaces.**

```
Two standard measures of women's managerial representation give opposite answers in the same data. Using EEOC EEO-1 Public Use Files across 2,779 metropolitan-area by NAICS-3 manufacturing cells in 2022-2023, women's share of management rises with their share of the workforce (+0.30), while their odds of holding management relative to men fall (-1.17). Decomposition locates the divergence: women's management rate declines (-0.83), men's rises (+0.22), and overall managerial intensity is unchanged. Positions are reallocated by sex, not removed, so flatter hierarchies in female-intensive industries do not explain the pattern. EEO-1 cells are administrative enumerations, not samples; against a fixed-margin randomization null the interval is [-0.15, +0.14]. Counts below three are withheld, and the 275 suppressed cells carry 12.2 percent of the estimation weight: sharp closed-form bounds place the identified set at [-1.86, -0.08], admitting a positive sign under a weaker continuity correction. The sign is stable across weighting and specification but not under suppression, so inequality estimates from these files should be reported as bounds.
```

---

## The Finding That Anchors the Closing Sentence

The agency withholds counts below three, so suppressed cells are known to hold
0, 1 or 2 female managers. Publishing those bounds would be circular — they are
already implied by the rule, and the sharp bounds below are computed from that
information alone. The binding constraint is different: **zero cannot be
distinguished from one or two**, and it is the zero case that makes the lower
bound diverge as the continuity correction goes to zero.

Flagging true zeros separately resolves it. Computed from the estimation sample:

| Continuity correction | Current, counts in {0,1,2} | True zeros flagged, counts in {1,2} | Width |
|---|---|---|---:|
| c = 0 | lower bound diverges | **[-1.462, -0.669]** | 0.79 |
| c = 0.25 | [-2.007, **+0.350**] | **[-1.470, -0.782]** | 0.69 |
| c = 0.50 | [-1.858, -0.077] | [-1.481, -0.872] | 0.61 |
| c = 1.00 | [-1.757, -0.481] | [-1.509, -1.007] | 0.50 |

Three things resolve at once: the sign becomes identified at every correction,
the set narrows by a factor of roughly 3.4, and the dependence on the correction
itself largely disappears. This table belongs on the poster. It is the only
quantitative evidence that the recommendation would work.

---

## Submission Checklist

| | Item | Notes |
|---|---|---|
| ☐ | Pay the abstract submission fee / registration deposit | Required **before** the submission form opens |
| ☐ | Log in via the link in the deposit confirmation email | |
| ☐ | Title, abstract, keywords | Paste as plain text; the system rejects LaTeX |
| ☐ | Primary sponsor: Government Statistics | |
| ☐ | Session subtype: Speed | |
| ☐ | **Alternate subtypes: yes** | Single highest-leverage box on the form |
| ☐ | Author contact details | One presenting author only; unique email required |
| ☐ | Verify the character count in the form itself | Counters differ; 25 characters of margin are built in |
| ☐ | Draft manuscript to the session chair | Due mid-May 2027. Slides, a handout or a detailed outline all qualify |

---

## What Still Needs Building Before May

1. **Speed talk, four minutes.** Four slides: the divergence (fig1 + fig2), the
   decomposition (fig3), the bounds (fig4), the zero-flag table above.
2. **E-poster layout**, 42-inch landscape.
3. **Draft manuscript.** `Technical_Documentation.md` is most of it; it needs an
   introduction, a literature paragraph, and the zero-flag table promoted to a
   result.
4. **Optional strengthening**: the counterfactual bounds table could be extended
   to alternative release rules — noise infusion, coarser flags — which would
   broaden the recommendation beyond a single fix.

---

## Known Weak Points a Discussant Will Raise

- **Cross-sectional ecological association.** No promotion or transition process
  is identified. The abstract says "representation", never "access".
- **Magnitude is not identified**, spanning roughly -0.4 to -2.2 across estimands.
  The abstract claims direction and shape only.
- **Specification search.** The outcome, geographic unit and sample split were
  revised after seeing results. The randomization test and the bounds are the
  defenses; the 2015-2021 estimate is not, because 76.5 percent of cells overlap.
- **The 2015-2021 regime is deliberately absent from the abstract.** There is no
  room to separate the two filing regimes properly in 1,200 characters, and
  mentioning both without that separation invites the objection directly.
