"""Template procedure file.

Copy this file and rename to match a sheet:
    Sheet "Sales Register"   -> sales_register.py
    Sheet "GL Detail"        -> gl_detail.py
    Sheet "Vendor Master"    -> vendor_master.py

Rules for the file name: lowercase, spaces -> underscores, drop punctuation.
"""

import pandas as pd


def run(df: pd.DataFrame, file_path: str = None, sheet_name: str = None, **_) -> dict:
    # df = the sheet as a DataFrame. Do whatever you need:
    # clean, validate, compute totals, find exceptions, etc.

    # Example placeholders — replace with real audit logic:
    cleaned = df.dropna(how="all")

    summary = pd.DataFrame({
        "metric": ["row_count", "column_count"],
        "value":  [len(cleaned), len(cleaned.columns)],
    })

    exceptions = cleaned.head(0)  # empty for the template

    return {
        "data":    cleaned,
        "reports": {"summary": summary, "exceptions": exceptions},
        "notes":   "Template ran — replace with real procedure.",
    }
