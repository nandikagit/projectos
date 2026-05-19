import marimo

__generated_with = "0.23.5"
app = marimo.App()


# -----------------------------
# Imports
# -----------------------------
@app.cell
def _():
    import pandas as pd
    import marimo as mo

    from func import (
        get_curr_standings_espn,
        join_espn_output,
        joined_df_col_renames,
        convert_to_numeric,
        plot_points,
        plot_points_over_races,
    )

    return (
        pd,
        mo,
        get_curr_standings_espn,
        join_espn_output,
        joined_df_col_renames,
        convert_to_numeric,
        plot_points,
        plot_points_over_races,
    )


# -----------------------------
# Load + preprocess data
# -----------------------------
@app.cell
def _(
    pd,
    get_curr_standings_espn,
    join_espn_output,
    joined_df_col_renames,
    convert_to_numeric,
):
    year = 2025

    tables = get_curr_standings_espn(year)
    df_joined = join_espn_output(tables)
    df_col_renamed = joined_df_col_renames(df_joined)
    df_numeric = convert_to_numeric(df_col_renamed)

    return df_numeric, year


# -----------------------------
# Driver slider (NEW)
# -----------------------------
@app.cell
def _(mo, df_numeric):
    max_drivers = len(df_numeric)

    driver_count = mo.ui.slider(
        start=1,
        stop=max_drivers,
        step=1,
        value=min(10, max_drivers),
        label="Number of Drivers"
    )

    driver_count
    return driver_count


# -----------------------------
# Filtered dataframe
# -----------------------------
@app.cell
def _(df_numeric, driver_count):
    df_filtered = df_numeric.iloc[:driver_count.value]
    return df_filtered


# -----------------------------
# Bar chart
# -----------------------------
@app.cell
def _(df_filtered, plot_points, year):
    fig = plot_points(df_filtered, year, "purple", "black")
    fig
    return fig


# -----------------------------
# Race progression chart
# -----------------------------
@app.cell
def _(df_filtered, plot_points_over_races, year):
    fig2 = plot_points_over_races(
        df_filtered,
        year,
        len(df_filtered),
        26
    )
    fig2
    return fig2


if __name__ == "__main__":
    app.run()