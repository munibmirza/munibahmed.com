"""Example procedure for a 'Sales Register' sheet.

Demonstrates a realistic audit-style check. Adapt column names to your file.
"""

import pandas as pd


def run(df: pd.DataFrame, **_) -> dict:
    df.columns = [str(c).strip() for c in df.columns]

    # --- 1. cleaning ---
    df = df.dropna(how="all")
    for c in df.select_dtypes(include="object").columns:
        df[c] = df[c].astype(str).str.strip()

    # --- 2. exception checks (only if the column exists) ---
    exceptions = []

    if "Invoice No" in df.columns:
        dup = df[df["Invoice No"].duplicated(keep=False)]
        if len(dup):
            exceptions.append(("Duplicate Invoice No", dup))

    if "Amount" in df.columns:
        amt = pd.to_numeric(df["Amount"], errors="coerce")
        neg = df[amt < 0]
        if len(neg):
            exceptions.append(("Negative Amount", neg))

    if "Date" in df.columns:
        dt = pd.to_datetime(df["Date"], errors="coerce")
        bad = df[dt.isna()]
        if len(bad):
            exceptions.append(("Invalid Date", bad))

    # --- 3. summary ---
    summary_rows = [("Total Rows", len(df))]
    if "Amount" in df.columns:
        amt = pd.to_numeric(df["Amount"], errors="coerce")
        summary_rows += [
            ("Total Amount", float(amt.sum(skipna=True))),
            ("Average Amount", float(amt.mean(skipna=True))),
            ("Max Amount", float(amt.max(skipna=True))),
        ]
    summary = pd.DataFrame(summary_rows, columns=["metric", "value"])

    reports = {"summary": summary}
    for label, edf in exceptions:
        reports[label.replace(" ", "_")] = edf

    notes = (
        f"{len(df)} rows after cleaning; "
        f"{sum(len(e) for _, e in exceptions)} exception rows across "
        f"{len(exceptions)} check(s)."
    )

    return {"data": df, "reports": reports, "notes": notes}
