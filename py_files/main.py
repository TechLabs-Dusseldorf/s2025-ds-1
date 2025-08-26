"""
main.py
-------
Entry point script that uses functions from clean_code.py.
This script:
1. Loads and cleans the electricity dataset
2. Runs a series of checks and aggregations
3. Prints summaries (tables/statistics)
4. Optionally plots yearly production
"""

import argparse
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
    renewables_growth_rate,   # <-- make sure this is here
    plot_solar_wind,          # <-- and this
)

def main(url: str, no_plot: bool, save_plot: str | None):
     # 1) Load dataset
    df = load_data(url)   # if url is not given, load_data uses DEFAULT_DATA_URL

    # 2) Quick structure checks
    print("Rows, Columns:", get_shape(df))
    print("\nColumns:", get_columns(df))
    print("\nMissing values per column:\n", missing_values(df))

    # 3) Clean
    df_clean = clean_data(df)
    print("\nAfter cleaning - Missing values per column:\n", missing_values(df_clean))

    # 4) Aggregations
    yearly = get_yearly_production(df_clean)
    print("\nYearly production (head):\n", yearly.head())

    params = get_unique_parameters(df_clean)
    print("\nUnique parameters:", params)

    by_param = sum_by_parameter(df_clean)
    print("\nTotal by parameter:\n", by_param)

    top5 = top_countries(df_clean, n=5, ascending=False)
    print("\nTop 5 countries by total production:\n", top5)
    top5_list = top5.index.tolist()


      # --- Intermediate Questions ---

    growth = renewables_growth_rate(df_clean, top5_list)
    print("\nYoY growth in Total Renewables (head):\n", growth.head())

    max_growth_country = growth.groupby("country_name")["YoY Growth (%)"].mean().idxmax()
    print("\nCountry with strongest avg YoY renewable growth:", max_growth_country)

    plot_solar_wind(df_clean, top5_list)
    # ---


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

    # 5) Plot (optional)
    if not no_plot:
        plot_yearly_production(yearly, show=True, save_path=save_plot)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run electricity production analysis pipeline.")
    parser.add_argument(
        "--url",
        type=str,
        default=None,
        help="CSV URL to load. If omitted, uses the default RAW URL from clean_code.py",
    )
    parser.add_argument("--no-plot", action="store_true", help="Disable plot display.")
    parser.add_argument(
        "--save-plot",
        type=str,
        default=None,
        help="Path to save the yearly production plot (PNG).",
    )
    args = parser.parse_args()

    # If no url is given, load_data() falls back to DEFAULT_DATA_URL
    main(args.url, args.no_plot, args.save_plot)

 # 5) Plots (optional)
    if not no_plot:
        # Create figures but don't show yet
        plot_yearly_production(yearly, show=False, save_path=save_plot)
        plot_solar_wind(df_clean, top5_list, show=False)

        # Now display *all* open figures together
        import matplotlib.pyplot as plt
        plt.show()