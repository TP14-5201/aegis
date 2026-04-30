import pandas as pd

from .utils import initial_cleaning_pipeline, clean_na_values


def fill_health_outcome_na_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill NA values in the health outcomes dataset. Because all categories are mutually exclusive, and the sum of all categories is 100%, we can fill the NA values by subtracting the sum of the other categories from 100%."""
    df["insecure_hunger_95ci_ul"] = df["insecure_hunger_95ci_ul"].astype(float)
    # Group by category and sum the values
    df_category_sum = df.groupby(["category"]).sum().reset_index()
    df_with_null_stats = df[df.isna().any(axis=1)]
    # The first 2 columns are not the stat values
    for column in df_with_null_stats.columns[2:]:
        expected_sum = 100 - float(df_category_sum[column].values[0])
        if expected_sum > 0:
            df[column] = df[column].fillna(expected_sum)
        else:
            df[column] = df[column].fillna(0)

    return df

def wrangle_health_outcome(df: pd.DataFrame) -> pd.DataFrame:
    """Wrangle the VPHS 2014 food insecurity health outcomes dataset (Table A1-19)."""
    df = initial_cleaning_pipeline(df)
    df = clean_na_values(df)
    df = fill_health_outcome_na_values(df)
    return df
