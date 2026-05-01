import pandas as pd

from .utils import initial_cleaning_pipeline


def translate_nutrient_goals_to_actions(df: pd.DataFrame) -> pd.DataFrame:
    """Translate nutrient goals to actionable guidance for parents."""
    def _get_guidance(row):
        age = row['age']
        nutrient = row['nutrient']
        
        guidance_map = {
            "Energy": {
                "0-6 months": "Stick to exclusive breastfeeding or formula.",
                "7-12 months": "Continue milk; add energy-dense mashed foods like banana or avocado.",
                "1-3 years": "Offer 3 small meals and 2 healthy snacks; don't worry if they eat less some days.",
                "4-8 years": "Provide a mix of grains, proteins, and fruits to fuel active play.",
                "9-13 years": "Increase portions of filling foods like potatoes and pasta for growth spurts."
            },
            "Protein": {
                "0-6 months": "Fully provided by breastmilk or formula.",
                "7-12 months": "Try iron-rich soft foods: mashed beans, lentils, eggs, or finely minced meat.",
                "1-3 years": "Milk, eggs, and peanut butter (if no allergy) are great low-cost proteins.",
                "4-8 years": "Include beans, peas, or canned tuna to help with growth and healing.",
                "9-13 years": "Focus on bigger servings of protein to support developing muscles and hormones."
            },
            "Dietary fibre": {
                "0-6 months": "Not needed; milk is fiber-free.",
                "7-12 months": "Focus on iron and energy first; fiber is not a priority yet.",
                "1-3 years": "Offer affordable high-fiber foods like oats (porridge) and seasonal fruits.",
                "4-8 years": "Use whole-grain bread and lentils to help keep their bathroom habits regular.",
                "9-13 years": "Encourage beans and high-fiber cereal for a healthy gut."
            },
            "Fluid": {
                "0-6 months": "No extra water needed; milk provides all hydration.",
                "7-12 months": "Offer a cup with small sips of water during meal times.",
                "default": "Water and plain milk are the best and cheapest ways to stay hydrated."
            }
        }

        # Return specific guidance or a fallback generic message
        nutrient_guide = guidance_map.get(nutrient, {})
        return nutrient_guide.get(age, nutrient_guide.get("default", "Eat a variety of affordable whole foods."))

    df['actionable_guidance'] = df.apply(_get_guidance, axis=1)
    return df
    

def add_portion_guidance(df: pd.DataFrame) -> pd.DataFrame:
    """Add portion guidance to the recommended macronutrients intake dataset."""
    def _get_portion(row):
        age = row['age']
        nutrient = row['nutrient']
        
        # Mapping technical goals to visual, easy-to-measure portions
        portions = {
            "Energy": {
                "0-6 months": "Feed on demand (usually 8-12 times a day)",
                "7-12 months": "About 1/2 to 1 cup of mashed food per meal",
                "1-3 years": "A child-sized bowl (about 1 cup) of food per meal",
                "4-8 years": "One small plate with a mix of food groups",
                "9-13 years": "An adult-sized plate, but slightly smaller portions"
            },
            "Protein": {
                "7-12 months": "1-2 tablespoons of mashed beans or minced meat",
                "1-3 years": "A piece of meat or tofu about the size of their palm",
                "4-8 years": "A portion about the size of their whole hand",
                "9-13 years": "2 portions the size of their palm throughout the day"
            },
            "Dietary fibre": {
                "1-3 years": "1-2 small handfuls of fruit or cooked veggies",
                "4-8 years": "2-3 handfuls of colorful veggies or beans",
                "9-13 years": "A large handful of high-fiber grains (oats/brown rice) at most meals"
            },
            "Fluid": {
                "0-6 months": "None (milk only)",
                "7-12 months": "A few small sips (2-4 oz) from a cup at meals",
                "1-3 years": "About 4 small child-sized cups per day",
                "4-8 years": "About 5 regular glasses of water daily",
                "9-13 years": "6-8 regular glasses of water daily"
            }
        }

        # Logic to return the portion or a default if not found
        nutrient_map = portions.get(nutrient, {})
        return nutrient_map.get(age, "Varies by appetite")
    
    df['portion_guide'] = df.apply(_get_portion, axis=1)
    return df


def wrangle_recommended_macronutrients_intake(df: pd.DataFrame) -> pd.DataFrame:
    """Wrangle the recommended macronutrients intake dataset."""
    df = initial_cleaning_pipeline(df)
    df = translate_nutrient_goals_to_actions(df)
    df = add_portion_guidance(df)

    return df
