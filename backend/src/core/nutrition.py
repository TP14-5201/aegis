NRV_PER_100G: dict[str, float] = {
    "protein":               50.0,
    "calcium":               1000.0,
    "carbohydrate":          310.0,
    "iron":                  18.0,
    "energy_kcal":           2000.0,
    "total_fat":             70.0,
    "vitamin_c":             45.0,
    "vitamin_d":             0.015,
    "zinc":                  8.0,
    "magnesium":             320.0,
    "potassium":             2800.0,
    "vitamin_b12":           0.0024,
    "vitamin_b6":            1.3,
    "folate":                0.4,
    "omega_3_polyunsaturated": 1.6,
}

NUTRIENT_BENEFIT_MAP: dict[str, str] = {
    "protein":                  "Muscles",
    "calcium":                  "Muscles",
    "carbohydrate":             "Energy",
    "iron":                     "Energy",
    "energy_kcal":              "Energy",
    "total_fat":                "Energy",
    "vitamin_c":                "Immunity",
    "vitamin_d":                "Immunity",
    "zinc":                     "Immunity",
    "vitamin_b12":              "Brain",
    "folate":                   "Brain",
    "omega_3_polyunsaturated":  "HeartHealthy",
    "potassium":                "HeartHealthy",
    "magnesium":                "BetterSleep",
    "vitamin_b6":               "StressEasing",
}

# Nutrients weighted in recommendation scoring (child-relevant per NHMRC NRVs)
SCORED_NUTRIENTS = {"protein", "iron", "vitamin_c", "calcium", "vitamin_d"}
