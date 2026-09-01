import pytest
from pydantic import ValidationError

from lab05.schemas import Item, Quest


def test_quest_ok():
    Quest(title="Тест", giver="A", objective="B", steps=["1", "2"], reward="C", difficulty=3)


def test_item_bad_rarity():
    with pytest.raises(ValidationError):
        Item(name="x", type="weapon", rarity="godlike", description="d")
