"""
Equipment model definitions
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum

class EquipmentType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    SHIELD = "shield"
    TOOL = "tool"
    ADVENTURING_GEAR = "adventuring_gear"
    CONSUMABLE = "consumable"
    TREASURE = "treasure"
    WONDROUS_ITEM = "wondrous_item"

class WeaponType(Enum):
    SIMPLE_MELEE = "simple_melee"
    SIMPLE_RANGED = "simple_ranged"
    MARTIAL_MELEE = "martial_melee"
    MARTIAL_RANGED = "martial_ranged"

class ArmorType(Enum):
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"

class Rarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    VERY_RARE = "very_rare"
    LEGENDARY = "legendary"
    ARTIFACT = "artifact"

@dataclass
class Equipment:
    """Base equipment item"""
    name: str
    type: EquipmentType
    description: str
    weight: float = 0.0
    value: int = 0  # in copper pieces
    rarity: Rarity = Rarity.COMMON
    requires_attunement: bool = False
    properties: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def value_in_gp(self) -> float:
        """Convert value to gold pieces"""
        return self.value / 100

@dataclass
class Weapon(Equipment):
    """Weapon equipment"""
    weapon_type: WeaponType = WeaponType.SIMPLE_MELEE
    damage_dice: str = "1d4"
    damage_type: str = "slashing"
    range_normal: Optional[int] = None
    range_long: Optional[int] = None
    
    def __post_init__(self):
        self.type = EquipmentType.WEAPON

@dataclass
class Armor(Equipment):
    """Armor equipment"""
    armor_type: ArmorType = ArmorType.LIGHT
    base_ac: int = 10
    max_dex_bonus: Optional[int] = None
    min_strength: Optional[int] = None
    stealth_disadvantage: bool = False
    
    def __post_init__(self):
        self.type = EquipmentType.ARMOR

@dataclass
class InventoryItem:
    """Item in character inventory"""
    equipment: Equipment
    quantity: int = 1
    equipped: bool = False
    attuned: bool = False
    
    @property
    def total_weight(self) -> float:
        """Calculate total weight of this inventory item"""
        return self.equipment.weight * self.quantity