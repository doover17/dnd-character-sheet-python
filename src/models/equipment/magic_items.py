"""
Magic items for D&D 5e equipment system
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from .base import Equipment, EquipmentType, Rarity
from .weapons import Weapon, WeaponCategory, DamageType, WeaponProperty
from .armor import Armor, ArmorCategory

class MagicSchool(Enum):
    ABJURATION = "abjuration"
    CONJURATION = "conjuration"
    DIVINATION = "divination"
    ENCHANTMENT = "enchantment"
    EVOCATION = "evocation"
    ILLUSION = "illusion"
    NECROMANCY = "necromancy"
    TRANSMUTATION = "transmutation"

@dataclass
class MagicProperty:
    """Magic property that can be applied to items"""
    name: str
    description: str
    activation: str = "passive"  # passive, action, bonus_action, reaction
    charges: Optional[int] = None
    recharge: Optional[str] = None  # "dawn", "1d6+4", etc.

@dataclass
class MagicItem(Equipment):
    """Base magic item implementation"""
    magic_bonus: int = 0
    magic_properties: List[MagicProperty] = field(default_factory=list)
    spell_effects: List[str] = field(default_factory=list)
    charges: Optional[int] = None
    max_charges: Optional[int] = None
    recharge_dice: Optional[str] = None
    curse: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.max_charges and self.charges is None:
            self.charges = self.max_charges
    
    def use_charge(self, count: int = 1) -> bool:
        """Use charges from the item"""
        if self.charges is None:
            return True  # Unlimited use
        
        if self.charges >= count:
            self.charges -= count
            return True
        return False
    
    def recharge(self, amount: int = None) -> None:
        """Recharge the item"""
        if self.charges is None or self.max_charges is None:
            return
        
        if amount is None:
            self.charges = self.max_charges
        else:
            self.charges = min(self.max_charges, self.charges + amount)
    
    def is_cursed(self) -> bool:
        """Check if item is cursed"""
        return self.curse is not None

@dataclass
class MagicWeapon(Weapon, MagicItem):
    """Magic weapon implementation"""
    
    def __post_init__(self):
        Weapon.__post_init__(self)
        MagicItem.__post_init__(self)
        if self.magic_bonus > 0:
            self.rarity = self._determine_rarity_by_bonus()
    
    def _determine_rarity_by_bonus(self) -> Rarity:
        """Determine rarity based on magic bonus"""
        if self.magic_bonus == 1:
            return Rarity.UNCOMMON
        elif self.magic_bonus == 2:
            return Rarity.RARE
        elif self.magic_bonus == 3:
            return Rarity.VERY_RARE
        else:
            return Rarity.LEGENDARY
    
    def calculate_attack_bonus(self, ability_modifier: int, proficiency_bonus: int, is_proficient: bool = True) -> int:
        """Calculate attack roll bonus including magic bonus"""
        base_bonus = super().calculate_attack_bonus(ability_modifier, proficiency_bonus, is_proficient)
        return base_bonus + self.magic_bonus
    
    def calculate_damage_bonus(self, ability_modifier: int) -> int:
        """Calculate damage roll bonus including magic bonus"""
        base_bonus = super().calculate_damage_bonus(ability_modifier)
        return base_bonus + self.magic_bonus

@dataclass
class MagicArmor(Armor, MagicItem):
    """Magic armor implementation"""
    
    def __post_init__(self):
        Armor.__post_init__(self)
        MagicItem.__post_init__(self)
        if self.magic_bonus > 0:
            self.rarity = self._determine_rarity_by_bonus()
    
    def _determine_rarity_by_bonus(self) -> Rarity:
        """Determine rarity based on magic bonus"""
        if self.magic_bonus == 1:
            return Rarity.UNCOMMON
        elif self.magic_bonus == 2:
            return Rarity.RARE
        elif self.magic_bonus == 3:
            return Rarity.VERY_RARE
        else:
            return Rarity.LEGENDARY
    
    def calculate_ac(self, dex_modifier: int) -> int:
        """Calculate AC including magic bonus"""
        base_ac = super().calculate_ac(dex_modifier)
        return base_ac + self.magic_bonus

@dataclass
class WondrousItem(MagicItem):
    """Wondrous magic item implementation"""
    
    def __post_init__(self):
        super().__post_init__()
        self.type = EquipmentType.WONDROUS_ITEM


# Predefined magic items
MAGIC_WEAPONS = {
    "Longsword +1": MagicWeapon(
        name="Longsword +1",
        category=WeaponCategory.MARTIAL_MELEE,
        damage_dice="1d8",
        damage_type=DamageType.SLASHING,
        properties=[WeaponProperty.VERSATILE],
        versatile_damage="1d10",
        magic_bonus=1,
        rarity=Rarity.UNCOMMON,
        weight=3.0,
        value=100000,  # 1000 gp
        description="A magical longsword with a +1 bonus to attack and damage rolls."
    ),
    "Flame Tongue": MagicWeapon(
        name="Flame Tongue",
        category=WeaponCategory.MARTIAL_MELEE,
        damage_dice="1d8",
        damage_type=DamageType.SLASHING,
        properties=[WeaponProperty.VERSATILE],
        versatile_damage="1d10",
        rarity=Rarity.RARE,
        weight=3.0,
        value=500000,  # 5000 gp
        requires_attunement=True,
        spell_effects=["2d6 fire damage on command"],
        description="A magical sword that can burst into flames, dealing extra fire damage."
    ),
    "Dagger +2": MagicWeapon(
        name="Dagger +2",
        category=WeaponCategory.SIMPLE_MELEE,
        damage_dice="1d4",
        damage_type=DamageType.PIERCING,
        properties=[WeaponProperty.FINESSE, WeaponProperty.LIGHT, WeaponProperty.THROWN],
        magic_bonus=2,
        rarity=Rarity.RARE,
        weight=1.0,
        value=200000,  # 2000 gp
        description="A finely crafted dagger with a +2 bonus to attack and damage rolls."
    ),
}

MAGIC_ARMOR = {
    "Leather Armor +1": MagicArmor(
        name="Leather Armor +1",
        category=ArmorCategory.LIGHT,
        base_ac=11,
        magic_bonus=1,
        rarity=Rarity.UNCOMMON,
        weight=10.0,
        value=500000,  # 5000 gp
        description="Well-crafted leather armor with a +1 bonus to AC."
    ),
    "Chain Mail +2": MagicArmor(
        name="Chain Mail +2",
        category=ArmorCategory.HEAVY,
        base_ac=16,
        max_dex_bonus=0,
        min_strength=13,
        stealth_disadvantage=True,
        magic_bonus=2,
        rarity=Rarity.RARE,
        weight=55.0,
        value=1000000,  # 10000 gp
        description="Masterwork chain mail with a +2 bonus to AC."
    ),
    "Elven Chain": MagicArmor(
        name="Elven Chain",
        category=ArmorCategory.MEDIUM,
        base_ac=13,
        max_dex_bonus=2,
        stealth_disadvantage=False,  # Special property
        magic_bonus=1,
        rarity=Rarity.RARE,
        weight=20.0,
        value=400000,  # 4000 gp
        description="Magical chain shirt that doesn't impose disadvantage on stealth checks."
    ),
}

WONDROUS_ITEMS = {
    "Bag of Holding": WondrousItem(
        name="Bag of Holding",
        rarity=Rarity.UNCOMMON,
        weight=15.0,
        value=400000,  # 4000 gp
        description="A magical bag that can hold up to 500 pounds and 64 cubic feet of material."
    ),
    "Cloak of Elvenkind": WondrousItem(
        name="Cloak of Elvenkind",
        rarity=Rarity.UNCOMMON,
        weight=1.0,
        value=500000,  # 5000 gp
        requires_attunement=True,
        description="Grants advantage on Dexterity (Stealth) checks and Wisdom (Perception) checks."
    ),
    "Ring of Protection": WondrousItem(
        name="Ring of Protection",
        rarity=Rarity.RARE,
        weight=0.0,
        value=350000,  # 3500 gp
        requires_attunement=True,
        description="Grants a +1 bonus to AC and saving throws."
    ),
    "Boots of Speed": WondrousItem(
        name="Boots of Speed",
        rarity=Rarity.RARE,
        weight=1.0,
        value=400000,  # 4000 gp
        requires_attunement=True,
        charges=3,
        max_charges=3,
        recharge_dice="1d4",
        description="Can be activated to double your speed for 10 minutes."
    ),
}

# Combined magic items database
ALL_MAGIC_ITEMS = {
    **MAGIC_WEAPONS,
    **MAGIC_ARMOR,
    **WONDROUS_ITEMS,
}