import pandas as pd

from .utils import initial_cleaning_pipeline, select_columns, rename_columns


# Manual mapping of 10 recipes per cuisine based on ingredient analysis
DISH_MAPPING = {
    # Brazilian
    31634: "Brazilian Rum Punch", 21052: "Coconut Chicken Stew", 623: "Brigadeiros",
    26667: "Classic Caipirinha", 15482: "Condensed Milk Pudding", 9812: "Moqueca (Fish Stew)",
    47029: "Pao de Queijo", 203: "Acai Bowl", 34662: "Lager Braised Chicken", 25507: "Coxinha",
    # British
    34466: "Lemon Raspberry Fool", 7473: "Eccles Cakes", 44776: "Yorkshire Pudding",
    24351: "Colcannon", 30649: "Current Scones", 47826: "Irish/British Lamb Stew",
    34240: "Summer Vegetable Tart", 28056: "Beer Battered Fish", 24410: "Fig Pudding",
    11757: "Marmite Bagel",
    # Cajun Creole
    27976: "Mango Salsa Fish", 34419: "Seafood Gumbo", 37963: "Quick Jambalaya",
    22825: "Blue Cheese Burger", 46975: "Cajun Jambalaya", 27008: "Cornflake Catfish",
    3457: "Andouille Bean Stew", 41363: "Classic Chicken Gumbo", 49175: "Cajun Grits",
    36583: "Fried Shrimp",
    # Chinese
    45887: "Green Bean Stir Fry", 29630: "Tofu Broccoli Stir Fry", 26705: "Beef Lo Mein",
    9197: "Pork Egg Rolls", 27564: "Mandarin Orange Cake", 4574: "Pork Dumplings",
    44812: "Five Spice Roast Duck", 9406: "Ginger Chicken Rice", 34367: "Pork Rib Soup",
    21467: "Shiitake Tofu Bowl",
    # Filipino
    20130: "Chicken Sisig", 11300: "Five Spice Chicken Thighs", 45605: "Filipino Cucumber Salad",
    1110: "Chicken Adobo", 48911: "Lumpiang Sariwa", 9829: "Adobo Pork Chops",
    23839: "Classic Pork Adobo", 29887: "Karioka (Coconut Balls)", 18329: "Beef Mami",
    30835: "Lemongrass Roasted Chicken",
    # French
    18515: "Fennel Grapefruit Salad", 275: "Pastry Cream", 43769: "Pumpkin Mousse",
    6886: "Foie Gras Toast", 39471: "Asparagus Quiche", 9069: "Mediterranean Bean Salad",
    7501: "Nicoise Sandwich", 40064: "Potato Gratin", 36862: "Apple Cinnamon Tart",
    18643: "Vanilla Custard",
    # Greek
    10259: "Greek Salad", 34471: "Sheftalia (Pork Sausages)", 4635: "Souvlakia",
    5980: "Honey Fig Pudding", 18031: "Spanakopita", 24338: "Lamb Burger with Feta",
    22678: "Lamb Gyros", 35408: "Classic Hummus", 32480: "Octopus in Red Wine",
    11665: "Mint Yogurt Parfait",
    # Indian
    22213: "Roti", 13162: "Butter Chicken", 24717: "Red Lentil Dal",
    36341: "Curry Salmon", 38112: "Dosa with Potatoes", 11913: "Chicken Curry",
    45839: "Chickpea Burgers", 14874: "Fenugreek Potatoes", 43399: "Garam Masala Blend",
    33989: "Shrimp Curry",
    # Irish
    5206: "Leek and Potato Soup", 31027: "Irish Tea Cake", 18624: "Blue Cheese Tart",
    35132: "Coddle", 37188: "Steel Cut Oats", 48576: "Guinness Beef Stew",
    12099: "Apple Wheat Germ Cake", 47406: "Shortbread", 24640: "Brown Bread",
    48722: "Beef Wellington",
    # Italian
    3735: "Cranberry Biscotti", 12734: "Bruschetta Topping", 5875: "Italian Sausage Mix",
    2698: "Walnut Trout", 31908: "Gnocchi Gratin", 1420: "Zesty Italian Chicken",
    49136: "Linguine Puttanesca", 22087: "Chicken Tetrazzini", 40429: "Polenta",
    39250: "Tomato Basil Sauce",
    # Jamaican
    6602: "Jamaican Ginger Cake", 3535: "Beef Patties", 20591: "Curried Mince",
    6043: "Coconut Chicken & Rice", 28342: "Jerk Chicken", 13554: "Spinach Zucchini Stew",
    38292: "Jerk Chicken Wings", 11696: "Jerk Pork Butt", 39364: "Escovitch Fish",
    19160: "Coconut Shrimp & Okra",
    # Japanese
    5767: "Sukiyaki", 47028: "Matcha Walnut Cake", 29061: "Beef and Asparagus",
    8997: "Tempura Prawns", 25751: "Tonkatsu", 41961: "Braised Beef with Daikon",
    46205: "Vegetable Samosas (Fusion)", 9010: "Miso Udon", 41833: "Miso Soup",
    8480: "Chicken Karaage",
    # Korean
    8530: "Bibimbap", 17004: "Barley Water", 7782: "Korean Steak Tacos",
    47095: "Jajangmyeon", 27165: "Korean Egg Soup", 34248: "Bulgogi Pork",
    2472: "Seaweed Soup", 14970: "Korean Fried Wings", 428: "Sesame Soy Kale",
    242: "Bulgogi Lettuce Wraps",
    # Mexican
    16903: "Pork Pineapple Tacos", 41995: "Carne Asada", 40523: "Pico de Gallo",
    1299: "Sausage Breakfast Burrito", 10276: "Taco Seasoning", 32304: "Chicken Enchiladas",
    29369: "Avocado Chicken Salad", 2107: "Guacamole", 25164: "Kahlua Espresso Cream",
    39600: "Green Pozole",
    # Moroccan
    699: "Ras el Hanout Mix", 16582: "Harira Soup", 9058: "Chicken Couscous",
    27858: "Lamb Penne with Ras el Hanout", 41301: "Saffron Chickpea Rice", 16712: "Lamb with Tomatoes",
    40300: "Eggplant Chickpea Stew", 33717: "Lamb Couscous", 35311: "Ginger Chicken Couscous",
    5687: "Apricot Lamb Couscous",
    # Russian
    38346: "Kasha with Mozzarella", 35962: "Borscht", 49388: "Mushroom Ham Crepes",
    15753: "Chicken Kiev", 39356: "Cabbage and Radish Salad", 9660: "Blini",
    24891: "Orange Glazed Beets", 43304: "Shchi (Cabbage Soup)", 14844: "Syrniki (Cheese Pancakes)",
    16450: "Beer Braised Ham",
    # Southern US
    25693: "Fried Green Tomatoes", 40989: "Potato Salad", 17610: "Black Eyed Pea Dip",
    37405: "Collard Greens with Ham", 3335: "Southern Cornbread", 4499: "Crawfish Dip",
    4906: "Creamy Coleslaw", 30748: "Cheese Grits", 44902: "Buttermilk Cornbread",
    49111: "Sweet Green Beans",
    # Spanish
    42779: "Spanish Surf and Turf", 11886: "Manchego Serrano Sandwich", 4969: "Tortilla Española",
    793: "Rum Glazed Shrimp", 20665: "Crema Catalana", 17771: "Spanish Pepper Salad",
    42967: "Mixed Paella", 45352: "Spinach Artichoke Salad", 31009: "Chickpea Spinach Tapas",
    18271: "White Bean and Kale Stew",
    # Thai
    2941: "Nam Jim (Dipping Sauce)", 13121: "Fresh Spring Rolls", 33465: "Pad Thai",
    38233: "Garlic Pepper Chicken", 39267: "Coconut Peanut Ribs", 43928: "Thai Red Curry",
    5924: "Green Curry Cashew Chicken", 26676: "Green Curry Noodle Soup", 6164: "Tom Yum Goong",
    19811: "Chicken Satay Wraps",
    # Vietnamese
    8152: "Vietnamese Fried Rice", 4715: "Vietnamese Iced Coffee", 33603: "Summer Rolls",
    30382: "Nuoc Cham Sauce", 20792: "Rice Flour Batter", 24365: "Bun Bo Nam Bo",
    38717: "Shaking Beef (Bo Luc Lac)", 30250: "Grilled Pork Spring Rolls", 14308: "Vietnamese Shrimp Salad",
    34784: "Vietnamese Noodle Salad"
}


def _add_dish_names(df: pd.DataFrame) -> pd.DataFrame:
    """Manually adds dish names based on the hardcoded mapping."""
    df["dish_name"] = df["id"].map(DISH_MAPPING).fillna("Unknown Dish")
    return df


def _capitalise_country(df: pd.DataFrame) -> pd.DataFrame:
    """Capitalises the cuisine/country name."""
    df["cuisine"] = df["cuisine"].str.replace('_', ' ').str.capitalize()
    return df


def wrangle_recipe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare recipe dataset with manual dish names."""
    df = initial_cleaning_pipeline(df)
    df = df[df["id"].isin(DISH_MAPPING.keys())]
    df = _add_dish_names(df)
    df = _capitalise_country(df)
    df = select_columns(df, included_cols=["id", "cuisine", "dish_name"])
    df = df.drop_duplicates()
    df = df.sort_values(by=["cuisine", "dish_name"])
    df = rename_columns(df, cols_rename_map={
        "id": "recipe_id", 
        "cuisine": "country",
    })
    
    return df