"""Analyze a transactions CSV."""

# Standard library imports
import os
import argparse
import pandas as pd

import rm_analyzer
from rm_analyzer import summarize, send


def main():
    """Analyzes a transactions CSV."""
    # Parse args
    parser = argparse.ArgumentParser(description="Analyze a transactions CSV.")
    parser.add_argument(
        "path",
        type=str,
        nargs="?",
        help="path to transactions CSV or directory containing CSVs",
        default=os.path.join(os.path.expanduser("~"), "Downloads"),
    )
    args = parser.parse_args()

    # Path validation
    path = args.path
    if os.path.isdir(path):
        children = [os.path.join(path, c) for c in os.listdir(path)]
        sheets = list(filter(lambda x: x.endswith("-transactions.csv"), children))
        if sheets:
            path = max(sheets, key=os.path.getctime)
        else:
            raise FileNotFoundError(f"No transactions CSV in directory: {path}")
    elif os.path.isfile(path):
        if not path.endswith("-transactions.csv"):
            raise FileExistsError(f"File is not a valid transactions CSV: {path}")
    else:
        raise FileNotFoundError(
            f"Path specified is not a valid directory or file path: {path}"
        )

    # Main logic
    print(f"Running rm-analyzer on: {path}")
    config = rm_analyzer.CONFIG

    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])

    summ_df = summarize.build_summary_df(df, config)
    tot_series = summ_df.sum(axis=1)
    tot_series.name = "Total"
    html = summarize.write_email_body(summ_df, tot_series, config)

    min_date = df["Date"].min().strftime("%m/%d")
    max_date = df["Date"].max().strftime("%m/%d")
    subject = f"Transactions Summary: {min_date} - {max_date}"
    source = config["Email"]
    dest = [p["Email"] for p in config["People"]]

    send.gmail_send_message(source, dest, subject, html)


if __name__ == "__main__":
    main()
