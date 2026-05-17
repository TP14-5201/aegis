import pandas as pd

from src.data.wranglers.recommended_macronutrients_intake_wrangler import (
    add_portion_guidance,
    translate_nutrient_goals_to_actions,
    wrangle_recommended_macronutrients_intake,
)


def test_translate_nutrient_goals_to_actions_uses_age_specific_guidance():
    df = pd.DataFrame(
        [
            {"age": "0-6 months", "nutrient": "Energy"},
            {"age": "7-12 months", "nutrient": "Protein"},
            {"age": "1-3 years", "nutrient": "Dietary fibre"},
            {"age": "9-13 years", "nutrient": "Fluid"},
            {"age": "4-8 years", "nutrient": "Unknown"},
        ]
    )

    result = translate_nutrient_goals_to_actions(df)

    assert result["actionable_guidance"].iloc[0] == "Stick to exclusive breastfeeding or formula."
    assert "iron-rich" in result["actionable_guidance"].iloc[1]
    assert "oats" in result["actionable_guidance"].iloc[2]
    assert result["actionable_guidance"].iloc[3] == "Water and plain milk are the best and cheapest ways to stay hydrated."
    assert result["actionable_guidance"].iloc[4] == "Eat a variety of affordable whole foods."


def test_add_portion_guidance_uses_age_specific_portions_and_fallbacks():
    df = pd.DataFrame(
        [
            {"age": "7-12 months", "nutrient": "Energy"},
            {"age": "9-13 years", "nutrient": "Protein"},
            {"age": "4-8 years", "nutrient": "Dietary fibre"},
            {"age": "0-6 months", "nutrient": "Fluid"},
            {"age": "0-6 months", "nutrient": "Protein"},
            {"age": "1-3 years", "nutrient": "Unknown"},
        ]
    )

    result = add_portion_guidance(df)

    assert result["portion_guide"].iloc[0] == "About 1/2 to 1 cup of mashed food per meal"
    assert result["portion_guide"].iloc[1] == "2 portions the size of their palm throughout the day"
    assert "colorful veggies" in result["portion_guide"].iloc[2]
    assert result["portion_guide"].iloc[3] == "None (milk only)"
    assert result["portion_guide"].iloc[4] == "Varies by appetite"
    assert result["portion_guide"].iloc[5] == "Varies by appetite"


def test_wrangle_recommended_macronutrients_intake_cleans_columns_and_adds_guidance():
    df = pd.DataFrame(
        [
            {
                "Age": " 1-3 years ",
                "Nutrient": "Protein",
                "Goal": "Grow",
            }
        ]
    )

    result = wrangle_recommended_macronutrients_intake(df)

    assert list(result.columns) == [
        "age",
        "nutrient",
        "goal",
        "actionable_guidance",
        "portion_guide",
    ]
    assert result["age"].iloc[0] == "1-3 years"
    assert "peanut butter" in result["actionable_guidance"].iloc[0]
    assert result["portion_guide"].iloc[0] == "A piece of meat or tofu about the size of their palm"
