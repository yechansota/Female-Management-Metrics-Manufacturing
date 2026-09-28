"""
================================================================================
 build_dataset.py  —  source pipeline (reference implementation)
--------------------------------------------------------------------------------
 Rebuilds gender_mgmt_cbsa_2023.csv and gender_mgmt_panel_2015_2021.csv from raw
 federal files. Included for transparency and reuse; the analysis in
 Gender_Management_Gap.py runs from the shipped CSVs and does NOT require this.

 RAW INPUTS (not redistributed — see README for source URLs)
   EEO1_<year>_PUF.xlsx                       EEOC,   2015-2023
   qwi_<id>.csv                               Census LEHD, metro x NAICS3 x sex
   <year>_annual_by_area.zip                  BLS QCEW
   list1_2023.xlsx                            OMB CBSA delineation

 NOTES
   * `pip install python-calamine` makes the EEO-1 reads ~7x faster.
   * EEO-1 files stack every geography and industry aggregation level in one
     sheet. Filtering on NAICS3 alone double-counts. See select_cbsa_rows().
================================================================================
"""
import io, re, zipfile, warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

MFG3 = [str(x) for x in
        list(range(311, 317)) + list(range(321, 328)) + list(range(331, 338)) + [339]]
EEO1_COLS = ["Region", "Division", "State", "CBSA", "County", "NAICS2", "NAICS3",
             "NAICS3_Name", "Establishments", "TOTAL10", "FT10",
             "TOTAL1", "TOTAL1_2", "FT1", "FT1_2"]
GEO_ORDER = ["Region", "Division", "State", "CBSA", "County"]


# ------------------------------------------------------------------- helpers
def clean(s):
    return (s.astype(str).str.strip()
             .replace({"nan": np.nan, "None": np.nan, "": np.nan})
             .str.replace(r"\.0$", "", regex=True))


def anchor(title):
    """Vintage-robust CBSA key: leading principal city + first state abbrev.

    EEO-1 carries an older delineation vintage than the current OMB file, so
    'Austin-Round Rock, TX' must match 'Austin-Round Rock-San Marcos, TX'.
    Leading city and state are stable across vintages; trailing cities are not.
    """
    t = str(title)
    city, _, st = t.partition(",")
    return (re.split(r"[-/]", city)[0].strip().lower() + "|"
            + re.split(r"[-]", st.strip())[0].strip().upper()[:2])


def select_cbsa_rows(df):
    """Keep only CBSA x NAICS-3 rows. A null geography column means 'aggregated
    over that level', so the deepest non-null column defines the level."""
    level = pd.Series("Nation", index=df.index)
    for c in GEO_ORDER:
        level = level.mask(df[c].notna(), c)
    return df[(level == "CBSA") & (df.NAICS3.isin(MFG3))].copy()


def haldane_log_odds(df, c=0.5):
    """log odds of holding mid-management, women relative to men."""
    f1 = df.mid_f + c
    f0 = df.emp_f - df.mid_f + c
    m1 = (df.mid_tot - df.mid_f) + c
    m0 = (df.emp - df.emp_f) - (df.mid_tot - df.mid_f) + c
    return np.log((f1 / f0) / (m1 / m0))


# -------------------------------------------------------------------- EEO-1
def parse_eeo1(path, year):
    try:
        df = pd.read_excel(path, dtype=str, engine="calamine", usecols=EEO1_COLS)
    except Exception:
        df = pd.read_excel(path, dtype=str, usecols=EEO1_COLS)
    for c in EEO1_COLS:
        df[c] = clean(df[c])
    m = select_cbsa_rows(df)
    num = lambda s: pd.to_numeric(s.where(s != "*"), errors="coerce")
    out = pd.DataFrame({
        "year": year,
        "regime": 1 if year <= 2021 else 2,          # filing-regime break at 2022
        "region": m.Region, "state": m.State, "cbsa": m.CBSA,
        "naics3": m.NAICS3, "naics3_name": m.NAICS3_Name,
        "estab": num(m.Establishments), "emp": num(m.TOTAL10), "emp_f": num(m.FT10),
        "exec_tot": num(m.TOTAL1), "exec_f": num(m.FT1),
        "mid_tot": num(m.TOTAL1_2), "mid_f": num(m.FT1_2),
        "supp_ft1": (m.FT1 == "*").astype(int),
        "supp_ft1_2": (m.FT1_2 == "*").astype(int)})
    return out


# ---------------------------------------------------------------------- QWI
def build_qwi(path_or_zip):
    """Metro x NAICS-3 x sex annual rates. Values are masked where the LEHD
    status flag is not '1'; cells need all four quarters publishable."""
    key = ["geo_level", "geography", "ind_level", "industry", "sex", "agegrp",
           "year", "quarter"]
    val = ["EarnS", "Emp", "EmpS", "HirAS", "SepS"]
    sts = ["sEarnS", "sEmp", "sEmpS", "sHirAS", "sSepS"]

    def chunks():
        if str(path_or_zip).endswith(".zip"):
            z = zipfile.ZipFile(path_or_zip)
            name = [n for n in z.namelist()
                    if n.lower().endswith(".csv") and not n.startswith("__MACOSX")][0]
            with z.open(name) as fh:
                yield from pd.read_csv(io.TextIOWrapper(fh, "utf-8"), dtype=str,
                                       usecols=key + val + sts, chunksize=600_000)
        else:
            yield from pd.read_csv(path_or_zip, dtype=str,
                                   usecols=key + val + sts, chunksize=600_000)

    keep = []
    for ch in chunks():
        sel = ch[(ch.geo_level == "M") & (ch.ind_level == "3")
                 & (ch.agegrp == "A00") & (ch.industry.isin(MFG3))]
        if len(sel):
            keep.append(sel)
    d = pd.concat(keep, ignore_index=True)
    for v, s in zip(val, sts):
        d[v] = pd.to_numeric(d[v], errors="coerce").where(d[s] == "1")

    g = (d.groupby(["geography", "industry", "sex"], as_index=False)
           .agg(nq=("EmpS", "count"), nqs=("SepS", "count"), nqh=("HirAS", "count"),
                EmpS=("EmpS", "mean"), Sep=("SepS", "sum"),
                Hir=("HirAS", "sum"), Earn=("EarnS", "mean")))
    g = g[(g.nq == 4) & (g.nqs == 4) & (g.nqh == 4) & (g.EmpS > 0)]
    g["sep_rate"] = g.Sep / g.EmpS
    g["hire_rate"] = g.Hir / g.EmpS
    g["cbsa_code"] = g.geography.str[2:]           # state FIPS(2) + CBSA(5)

    w = g.pivot_table(index=["cbsa_code", "industry"], columns="sex",
                      values=["EmpS", "sep_rate", "hire_rate", "Earn"], aggfunc="first")
    w.columns = [f"{a}_{'all' if b == '0' else ('m' if b == '1' else 'f')}"
                 for a, b in w.columns]
    w = w.reset_index().rename(columns={"industry": "naics3"})
    w["sep_gap"] = w.sep_rate_f - w.sep_rate_m
    w["hire_gap"] = w.hire_rate_f - w.hire_rate_m
    w["earn_ratio"] = w.Earn_f / w.Earn_m
    w["fem_share_qwi"] = w.EmpS_f / (w.EmpS_f + w.EmpS_m)
    return w


# --------------------------------------------------------------------- QCEW
def build_qcew(area_zip):
    """CBSA x NAICS-3 private manufacturing. agglvl 45 is the CBSA/NAICS-3 level;
    micropolitan areas carry no 3-digit detail."""
    z = zipfile.ZipFile(area_zip)
    rows = []
    for mem in [m for m in z.namelist() if re.search(r"annual C\d+", m) and m.endswith(".csv")]:
        d = pd.read_csv(io.BytesIO(z.read(mem)), dtype=str)
        d = d[(d.own_code == "5") & (d.industry_code.isin(MFG3))]
        if len(d):
            rows.append(d[["area_fips", "industry_code", "agglvl_code",
                           "annual_avg_estabs_count", "annual_avg_emplvl"]])
    q = pd.concat(rows, ignore_index=True)
    q = q[q.agglvl_code == "45"]
    for c in ["annual_avg_estabs_count", "annual_avg_emplvl"]:
        q[c] = pd.to_numeric(q[c], errors="coerce")
    q["cbsa_code"] = q.area_fips.str.extract(r"C(\d{4})")[0] + "0"
    return q.rename(columns={"industry_code": "naics3",
                             "annual_avg_estabs_count": "q_estab",
                             "annual_avg_emplvl": "q_emp"})[
        ["cbsa_code", "naics3", "q_estab", "q_emp"]]


# ----------------------------------------------------------------- assembly
def anchor_match(eeo1, delineation_xlsx):
    dl = pd.read_excel(delineation_xlsx, header=2, dtype=str).rename(
        columns={"CBSA Code": "cbsa_code", "CBSA Title": "title",
                 "Metropolitan/Micropolitan Statistical Area": "cbsa_type"})
    dl = dl[dl.cbsa_code.str.match(r"^\d{5}$", na=False)].drop_duplicates("cbsa_code")
    dl["metro"] = dl.cbsa_type.str.contains("Metropolitan", na=False).astype(int)
    dl["exact"] = dl.title.str.replace(r"[^A-Za-z0-9,]", "", regex=True).str.lower()
    dl["anchor"] = dl.title.map(anchor)
    unique_anchor = dl[~dl.anchor.duplicated(keep=False)][["anchor", "cbsa_code", "metro"]]

    eeo1 = eeo1.copy()
    eeo1["exact"] = eeo1.cbsa.str.replace(r"[^A-Za-z0-9,]", "", regex=True).str.lower()
    eeo1["anchor"] = eeo1.cbsa.map(anchor)
    hit = eeo1.merge(dl[["exact", "cbsa_code", "metro"]], on="exact", how="left")
    miss = hit.cbsa_code.isna()
    fixed = (hit[miss].drop(columns=["cbsa_code", "metro"])
                      .merge(unique_anchor, on="anchor", how="left"))
    return pd.concat([hit[~miss], fixed], ignore_index=True)


def assemble(eeo1_years, qwi_path, qcew_zip, delineation_xlsx):
    panel = pd.concat([parse_eeo1(p, y) for y, p in eeo1_years.items()], ignore_index=True)
    panel["emp_per_estab"] = panel.emp / panel.estab
    panel["mgmt_intensity"] = (panel.exec_tot.fillna(0) + panel.mid_tot.fillna(0)) / panel.emp
    panel = anchor_match(panel, delineation_xlsx)

    # regime 2 cross-section: average 2022 and 2023 where both are present
    r2 = (panel[panel.regime == 2]
          .groupby(["cbsa_code", "cbsa", "naics3", "naics3_name", "region", "metro"],
                   dropna=False, as_index=False)
          .agg(n_years=("year", "size"), **{c: (c, "mean") for c in
               ["estab", "emp", "emp_f", "exec_tot", "exec_f", "mid_tot", "mid_f",
                "emp_per_estab", "mgmt_intensity", "supp_ft1", "supp_ft1_2"]}))
    r2 = (r2.merge(build_qwi(qwi_path), on=["cbsa_code", "naics3"], how="left")
            .merge(build_qcew(qcew_zip), on=["cbsa_code", "naics3"], how="left"))

    for df in (r2, panel):
        df["ln_theta"] = haldane_log_odds(df)
        df["fem_share_eeo1"] = df.emp_f / df.emp
        df["mid_fem_share"] = df.mid_f / df.mid_tot
        df["ln_emp"] = np.log(df.emp)
        df["ln_estab_size"] = np.log(df.emp_per_estab)
        df["R_mid"] = df.mid_fem_share / df.fem_share_eeo1
        df["R_exec"] = (df.exec_f / df.exec_tot) / df.fem_share_eeo1
    r2["fem_share"] = r2.fem_share_qwi.fillna(r2.fem_share_eeo1)
    r2["cov_cell"] = r2.emp / r2.q_emp

    keep = lambda df: df[(df.mid_tot >= 10) & (df.emp >= 50)
                         & df.cbsa_code.notna() & np.isfinite(df.ln_theta)]
    r2 = keep(r2[r2.sep_rate_all.notna()])
    r1 = keep(panel[panel.regime == 1])

    r2.to_csv("gender_mgmt_cbsa_2023.csv", index=False)
    r1.to_csv("gender_mgmt_panel_2015_2021.csv", index=False)
    print(f"regime 2: {len(r2):,} cells   regime 1: {len(r1):,} cell-years")
    return r2, r1


if __name__ == "__main__":
    EEO1 = {y: f"EEO1_{y}_PUF.xlsx" for y in range(2015, 2024)}
    assemble(EEO1, "qwi_metro_naics3_sex_2023.csv.zip",
             "2023_annual_by_area.zip", "list1_2023.xlsx")
