"""
Base character model definitions
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class AbilityType(Enum):
    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    CONSTITUTION = "constitution"
    INTELLIGENCE = "intelligence"
    WISDOM = "wisdom"
    CHARISMA = "charisma"

@dataclass
class AbilityScores:
    """Character ability scores"""
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    
    def get_modifier(self, ability: AbilityType) -> int:
        """Calculate ability modifier"""
        score = getattr(self, ability.value)
        return (score - 10) // 2
    
    def get_all_modifiers(self) -> Dict[str, int]:
        """Get all ability modifiers"""
        return {
            ability.value: self.get_modifier(ability)
            for ability in AbilityType
        }

@dataclass
class CharacterVitals:
    """Character health and defensive stats"""
    hit_points: int = 8
    max_hit_points: int = 8
    temporary_hit_points: int = 0
    armor_class: int = 10
    speed: int = 30
    initiative_modifier: int = 0
    death_saves_successes: int = 0
    death_saves_failures: int = 0
    conditions: List[str] = field(default_factory=list)

    @property
    def current_hit_points(self) -> int:
        return self.hit_points + self.temporary_hit_points

    def calculate_initiative(self, dex_modifier: int) -> int:
        return dex_modifier + self.initiative_modifier

@dataclass
class CharacterProgression:
    """Character level and experience"""
    level: int = 1
    experience_points: int = 0
    proficiency_bonus: int = 2
    
    def calculate_proficiency_bonus(self) -> int:
        """Calculate proficiency bonus from level"""
        return 2 + ((self.level - 1) // 4)

@dataclass
class Character:
    """Main character model"""
    # Basic Info
    name: str = ""
    character_class: str = ""
    race: str = ""
    background: str = ""
    alignment: str = ""
    
    # Core Stats
    ability_scores: AbilityScores = field(default_factory=AbilityScores)
    vitals: CharacterVitals = field(default_factory=CharacterVitals)
    progression: CharacterProgression = field(default_factory=CharacterProgression)
    
    # Skills & Proficiencies
    skill_proficiencies: List[str] = field(default_factory=list)
    language_proficiencies: List[str] = field(default_factory=list)
    tool_proficiencies: List[str] = field(default_factory=list)
    
    # Combat
    saving_throw_proficiencies: List[str] = field(default_factory=list)
    
    # Equipment
    equipment: List[str] = field(default_factory=list)
    
    # Spells
    spell_slots: Dict[int, int] = field(default_factory=dict)
    spells_known: List[str] = field(default_factory=list)
    
    # Features & Traits
    racial_traits: List[str] = field(default_factory=list)
    class_features: List[str] = field(default_factory=list)
    
    # Metadata
    notes: str = ""
    
    def __post_init__(self):
        """Initialize calculated values"""
        if not self.name:
            self.name = "Unnamed Character"
        
        # Update proficiency bonus based on level
        self.progression.proficiency_bonus = self.progression.calculate_proficiency_bonus()