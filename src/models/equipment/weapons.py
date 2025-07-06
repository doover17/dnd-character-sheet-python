"""
Weapon models for D&D 5e equipment system
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from .base import Equipment, EquipmentType, Rarity

class WeaponCategory(Enum):
    SIMPLE_MELEE = "simple_melee"
    SIMPLE_RANGED = "simple_ranged"
    MARTIAL_MELEE = "martial_melee"
    MARTIAL_RANGED = "martial_ranged"

class DamageType(Enum):
    BLUDGEONING = "bludgeoning"
    PIERCING = "piercing"
    SLASHING = "slashing"
    ACID = "acid"
    COLD = "cold"
    FIRE = "fire"
    FORCE = "force"
    LIGHTNING = "lightning"
    NECROTIC = "necrotic"
    POISON = "poison"
    PSYCHIC = "psychic"
    RADIANT = "radiant"
    THUNDER = "thunder"

class WeaponProperty(Enum):
    AMMUNITION = "ammunition"
    FINESSE = "finesse"
    HEAVY = "heavy"
    LIGHT = "light"
    LOADING = "loading"
    RANGE = "range"
    REACH = "reach"
    SPECIAL = "special"
    THROWN = "thrown"
    TWO_HANDED = "two_handed"
    VERSATILE = "versatile"

@dataclass
class WeaponRange:
    """Weapon range information"""
    normal: int
    long: Optional[int] = None
    
    @property
    def is_ranged(self) -> bool:
        return self.long is not None

@dataclass
class Weapon(Equipment):
    """D&D 5e weapon implementation"""
    category: WeaponCategory = WeaponCategory.SIMPLE_MELEE
    damage_dice: str = "1d4"
    damage_type: DamageType = DamageType.BLUDGEONING
    properties: List[WeaponProperty] = field(default_factory=list)
    weapon_range: Optional[WeaponRange] = None
    versatile_damage: Optional[str] = None  # For versatile weapons
    magic_bonus: int = 0
    
    def __post_init__(self):
        super().__post_init__()
        self.type = EquipmentType.WEAPON
        
        # Set default range for melee weapons
        if not self.weapon_range:
            if self.category in [WeaponCategory.SIMPLE_MELEE, WeaponCategory.MARTIAL_MELEE]:
                reach = 10 if WeaponProperty.REACH in self.properties else 5
                self.weapon_range = WeaponRange(normal=reach)
    
    def calculate_attack_bonus(self, ability_modifier: int, proficiency_bonus: int, is_proficient: bool = True) -> int:
        """Calculate attack roll bonus"""
        bonus = ability_modifier + self.magic_bonus
        if is_proficient:
            bonus += proficiency_bonus
        return bonus
    
    def calculate_damage_bonus(self, ability_modifier: int) -> int:
        """Calculate damage roll bonus"""
        return ability_modifier + self.magic_bonus
    
    def get_damage_dice(self, two_handed: bool = False) -> str:
        """Get damage dice, accounting for versatile weapons"""
        if two_handed and self.versatile_damage and WeaponProperty.VERSATILE in self.properties:
            return self.versatile_damage
        return self.damage_dice
    
    def is_finesse_weapon(self) -> bool:
        """Check if weapon has finesse property"""
        return WeaponProperty.FINESSE in self.properties
    
    def is_light_weapon(self) -> bool:
        """Check if weapon has light property"""
        return WeaponProperty.LIGHT in self.properties
    
    def is_heavy_weapon(self) -> bool:
        """Check if weapon has heavy property"""
        return WeaponProperty.HEAVY in self.properties
    
    def is_two_handed_weapon(self) -> bool:
        """Check if weapon has two-handed property"""
        return WeaponProperty.TWO_HANDED in self.properties
    
    def is_ranged_weapon(self) -> bool:
        """Check if weapon is ranged"""
        return self.category in [WeaponCategory.SIMPLE_RANGED, WeaponCategory.MARTIAL_RANGED]
    
    def requires_ammunition(self) -> bool:
        """Check if weapon requires ammunition"""
        return WeaponProperty.AMMUNITION in self.properties


# Predefined weapons from D&D 5e SRD
SIMPLE_MELEE_WEAPONS = {
    "Club": Weapon(
        name="Club",
        category=WeaponCategory.SIMPLE_MELEE,
        damage_dice="1d4",
        damage_type=DamageType.BLUDGEONING,
        properties=[WeaponProperty.LIGHT],
        weight=2.0,
        value=10  # 1 sp
    ),
    "Dagger": Weapon(
        name="Dagger",
        category=WeaponCategory.SIMPLE_MELEE,
        damage_dice="1d4",
        damage_type=DamageType.PIERCING,
        properties=[WeaponProperty.FINESSE, WeaponProperty.LIGHT, WeaponProperty.THROWN],
        weapon_range=WeaponRange(normal=20, long=60),
        weight=1.0,
        value=200  # 2 gp
    ),
    "Handaxe": Weapon(
        name="Handaxe",
        category=WeaponCategory.SIMPLE_MELEE,
        damage_dice="1d6",
        damage_type=DamageType.SLASHING,
        properties=[WeaponProperty.LIGHT, WeaponProperty.THROWN],
        weapon_range=WeaponRange(normal=20, long=60),
        weight=2.0,
        value=500  # 5 gp
    ),
    "Javelin": Weapon(
        name="Javelin",
        category=WeaponCategory.SIMPLE_MELEE,
        damage_dice="1d6",
        damage_type=DamageType.PIERCING,
        properties=[WeaponProperty.THROWN],
        weapon_range=WeaponRange(normal=30, long=120),
        weight=2.0,
        value=50  # 5 sp
    ),
    "Mace": Weapon(
        name="Mace",
        category=WeaponCategory.SIMPLE_MELEE,
        damage_dice="1d6",
        damage_type=DamageType.BLUDGEONING,
        weight=4.0,
        value=500  # 5 gp
    ),
    "Quarterstaff": Weapon(
        name="Quarterstaff",
        category=WeaponCategory.SIMPLE_MELEE,
        damage_dice="1d6",
        damage_type=DamageType.BLUDGEONING,
        properties=[WeaponProperty.VERSATILE],
        versatile_damage="1d8",
        weight=4.0,
        value=20  # 2 sp
    ),
    "Spear": Weapon(
        name="Spear",
        category=WeaponCategory.SIMPLE_MELEE,
        damage_dice="1d6",
        damage_type=DamageType.PIERCING,
        properties=[WeaponProperty.THROWN, WeaponProperty.VERSATILE],
        versatile_damage="1d8",
        weapon_range=WeaponRange(normal=20, long=60),
        weight=3.0,
        value=100  # 1 gp
    ),
}

SIMPLE_RANGED_WEAPONS = {
    "Crossbow, light": Weapon(
        name="Crossbow, light",
        category=WeaponCategory.SIMPLE_RANGED,
        damage_dice="1d8",
        damage_type=DamageType.PIERCING,
        properties=[WeaponProperty.AMMUNITION, WeaponProperty.LOADING, WeaponProperty.TWO_HANDED],
        weapon_range=WeaponRange(normal=80, long=320),
        weight=5.0,
        value=2500  # 25 gp
    ),
    "Dart": Weapon(
        name="Dart",
        category=WeaponCategory.SIMPLE_RANGED,
        damage_dice="1d4",
        damage_type=DamageType.PIERCING,
        properties=[WeaponProperty.FINESSE, WeaponProperty.THROWN],
        weapon_range=WeaponRange(normal=20, long=60),
        weight=0.25,
        value=5  # 5 cp
    ),
    "Shortbow": Weapon(
        name="Shortbow",
        category=WeaponCategory.SIMPLE_RANGED,
        damage_dice="1d6",
        damage_type=DamageType.PIERCING,
        properties=[WeaponProperty.AMMUNITION, WeaponProperty.TWO_HANDED],
        weapon_range=WeaponRange(normal=80, long=320),
        weight=2.0,
        value=2500  # 25 gp
    ),
    "Sling": Weapon(
        name="Sling",
        category=WeaponCategory.SIMPLE_RANGED,
        damage_dice="1d4",
        damage_type=DamageType.BLUDGEONING,
        properties=[WeaponProperty.AMMUNITION],
        weapon_range=WeaponRange(normal=30, long=120),
        weight=0.0,
        value=10  # 1 sp
    ),
}

MARTIAL_MELEE_WEAPONS = {
    "Battleaxe": Weapon(
        name="Battleaxe",
        category=WeaponCategory.MARTIAL_MELEE,
        damage_dice="1d8",
        damage_type=DamageType.SLASHING,
        properties=[WeaponProperty.VERSATILE],
        versatile_damage="1d10",
        weight=4.0,
        value=1000  # 10 gp
    ),
    "Longsword": Weapon(
        name="Longsword",
        category=WeaponCategory.MARTIAL_MELEE,
        damage_dice="1d8",
        damage_type=DamageType.SLASHING,
        properties=[WeaponProperty.VERSATILE],
        versatile_damage="1d10",
        weight=3.0,
        value=1500  # 15 gp
    ),
    "Rapier": Weapon(
        name="Rapier",
        category=WeaponCategory.MARTIAL_MELEE,
        damage_dice="1d8",
        damage_type=DamageType.PIERCING,
        properties=[WeaponProperty.FINESSE],
        weight=2.0,
        value=2500  # 25 gp
    ),
    "Shortsword": Weapon(
        name="Shortsword",
        category=WeaponCategory.MARTIAL_MELEE,
        damage_dice="1d6",
        damage_type=DamageType.PIERCING,
        properties=[WeaponProperty.FINESSE, WeaponProperty.LIGHT],
        weight=2.0,
        value=1000  # 10 gp
    ),
    "Greatsword": Weapon(
        name="Greatsword",
        category=WeaponCategory.MARTIAL_MELEE,
        damage_dice="2d6",
        damage_type=DamageType.SLASHING,
        properties=[WeaponProperty.HEAVY, WeaponProperty.TWO_HANDED],
        weight=6.0,
        value=5000  # 50 gp
    ),
}

MARTIAL_RANGED_WEAPONS = {
    "Longbow": Weapon(
        name="Longbow",
        category=WeaponCategory.MARTIAL_RANGED,
        damage_dice="1d8",
        damage_type=DamageType.PIERCING,
        properties=[WeaponProperty.AMMUNITION, WeaponProperty.HEAVY, WeaponProperty.TWO_HANDED],
        weapon_range=WeaponRange(normal=150, long=600),
        weight=2.0,
        value=5000  # 50 gp
    ),
    "Crossbow, heavy": Weapon(
        name="Crossbow, heavy",
        category=WeaponCategory.MARTIAL_RANGED,
        damage_dice="1d10",
        damage_type=DamageType.PIERCING,
        properties=[WeaponProperty.AMMUNITION, WeaponProperty.HEAVY, WeaponProperty.LOADING, WeaponProperty.TWO_HANDED],
        weapon_range=WeaponRange(normal=100, long=400),
        weight=18.0,
        value=5000  # 50 gp
    ),
}

# Combined weapon database
ALL_WEAPONS = {
    **SIMPLE_MELEE_WEAPONS,
    **SIMPLE_RANGED_WEAPONS,
    **MARTIAL_MELEE_WEAPONS,
    **MARTIAL_RANGED_WEAPONS,
}