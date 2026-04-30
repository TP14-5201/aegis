import pandas as pd

from .utils import initial_cleaning_pipeline, clean_na_values


def wrangle_health_outcome(df: pd.DataFrame) -> pd.DataFrame:
    """Wrangle the VPHS 2014 food insecurity health outcomes dataset (Table A1-19)."""
    df = initial_cleaning_pipeline(df)
    df = clean_na_values(df)
    return df
