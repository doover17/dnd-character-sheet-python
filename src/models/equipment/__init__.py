# Equipment models package

from .base import Equipment, EquipmentType, Rarity, InventoryItem
from .weapons import Weapon, WeaponCategory, DamageType, WeaponProperty, ALL_WEAPONS
from .armor import Armor, ArmorCategory, Shield, ALL_ARMOR
from .inventory import Inventory, InventoryItem, EquipmentSlot, Currency
from .magic_items import MagicItem, MagicWeapon, MagicArmor, WondrousItem, ALL_MAGIC_ITEMS

__all__ = [
    # Base classes
    'Equipment', 'EquipmentType', 'Rarity', 'InventoryItem',
    
    # Weapons
    'Weapon', 'WeaponCategory', 'DamageType', 'WeaponProperty', 'ALL_WEAPONS',
    
    # Armor
    'Armor', 'ArmorCategory', 'Shield', 'ALL_ARMOR',
    
    # Inventory
    'Inventory', 'InventoryItem', 'EquipmentSlot', 'Currency',
    
    # Magic Items
    'MagicItem', 'MagicWeapon', 'MagicArmor', 'WondrousItem', 'ALL_MAGIC_ITEMS',
]