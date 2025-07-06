"""
Tests for equipment models
"""
import pytest
from src.models.equipment.weapons import Weapon, WeaponCategory, DamageType, WeaponProperty, SIMPLE_MELEE_WEAPONS
from src.models.equipment.armor import Armor, ArmorCategory, LIGHT_ARMOR, HEAVY_ARMOR
from src.models.equipment.inventory import Inventory, InventoryItem, EquipmentSlot, Currency
from src.models.equipment.magic_items import MagicWeapon, MagicArmor, MAGIC_WEAPONS

class TestWeapon:
    """Test weapon functionality"""
    
    def test_weapon_creation(self):
        """Test basic weapon creation"""
        sword = Weapon(
            name="Test Sword",
            category=WeaponCategory.MARTIAL_MELEE,
            damage_dice="1d8",
            damage_type=DamageType.SLASHING
        )
        
        assert sword.name == "Test Sword"
        assert sword.category == WeaponCategory.MARTIAL_MELEE
        assert sword.damage_dice == "1d8"
        assert sword.damage_type == DamageType.SLASHING
    
    def test_attack_bonus_calculation(self):
        """Test attack bonus calculation"""
        sword = SIMPLE_MELEE_WEAPONS["Mace"]
        
        # Proficient character: STR 16 (+3), Prof +2
        attack_bonus = sword.calculate_attack_bonus(3, 2, True)
        assert attack_bonus == 5  # 3 + 2 + 0 (no magic bonus)
        
        # Non-proficient character
        attack_bonus = sword.calculate_attack_bonus(3, 2, False)
        assert attack_bonus == 3  # 3 + 0 + 0
    
    def test_damage_bonus_calculation(self):
        """Test damage bonus calculation"""
        sword = SIMPLE_MELEE_WEAPONS["Mace"]
        
        damage_bonus = sword.calculate_damage_bonus(3)  # STR 16 (+3)
        assert damage_bonus == 3
    
    def test_versatile_weapon(self):
        """Test versatile weapon damage"""
        quarterstaff = SIMPLE_MELEE_WEAPONS["Quarterstaff"]
        
        # One-handed
        assert quarterstaff.get_damage_dice(False) == "1d6"
        
        # Two-handed
        assert quarterstaff.get_damage_dice(True) == "1d8"
    
    def test_weapon_properties(self):
        """Test weapon property checks"""
        dagger = SIMPLE_MELEE_WEAPONS["Dagger"]
        
        assert dagger.is_finesse_weapon() == True
        assert dagger.is_light_weapon() == True
        assert dagger.is_heavy_weapon() == False
        assert dagger.is_ranged_weapon() == False

class TestArmor:
    """Test armor functionality"""
    
    def test_armor_creation(self):
        """Test basic armor creation"""
        armor = Armor(
            name="Test Armor",
            category=ArmorCategory.MEDIUM,
            base_ac=14,
            max_dex_bonus=2
        )
        
        assert armor.name == "Test Armor"
        assert armor.category == ArmorCategory.MEDIUM
        assert armor.base_ac == 14
        assert armor.max_dex_bonus == 2
    
    def test_ac_calculation(self):
        """Test AC calculation with different armor types"""
        # Light armor (unlimited dex bonus)
        leather = LIGHT_ARMOR["Leather"]
        assert leather.calculate_ac(3) == 14  # 11 + 3 dex
        assert leather.calculate_ac(5) == 16  # 11 + 5 dex
        
        # Medium armor (max +2 dex)
        scale_mail = Armor(
            name="Scale Mail",
            category=ArmorCategory.MEDIUM,
            base_ac=14,
            max_dex_bonus=2
        )
        assert scale_mail.calculate_ac(1) == 15  # 14 + 1 dex
        assert scale_mail.calculate_ac(3) == 16  # 14 + 2 dex (capped)
        
        # Heavy armor (no dex bonus)
        plate = HEAVY_ARMOR["Plate"]
        assert plate.calculate_ac(0) == 18  # 18 + 0 dex
        assert plate.calculate_ac(3) == 18  # 18 + 0 dex (capped)
    
    def test_strength_requirement(self):
        """Test armor strength requirements"""
        chain_mail = HEAVY_ARMOR["Chain mail"]
        
        assert chain_mail.meets_strength_requirement(13) == True
        assert chain_mail.meets_strength_requirement(12) == False
        assert chain_mail.meets_strength_requirement(15) == True

class TestInventory:
    """Test inventory management"""
    
    def test_inventory_creation(self):
        """Test basic inventory creation"""
        inventory = Inventory()
        assert len(inventory.items) == 0
        assert len(inventory.equipped_items) == 0
    
    def test_add_item(self):
        """Test adding items to inventory"""
        inventory = Inventory()
        sword = SIMPLE_MELEE_WEAPONS["Mace"]
        
        item = inventory.add_item(sword, 1)
        assert len(inventory.items) == 1
        assert item.equipment == sword
        assert item.quantity == 1
    
    def test_stackable_items(self):
        """Test that identical items stack"""
        inventory = Inventory()
        dagger = SIMPLE_MELEE_WEAPONS["Dagger"]
        
        # Add first dagger
        item1 = inventory.add_item(dagger, 1)
        assert len(inventory.items) == 1
        assert item1.quantity == 1
        
        # Add second dagger - should stack
        item2 = inventory.add_item(dagger, 2)
        assert len(inventory.items) == 1  # Still only one item entry
        assert item1 == item2  # Same item object
        assert item1.quantity == 3  # Stacked quantity
    
    def test_equip_weapon(self):
        """Test equipping weapons"""
        inventory = Inventory()
        sword = SIMPLE_MELEE_WEAPONS["Mace"]
        
        item = inventory.add_item(sword)
        success = inventory.equip_item(item)
        
        assert success == True
        assert item.equipped == True
        assert item.equipped_slot == EquipmentSlot.MAIN_HAND
        assert EquipmentSlot.MAIN_HAND in inventory.equipped_items
    
    def test_equip_armor(self):
        """Test equipping armor"""
        inventory = Inventory()
        armor = LIGHT_ARMOR["Leather"]
        
        item = inventory.add_item(armor)
        success = inventory.equip_item(item)
        
        assert success == True
        assert item.equipped == True
        assert item.equipped_slot == EquipmentSlot.ARMOR
    
    def test_ac_calculation_with_equipment(self):
        """Test AC calculation with equipped armor"""
        inventory = Inventory()
        leather = LIGHT_ARMOR["Leather"]
        
        # No armor equipped
        ac = inventory.calculate_ac(3)  # DEX +3
        assert ac == 13  # 10 + 3 dex
        
        # Equip leather armor
        item = inventory.add_item(leather)
        inventory.equip_item(item)
        
        ac = inventory.calculate_ac(3)  # DEX +3
        assert ac == 14  # 11 + 3 dex
    
    def test_carrying_capacity(self):
        """Test carrying capacity and encumbrance"""
        inventory = Inventory()
        
        # Base carrying capacity (STR 15 = 225 lbs)
        capacity = inventory.calculate_carrying_capacity(15)
        assert capacity == 225
        
        # Add heavy items
        heavy_item = Armor(name="Heavy Armor", weight=100.0)
        inventory.add_item(heavy_item, 3)  # 300 lbs total
        
        # Should be encumbered
        assert inventory.is_encumbered(15) == True
        assert inventory.get_encumbrance_level(15) == "Heavily Encumbered"

class TestCurrency:
    """Test currency management"""
    
    def test_currency_creation(self):
        """Test basic currency creation"""
        currency = Currency()
        assert currency.copper == 0
        assert currency.silver == 0
        assert currency.gold == 0
        assert currency.platinum == 0
    
    def test_total_value_calculation(self):
        """Test total value calculations"""
        currency = Currency(copper=50, silver=10, gold=5, platinum=2)
        
        # Total in copper: 50 + (10*10) + (5*100) + (2*1000) = 2650
        assert currency.total_copper_value == 2650
        assert currency.total_gold_value == 26.5
    
    def test_add_value_conversion(self):
        """Test adding value with automatic conversion"""
        currency = Currency()
        
        # Add 2550 copper pieces
        currency.add_value_in_copper(2550)
        
        # Should convert to higher denominations
        assert currency.platinum == 2  # 2000 cp
        assert currency.gold == 5      # 500 cp
        assert currency.silver == 5    # 50 cp
        assert currency.copper == 0    # 0 cp remaining
    
    def test_spend_money(self):
        """Test spending money"""
        currency = Currency(gold=10)  # 1000 cp total
        
        # Can afford 500 cp purchase
        assert currency.can_afford(500) == True
        success = currency.spend(500)
        assert success == True
        assert currency.total_copper_value == 500
        
        # Cannot afford 600 cp purchase
        assert currency.can_afford(600) == False
        success = currency.spend(600)
        assert success == False
        assert currency.total_copper_value == 500  # Unchanged

class TestMagicItems:
    """Test magic item functionality"""
    
    def test_magic_weapon_bonuses(self):
        """Test magic weapon attack and damage bonuses"""
        magic_sword = MAGIC_WEAPONS["Longsword +1"]
        
        # Attack bonus includes magic bonus
        attack_bonus = magic_sword.calculate_attack_bonus(3, 2, True)
        assert attack_bonus == 6  # 3 + 2 + 1 (magic)
        
        # Damage bonus includes magic bonus
        damage_bonus = magic_sword.calculate_damage_bonus(3)
        assert damage_bonus == 4  # 3 + 1 (magic)
    
    def test_magic_armor_ac(self):
        """Test magic armor AC bonus"""
        magic_leather = MagicArmor(
            name="Leather +1",
            category=ArmorCategory.LIGHT,
            base_ac=11,
            magic_bonus=1
        )
        
        ac = magic_leather.calculate_ac(3)  # DEX +3
        assert ac == 15  # 11 + 3 + 1 (magic)
    
    def test_charges_system(self):
        """Test magic item charges"""
        from src.models.equipment.magic_items import WondrousItem
        
        boots = WondrousItem(
            name="Boots of Speed",
            charges=3,
            max_charges=3
        )
        
        # Use charges
        assert boots.use_charge(1) == True
        assert boots.charges == 2
        
        assert boots.use_charge(2) == True
        assert boots.charges == 0
        
        # Cannot use more charges
        assert boots.use_charge(1) == False
        assert boots.charges == 0
        
        # Recharge
        boots.recharge(2)
        assert boots.charges == 2