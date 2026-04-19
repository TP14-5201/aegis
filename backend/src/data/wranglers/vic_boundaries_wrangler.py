import geopandas as gpd
import pandas as pd

from .utils import standardize_columns


def standardise_geospatial_projection(df: pd.DataFrame) -> pd.DataFrame:
    gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df["geometry"]))
    # GDA2020 (Geocentric Datum of Australia 2020) — EPSG:7899 (Lat/Long)
    gdf = gdf.set_crs(epsg=7899, allow_override=True)
    # Reproject to WGS84
    gdf = gdf.to_crs(epsg=4326) 
    # Convert geometry back to WKT string for seeding
    df["geometry"] = gdf["geometry"].apply(lambda g: g.wkt if g else None)
    return df

def take_latest_phu_boundaries(df: pd.DataFrame) -> pd.DataFrame:
    df['ufi_created'] = pd.to_datetime(df['ufi_created'])
    df_latest = df.sort_values('ufi_created').drop_duplicates(
        subset=['vicgov_region'], 
        keep='last'
    )
    return df_latest


def wrangle_vic_boundaries(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df)
    df = take_latest_phu_boundaries(df)
    df = standardise_geospatial_projection(df)

    return df