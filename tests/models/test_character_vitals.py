import pytest
from src.models.character.base import CharacterVitals, AbilityScores, AbilityType

@pytest.fixture
def vitals():
    return CharacterVitals()

@pytest.fixture
def abilities():
    return AbilityScores(dexterity=14) # Dex modifier of +2

def test_initiative_calculation(vitals, abilities):
    dex_modifier = abilities.get_modifier(AbilityType.DEXTERITY)
    assert vitals.calculate_initiative(dex_modifier) == 2

    vitals.initiative_modifier = 3
    assert vitals.calculate_initiative(dex_modifier) == 5

def test_death_saves(vitals):
    assert vitals.death_saves_successes == 0
    assert vitals.death_saves_failures == 0

    vitals.death_saves_successes = 1
    vitals.death_saves_failures = 2
    assert vitals.death_saves_successes == 1
    assert vitals.death_saves_failures == 2

def test_conditions(vitals):
    assert vitals.conditions == []

    vitals.conditions.append("Prone")
    assert "Prone" in vitals.conditions
