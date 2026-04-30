import pandas as pd

from .utils import initial_cleaning_pipeline, clean_na_values


def fill_health_outcome_na_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill NA values in the health outcomes dataset. Because all categories are mutually exclusive, and the sum of all categories is 100%, we can fill the NA values by subtracting the sum of the other categories from 100%."""
    df["relied_lowcost_yes_95ci_ul"] = df["relied_lowcost_yes_95ci_ul"].astype(float)
    # Group by category and sum the values
    df_category_sum = df.groupby(["category"]).sum().reset_index()
    df_with_null_stats = df[df.isna().any(axis=1)]
    # The first 2 columns are not the stat values
    for column in df_with_null_stats.columns[2:]:
        df[column] = df[column].fillna(100 - float(df_category_sum[column].values[0]))
        
    return df

def wrangle_low_cost_diet(df: pd.DataFrame) -> pd.DataFrame:
    """Wrangle the VPHS 2014 parents low cost diet table (Table A1-27)."""
    df = initial_cleaning_pipeline(df)
    df = clean_na_values(df)
    df = fill_health_outcome_na_values(df)
    return df