import geopandas as gpd
import pandas as pd


def wrangle_vic_boundaries(df: pd.DataFrame) -> pd.DataFrame:
    gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df["geometry"]))
    
    # GDA2020 (Geocentric Datum of Australia 2020) — EPSG:7899 (Lat/Long)
    gdf = gdf.set_crs(epsg=7899, allow_override=True)
    # Reproject to WGS84
    gdf = gdf.to_crs(epsg=4326) 
    
    # Convert geometry back to WKT string for seeding
    df["geometry"] = gdf["geometry"].apply(lambda g: g.wkt if g else None)
    df.columns = df.columns.str.lower()

    return df