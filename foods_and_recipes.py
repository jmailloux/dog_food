# foods_and_recipes.py
from __future__ import annotations

from typing import Dict, List
import pandas as pd

from nutrition_models import FoodCategory, FoodItem, Recipe


# Units:
# * kj_per_kg: prepared food energy density in kJ/kg
# * dollars_per_kg: prepared food cost in CAD per kg
#
# References for energy density are from USDA FoodData Central via MyFoodData pages.
# References for grocery prices are from Canadian grocery listings (No Frills / Real Canadian Superstore).
#
# Notes:
# * Rice dollars_per_kg is for *cooked* rice (dry rice cost / cooked yield). See notes on the FoodItem.

# --- Foods (prepared/cooked weights) ---

cooked_chicken_breast = FoodItem(
    name="Chicken breast, cooked (meat only)",
    category=FoodCategory.PROTEIN,
    kj_per_kg=6903.6,        # 165 kcal/100g -> 1650 kcal/kg -> 6903.6 kJ/kg
    dollars_per_kg=17.61,    # Real Canadian Superstore: $17.61/kg club pack listing (typical Waterloo pricing)
    notes="Energy: roasted chicken breast (USDA via MyFoodData). Price: RCS online listing.",
)

cooked_chicken_thigh = FoodItem(
    name="Chicken thigh, cooked (boneless/skinless)",
    category=FoodCategory.PROTEIN,
    kj_per_kg=7490.0,        # 179 kcal/100g -> 1790 kcal/kg -> ~7490 kJ/kg
    dollars_per_kg=20.92,    # Real Canadian Superstore search listing: $20.92/kg for boneless skinless thighs club pack
    notes="Energy: cooked boneless/skinless thigh (USDA via MyFoodData). Price: RCS online listing.",
)

cooked_white_rice = FoodItem(
    name="White rice, cooked (long-grain, enriched)",
    category=FoodCategory.CARB,
    kj_per_kg=5439.2,        # 130 kcal/100g -> 1300 kcal/kg -> 5439.2 kJ/kg
    dollars_per_kg=0.75,     # Derived from No Frills dry rice listing: $17 / 8 kg dry; assume 1 kg dry -> ~3 kg cooked
    notes="Energy: cooked long-grain white rice (USDA via FoodStruct). Price: derived from No Frills 8 kg bag; assumes ~3x cooked yield.",
)

mixed_vegetables = FoodItem(
    name="Mixed vegetables, frozen (prepared/cooked)",
    category=FoodCategory.VEG,
    kj_per_kg=3012.5,        # 72 kcal/100g -> 720 kcal/kg -> 3012.5 kJ/kg
    dollars_per_kg=3.25,     # No Frills: 2 kg bag $6.49 -> $3.25/kg
    notes="Energy: mixed veg frozen unprepared (USDA-style listing; close enough for cooked). Price: No Frills 2 kg frozen bag listing.",
)

green_beans = FoodItem(
    name="Green beans, cooked",
    category=FoodCategory.VEG,
    kj_per_kg=1757.3,        # 42 kcal/100g -> 420 kcal/kg -> 1757.3 kJ/kg
    dollars_per_kg=4.00,     # No Frills: 750 g $3.00 -> $4.00/kg
    notes="Energy: cooked green beans (USDA via MyFoodData). Price: No Frills frozen 750 g listing.",
)

cooked_carrots = FoodItem(
    name="Carrots, cooked (boiled, drained)",
    category=FoodCategory.VEG,
    kj_per_kg=1475.1,        # MyFoodData: 55 kcal per 156g -> 35.26 kcal/100g -> 352.6 kcal/kg -> 1475.1 kJ/kg
    dollars_per_kg=2.60,     # No Frills: 3 lb (1.362 kg) bag $3.49 -> $2.56/kg (rounded)
    notes="Energy: cooked carrots (USDA via MyFoodData; converted from 1 cup 156 g). Price: No Frills carrots bag listing.",
)

roasted_butternut_squash = FoodItem(
    name="Butternut squash, cooked (baked/roasted)",
    category=FoodCategory.VEG,
    kj_per_kg=1673.6,        # 82 kcal per 205g cup -> 40.0 kcal/100g -> 400 kcal/kg -> 1673.6 kJ/kg
    dollars_per_kg=4.39,     # No Frills: $4.39/kg fresh butternut squash
    notes="Energy: baked butternut squash (USDA via MyFoodData; converted from 1 cup 205 g). Price: No Frills fresh produce listing.",
)

eggshell_powder = FoodItem(
    name="Eggshell powder (calcium)",
    category=FoodCategory.SUPPLEMENT,
    kj_per_kg=0.0,
    dollars_per_kg=0.0,
    notes="Calories negligible. Calcium density is approximate; grind finely and mix thoroughly.",
)

fish_oil = FoodItem(
    name="Fish oil (omega-3 supplement)",
    category=FoodCategory.SUPPLEMENT,
    kj_per_kg=37000.0,       # ~9000 kcal/kg -> 37,656 kJ/kg (rounded)
    dollars_per_kg=115.0,    # Approx from Canadian retail liquid fish oil pricing (~$20.97 for ~200 ml)
    notes="Calories are real (fat). Price is a realistic retail estimate for liquid fish oil in Canada.",
)

FOODS: List[FoodItem] = [
    cooked_chicken_breast,
    cooked_chicken_thigh,
    cooked_white_rice,
    mixed_vegetables,
    green_beans,
    cooked_carrots,
    roasted_butternut_squash,
    eggshell_powder,
    fish_oil,
]

FOODS_BY_NAME: Dict[str, FoodItem] = {f.name: f for f in FOODS}


# --- Recipes (1 serving == 1 meal) ---
#
# Oakley is fed twice per day, so 2 servings/day.
# Targets are computed in the notebook via weight_loss_target_kj(ideal_weight_kg),
# and each of these recipes is tuned to be ~half the daily target for a 35 kg ideal weight
# (~2107 kJ per meal).

RECIPES: List[Recipe] = []

def _r(name: str) -> Recipe:
    r = Recipe(name=name)
    RECIPES.append(r)
    return r

# 1) Chicken breast + rice + mixed veg
r = _r("Breast + rice + mixed veg")
r.add(cooked_chicken_breast, 140)
r.add(cooked_white_rice, 156)
r.add(mixed_vegetables, 70)
r.add(fish_oil, 2)
r.add(eggshell_powder, 2)

# 2) Chicken thigh + rice + green beans
r = _r("Thigh + rice + green beans")
r.add(cooked_chicken_thigh, 130)
r.add(cooked_white_rice, 146)
r.add(green_beans, 150)
r.add(fish_oil, 2)
r.add(eggshell_powder, 2)

# 3) Mixed chicken + rice + carrots
r = _r("Mixed chicken + rice + carrots")
r.add(cooked_chicken_breast, 80)
r.add(cooked_chicken_thigh, 60)
r.add(cooked_white_rice, 136)
r.add(cooked_carrots, 200)
r.add(fish_oil, 2)
r.add(eggshell_powder, 2)

# 4) Chicken thigh + rice + roasted squash
r = _r("Thigh + rice + roasted squash")
r.add(cooked_chicken_thigh, 120)
r.add(cooked_white_rice, 146)
r.add(roasted_butternut_squash, 200)
r.add(fish_oil, 2)
r.add(eggshell_powder, 2)

RECIPES_BY_NAME: Dict[str, Recipe] = {r.name: r for r in RECIPES}


# --- Convenience DataFrames for the notebook ---

def foods_df() -> pd.DataFrame:
    rows = []
    for f in FOODS:
        rows.append(
            {
                "name": f.name,
                "category": f.category.name,
                "kj_per_kg": f.kj_per_kg,
                "dollars_per_kg": f.dollars_per_kg,
                "notes": f.notes,
            }
        )
    return pd.DataFrame(rows)

def recipes_df() -> pd.DataFrame:
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
