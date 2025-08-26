"""
clean_code.py
--------------
Reusable data loading, cleaning, aggregation, and plotting utilities
extracted from the exploratory notebook.
"""
# -----------------------------
# Module header & imports : 
# -----------------------------

# -----------------------------
# from typing import Iterable, List, Tuple 
# Used for type hints (to clarify function inputs/outputs).
from typing import Iterable, List, Tuple

# -----------------------------
# Pandas handles tabular data loading, cleaning, grouping, etc.
import pandas as pd

# -----------------------------
# Matplotlib draws the line plot at the end.
import matplotlib.pyplot as plt


# -----------------------------
# Loading & Cleaning
# -----------------------------

# Define default URL first
DEFAULT_DATA_URL = "https://raw.githubusercontent.com/TechLabs-Dusseldorf/s2025-ds-1/main/data/raw/global_electricity_production_data.csv"

def load_data(url: str = DEFAULT_DATA_URL) -> pd.DataFrame:
    """
    Load the CSV from the provided URL into a pandas DataFrame.
    Defaults to the TechLabs-Dusseldorf electricity production dataset.
    """
    if url is None:
        url = "/Users/tanjucoskun/s2025-ds-1/data/global_electricity_production_data.csv"  # local file
    try:
        return pd.read_csv(url)
    except Exception as e:
        raise RuntimeError(f"Failed to load data from {url}") from e


# cleaning the data
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw dataframe:
    - Drop rows where 'value' is missing.
    - Convert 'date' to datetime.
    - Drop rows where 'date' conversion failed.
    - Add integer 'year' column.
    """
    # Drop missing values in value:
    df_clean = df.dropna(subset=['value']).copy()
    # Convert date to datetime:
    df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
    # Drop rows with failed date conversion:
    df_clean = df_clean[df_clean['date'].notnull()].copy()
    # Extract year as integer:
    df_clean['year'] = df_clean['date'].dt.year.astype(int)
    # Returns: A cleaned DataFrame with all original columns plus a new year column.
    return df_clean


# Explorations / Aggregations
# These functions expect either the raw df or the cleaned df_clean and compute basic summaries.
# based on the begginer questions

# size of the data (quick size check
def get_shape(df: pd.DataFrame) -> Tuple[int, int]:
    return df.shape

# Purpose: List the column names. 
def get_columns(df: pd.DataFrame) -> List[str]:
    return list(df.columns)

# Purpose: Count missing values per column. ( -value should have 14 missing values)
def missing_values(df: pd.DataFrame) -> pd.Series:
    return df.isnull().sum()

# Purpose: Get yearly production totals.
def get_yearly_production(df_clean: pd.DataFrame) -> pd.DataFrame:
    """Sum of 'value' per year."""
    return df_clean.groupby('year', as_index=False)['value'].sum()

# Purpose: List unique parameters in order.
def get_unique_parameters(df_clean: pd.DataFrame) -> List[str]:
    return sorted(df_clean['parameter'].dropna().unique().tolist())

# Purpose: Sum of 'value' per parameter.
def sum_by_parameter(df_clean: pd.DataFrame) -> pd.Series:
    return df_clean.groupby('parameter')['value'].sum().sort_values(ascending=True)

# Rank countries by total value across all rows.
def top_countries(df_clean: pd.DataFrame, n: int = 5, ascending: bool = False) -> pd.Series:
    """Return the top/bottom n countries by total 'value'."""
    return (
        df_clean.groupby('country_name')['value']
        .sum()
        .sort_values(ascending=ascending)
        .head(n)
    )

# For a list of countries, compute the mean of value per country across the dataset.
def avg_monthly_for_countries(df_clean: pd.DataFrame, countries: Iterable[str]) -> pd.Series:
    """Average of 'value' per country across all rows (proxy for monthly avg in the dataset)."""
    subset = df_clean[df_clean['country_name'].isin(list(countries))]
    return subset.groupby('country_name')['value'].mean()

# Rank energy product categories by total value.
def top_products(df_clean: pd.DataFrame, n: int = 3) -> pd.Series:
    return df_clean.groupby('product')['value'].sum().sort_values(ascending=False).head(n)

# For selected products (top_products), show per-year totals and their percentage share of that year’s grand total.
def product_share_over_time(df_clean: pd.DataFrame, products: Iterable[str]) -> pd.DataFrame:
    """
    For the selected products, compute per-year totals and their percentage share
    of the total annual 'value' across the whole dataset.
    Returns columns: ['year', 'product', 'value', 'total_value', 'percent']
    """
    prods = list(products)
    top_product_data = df_clean[df_clean['product'].isin(prods)]
    product_share = top_product_data.groupby(['year', 'product'], as_index=False)['value'].sum()
    total_by_year = df_clean.groupby('year', as_index=False)['value'].sum().rename(columns={'value': 'total_value'})
    merged = product_share.merge(total_by_year, on='year')
    merged['percent'] = (merged['value'] / merged['total_value']) * 100
    return merged

# Yearly totals for the single aggregated product:
def total_renewables_yearly(df_clean: pd.DataFrame) -> pd.DataFrame:
    """Yearly totals for 'Total Renewables (Hydro, Geo, Solar, Wind, Other)'."""
    mask = df_clean['product'] == 'Total Renewables (Hydro, Geo, Solar, Wind, Other)'
    return df_clean[mask].groupby('year', as_index=False)['value'].sum()

# Totals for individual renewable sources across the entire dataset.
def renewables_totals(df_clean: pd.DataFrame) -> pd.DataFrame:
    """Totals across the full dataset for key renewable sources."""
    renewables_sources = ('Combustible Renewables','Solar', 'Wind', 'Hydro')
    subset = df_clean[df_clean['product'].isin(renewables_sources)]
    return subset.groupby('product', as_index=False)['value'].sum()

# -----------------------------
# Plotting
# -----------------------------

#Simple line plot of value over year.
def plot_yearly_production(yearly_df: pd.DataFrame, show: bool = True, save_path: str = None) -> None:
    """
    Line plot of total electricity production by year.
    Note: Does not set explicit colors or styles.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(yearly_df['year'], yearly_df['value'], marker='o')
    plt.title('Global Electricity Production Over Time')
    plt.xlabel('Year')
    plt.ylabel('Total Electricity Production (GWh)')
    plt.grid(True)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    if show:
        plt.show()
    plt.close()

# -----------------------------
# TEST - Advanced Questions
# -----------------------------
def renewables_growth_rate(df: pd.DataFrame, countries: list[str]) -> pd.DataFrame:
    """
    YoY % growth for 'Total Renewables (Hydro, Geo, Solar, Wind, Other)'
    per country/year. Uses lowercase column names.
    """
    mask = (
        (df["product"] == "Total Renewables (Hydro, Geo, Solar, Wind, Other)")
        & (df["country_name"].isin(countries))
    )
    df_renew = df.loc[mask, ["country_name", "year", "value"]].copy()

    yearly = (
        df_renew.groupby(["country_name", "year"], as_index=False)["value"]
        .sum()
    )
    yearly["YoY Growth (%)"] = (
        yearly.groupby("country_name")["value"].pct_change() * 100
    )
    return yearly


def plot_solar_wind(df: pd.DataFrame, countries: list[str]) -> None:
    """
    Line plot of Solar & Wind production over time for selected countries.
    Uses lowercase column names.
    """
    df_sw = df[
        (df["product"].isin(["Solar", "Wind"])) & (df["country_name"].isin(countries))
    ].copy()

    yearly = (
        df_sw.groupby(["country_name", "year", "product"], as_index=False)["value"]
        .sum()
    )

    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    for param in ["Solar", "Wind"]:
        subset = yearly[yearly["product"] == param]
        for c in countries:
            cd = subset[subset["country_name"] == c]
            plt.plot(cd["year"], cd["value"], label=f"{c} - {param}")

    plt.title("Solar & Wind Production Over Time (Top 5 Countries)")
    plt.xlabel("Year")
    plt.ylabel("Production Value")
    plt.legend()
    plt.tight_layout()
    plt.show()
