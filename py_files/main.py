"""
CLI entry for the electricity production analysis (local CSV).
Works from any CWD because clean_code resolves the default path
relative to this file location (py_files/../data/...).
"""
from __future__ import annotations

import argparse
from typing import Optional, List

from clean_code import (
    load_data,
    clean_data,
    get_shape,
    get_columns,
    missing_values,
    get_yearly_production,
    get_unique_parameters,
    sum_by_parameter,
    top_countries,
    avg_monthly_for_countries,
    top_products,
    product_share_over_time,
    total_renewables_yearly,
    renewables_totals,
    plot_yearly_production,
    renewables_growth_rate,
    plot_solar_wind,
)


def main(path: Optional[str], no_plot: bool, save_plot: Optional[str], save_solar_wind: Optional[str]) -> None:
    df = load_data(path)

    print("Rows, Columns:", get_shape(df))
    print("\nColumns:", get_columns(df))
    print("\nMissing values per column:\n", missing_values(df))

    df_clean = clean_data(df)
    print("\nAfter cleaning - Missing values per column:\n", missing_values(df_clean))

    yearly = get_yearly_production(df_clean)
    print("\nYearly production (head):\n", yearly.head())

    params = get_unique_parameters(df_clean)
    print("\nUnique parameters:", params)

    by_param = sum_by_parameter(df_clean)
    print("\nTotal by parameter:\n", by_param)

    top5 = top_countries(df_clean, n=5, ascending=False)
    print("\nTop 5 countries by total production:\n", top5)
    top5_list: List[str] = top5.index.tolist()

    growth = renewables_growth_rate(df_clean, top5_list)
    if not growth.empty:
        print("\nYoY growth in Total Renewables (head):\n", growth.head())
        max_growth_country = growth.groupby("country_name")["YoY Growth (%)"].mean().idxmax()
        print("\nCountry with strongest avg YoY renewable growth:", max_growth_country)
    else:
        print("\nYoY growth could not be computed (no matching rows).")

    avg_monthly = avg_monthly_for_countries(df_clean, top5_list)
    print("\nAvg monthly proxy for top 5 countries:\n", avg_monthly)

    top3_products = top_products(df_clean, n=3)
    print("\nTop 3 products by total value:\n", top3_products)
    top3_list = top3_products.index.tolist()

    shares = product_share_over_time(df_clean, top3_list)
    print("\nProduct share over time (head):\n", shares.head())

    renew_yearly = total_renewables_yearly(df_clean)
    print("\nTotal renewables yearly:\n", renew_yearly)

    renew_totals = renewables_totals(df_clean)
    print("\nRenewables totals across dataset:\n", renew_totals)

    if not no_plot:
        plot_yearly_production(yearly, show=True, save_path=save_plot)
        plot_solar_wind(df_clean, top5_list, show=True, save_path=save_solar_wind)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run electricity production analysis (local CSV).")
    parser.add_argument("--path", type=str, default=None,
                        help="Local CSV path. If omitted, uses path resolved relative to this file (py_files/../data/...).")
    parser.add_argument("--no-plot", action="store_true", help="Disable all plots.")
    parser.add_argument("--save-plot", type=str, default=None, help="Path to save yearly totals plot (PNG).")
    parser.add_argument("--save-solar-wind", type=str, default=None, help="Path to save Solar/Wind plot (PNG).")
    args = parser.parse_args()

    main(args.path, args.no_plot, args.save_plot, args.save_solar_wind)
