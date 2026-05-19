import marimo

__generated_with = "0.23.5"
app = marimo.App()


@app.cell
def _():
    import pandas as pd
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
        get_curr_standings_espn,
        join_espn_output,
        joined_df_col_renames,
        convert_to_numeric,
        plot_points,
        plot_points_over_races,
    )


@app.cell
def _(
    pd,
    get_curr_standings_espn,
    join_espn_output,
    joined_df_col_renames,
    convert_to_numeric,
):
    year = 2024

    tables = get_curr_standings_espn(year)
    df_joined = join_espn_output(tables)
    df_col_renamed = joined_df_col_renames(df_joined)
    df_numeric = convert_to_numeric(df_col_renamed)

    return df_numeric, year


@app.cell
def _(df_numeric, plot_points, year):
    fig = plot_points(df_numeric, year, "purple", "black")
    fig
    return fig


@app.cell
def _(df_numeric, plot_points_over_races, year):
    fig2 = plot_points_over_races(df_numeric, year, 10, 5)
    fig2
    return fig2


if __name__ == "__main__":
    app.run()