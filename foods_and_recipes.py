# foods_and_recipes.py
from __future__ import annotations
from typing import Dict, List
import pandas as pd

from nutrition_models import FoodCategory, FoodItem, Recipe

# Approximate example values.
# You can refine these per 100 g labels, then convert:
# kcal/100g * 10 = kcal/kg; then * 4.184 = kJ/kg.

# --- Foods ---

chicken_breast = FoodItem(
    name="Cooked chicken breast",
    category=FoodCategory.PROTEIN,
    kj_per_kg=6900.0,      # ~1650 kcal/kg * 4.184
    dollars_per_kg=12.00,  # example price
)

brown_rice = FoodItem(
    name="Cooked brown rice",
    category=FoodCategory.CARB,
    kj_per_kg=4600.0,      # ~1100 kcal/kg * 4.184
    dollars_per_kg=3.00,
)

mixed_veg = FoodItem(
    name="Steamed mixed veg",
    category=FoodCategory.VEG,
    kj_per_kg=1500.0,      # ~360 kcal/kg * 4.184 (rough)
    dollars_per_kg=4.00,
)

pumpkin_puree = FoodItem(
    name="Pumpkin puree",
    category=FoodCategory.CARB,
    kj_per_kg=1500.0,      # rough placeholder
    dollars_per_kg=2.50,
    notes="Check max daily fiber amount with vet",
)

fish_oil = FoodItem(
    name="Fish oil",
    category=FoodCategory.SUPPLEMENT,
    kj_per_kg=38000.0,     # ~9000 kcal/kg * 4.184
    dollars_per_kg=30.00,
    notes="Dose per vet instructions",
)

FOODS_BY_NAME: Dict[str, FoodItem] = {
    f.name: f
    for f in [
        chicken_breast,
        brown_rice,
        mixed_veg,
        pumpkin_puree,
        fish_oil,
    ]
}

FOODS: List[FoodItem] = list(FOODS_BY_NAME.values())


def foods_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": [f.name for f in FOODS],
            "category": [f.category.name for f in FOODS],
            "kj_per_kg": [f.kj_per_kg for f in FOODS],
            "dollars_per_kg": [f.dollars_per_kg for f in FOODS],
            "notes": [f.notes for f in FOODS],
        }
    )


# --- Recipes ---

# Base weight-loss daily stew (example numbers)
base_daily = Recipe(name="Base daily stew")
base_daily.add(chicken_breast, grams=250.0)
base_daily.add(brown_rice, grams=150.0)
base_daily.add(mixed_veg, grams=100.0)
base_daily.add(pumpkin_puree, grams=50.0)
base_daily.add(fish_oil, grams=5.0)

# Slightly lighter variant
light_daily = Recipe(name="Light daily stew")
light_daily.add(chicken_breast, grams=220.0)
light_daily.add(brown_rice, grams=130.0)
light_daily.add(mixed_veg, grams=120.0)
light_daily.add(pumpkin_puree, grams=70.0)
light_daily.add(fish_oil, grams=5.0)

RECIPES_BY_NAME: Dict[str, Recipe] = {
    r.name: r
    for r in [
        base_daily,
        light_daily,
    ]
}

RECIPES: List[Recipe] = list(RECIPES_BY_NAME.values())


def recipes_df() -> pd.DataFrame:
    """
    One row per ingredient per recipe, with energy and cost.
    """
    rows = []
    for r in RECIPES:
        for ing in r.ingredients:
            rows.append(
                {
                    "recipe_name": r.name,
                    "food_name": ing.food.name,
                    "grams": ing.grams,
                    "energy_kj": ing.energy_kj,
                    "energy_kcal": ing.energy_kcal,
                    "ingredient_cost": ing.cost,
                    "recipe_total_kj": r.total_kj,
                    "recipe_total_kcal": r.total_kcal,
                    "recipe_total_cost": r.total_cost,
                }
            )
    return pd.DataFrame(rows)