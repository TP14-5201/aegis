import pandas as pd
import numpy as np

from .utils import initial_cleaning_pipeline, clean_na_values, normalize_website, select_columns, add_source_column


def remove_missing_service_names(df: pd.DataFrame) -> pd.DataFrame:
    """Removes rows with missing names."""
    df = df.dropna(subset=["name"])
    return df


def normalize_address(df: pd.DataFrame) -> pd.DataFrame:
    """Normalizes the address column."""
    df["address_1"] = df["address_1"].fillna("")
    df["address_2"] = df["address_2"].fillna("")
    df["address"] = df["address_1"] + ", " + df["address_2"] 
    # Clean up trailing/leading commas if address_1 side was empty
    df["address"] = df["address"].str.lstrip(", ")

    df = df.drop(columns=["address_1", "address_2"])    
    
    return df


def normalize_phone(df: pd.DataFrame) -> pd.DataFrame:
    """Normalizes the phone column."""
    phone1 = df["phone"].fillna("").astype(str).str.strip()
    phone2 = df["phone_2"].fillna("").astype(str).str.strip()
    phone_free = df["free_call"].fillna("").astype(str).str.strip()

    # Prioritize Free Call, then Phone 1
    df["primary_phone"] = phone_free.where(phone_free != "", phone1)

    # Alternatively, create all phones list for the UI
    def _build_phone_list(row):
        numbers = []
        if row["free_call"]: numbers.append(f"Free Call: {str(row['free_call'])}")
        if row["phone"]: numbers.append(f"Phone 1: {str(row['phone'])}")
        if row["phone_2"]: numbers.append(f"Phone 2: {str(row['phone_2'])}")
        return " | ".join(numbers)
    df["phone_display"] = df.apply(_build_phone_list, axis=1)

    df = df.drop(columns=["phone", "phone_2", "free_call"])

    return df


def normalize_social_media(df: pd.DataFrame) -> pd.DataFrame:
    """Normalizes the social media column."""
    df["social_media"] = df["social_media"].str.replace(r"^acebook.com", "facebook.com", regex=True)
    return df


def clean_opening_hours_text(val):
    """Cleans the opening hours text by removing newlines and extra spaces."""
    if pd.isna(val) or str(val).lower() == 'closed':
        return "Closed"

    text = str(val).replace('\n', ' ').replace('\r', ' ')
    # Remove double spaces
    text = " ".join(text.split())
    return text


def transform_opening_hours(df: pd.DataFrame):
    """Transforms the opening hours column by collapsing and merging multiple day columns into a single JSON object."""
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'public_holidays']
    for day in days:
        if day in df.columns:
            df[day] = df[day].apply(clean_opening_hours_text)

    def _collapse_to_json(row):
        return {day: row[day] for day in days if day in row}

    df["opening_hours"] = df.apply(_collapse_to_json, axis=1)

    # Drop the original day columns
    df = df.drop(columns=days)
    
    return df


def transform_categories(df: pd.DataFrame):
    """Transforms the categories column by collapsing and merging multiple category columns into a single list."""
    # List of the source column names
    cat_cols = [f"category_{i}" for i in range(1, 7)]
    
    def _collapse_cats(row):
        # 1. Get values from all 6 columns
        # 2. Convert to string and strip whitespace
        # 3. Filter out Nones, NaNs, or empty strings
        cats = [
            str(row[col]).strip() 
            for col in cat_cols 
            if pd.notnull(row[col]) and str(row[col]).strip() != ""
        ]
        # Return unique categories only
        return list(set(cats))

    df["categories"] = df.apply(_collapse_cats, axis=1)
    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Renames the 'What' and 'Who' column headers to make it more descriptive"""
    cols_rename_map = {
        "what": "description",
        "who": "target_audience"
    }
    df = df.rename(columns=cols_rename_map)
    return df


def wrangle_melbourne(df: pd.DataFrame) -> pd.DataFrame:
    """Wrangling pipeline for Melbourne data."""
    df = initial_cleaning_pipeline(df)
    df = remove_missing_service_names(df)
    df = normalize_address(df)
    df = normalize_phone(df)
    df = normalize_website(df)
    df = normalize_social_media(df)
    df = transform_opening_hours(df)
    df = transform_categories(df)
    df = rename_columns(df)
    df = select_columns(df)
    df = add_source_column(df, source="City of Melbourne")
    df = clean_na_values(df)

    return df
