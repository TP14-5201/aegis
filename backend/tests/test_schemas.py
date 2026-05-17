import math

from src.schemas import SubstituteSlotOut


def _slot_payload(**overrides):
    payload = {
        "ingredient_code": "A1",
        "product_name": "Apples",
        "similarity_score": 0.9,
        "objective_score": 0.8,
    }
    payload.update(overrides)
    return payload


def test_substitute_slot_converts_nan_sub_category_to_none():
    slot = SubstituteSlotOut(**_slot_payload(sub_category=math.nan))

    assert slot.sub_category is None


def test_substitute_slot_converts_nan_brands_to_none():
    slot = SubstituteSlotOut(**_slot_payload(brands=math.nan))

    assert slot.brands is None


def test_substitute_slot_keeps_non_nan_values():
    slot = SubstituteSlotOut(**_slot_payload(sub_category="Fruit", brands="Market"))

    assert slot.sub_category == "Fruit"
    assert slot.brands == "Market"
