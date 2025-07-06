"""
Armor models for D&D 5e equipment system
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from enum import Enum
from .base import Equipment, EquipmentType, Rarity

class ArmorCategory(Enum):
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"
    SHIELD = "shield"

@dataclass
class Armor(Equipment):
    """D&D 5e armor implementation"""
    category: ArmorCategory = ArmorCategory.LIGHT
    base_ac: int = 10
    max_dex_bonus: Optional[int] = None  # None = unlimited
    min_strength: Optional[int] = None
    stealth_disadvantage: bool = False
    magic_bonus: int = 0
    
    def __post_init__(self):
        super().__post_init__()
        self.type = EquipmentType.ARMOR
    
    def calculate_ac(self, dex_modifier: int) -> int:
        """Calculate AC with this armor equipped"""
        if self.max_dex_bonus is not None:
            dex_bonus = min(dex_modifier, self.max_dex_bonus)
        else:
            dex_bonus = dex_modifier
        
        return self.base_ac + dex_bonus + self.magic_bonus
    
    def meets_strength_requirement(self, strength_score: int) -> bool:
        """Check if character meets strength requirement"""
        if self.min_strength is None:
            return True
        return strength_score >= self.min_strength
    
    def causes_stealth_disadvantage(self) -> bool:
        """Check if armor causes stealth disadvantage"""
        return self.stealth_disadvantage
    
    def is_light_armor(self) -> bool:
        return self.category == ArmorCategory.LIGHT
    
    def is_medium_armor(self) -> bool:
        return self.category == ArmorCategory.MEDIUM
    
    def is_heavy_armor(self) -> bool:
        return self.category == ArmorCategory.HEAVY
    
    def is_shield(self) -> bool:
        return self.category == ArmorCategory.SHIELD

@dataclass
class Shield(Armor):
    """Shield implementation"""
    
    def __init__(self, name: str = "Shield", **kwargs):
        super().__init__(
            name=name,
            category=ArmorCategory.SHIELD,
            base_ac=2,  # Shields add +2 AC
            max_dex_bonus=None,
            **kwargs
        )
    
    def calculate_ac_bonus(self) -> int:
        """Shields provide AC bonus, not base AC"""
        return self.base_ac + self.magic_bonus


# Predefined armor from D&D 5e SRD
LIGHT_ARMOR = {
    "Padded": Armor(
        name="Padded",
        category=ArmorCategory.LIGHT,
        base_ac=11,
        max_dex_bonus=None,
        stealth_disadvantage=True,
        weight=8.0,
        value=500  # 5 gp
    ),
    "Leather": Armor(
        name="Leather",
        category=ArmorCategory.LIGHT,
        base_ac=11,
        max_dex_bonus=None,
        weight=10.0,
        value=1000  # 10 gp
    ),
    "Studded leather": Armor(
        name="Studded leather",
        category=ArmorCategory.LIGHT,
        base_ac=12,
        max_dex_bonus=None,
        weight=13.0,
        value=4500  # 45 gp
    ),
}

MEDIUM_ARMOR = {
    "Hide": Armor(
        name="Hide",
        category=ArmorCategory.MEDIUM,
        base_ac=12,
        max_dex_bonus=2,
        weight=12.0,
        value=1000  # 10 gp
    ),
    "Chain shirt": Armor(
        name="Chain shirt",
        category=ArmorCategory.MEDIUM,
        base_ac=13,
        max_dex_bonus=2,
        weight=20.0,
        value=5000  # 50 gp
    ),
    "Scale mail": Armor(
        name="Scale mail",
        category=ArmorCategory.MEDIUM,
        base_ac=14,
        max_dex_bonus=2,
        stealth_disadvantage=True,
        weight=45.0,
        value=5000  # 50 gp
    ),
    "Breastplate": Armor(
        name="Breastplate",
        category=ArmorCategory.MEDIUM,
        base_ac=14,
        max_dex_bonus=2,
        weight=20.0,
        value=40000  # 400 gp
    ),
    "Half plate": Armor(
        name="Half plate",
        category=ArmorCategory.MEDIUM,
        base_ac=15,
        max_dex_bonus=2,
        stealth_disadvantage=True,
        weight=40.0,
        value=75000  # 750 gp
    ),
}

HEAVY_ARMOR = {
    "Ring mail": Armor(
        name="Ring mail",
        category=ArmorCategory.HEAVY,
        base_ac=14,
        max_dex_bonus=0,
        stealth_disadvantage=True,
        weight=40.0,
        value=3000  # 30 gp
    ),
    "Chain mail": Armor(
        name="Chain mail",
        category=ArmorCategory.HEAVY,
        base_ac=16,
        max_dex_bonus=0,
        min_strength=13,
        stealth_disadvantage=True,
        weight=55.0,
        value=7500  # 75 gp
    ),
    "Splint": Armor(
        name="Splint",
        category=ArmorCategory.HEAVY,
        base_ac=17,
        max_dex_bonus=0,
        min_strength=15,
        stealth_disadvantage=True,
        weight=60.0,
        value=200000  # 200 gp
    ),
    "Plate": Armor(
        name="Plate",
        category=ArmorCategory.HEAVY,
        base_ac=18,
        max_dex_bonus=0,
        min_strength=15,
        stealth_disadvantage=True,
        weight=65.0,
        value=150000  # 1500 gp
    ),
}

SHIELDS = {
    "Shield": Shield(
        name="Shield",
        weight=6.0,
        value=1000  # 10 gp
    ),
}

# Combined armor database
ALL_ARMOR = {
    **LIGHT_ARMOR,
    **MEDIUM_ARMOR,
    **HEAVY_ARMOR,
    **SHIELDS,
}