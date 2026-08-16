"""Reason 칼럼 범주 전수 확인 (Full inventory of "Reason" column categories).

The `Reason` column in the source workbook can hold multiple, semicolon
(`;`)-separated reason codes per row (e.g. "A; +B; C"). This script:

1. Loads the workbook.
2. Splits each row's `Reason` value on `;`, strips whitespace and any
   leading `+` markers, and explodes the result into one row per reason.
3. Counts how often each distinct reason occurs and what share of all
   *records* (not reason mentions) it represents.
4. Prints a summary and writes the full frequency table to CSV.

Usage
-----
    python scripts/reason_category_analysis.py \
        --input path/to/rw_analysis_final.xlsx \
        --output output/reason_categories.csv

Both arguments are optional; sensible defaults are used if omitted.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

DEFAULT_INPUT = "rw_analysis_final.xlsx"
DEFAULT_OUTPUT = "output/reason_categories.csv"


def build_reason_frequency_table(analysis: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Explode the ``Reason`` column into individual reason codes and
    return (frequency/percentage table, exploded reasons series)."""
    if "Reason" not in analysis.columns:
        raise KeyError("Expected a 'Reason' column in the input data.")

    reasons = (
        analysis["Reason"]
        .fillna("")
        .astype(str)
        .str.split(";")
        .explode()
        .str.strip()
        .str.lstrip("+")
        .replace("", np.nan)
        .dropna()
    )

    freq_df = (
        reasons.value_counts()
        .to_frame("건수")
        .assign(비율=lambda x: (x["건수"] / len(analysis) * 100).round(2))
    )

    return freq_df, reasons


def run(input_path: str | Path, output_path: str | Path) -> pd.DataFrame:
    input_path = Path(input_path)
    output_path = Path(output_path)

    analysis = pd.read_excel(input_path)
    print("불러온 데이터:", analysis.shape)

    freq_df, reasons = build_reason_frequency_table(analysis)

    print(f"\n고유 Reason 범주  : {len(freq_df):,}")
    print(f"레코드당 평균 사유: {len(reasons) / len(analysis):.2f}개\n")

    with pd.option_context("display.max_rows", None, "display.width", 200):
        print(freq_df)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    freq_df.to_csv(output_path, encoding="utf-8-sig")
    print(f"\n저장 완료: {output_path}")

    return freq_df


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        help=f"Path to the source Excel workbook (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Path to write the frequency table CSV (default: {DEFAULT_OUTPUT})",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    run(args.input, args.output)


if __name__ == "__main__":
    main()
