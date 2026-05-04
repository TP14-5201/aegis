"""Builds ingredients_pricing_raw.csv from the thedevastator grocery dataset.

Filters to Victorian postcodes (3xxx), selects one representative item per
Product_Group (the item whose price is closest to the group median), parses
pack weight from the package description, and saves the result to
settings.INGREDIENTS_PRICING_RAW_PATH.

Usage:
    python -m src.scripts.fetch_vic_grocery_ingredients
"""

import glob
import os
import re
import zipfile

import kagglehub
import pandas as pd

from src.core.config import settings
from src.core.logging import logger

_PRICE_SOURCE = "open_food_facts"
_PRICE_AS_OF = "2022-09-01"

_PACK_KG_RE = re.compile(r"(\d+\.?\d*)\s*kg", re.IGNORECASE)
_PACK_G_RE = re.compile(r"(\d+\.?\d*)\s*g\b", re.IGNORECASE)
_PACK_BARE_RE = re.compile(r"(\d+\.?\d*)")


def _parse_pack_grams(package_str: str) -> float | None:
    """Extract gram weight from a package description string."""
    s = str(package_str).lower().strip()
    m = _PACK_KG_RE.search(s)
    if m:
        return float(m.group(1)) * 1000
    m = _PACK_G_RE.search(s)
    if m:
        return float(m.group(1))
    m = _PACK_BARE_RE.search(s)
    if m:
        return float(m.group(1))
    return None


def _find_csv(folder: str) -> str | None:
    """Return path to Australia_Grocery CSV inside folder (or any CSV if not found by name)."""
    matches = glob.glob(os.path.join(folder, "**", "Australia_Grocery*.csv"), recursive=True)
    if matches:
        return matches[0]
    all_csv = glob.glob(os.path.join(folder, "**", "*.csv"), recursive=True)
    return all_csv[0] if all_csv else None


def _load_csv(path: str) -> pd.DataFrame:
    """Read a CSV trying latin-1 then utf-8-sig encodings."""
    for enc in ("latin-1", "utf-8-sig", "cp1252"):
        try:
            return pd.read_csv(path, encoding=enc, engine="python", on_bad_lines="skip")
        except Exception:
            continue
    raise ValueError(f"Could not read {path} with any supported encoding.")


def fetch_vic_grocery_ingredients() -> None:
    """Downloads the grocery dataset, filters to VIC, picks 1 item per Product_Group,
    and saves the result to ingredients_pricing_raw.csv."""

    logger.info(f"Downloading {settings.GROCERY_KAGGLE_DATASET} via kagglehub ...")
    dataset_path = kagglehub.dataset_download(settings.GROCERY_KAGGLE_DATASET)
    logger.info(f"Dataset downloaded to: {dataset_path}")

    # Extract any zip files found in the download folder
    for zip_path in glob.glob(os.path.join(dataset_path, "**", "*.zip"), recursive=True):
        logger.info(f"Extracting {zip_path} ...")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(dataset_path)

    csv_path = _find_csv(dataset_path)
    if not csv_path:
        logger.error(f"No CSV found in {dataset_path}. Contents: {os.listdir(dataset_path)}")
        return

    logger.info(f"Reading CSV: {csv_path}")
    df = _load_csv(csv_path)
    df.columns = df.columns.str.strip()
    logger.info(f"Loaded {len(df)} rows. Columns: {df.columns.tolist()}")

    # Find postcode column
    postal_col = next((c for c in df.columns if c.lower().startswith("postal")), None)
    if not postal_col:
        logger.error(f"No postcode column found. Columns: {df.columns.tolist()}")
        return

    # Filter to VIC (postcodes 3000–3999)
    df[postal_col] = df[postal_col].astype(str).str.strip()
    df_vic = df[df[postal_col].str.startswith("3")].copy()
    logger.info(f"VIC rows: {len(df_vic)}")

    if df_vic.empty:
        logger.error("No VIC rows found — check postcode column values.")
        return

    # Actual columns: package_size, Retail_price, Package_price, Price_per_unit
    # Parse pack_grams from 'package_size'
    package_col = next((c for c in df_vic.columns if c.lower() == "package_size"), None)
    df_vic["pack_grams"] = df_vic[package_col].apply(_parse_pack_grams) if package_col else None

    # price_aud  → Retail_price (actual shelf price)
    retail_col = next((c for c in df_vic.columns if c.lower() == "retail_price"), None)
    if not retail_col:
        logger.error(f"No Retail_price column found. Columns: {df_vic.columns.tolist()}")
        return
    df_vic["price_aud"] = pd.to_numeric(df_vic[retail_col], errors="coerce")

    # price_per_100g → Package_price (pre-computed per-unit price in dataset)
    pkg_price_col = next((c for c in df_vic.columns if c.lower() == "package_price"), None)
    if pkg_price_col:
        df_vic["price_per_100g"] = pd.to_numeric(df_vic[pkg_price_col], errors="coerce")
    else:
        pack = df_vic["pack_grams"].replace(0, float("nan"))
        df_vic["price_per_100g"] = (df_vic["price_aud"] / pack * 100).round(4)

    # Category / name columns
    cat_col   = next((c for c in df_vic.columns if c.lower() == "category"), None)
    sub_col   = next((c for c in df_vic.columns if c.lower() == "sub_category"), None)
    group_col = next((c for c in df_vic.columns if c.lower() == "product_group"), None)
    name_col  = next((c for c in df_vic.columns if c.lower() == "product_name"), None)

    if not name_col:
        logger.error(f"No Product_Name column. Columns: {df_vic.columns.tolist()}")
        return
    if not group_col:
        logger.error(f"No Product_Group column. Columns: {df_vic.columns.tolist()}")
        return

    df_vic["name"]        = df_vic[name_col].astype(str).str.strip()
    df_vic["category"]    = df_vic[cat_col].astype(str).str.strip() if cat_col else None
    df_vic["sub_category"] = df_vic[sub_col].astype(str).str.strip() if sub_col else None
    df_vic["_group"]      = df_vic[group_col].astype(str).str.strip()

    df_vic = df_vic.dropna(subset=["price_aud", "price_per_100g"])

    # 1 representative item per Product_Group (closest to group median price)
    group_keys = ["category", "sub_category", "_group"]
    group_medians = df_vic.groupby(group_keys)["price_aud"].transform("median")
    df_vic["_price_dist"] = (df_vic["price_aud"] - group_medians).abs()
    df_rep = (
        df_vic.sort_values("_price_dist")
        .groupby(group_keys, sort=False)
        .first()
        .reset_index()
    )

    keep = ["name", "category", "sub_category", "price_aud", "price_per_100g", "pack_grams"]
    if package_col and package_col in df_rep.columns:
        keep.append(package_col)

    df_out = df_rep[[c for c in keep if c in df_rep.columns]].copy()
    if package_col and package_col in df_out.columns:
        df_out = df_out.rename(columns={package_col: "package_size"})

    df_out["price_source"] = _PRICE_SOURCE
    df_out["price_as_of"]  = _PRICE_AS_OF
    df_out["benefit_tags"] = None

    df_out.to_csv(settings.INGREDIENTS_PRICING_RAW_PATH, index=False)
    logger.info(
        f"Saved {len(df_out)} rows ({df_out['category'].nunique()} categories) "
        f"→ {settings.INGREDIENTS_PRICING_RAW_PATH}"
    )


if __name__ == "__main__":
    fetch_vic_grocery_ingredients()
