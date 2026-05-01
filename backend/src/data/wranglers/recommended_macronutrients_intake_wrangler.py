import pandas as pd

from .utils import initial_cleaning_pipeline


def wrangle_recommended_macronutrients_intake(df: pd.DataFrame) -> pd.DataFrame:
    """Wrangle the recommended macronutrients intake dataset."""
    return initial_cleaning_pipeline(df)
