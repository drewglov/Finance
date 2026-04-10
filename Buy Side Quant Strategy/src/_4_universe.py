from __future__ import annotations
from pathlib import Path
import pandas as pd

def build_universe(
    qc_csv: Path,
    min_rows: int = 750,
    max_zero_vol_frac: float = 0.01,
    max_bad_bar_frac: float = 0.005,
    max_nonpos_price_frac: float = 0.0,
) -> pd.DataFrame:
    qc = pd.read_csv(qc_csv, parse_dates=["start_date", "end_date"])

    nonpos_frac = qc["nonpos_price_rows"] / qc["rows"]
    bad_high_frac = qc["bad_high_rows"] / qc["rows"]
    bad_low_frac = qc["bad_low_rows"] / qc["rows"]
    zero_vol_frac = qc["zero_volume_rows"] / qc["rows"]

    ok = (
        (qc["rows"] >= min_rows) &
        (nonpos_frac <= max_nonpos_price_frac) &
        (bad_high_frac <= max_bad_bar_frac) &
        (bad_low_frac <= max_bad_bar_frac) &
        (zero_vol_frac <= max_zero_vol_frac)
    )

    universe = qc.loc[ok].copy()
    universe = universe.sort_values(["start_date", "rows"], ascending=[True, False])

    return universe
