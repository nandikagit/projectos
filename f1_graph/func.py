from matplotlib import pyplot as plt
import pandas as pd
import ssl

# temporary SSL workaround for macOS certificate issues
ssl._create_default_https_context = ssl._create_unverified_context


def get_curr_standings_espn(year: int) -> list[pd.DataFrame]:
    """
    Reads in the current year and returns a
    list of dataframes with ESPN Driver Stats (unfiltered)
    """
    url = f"https://www.espn.com/f1/standings/_/season/{year}"
    tables = pd.read_html(url)
    return tables


def join_espn_output(tables: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Return joined DataFrame from output returned by ESPN
    """
    df_joined = tables[0].join(tables[1])
    return df_joined


def joined_df_col_renames(df: pd.DataFrame) -> pd.DataFrame:
    """
    Do the following transformations on the joined ESPN DF:
    1. rename first col from Unnamed: 0 to Driver
    2. Clean up Driver names to not have their number + country
    3. Drop last column (usually some variation of Unnamed: ##)
    """
    df = df.copy()

    # rename first column
    df = df.rename(columns={"Unnamed: 0": "Driver"})

    # clean driver names
    df["Driver"] = df["Driver"].str.replace(
        r"^\d+[A-Z]{3}\s*",
        "",
        regex=True
    )

    # drop last unnamed column
    df = df.drop(columns=df.columns[-1])

    return df


def convert_to_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert PTS + Race scores to numeric values
    Example: NaN -> 0
    """
    df = df.copy()

    race_cols = df.columns[2:]

    df[race_cols] = (
        df[race_cols]
        .apply(pd.to_numeric, errors="coerce")
        .fillna(0)
    )

    return df


def plot_points(
    df: pd.DataFrame,
    year: int,
    color_def: str,
    edgecolor_def: str
):
    """
    Create aggregate driver points chart
    """
    pts = df[["Driver", "PTS"]].copy()

    pts["PTS"] = pd.to_numeric(pts["PTS"], errors="coerce").fillna(0)

    pts = pts.sort_values("PTS", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 7))

    ax.barh(
        pts["Driver"],
        pts["PTS"],
        color=color_def,
        edgecolor=edgecolor_def
    )

    ax.set_xlabel("PTS")
    ax.set_ylabel("Drivers")
    ax.set_title(f"F1 Driver Standings: {year}")

    plt.tight_layout()

    return fig


def plot_points_over_races(
    df: pd.DataFrame,
    year: int,
    num_drivers: int = 100,
    num_races: int = 100
):
    """
    Plot cumulative driver points over races
    """
    df = df.copy()

    # set driver names as index
    df = df.set_index("Driver")

    # remove total points column
    if "PTS" in df.columns:
        df = df.drop(columns="PTS")

    # limit drivers and races
    df = df.iloc[:num_drivers, :num_races]

    # cumulative totals across races
    cumulative = df.cumsum(axis=1)

    fig, ax = plt.subplots(figsize=(13, 6))

    for i in range(len(cumulative)):
        ax.plot(
            cumulative.columns,
            cumulative.iloc[i],
            marker="x",
            label=cumulative.index[i]
        )

    ax.set_ylabel("Cumulative Points")
    ax.set_xlabel("Race")
    ax.set_title(f"F1 Season Progression: {year}")

    ax.legend(
        bbox_to_anchor=(1.05, 0.5),
        loc="center left"
    )

    plt.tight_layout()

    return fig