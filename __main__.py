"""Analyze a transactions CSV."""

import os
import json
import argparse
import pandas as pd
import yattag
import send_message

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


# Functions
def load_config(json_path):
    """Loads the config from the JSON file."""
    with open(json_path, encoding="UTF-8") as f:
        return json.load(f)


def to_money(n):
    """Formats a number as money."""
    return f"{n:.2f}"


def write_summary_sentence(summ_df, tot_series, config):
    """Writes the transactions CSV summary sentence."""
    k = config["Factor"]
    people = list(summ_df.index)
    if len(people) == 2:
        p1, p2 = people
        s = (
            f"Using a scale factor of {k} for {p1}, {p1} owes {p2}: "
            f"{to_money(k * tot_series.sum() - tot_series[p1])}."
        )
    else:
        s = "See the table above for transaction totals by person, category."
    return s


def write_email_body(summ_df, tot_series, config):
    """Writes the summary HTML for email body."""
    cats = list(summ_df.columns)
    people = list(summ_df.index)

    doc, tag, text = yattag.Doc().tagtext()
    doc.asis("<!DOCTYPE html>")
    with tag("html"):
        # HTML head
        with tag("head"):
            doc.asis(
                "<style>table {border-collapse: collapse; width: 100%} \
                th, td {border: 1px solid black; padding: 8px 12px; text-align: left;} \
                th {background-color: #f2f2f2;}</style>"
            )
        # HTML body
        with tag("body"):
            # Table
            with tag("table", border="1"):
                # Table header
                with tag("thead"):
                    with tag("tr"):
                        with tag("th"):
                            text("")
                        for c in cats:
                            with tag("th"):
                                text(c)
                        with tag("th"):
                            text("Total")
                # Table body
                with tag("tbody"):
                    # Create a row for each person
                    for p in people:
                        with tag("tr"):
                            with tag("td"):
                                text(p)
                            for c in cats:
                                with tag("td"):
                                    text(to_money(summ_df.at[p, c]))
                            with tag("td"):
                                text(to_money(tot_series[p]))
                    # If there are two people, create a row for the differences
                    if len(people) == 2:
                        p1, p2 = people
                        with tag("tr"):
                            with tag("td"):
                                text("Difference")
                            for c in cats:
                                with tag("td"):
                                    text(
                                        to_money(summ_df.at[p1, c] - summ_df.at[p2, c])
                                    )
                            with tag("td"):
                                text(to_money(tot_series[p1] - tot_series[p2]))
            # Summary sentence
            with tag("p"):
                text(write_summary_sentence(summ_df, tot_series, config))
    body = doc.getvalue()

    return body


def build_owners_json(config):
    """Builds dataframe containing Account Owner, Account Number data from config."""
    owners_json = {"Owner": {}, "Account Number": {}}
    c = 0
    for p in config["People"]:
        for n in p["Accounts"]:
            owners_json["Owner"][c] = p["Name"]
            owners_json["Account Number"][c] = n
            c += 1
    return owners_json


def build_summary_df(df, config):
    """Builds the transactions CSV summary dataframe."""
    owners_df = pd.DataFrame(build_owners_json(config))
    cats = config["Categories"]
    df_filtered = df[df["Ignored From"].isnull() * df["Category"].isin(cats)]
    df_merged = pd.merge(df_filtered, owners_df, how="left", on="Account Number")
    df_agg = df_merged.groupby(["Category", "Owner"])[["Amount"]].sum().reset_index()
    df_pivot = df_agg.pivot(index="Owner", columns="Category", values="Amount").fillna(
        0
    )
    return df_pivot


def main():
    """Main entrypoint to analyze a transactions CSV."""
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
    config_path = os.path.join(SCRIPT_PATH, os.path.join(".config", "config.json"))
    config = load_config(config_path)

    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])

    summ_df = build_summary_df(df, config)
    tot_series = summ_df.sum(axis=1)
    tot_series.name = "Total"
    html = write_email_body(summ_df, tot_series, config)

    min_date = df["Date"].min().strftime("%m/%d")
    max_date = df["Date"].max().strftime("%m/%d")
    subject = f"Transactions Summary: {min_date} - {max_date}"
    source = config["Email"]
    dest = [p["Email"] for p in config["People"]]

    send_message.gmail_send_message(source, dest, subject, html)


# Main
if __name__ == "__main__":
    main()
