# Backend/Models Development Tasks

## Team Lead: Backend/Data Architect
**Focus**: Data models, business logic, calculations, and D&D rules implementation

---

## 🔥 HIGH PRIORITY TASKS

### TASK-BE-001: Combat Stats Model Enhancement
**Estimated Time**: 2-3 days  
**Assignee**: [Senior Backend Developer]

**Description**: Enhance the character vitals model to support complete combat statistics and calculations.

**Requirements**:
- Extend CharacterVitals model with initiative and death saves
- Add combat-related calculations (initiative modifier, damage resistance)
- Implement temporary HP logic
- Add armor class calculation from equipment
- Support for conditions and status effects

**Acceptance Criteria**:
- [ ] CharacterVitals model includes all combat stats
- [ ] Initiative modifier calculation (Dex + bonuses)
- [ ] Death saves tracking (successes/failures)
- [ ] Temporary HP stacking rules implemented
- [ ] AC calculation from multiple sources
- [ ] Condition/status effect tracking

**Technical Details**:
```python
# Extend CharacterVitals in src/models/character/base.py
@dataclass
class CharacterVitals:
    # Existing fields...
    initiative_modifier: int = 0
    death_saves_successes: int = 0
    death_saves_failures: int = 0
    conditions: List[str] = field(default_factory=list)
    
    def calculate_initiative(self, dex_modifier: int) -> int:
        return dex_modifier + self.initiative_modifier
```

**Files to Modify**:
- `src/models/character/base.py`
- Add unit tests in `tests/models/test_character_vitals.py`

---

### TASK-BE-002: Skills System Implementation
**Estimated Time**: 2-3 days  
**Assignee**: [Mid-Level Backend Developer]

**Description**: Implement complete D&D 5e skills system with proficiency and expertise tracking.

**Requirements**:
- Create Skills model with all 18 D&D skills
- Implement skill proficiency tracking
- Add expertise (double proficiency) support
- Calculate skill modifiers correctly
- Support for situational bonuses

**Acceptance Criteria**:
- [ ] All 18 skills defined with correct ability associations
- [ ] Proficiency bonus calculation
- [ ] Expertise handling (double proficiency)
- [ ] Skill modifier calculation (ability + proficiency)
- [ ] Jack of All Trades support (half proficiency)
- [ ] Situational modifier support

**Technical Details**:
```python
# Create new file: src/models/character/skills.py
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List

class SkillType(Enum):
    ACROBATICS = ("acrobatics", "dexterity")
    ANIMAL_HANDLING = ("animal_handling", "wisdom")
    # ... all 18 skills

@dataclass
class Skills:
    proficiencies: List[SkillType] = field(default_factory=list)
    expertise: List[SkillType] = field(default_factory=list)
    jack_of_all_trades: bool = False
    
    def get_skill_modifier(self, skill: SkillType, ability_scores: AbilityScores, proficiency_bonus: int) -> int:
        # Implementation here
```

**Files to Create**:
- `src/models/character/skills.py`
- `tests/models/test_skills.py`

---

### TASK-BE-003: Saving Throws Model
**Estimated Time**: 1-2 days  
**Assignee**: [Junior Backend Developer]

**Description**: Implement saving throws system with proficiency tracking.

**Requirements**:
- Create SavingThrows model for all 6 ability-based saves
- Track proficiency in saving throws
- Calculate saving throw bonuses
- Support for situational modifiers
- Integration with character class proficiencies

**Acceptance Criteria**:
- [ ] SavingThrows model created
- [ ] Proficiency tracking per ability
- [ ] Modifier calculation (ability + proficiency)
- [ ] Class-based proficiency assignment
- [ ] Situational modifier support

**Technical Details**:
```python
# Create new file: src/models/character/saving_throws.py
@dataclass
class SavingThrows:
    proficiencies: List[AbilityType] = field(default_factory=list)
    
    def get_saving_throw_modifier(self, ability: AbilityType, ability_scores: AbilityScores, proficiency_bonus: int) -> int:
        modifier = ability_scores.get_modifier(ability)
        if ability in self.proficiencies:
            modifier += proficiency_bonus
        return modifier
```

**Files to Create**:
- `src/models/character/saving_throws.py`
- `tests/models/test_saving_throws.py`

---

## 🟡 MEDIUM PRIORITY TASKS

### TASK-BE-004: Equipment System Enhancement
**Estimated Time**: 4-5 days  
**Assignee**: [Senior Backend Developer]

**Description**: Enhance equipment models with complete D&D item system.

**Requirements**:
- Extend Equipment model with magic items
- Implement armor class calculations
- Add weapon attack/damage calculations
- Create equipment effects system
- Support for equipment prerequisites

**Acceptance Criteria**:
- [ ] Magic item properties and effects
- [ ] AC calculation from equipped armor
- [ ] Weapon attack bonus calculation
- [ ] Damage dice and bonus calculation
- [ ] Equipment attunement system
- [ ] Carrying capacity calculations

**Technical Details**:
```python
# Enhance src/models/equipment/base.py
@dataclass
class MagicItem(Equipment):
    magic_bonus: int = 0
    spell_effects: List[str] = field(default_factory=list)
    charges: Optional[int] = None
    recharge_dice: Optional[str] = None
    
    def calculate_ac_bonus(self) -> int:
        # Implementation
        
    def calculate_attack_bonus(self) -> int:
        # Implementation
```

**Files to Modify**:
- `src/models/equipment/base.py`
- Add `src/models/equipment/magic_items.py`
- `tests/models/test_equipment.py`

---

### TASK-BE-005: Spell System Implementation
**Estimated Time**: 5-6 days  
**Assignee**: [Senior Backend Developer]

**Description**: Implement comprehensive spell system with slots, preparation, and casting.

**Requirements**:
- Create spell slot management system
- Implement spell preparation mechanics
- Add spellcasting ability calculations
- Support for ritual casting
- Spell level scaling effects

**Acceptance Criteria**:
- [ ] Spell slot tracking by level (1-9)
- [ ] Spell preparation system
- [ ] Spell save DC calculation
- [ ] Spell attack bonus calculation
- [ ] Ritual casting support
- [ ] Spell level up-casting

**Technical Details**:
```python
# Create new file: src/models/character/spellcasting.py
@dataclass
class SpellSlots:
    level_1: int = 0
    level_2: int = 0
    # ... through level 9
    used_slots: Dict[int, int] = field(default_factory=dict)
    
    def cast_spell(self, spell_level: int, slot_level: int) -> bool:
        # Implementation

@dataclass
class Spellcasting:
    spell_slots: SpellSlots
    spells_known: List[Spell] = field(default_factory=list)
    spells_prepared: List[Spell] = field(default_factory=list)
    spellcasting_ability: AbilityType = AbilityType.INTELLIGENCE
    
    def calculate_spell_save_dc(self, ability_modifier: int, proficiency_bonus: int) -> int:
        return 8 + ability_modifier + proficiency_bonus
```

**Files to Create**:
- `src/models/character/spellcasting.py`
- `tests/models/test_spellcasting.py`

---

### TASK-BE-006: Character Progression System
**Estimated Time**: 3-4 days  
**Assignee**: [Mid-Level Backend Developer]

**Description**: Implement character leveling and progression mechanics.

**Requirements**:
- Level-up calculation system
- Hit point progression
- Ability score improvements
- Proficiency bonus scaling
- Feature unlocking by level

**Acceptance Criteria**:
- [ ] Level-up hit point calculation
- [ ] Ability score improvement tracking
- [ ] Proficiency bonus auto-calculation
- [ ] Class feature unlocking
- [ ] Multi-class support preparation

**Technical Details**:
```python
# Enhance src/models/character/base.py
@dataclass
class CharacterProgression:
    # Existing fields...
    ability_score_improvements: Dict[AbilityType, int] = field(default_factory=dict)
    hit_point_rolls: List[int] = field(default_factory=list)
    
    def level_up(self, character_class: str, constitution_modifier: int, hit_die: int) -> None:
        # Implementation
        
    def get_available_asi_points(self) -> int:
        # Ability Score Improvement calculation
```

**Files to Modify**:
- `src/models/character/base.py`
- `tests/models/test_character_progression.py`

---

## 🔵 LOW PRIORITY TASKS

### TASK-BE-007: Character Creation System
**Estimated Time**: 4-5 days  
**Assignee**: [Mid-Level Backend Developer]

**Description**: Create character creation and validation system.

**Requirements**:
- Race and class template system
- Starting equipment calculation
- Racial ability score bonuses
- Class skill proficiencies
- Background features

**Acceptance Criteria**:
- [ ] Race templates with bonuses
- [ ] Class templates with features
- [ ] Starting equipment by class
- [ ] Skill proficiency assignment
- [ ] Background trait assignment

---

### TASK-BE-008: Rules Validation System
**Estimated Time**: 3-4 days  
**Assignee**: [Senior Backend Developer]

**Description**: Implement D&D rules validation and enforcement.

**Requirements**:
- Validate character creation choices
- Enforce multiclassing requirements
- Check spell/equipment prerequisites
- Validate ability score limits
- Rules conflict detection

**Acceptance Criteria**:
- [ ] Character creation validation
- [ ] Multiclassing requirement checks
- [ ] Spell prerequisite validation
- [ ] Equipment restriction enforcement
- [ ] Comprehensive error messages

---

### TASK-BE-009: Homebrew Content System
**Estimated Time**: 6-8 days  
**Assignee**: [Senior Backend Developer]

**Description**: Create system for custom/homebrew content support.

**Requirements**:
- Custom race/class definitions
- Homebrew spell creation
- Custom equipment items
- Rule modification system
- Import/export homebrew content

**Acceptance Criteria**:
- [ ] Custom race/class support
- [ ] Homebrew spell integration
- [ ] Custom equipment creation
- [ ] Rule override system
- [ ] JSON-based homebrew format

---

## Data Structure Examples

### Core Models Integration
```python
# Enhanced Character model
@dataclass
class Character:
    # Existing fields...
    skills: Skills = field(default_factory=Skills)
    saving_throws: SavingThrows = field(default_factory=SavingThrows)
    spellcasting: Optional[Spellcasting] = None
    inventory: List[InventoryItem] = field(default_factory=list)
    
    def calculate_ac(self) -> int:
        # Calculate AC from equipment, abilities, etc.
        
    def get_attack_bonus(self, weapon: Weapon) -> int:
        # Calculate attack bonus with weapon
        
    def get_damage_bonus(self, weapon: Weapon) -> int:
        # Calculate damage bonus with weapon
```

## Development Guidelines

### Code Quality Standards
- Use dataclasses for all models
- Include comprehensive docstrings
- Add type hints for all methods
- Follow single responsibility principle
- Implement proper error handling

### Testing Requirements
- Unit tests for all calculations
- Edge case testing (level 1 vs level 20)
- Integration tests with Character model
- Performance tests for complex calculations

### D&D Rules Compliance
- Reference Player's Handbook for accuracy
- Implement official rules precisely
- Document any house rules clearly
- Support for optional rules (feats, multiclassing)

### Data Validation
- Validate all user inputs
- Enforce D&D rules constraints
- Provide meaningful error messages
- Support for warnings vs. errors

### Questions?
- Check Player's Handbook for rule clarifications
- Ask in #backend-team channel for architecture questions
- Consult with frontend team for data structure needs
- Review existing models for patterns