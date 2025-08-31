from typing import Iterable, List, Tuple, Optional
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# DEFAULT_DATA_PATH is resolved *relative to this file* (py_files/../data/...), so the code works no matter where you run it from (repo root, notebook folder, etc.).
DEFAULT_DATA_PATH = (Path(__file__).resolve().parent.parent
                     / "data" / "global_electricity_production_data.csv")


def load_data(path: Optional[str] = None) -> pd.DataFrame:
    # Load CSV from a local path. If path is None, use DEFAULT_DATA_PATH resolved relative to this file (py_files/../data/...).
    p = Path(path) if path is not None else DEFAULT_DATA_PATH
    try:
        return pd.read_csv(p)
    except Exception as e:
        raise RuntimeError(f"Failed to load data from {p}") from e


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Basic cleaning:
    # Drop rows with missing `value`.
    # Parse `date` to datetime (coerce invalids to NaT) and drop invalid rows.
    # Add an integer `year` column for groupbys.
    
    df_clean = df.dropna(subset=['value']).copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
    df_clean = df_clean[df_clean['date'].notnull()].copy()
    df_clean['year'] = df_clean['date'].dt.year.astype(int)
    return df_clean

# Quick structure helpers
def get_shape(df: pd.DataFrame) -> Tuple[int, int]:
    return df.shape

def get_columns(df: pd.DataFrame) -> List[str]:
    return list(df.columns)

def missing_values(df: pd.DataFrame) -> pd.Series:
    return df.isnull().sum()

# Aggregations (for analysis)
def get_yearly_production(df_clean: pd.DataFrame) -> pd.DataFrame:
    return df_clean.groupby('year', as_index=False)['value'].sum()

def get_unique_parameters(df_clean: pd.DataFrame) -> List[str]:
    return sorted(df_clean['parameter'].dropna().unique().tolist())

def sum_by_parameter(df_clean: pd.DataFrame) -> pd.Series:
    return df_clean.groupby('parameter')['value'].sum().sort_values(ascending=True)

def top_countries(df_clean: pd.DataFrame, n: int = 5, ascending: bool = False) -> pd.Series:
    # Rank countries by total `value`.
    # - ascending=False → Top N
    # - ascending=True  → Bottom N
    return (
        df_clean.groupby('country_name')['value']
        .sum()
        .sort_values(ascending=ascending)
        .head(n)
    )

def avg_monthly_for_countries(df_clean: pd.DataFrame, countries: Iterable[str]) -> pd.Series:
    # Mean `value` per country across all rows.
    # (Acts as a proxy for a monthly average given dataset granularity.)
    subset = df_clean[df_clean['country_name'].isin(list(countries))]
    return subset.groupby('country_name')['value'].mean()

def top_products(df_clean: pd.DataFrame, n: int = 3) -> pd.Series:
    # Top N products by total `value` (global).
    return df_clean.groupby('product')['value'].sum().sort_values(ascending=False).head(n)

def product_share_over_time(df_clean: pd.DataFrame, products: Iterable[str]) -> pd.DataFrame:
    # Per-year totals for selected `products` + their share of the year total.
    # Returns: ['year', 'product', 'value', 'total_value', 'percent']   
    prods = list(products)
    top_product_data = df_clean[df_clean['product'].isin(prods)]
    product_share = top_product_data.groupby(['year', 'product'], as_index=False)['value'].sum()
    total_by_year = df_clean.groupby('year', as_index=False)['value'].sum().rename(columns={'value': 'total_value'})
    merged = product_share.merge(total_by_year, on='year')
    merged['percent'] = (merged['value'] / merged['total_value']) * 100
    return merged

def total_renewables_yearly(df_clean: pd.DataFrame) -> pd.DataFrame:
    # Yearly totals for the aggregated renewables product
    mask = df_clean['product'] == 'Total Renewables (Hydro, Geo, Solar, Wind, Other)'
    return df_clean[mask].groupby('year', as_index=False)['value'].sum()

def renewables_totals(df_clean: pd.DataFrame) -> pd.DataFrame:
    # Totals across the dataset for key renewables
    renewables_sources = ('Combustible Renewables','Solar', 'Wind', 'Hydro')
    subset = df_clean[df_clean['product'].isin(renewables_sources)]
    return subset.groupby('product', as_index=False)['value'].sum()

# Plotting functions
def plot_yearly_production(yearly_df: pd.DataFrame, show: bool = True, save_path: Optional[str] = None) -> None:
    #Line plot of global totals by year.
    #- show=True displays a window (good for local dev).
    #- save_path saves a PNG (good for reports/automation).
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

# Advanced QS (growth + multi-series plot)
def renewables_growth_rate(df: pd.DataFrame, countries: List[str]) -> pd.DataFrame:
    mask = (
        (df["product"] == "Total Renewables (Hydro, Geo, Solar, Wind, Other)")
        & (df["country_name"].isin(countries))
    )
    df_renew = df.loc[mask, ["country_name", "year", "value"]].copy()
    yearly = df_renew.groupby(["country_name", "year"], as_index=False)["value"].sum()
    yearly["YoY Growth (%)"] = yearly.groupby("country_name")["value"].pct_change() * 100
    return yearly


def plot_solar_wind(
    df: pd.DataFrame,
    countries: List[str],
    show: bool = True,
    save_path: Optional[str] = None
) -> None:
    #Multi-line plot: Solar & Wind per selected countries over time.
    #- Groups by (country, year, product) and plots two series per country
    df_sw = df[
        (df["product"].isin(["Solar", "Wind"])) & (df["country_name"].isin(countries))
    ].copy()
    yearly = df_sw.groupby(["country_name", "year", "product"], as_index=False)["value"].sum()

    plt.figure(figsize=(10, 6))
    for param in ["Solar", "Wind"]:
        subset = yearly[yearly["product"] == param]
        for c in countries:
            cd = subset[subset["country_name"] == c]
            if not cd.empty:
                plt.plot(cd["year"], cd["value"], label=f"{c} - {param}")

    plt.title("Solar & Wind Production Over Time (Selected Countries)")
    plt.xlabel("Year")
    plt.ylabel("Production Value (GWh)")
    plt.legend()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    if show:
        plt.show()
        plt.close()
