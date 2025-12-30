# nutrition_models.py
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict
from datetime import date

# --- Constants and conversions ---

KJ_PER_KCAL = 4.184


def kcal_to_kj(kcal: float) -> float:
    return kcal * KJ_PER_KCAL


def kj_to_kcal(kj: float) -> float:
    return kj / KJ_PER_KCAL


# --- Core enums and dataclasses ---

class FoodCategory(Enum):
    PROTEIN = auto()
    CARB = auto()
    FAT = auto()
    VEG = auto()
    SUPPLEMENT = auto()
    OTHER = auto()


@dataclass(frozen=True)
class FoodItem:
    """
    Energy: kJ/kg (SI)
    Cost: dollars/kg (CAD or whatever you want)
    """
    name: str
    category: FoodCategory
    kj_per_kg: float
    dollars_per_kg: float
    notes: str = ""

    @property
    def kj_per_gram(self) -> float:
        return self.kj_per_kg / 1000.0

    def energy_kj(self, grams: float) -> float:
        return self.kj_per_gram * grams

    def energy_kcal(self, grams: float) -> float:
        return kj_to_kcal(self.energy_kj(grams))

    def cost(self, grams: float) -> float:
        return self.dollars_per_kg * (grams / 1000.0)


@dataclass
class RecipeIngredient:
    food: FoodItem
    grams: float

    @property
    def energy_kj(self) -> float:
        return self.food.energy_kj(self.grams)

    @property
    def energy_kcal(self) -> float:
        return self.food.energy_kcal(self.grams)

    @property
    def cost(self) -> float:
        return self.food.cost(self.grams)


@dataclass
class Recipe:
    name: str
    ingredients: List[RecipeIngredient] = field(default_factory=list)
    notes: str = ""

    def add(self, food: FoodItem, grams: float) -> None:
        self.ingredients.append(RecipeIngredient(food, grams))

    @property
    def total_kj(self) -> float:
        return sum(ing.energy_kj for ing in self.ingredients)

    @property
    def total_kcal(self) -> float:
        return kj_to_kcal(self.total_kj)

    @property
    def total_cost(self) -> float:
        return sum(ing.cost for ing in self.ingredients)

    def energy_kj_by_food(self) -> Dict[str, float]:
        out: Dict[str, float] = {}
        for ing in self.ingredients:
            name = ing.food.name
            out[name] = out.get(name, 0.0) + ing.energy_kj
        return out

    def energy_kj_by_category(self) -> Dict[FoodCategory, float]:
        out: Dict[FoodCategory, float] = {}
        for ing in self.ingredients:
            cat = ing.food.category
            out[cat] = out.get(cat, 0.0) + ing.energy_kj
        return out


@dataclass
class DogProfile:
    name: str
    current_weight_kg: float
    ideal_weight_kg: float
    neutered: bool = True
    notes: str = ""


@dataclass
class WeightEntry:
    day: date
    weight_kg: float
    notes: str = ""


# --- Calorie (kcal) math for RER / weight loss ---

def rer_kg(weight_kg: float) -> float:
    """
    Resting Energy Requirement (kcal/day) = 70 * kg^0.75
    Uses kcal because that’s how the veterinary formulas are defined.
    """
    return 70.0 * (weight_kg ** 0.75)


def weight_loss_target_kcal(ideal_weight_kg: float, factor: float = 0.8) -> float:
    """
    Typical guideline: feed ~80% of ideal-weight RER for weight loss.
    Returns kcal/day.
    """
    return rer_kg(ideal_weight_kg) * factor


def weight_loss_target_kj(ideal_weight_kg: float, factor: float = 0.8) -> float:
    """
    Same as weight_loss_target_kcal, but in kJ/day.
    """
    return kcal_to_kj(weight_loss_target_kcal(ideal_weight_kg, factor=factor))


@dataclass
class DailyMealPlan:
    day: date
    recipes: List[Recipe] = field(default_factory=list)

    def add_recipe(self, recipe: Recipe) -> None:
        self.recipes.append(recipe)

    @property
    def total_kj(self) -> float:
        return sum(r.total_kj for r in self.recipes)

    @property
    def total_kcal(self) -> float:
        return kj_to_kcal(self.total_kj)

    @property
    def total_cost(self) -> float:
        return sum(r.total_cost for r in self.recipes)


def grocery_list_from_plans(plans: List[DailyMealPlan]) -> Dict[FoodItem, float]:
    """
    Returns mapping FoodItem -> total grams across the given plans.
    """
    totals: Dict[FoodItem, float] = {}
    for plan in plans:
        for recipe in plan.recipes:
            for ing in recipe.ingredients:
                totals[ing.food] = totals.get(ing.food, 0.0) + ing.grams
    return totals
