"""Count Yes/No/Abstain/Absent per country per year on Israel-Palestine UNGA roll calls.

Usage: python3 -I analyze.py <UNVotes-1.RData or .pkl> <outdir> [un-project ga_votes_12countries.csv]
Selection rule: see SELECTION_RULE.md (fixed before results were viewed).
"""
import sys, re, os
import pandas as pd

COUNTRIES = ["USA", "CAN", "GBR", "FRA", "DEU", "IRL", "NOR", "ESP", "QAT", "TUR", "IRN", "EGY"]
# Correlates of War codes (codebook: ccode = COW code). Used instead of `Country`, which holds
# full names (not ISO3) for 2019 rows and is blank for one row per roll call from Sep 2023.
COW = {"2": "USA", "20": "CAN", "200": "GBR", "220": "FRA", "255": "DEU", "205": "IRL", "385": "NOR",
       "230": "ESP", "694": "QAT", "640": "TUR", "630": "IRN", "651": "EGY"}
TEXT_RE = re.compile(r"PALESTIN|ISRAEL|GAZA|JERUSALEM|UNRWA|OCCUPIED ARAB|OCCUPIED SYRIAN|GOLAN|MIDDLE EAST|NEAR EAST", re.I)
VOTE = {1: "Yes", 2: "Abstain", 3: "No", 8: "Absent"}


def load(path):
    if path.endswith(".pkl"):
        return pd.read_pickle(path)
    import pyreadr
    return next(iter(pyreadr.read_r(path).values()))


def extension(ext_csv, after, out):
    """Secondary source (un-project.org per-country GA votes) for votes after Voeten's last selected date.
    Same text regex; Voeten's `me` flag is unavailable there, so this is text-route only.
    Absent = 'non_voting'. Each roll call is keyed by (res, date)."""
    u = pd.read_csv(ext_csv).fillna("")
    u = u[(u["date"] > after) & u["res"].str.startswith("A/RES") & u["title"].str.contains(TEXT_RE)].copy()
    u["year"] = u["date"].str[:4].astype(int)
    u["choice"] = u["pos"].map({"yes": "Yes", "no": "No", "abstain": "Abstain", "non_voting": "Absent"})
    u.drop_duplicates(["C", "res", "date"])[["C", "res", "date", "choice", "title"]].to_csv(f"{out}/ext_country_votes_long.csv", index=False)
    t = u.pivot_table(index=["C", "year"], columns="choice", values="res", aggfunc="count", fill_value=0)
    for c in ["Yes", "No", "Abstain", "Absent"]:
        if c not in t:
            t[c] = 0
    t = t[["Yes", "No", "Abstain", "Absent"]].reset_index().rename(columns={"C": "Country"})
    t.to_csv(f"{out}/ext_country_year_counts.csv", index=False)
    rc = u.drop_duplicates(["res", "date"])
    return f"EXTENSION (un-project.org, text route only, after {after}): {len(rc)} roll calls " + str(rc.groupby("year").size().to_dict())


def main(src, out):
    os.makedirs(out, exist_ok=True)
    df = load(src)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Implementation fixes (logged in votes.md):
    #  - amend/para are NaN for all pre-2020 rows; NaN = not flagged.
    #  - in the v33 file, rcid is not a stable roll-call key for 2023-24 (same rcid on different
    #    resolutions), so a roll call is keyed by (unres, date) and selection is applied per row.
    df["amend"] = df["amend"].fillna(0)
    df["para"] = df["para"].fillna(0)
    df = df[df["date"] >= "1993-01-01"].copy()
    df["cc"] = df["ccode"].astype(str).str.replace(r"\.0$", "", regex=True)
    df.loc[df["ccode"].isna(), "cc"] = None
    df["key"] = df["unres"].astype(str) + "|" + df["date"].dt.strftime("%Y-%m-%d")
    df["by_me"] = df["me"] == 1
    df["by_text"] = (df["short"].fillna("") + " " + df["descr"].fillna("")).str.contains(TEXT_RE)
    # Turkey imputation: from Sep 2023 each roll call has one row with blank ccode and no 640 row.
    df["tur_imputed"] = False
    for k, g in df.groupby("key"):
        if g["cc"].isna().sum() == 1 and not (g["cc"] == "640").any():
            idx = g.index[g["cc"].isna()][0]
            df.loc[idx, "cc"] = "640"; df.loc[idx, "tur_imputed"] = True
    df["C"] = df["cc"].map(COW)
    # duplicate records of the same vote (different rcid, same resolution/date/country): keep first whole-resolution row
    df = df.sort_values(["para", "amend", "rcid"]).drop_duplicates(["key", "cc", "para", "amend"], keep="first")
    hit = df[(df["by_me"] | df["by_text"])]
    rc = hit.groupby("key").agg(date=("date", "first"), unres=("unres", "first"), short=("short", "first"),
                                amend=("amend", "max"), para=("para", "max"), by_me=("by_me", "max"),
                                by_text=("by_text", "max"), rows=("vote", "size"),
                                off_yes=("yes", "first"), off_no=("no", "first"), off_abs=("abstain", "first")).reset_index()
    side = rc[(rc["amend"] == 1) | (rc["para"] == 1)]
    sel = rc[(rc["amend"] == 0) & (rc["para"] == 0)].copy()
    sel["route"] = sel.apply(lambda r: "me+text" if r.by_me and r.by_text else ("me_only" if r.by_me else "text_only"), axis=1)
    sel.sort_values("date").to_csv(f"{out}/selected_rollcalls.csv", index=False)

    v = df[df["key"].isin(sel["key"]) & df["C"].notna() & (df["amend"] == 0) & (df["para"] == 0)].copy()
    v = v.drop_duplicates(["key", "C"])
    v["Country"] = v["C"]
    v = v[v["vote"].isin(VOTE.keys())]
    v["year"] = v["date"].dt.year
    v["choice"] = v["vote"].astype(int).map(VOTE)
    v[["Country", "key", "unres", "date", "choice", "tur_imputed"]].sort_values(["Country", "date"]).to_csv(f"{out}/country_votes_long.csv", index=False)
    cover = v.groupby(["Country", "year"]).size().unstack(0, fill_value=0)
    exp = sel.groupby(sel["date"].dt.year).size()
    gaps = [(c, y, int(cover.loc[y, c]) if y in cover.index else 0, int(exp[y])) for c in COUNTRIES for y in exp.index
            if (cover.loc[y, c] if (y in cover.index and c in cover) else 0) != exp[y]]

    tab = v.pivot_table(index=["Country", "year"], columns="choice", values="rcid", aggfunc="count", fill_value=0)
    for c in VOTE.values():
        if c not in tab:
            tab[c] = 0
    tab = tab[["Yes", "No", "Abstain", "Absent"]].reset_index()
    cast = tab["Yes"] + tab["No"] + tab["Abstain"]
    tab["yes_share"] = (tab["Yes"] / cast.where(cast > 0)).round(3)
    tab["modal"] = tab[["Yes", "No", "Abstain"]].idxmax(axis=1)
    tab.to_csv(f"{out}/country_year_counts.csv", index=False)

    lines = []
    lines.append(f"Roll calls selected (whole-resolution, >=1993): {len(sel)}; routes: {sel['route'].value_counts().to_dict()}")
    lines.append(f"Amendment/paragraph roll calls excluded: {len(side)}")
    lines.append(f"Dataset last vote date: {df['date'].max().date()}; last selected: {sel['date'].max().date()}")
    lines.append(f"Turkey rows imputed from blank ccode: {int(v['tur_imputed'].sum())}")
    lines.append("Coverage gaps (country, year, rows found, roll calls selected): " + str(gaps))
    lines.append("Votes per year selected: " + str(sel.groupby(sel['date'].dt.year).size().to_dict()))
    for c in COUNTRIES:
        t = tab[tab["Country"] == c].set_index("year")
        if t.empty:
            lines.append(f"{c}: no data"); continue
        tot = t[["Yes", "No", "Abstain", "Absent"]].sum()
        lines.append(f"\n{c}: totals {tot.to_dict()}; overall yes-share {round(tot.Yes/(tot.Yes+tot.No+tot.Abstain),3)}")
        prev_modal = None
        ys = t["yes_share"]
        for y in t.index:
            prior = ys[(ys.index < y) & (ys.index >= y - 3)]
            note = []
            if len(prior) and pd.notna(ys[y]) and abs(ys[y] - prior.mean()) >= 0.15:
                note.append(f"yes-share {ys[y]} vs prior-3yr mean {round(prior.mean(),3)}")
            if prev_modal is not None and t.loc[y, "modal"] != prev_modal:
                note.append(f"modal vote {prev_modal}->{t.loc[y,'modal']}")
            prev_modal = t.loc[y, "modal"]
            if note:
                lines.append(f"  {y}: " + "; ".join(note))
    if len(sys.argv) > 3:
        lines.append(extension(sys.argv[3], str(sel["date"].max().date()), out))
    open(f"{out}/summary.txt", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
