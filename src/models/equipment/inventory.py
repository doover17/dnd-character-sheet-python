"""
Inventory management system for D&D 5e equipment
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum
from .base import Equipment, EquipmentType
from .weapons import Weapon
from .armor import Armor, Shield

class EquipmentSlot(Enum):
    """Equipment slots for worn/wielded items"""
    MAIN_HAND = "main_hand"
    OFF_HAND = "off_hand"
    ARMOR = "armor"
    SHIELD = "shield"
    HELMET = "helmet"
    GLOVES = "gloves"
    BOOTS = "boots"
    CLOAK = "cloak"
    AMULET = "amulet"
    RING_1 = "ring_1"
    RING_2 = "ring_2"
    BELT = "belt"

@dataclass
class InventoryItem:
    """Item in character inventory"""
    equipment: Equipment
    quantity: int = 1
    equipped: bool = False
    equipped_slot: Optional[EquipmentSlot] = None
    attuned: bool = False
    custom_name: Optional[str] = None  # For renamed items
    notes: str = ""
    
    @property
    def display_name(self) -> str:
        """Get display name (custom name if set, otherwise equipment name)"""
        return self.custom_name or self.equipment.name
    
    @property
    def total_weight(self) -> float:
        """Calculate total weight of this inventory item"""
        return self.equipment.weight * self.quantity
    
    @property
    def total_value(self) -> int:
        """Calculate total value in copper pieces"""
        return self.equipment.value * self.quantity
    
    def can_equip(self) -> bool:
        """Check if item can be equipped"""
        return self.equipment.type in [
            EquipmentType.WEAPON,
            EquipmentType.ARMOR,
            EquipmentType.SHIELD,
            EquipmentType.WONDROUS_ITEM
        ]
    
    def requires_attunement(self) -> bool:
        """Check if item requires attunement"""
        return self.equipment.requires_attunement

@dataclass
class Currency:
    """Character currency"""
    copper: int = 0
    silver: int = 0
    electrum: int = 0
    gold: int = 0
    platinum: int = 0
    
    @property
    def total_copper_value(self) -> int:
        """Total value in copper pieces"""
        return (
            self.copper +
            self.silver * 10 +
            self.electrum * 50 +
            self.gold * 100 +
            self.platinum * 1000
        )
    
    @property
    def total_gold_value(self) -> float:
        """Total value in gold pieces"""
        return self.total_copper_value / 100
    
    def add_copper(self, amount: int) -> None:
        """Add copper pieces"""
        self.copper += amount
    
    def add_value_in_copper(self, copper_value: int) -> None:
        """Add value and convert to appropriate denominations"""
        # Convert to highest denomination possible
        if copper_value >= 1000:
            platinum_to_add = copper_value // 1000
            self.platinum += platinum_to_add
            copper_value -= platinum_to_add * 1000
        
        if copper_value >= 100:
            gold_to_add = copper_value // 100
            self.gold += gold_to_add
            copper_value -= gold_to_add * 100
        
        if copper_value >= 50:
            electrum_to_add = copper_value // 50
            self.electrum += electrum_to_add
            copper_value -= electrum_to_add * 50
        
        if copper_value >= 10:
            silver_to_add = copper_value // 10
            self.silver += silver_to_add
            copper_value -= silver_to_add * 10
        
        self.copper += copper_value
    
    def can_afford(self, cost_in_copper: int) -> bool:
        """Check if character can afford a purchase"""
        return self.total_copper_value >= cost_in_copper
    
    def spend(self, cost_in_copper: int) -> bool:
        """Spend money if affordable"""
        if not self.can_afford(cost_in_copper):
            return False
        
        # Simple implementation: convert all to copper, subtract, then convert back
        total_copper = self.total_copper_value - cost_in_copper
        
        # Reset all currencies
        self.copper = self.silver = self.electrum = self.gold = self.platinum = 0
        
        # Convert back to denominations
        self.add_value_in_copper(total_copper)
        return True

@dataclass
class Inventory:
    """Character inventory management"""
    items: List[InventoryItem] = field(default_factory=list)
    equipped_items: Dict[EquipmentSlot, InventoryItem] = field(default_factory=dict)
    currency: Currency = field(default_factory=Currency)
    carrying_capacity_override: Optional[int] = None
    
    def add_item(self, equipment: Equipment, quantity: int = 1) -> InventoryItem:
        """Add item to inventory"""
        # Check if item already exists (stackable)
        for item in self.items:
            if (item.equipment.name == equipment.name and 
                item.equipment.type == equipment.type and
                not item.equipped):
                item.quantity += quantity
                return item
        
        # Create new inventory item
        new_item = InventoryItem(equipment=equipment, quantity=quantity)
        self.items.append(new_item)
        return new_item
    
    def remove_item(self, item: InventoryItem, quantity: int = None) -> bool:
        """Remove item from inventory"""
        if item not in self.items:
            return False
        
        if quantity is None or quantity >= item.quantity:
            # Remove entire stack
            if item.equipped:
                self.unequip_item(item)
            self.items.remove(item)
        else:
            # Remove partial quantity
            item.quantity -= quantity
        
        return True
    
    def equip_item(self, item: InventoryItem, slot: EquipmentSlot = None) -> bool:
        """Equip an item to a slot"""
        if item not in self.items or not item.can_equip():
            return False
        
        # Determine slot if not specified
        if slot is None:
            slot = self._determine_equipment_slot(item.equipment)
            if slot is None:
                return False
        
        # Check if slot is available
        if slot in self.equipped_items:
            # Unequip current item in slot
            current_item = self.equipped_items[slot]
            self.unequip_item(current_item)
        
        # Equip the item
        item.equipped = True
        item.equipped_slot = slot
        self.equipped_items[slot] = item
        
        return True
    
    def unequip_item(self, item: InventoryItem) -> bool:
        """Unequip an item"""
        if not item.equipped or item.equipped_slot is None:
            return False
        
        # Remove from equipped items
        if item.equipped_slot in self.equipped_items:
            del self.equipped_items[item.equipped_slot]
        
        item.equipped = False
        item.equipped_slot = None
        item.attuned = False  # Lose attunement when unequipped
        
        return True
    
    def _determine_equipment_slot(self, equipment: Equipment) -> Optional[EquipmentSlot]:
        """Determine appropriate slot for equipment"""
        if equipment.type == EquipmentType.WEAPON:
            # Prefer main hand, fallback to off hand
            if EquipmentSlot.MAIN_HAND not in self.equipped_items:
                return EquipmentSlot.MAIN_HAND
            elif EquipmentSlot.OFF_HAND not in self.equipped_items:
                return EquipmentSlot.OFF_HAND
        elif equipment.type == EquipmentType.ARMOR:
            return EquipmentSlot.ARMOR
        elif equipment.type == EquipmentType.SHIELD:
            return EquipmentSlot.SHIELD
        
        return None
    
    def get_equipped_weapon(self, slot: EquipmentSlot = EquipmentSlot.MAIN_HAND) -> Optional[Weapon]:
        """Get equipped weapon in specified slot"""
        if slot in self.equipped_items:
            item = self.equipped_items[slot]
            if isinstance(item.equipment, Weapon):
                return item.equipment
        return None
    
    def get_equipped_armor(self) -> Optional[Armor]:
        """Get equipped armor"""
        if EquipmentSlot.ARMOR in self.equipped_items:
            item = self.equipped_items[EquipmentSlot.ARMOR]
            if isinstance(item.equipment, Armor):
                return item.equipment
        return None
    
    def get_equipped_shield(self) -> Optional[Shield]:
        """Get equipped shield"""
        if EquipmentSlot.SHIELD in self.equipped_items:
            item = self.equipped_items[EquipmentSlot.SHIELD]
            if isinstance(item.equipment, Shield):
                return item.equipment
        return None
    
    def calculate_total_weight(self) -> float:
        """Calculate total weight of all items"""
        return sum(item.total_weight for item in self.items)
    
    def calculate_carrying_capacity(self, strength_score: int) -> int:
        """Calculate carrying capacity based on strength"""
        if self.carrying_capacity_override is not None:
            return self.carrying_capacity_override
        return strength_score * 15  # Standard D&D rule
    
    def is_encumbered(self, strength_score: int) -> bool:
        """Check if character is encumbered"""
        total_weight = self.calculate_total_weight()
        capacity = self.calculate_carrying_capacity(strength_score)
        return total_weight > capacity
    
    def get_encumbrance_level(self, strength_score: int) -> str:
        """Get encumbrance level description"""
        total_weight = self.calculate_total_weight()
        capacity = self.calculate_carrying_capacity(strength_score)
        
        if total_weight <= capacity * 5 / 6:
            return "Unencumbered"
        elif total_weight <= capacity:
            return "Encumbered"
        else:
            return "Heavily Encumbered"
    
    def calculate_ac(self, dex_modifier: int, base_ac: int = 10) -> int:
        """Calculate AC from equipped armor and shield"""
        armor = self.get_equipped_armor()
        shield = self.get_equipped_shield()
        
        if armor:
            ac = armor.calculate_ac(dex_modifier)
        else:
            # No armor - use base AC + dex modifier
            ac = base_ac + dex_modifier
        
        if shield:
            ac += shield.calculate_ac_bonus()
        
        return ac
    
    def get_items_by_type(self, equipment_type: EquipmentType) -> List[InventoryItem]:
        """Get all items of a specific type"""
        return [item for item in self.items if item.equipment.type == equipment_type]
    
    def get_attuned_items(self) -> List[InventoryItem]:
        """Get all attuned items"""
        return [item for item in self.items if item.attuned]
    
    def can_attune_item(self, item: InventoryItem) -> bool:
        """Check if character can attune to item (max 3 attuned items)"""
        if not item.requires_attunement():
            return False
        
        attuned_count = len(self.get_attuned_items())
        return attuned_count < 3
    
    def attune_item(self, item: InventoryItem) -> bool:
        """Attune to an item"""
        if not self.can_attune_item(item) or item.attuned:
            return False
        
        item.attuned = True
        return True
    
    def unattune_item(self, item: InventoryItem) -> bool:
        """Remove attunement from item"""
        if not item.attuned:
            return False
        
        item.attuned = False
        return True