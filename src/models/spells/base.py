"""
Spell model definitions
"""
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

class SpellSchool(Enum):
    ABJURATION = "abjuration"
    CONJURATION = "conjuration"
    DIVINATION = "divination"
    ENCHANTMENT = "enchantment"
    EVOCATION = "evocation"
    ILLUSION = "illusion"
    NECROMANCY = "necromancy"
    TRANSMUTATION = "transmutation"

class SpellComponent(Enum):
    VERBAL = "V"
    SOMATIC = "S"
    MATERIAL = "M"

@dataclass
class Spell:
    """Spell definition"""
    name: str
    level: int
    school: SpellSchool
    casting_time: str
    range: str
    components: List[SpellComponent]
    duration: str
    description: str
    material_components: Optional[str] = None
    higher_levels: Optional[str] = None
    ritual: bool = False
    concentration: bool = False
    
    @property
    def component_string(self) -> str:
        """Get formatted component string"""
        components = [comp.value for comp in self.components]
        return ", ".join(components)
    
    @property
    def is_cantrip(self) -> bool:
        """Check if spell is a cantrip"""
        return self.level == 0