from __future__ import annotations

from pathlib import Path
import pandas as pd
from tqdm import tqdm

from src.io import list_data_files, read_one_ohlcv
from src.quality import qc_metrics


def ticker_from_filename(fp: Path) -> str:
    # e.g. aadr.us.txt -> AADR.US
    return fp.stem.upper()


def main():
    etf_dir = Path("Data/ETFs")
    curated_dir = Path("data/curated/ETFs")
    outputs_dir = Path("outputs")

    curated_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    files = list_data_files(etf_dir)
    if not files:
        raise RuntimeError(f"No files found under {etf_dir.resolve()}")

    qc_rows = []

    for fp in tqdm(files, desc="curate ETFs"):
        ticker = ticker_from_filename(fp)

        try:
            df = read_one_ohlcv(fp)
            qc = qc_metrics(df)

            qc["ticker"] = ticker
            qc["file"] = fp.name

            # Save curated single-asset data
            out_fp = curated_dir / f"{ticker}.parquet"
            df.to_parquet(out_fp, index=True)

            qc_rows.append(qc)

        except Exception as e:
            # Record failure but keep the pipeline running
            qc_rows.append({
                "ticker": ticker,
                "file": fp.name,
                "error": str(e),
            })

    qc_df = pd.DataFrame(qc_rows)

    # Put key columns first if they exist
    preferred = ["ticker", "file", "rows", "start_date", "end_date",
                 "nonpos_price_rows", "bad_high_rows", "bad_low_rows", "zero_volume_rows", "error"]
    cols = [c for c in preferred if c in qc_df.columns] + [c for c in qc_df.columns if c not in preferred]
    qc_df = qc_df[cols].sort_values("ticker")

    qc_out = outputs_dir / "qc_summary.csv"
    qc_df.to_csv(qc_out, index=False)
    print("Saved:", qc_out.resolve())
    print("Curated parquet dir:", curated_dir.resolve())


if __name__ == "__main__":
    main()
