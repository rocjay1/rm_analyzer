"""Functions for summarizing a transactions CSV."""

# Standard library imports
import pandas as pd


def _to_money(n):
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
            f"{_to_money(k * tot_series.sum() - tot_series[p1])}."
        )
    else:
        s = "See the table above for transaction totals by person, category."
    return s


def write_email_body(summ_df, tot_series, config):
    """Writes the summary HTML for email body."""
    cats = list(summ_df.columns)
    people = list(summ_df.index)

    body_strs = []
    body_strs.append(
        """\
<!DOCTYPE html>
<html>
<head>
    <style>
        table {
            border-collapse: collapse;
            width: 100%
        }
        th,td {
            border: 1px solid black;
            padding: 8px 12px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <table border="1">
        <thead>
            <tr>
                <th></th>"""
    )

    for c in cats:
        body_strs.append(
            f"""
                <th>{c}</th>"""
        )

    body_strs.append(
        """
                <th>Total</th>
            </tr>
        </thead>
        <tbody>"""
    )

    for p in people:
        body_strs.append(
            f"""
            <tr>
                <td>{p}</td>"""
        )
        for c in cats:
            body_strs.append(
                f"""
                <td>{_to_money(summ_df.at[p, c])}</td>"""
            )
        body_strs.append(
            f"""
                <td>{_to_money(tot_series[p])}</td>
            </tr>"""
        )

    if len(people) == 2:
        p1, p2 = people
        body_strs.append(
            """
            <tr>
                <td>Difference</td>"""
        )
        for c in cats:
            body_strs.append(
                f"""
                <td>{_to_money(summ_df.at[p1, c] - summ_df.at[p2, c])}</td>"""
            )
        body_strs.append(
            f"""
                <td>{_to_money(tot_series[p1] - tot_series[p2])}</td>
            </tr>"""
        )

    body_strs.append(
        """
        </tbody>
    </table>"""
    )

    body_strs.append(
        f"""
    <p>{write_summary_sentence(summ_df, tot_series, config)}</p>
</body>
</html>"""
    )

    body = "".join(body_strs).replace("&", "&amp;")
    return body


def _build_owners_json(config):
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
    owners_df = pd.DataFrame(_build_owners_json(config))
    cats = config["Categories"]
    df_filtered = df[df["Ignored From"].isnull() * df["Category"].isin(cats)]
    df_merged = pd.merge(df_filtered, owners_df, how="left", on="Account Number")
    df_agg = df_merged.groupby(["Category", "Owner"])[["Amount"]].sum().reset_index()
    df_pivot = df_agg.pivot(index="Owner", columns="Category", values="Amount").fillna(
        0
    )
    return df_pivot
