import pandas as pd

from .utils import initial_cleaning_pipeline


def wrangle_diet_indicator(df: pd.DataFrame) -> pd.DataFrame:
    """Wrangle the VPHS 2014 food insecurity diet indicators dataset (Table A1-18)."""
    return initial_cleaning_pipeline(df)
