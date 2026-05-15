"""
personalisation_service.py
--------------------------
Extracts structured shopping preferences from a free-text description
using the Groq API (free tier, no billing required).

Requires GROQ_API_KEY environment variable. Without it the function
returns empty preferences and logs a warning.

Get a free key at: https://console.groq.com

Expected output (JSON):
{
  "preferred_sub_categories": ["Seafood", "Vegetables"],
  "nutrient_priorities": ["protein_g", "fibre_g"],
  "avoid_sub_categories": ["Pork"]
}

Valid sub_category values in the dataset:
Beef & veal, Breakfast, Cheese, Dairy, Eggs, Fruit, Lamb, Milk,
Mince, Oils & vinegars, Packaged Breads, Poultry, Pork, Seafood, Vegetables
"""
from __future__ import annotations

import json
import logging
import os
from typing import TypedDict

logger = logging.getLogger(__name__)

_GROQ_MODEL = "llama-3.1-8b-instant"
_MAX_TOKENS  = 300

_KNOWN_SUB_CATEGORIES = (
    "Beef & veal, Breakfast, Cheese, Dairy, Eggs, Fruit, Lamb, Milk, "
    "Mince, Oils & vinegars, Packaged Breads, Poultry, Pork, Seafood, Vegetables"
)

_SYSTEM_PROMPT = f"""You are a grocery planning assistant. Given a shopper's description, \
extract their preferences as JSON with exactly these three fields:
- preferred_sub_categories: list of sub-categories they would likely enjoy
- nutrient_priorities: list of nutrient column names they care about
  (valid values only: "protein_g", "fibre_g", "fat_total_g", "total_sugars_g")
- avoid_sub_categories: list of sub-categories to exclude

Only use sub-categories from this exact list: {_KNOWN_SUB_CATEGORIES}

Return ONLY valid JSON, no markdown, no explanation. Use empty lists when uncertain."""


class ShoppingPreferences(TypedDict):
    preferred_sub_categories: list[str]
    nutrient_priorities: list[str]
    avoid_sub_categories: list[str]


_EMPTY_PREFERENCES: ShoppingPreferences = {
    "preferred_sub_categories": [],
    "nutrient_priorities": [],
    "avoid_sub_categories": [],
}


def extract_preferences(description: str | None) -> ShoppingPreferences:
    """Call Groq to extract structured preferences from a free-text description.

    Returns empty preferences if description is blank, GROQ_API_KEY is not set,
    or the API call fails for any reason.
    """
    if not description or not description.strip():
        return _EMPTY_PREFERENCES

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        logger.warning("GROQ_API_KEY not set; skipping preference extraction.")
        return _EMPTY_PREFERENCES

    try:
        from groq import Groq  # lazy import — only required when key is present

        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=_GROQ_MODEL,
            max_tokens=_MAX_TOKENS,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user",   "content": description.strip()[:300]},
            ],
        )
        raw = response.choices[0].message.content.strip()

        # Strip markdown code fences if the model wraps the JSON anyway
        if raw.startswith("```"):
            parts = raw.split("```")
            raw = parts[1] if len(parts) > 1 else raw
            if raw.startswith("json"):
                raw = raw[4:]

        prefs = json.loads(raw)
        return {
            "preferred_sub_categories": list(prefs.get("preferred_sub_categories") or []),
            "nutrient_priorities":      list(prefs.get("nutrient_priorities") or []),
            "avoid_sub_categories":     list(prefs.get("avoid_sub_categories") or []),
        }

    except Exception as exc:
        logger.warning("Preference extraction failed: %s", exc)
        return _EMPTY_PREFERENCES
