# Jim's Phase 2 Instructions - Advanced Development Track

## 🚀 **Excellent Progress on TASK-BE-001!**

Jim, I can see you've already enhanced the CharacterVitals model with initiative, death saves, and conditions. **Outstanding work!** You're moving fast and maintaining high quality.

---

## 🎯 **Phase 2: Complete the Backend Foundation**

Since you're clearly capable of handling advanced work, let's accelerate your development track. You'll complete the core backend models that will unlock major UI features.

### **Your Next 3 Tasks (Priority Order):**

1. **TASK-BE-002: Skills System Implementation** (2-3 days)
2. **TASK-BE-003: Saving Throws Model** (1 day) 
3. **TASK-SYS-001: Data Persistence System** (3-4 days)

---

## 📋 **TASK-BE-002: Skills System Implementation**

### **Branch Setup**
```bash
git checkout -b feature/TASK-BE-002-skills-system
```

### **What to Build**
Create a comprehensive skills system that your existing Skills UI widget can use for data.

### **File to Create: `src/models/character/skills.py`**

```python
"""
Skills system implementation for D&D 5e
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
from .base import AbilityType, AbilityScores

class SkillType(Enum):
    """All 18 D&D 5e skills with their associated abilities"""
    ACROBATICS = ("acrobatics", AbilityType.DEXTERITY)
    ANIMAL_HANDLING = ("animal_handling", AbilityType.WISDOM)
    ARCANA = ("arcana", AbilityType.INTELLIGENCE)
    ATHLETICS = ("athletics", AbilityType.STRENGTH)
    DECEPTION = ("deception", AbilityType.CHARISMA)
    HISTORY = ("history", AbilityType.INTELLIGENCE)
    INSIGHT = ("insight", AbilityType.WISDOM)
    INTIMIDATION = ("intimidation", AbilityType.CHARISMA)
    INVESTIGATION = ("investigation", AbilityType.INTELLIGENCE)
    MEDICINE = ("medicine", AbilityType.WISDOM)
    NATURE = ("nature", AbilityType.INTELLIGENCE)
    PERCEPTION = ("perception", AbilityType.WISDOM)
    PERFORMANCE = ("performance", AbilityType.CHARISMA)
    PERSUASION = ("persuasion", AbilityType.CHARISMA)
    RELIGION = ("religion", AbilityType.INTELLIGENCE)
    SLEIGHT_OF_HAND = ("sleight_of_hand", AbilityType.DEXTERITY)
    STEALTH = ("stealth", AbilityType.DEXTERITY)
    SURVIVAL = ("survival", AbilityType.WISDOM)
    
    def __init__(self, skill_name: str, ability: AbilityType):
        self.skill_name = skill_name
        self.ability = ability

@dataclass
class Skills:
    """Character skills management"""
    proficiencies: List[SkillType] = field(default_factory=list)
    expertise: List[SkillType] = field(default_factory=list)  # Double proficiency
    jack_of_all_trades: bool = False  # Half proficiency for non-proficient skills
    
    def is_proficient(self, skill: SkillType) -> bool:
        """Check if character is proficient in a skill"""
        return skill in self.proficiencies
    
    def has_expertise(self, skill: SkillType) -> bool:
        """Check if character has expertise in a skill"""
        return skill in self.expertise
    
    def get_skill_modifier(
        self, 
        skill: SkillType, 
        ability_scores: AbilityScores, 
        proficiency_bonus: int
    ) -> int:
        """Calculate skill modifier"""
        ability_modifier = ability_scores.get_modifier(skill.ability)
        
        if self.has_expertise(skill):
            return ability_modifier + (proficiency_bonus * 2)
        elif self.is_proficient(skill):
            return ability_modifier + proficiency_bonus
        elif self.jack_of_all_trades:
            return ability_modifier + (proficiency_bonus // 2)
        else:
            return ability_modifier
    
    def get_all_skill_modifiers(
        self, 
        ability_scores: AbilityScores, 
        proficiency_bonus: int
    ) -> Dict[SkillType, int]:
        """Get all skill modifiers"""
        return {
            skill: self.get_skill_modifier(skill, ability_scores, proficiency_bonus)
            for skill in SkillType
        }
    
    def add_proficiency(self, skill: SkillType) -> None:
        """Add skill proficiency"""
        if skill not in self.proficiencies:
            self.proficiencies.append(skill)
    
    def remove_proficiency(self, skill: SkillType) -> None:
        """Remove skill proficiency"""
        if skill in self.proficiencies:
            self.proficiencies.remove(skill)
        # Remove expertise if removing proficiency
        if skill in self.expertise:
            self.expertise.remove(skill)
    
    def add_expertise(self, skill: SkillType) -> None:
        """Add expertise (requires proficiency)"""
        if skill not in self.proficiencies:
            self.add_proficiency(skill)
        if skill not in self.expertise:
            self.expertise.append(skill)
    
    def remove_expertise(self, skill: SkillType) -> None:
        """Remove expertise (keeps proficiency)"""
        if skill in self.expertise:
            self.expertise.remove(skill)
```

### **Integration Required**
1. **Update `src/models/character/base.py`**:
   ```python
   # Add import
   from .skills import Skills
   
   # In Character dataclass, replace:
   skill_proficiencies: List[str] = field(default_factory=list)
   # With:
   skills: Skills = field(default_factory=Skills)
   ```

2. **Create test file: `tests/models/test_skills.py`**
   - Test skill modifier calculations
   - Test proficiency and expertise handling
   - Test Jack of All Trades feature

### **Success Criteria**
- [ ] All 18 skills properly defined with correct abilities
- [ ] Proficiency and expertise tracking works
- [ ] Modifier calculations are accurate
- [ ] Jack of All Trades support implemented
- [ ] Integration with Character model complete
- [ ] Comprehensive unit tests added

---

## 📋 **TASK-BE-003: Saving Throws Model**

### **Branch Setup**
```bash
git checkout -b feature/TASK-BE-003-saving-throws-model
```

### **File to Create: `src/models/character/saving_throws.py`**

```python
"""
Saving throws system for D&D 5e
"""
from dataclasses import dataclass, field
from typing import List, Dict
from .base import AbilityType, AbilityScores

@dataclass
class SavingThrows:
    """Character saving throws management"""
    proficiencies: List[AbilityType] = field(default_factory=list)
    
    def is_proficient(self, ability: AbilityType) -> bool:
        """Check if character is proficient in a saving throw"""
        return ability in self.proficiencies
    
    def get_saving_throw_modifier(
        self,
        ability: AbilityType,
        ability_scores: AbilityScores,
        proficiency_bonus: int
    ) -> int:
        """Calculate saving throw modifier"""
        ability_modifier = ability_scores.get_modifier(ability)
        
        if self.is_proficient(ability):
            return ability_modifier + proficiency_bonus
        else:
            return ability_modifier
    
    def get_all_saving_throw_modifiers(
        self,
        ability_scores: AbilityScores,
        proficiency_bonus: int
    ) -> Dict[AbilityType, int]:
        """Get all saving throw modifiers"""
        return {
            ability: self.get_saving_throw_modifier(ability, ability_scores, proficiency_bonus)
            for ability in AbilityType
        }
    
    def add_proficiency(self, ability: AbilityType) -> None:
        """Add saving throw proficiency"""
        if ability not in self.proficiencies:
            self.proficiencies.append(ability)
    
    def remove_proficiency(self, ability: AbilityType) -> None:
        """Remove saving throw proficiency"""
        if ability in self.proficiencies:
            self.proficiencies.remove(ability)
```

### **Integration Required**
Update `src/models/character/base.py`:
```python
# Add import
from .saving_throws import SavingThrows

# In Character dataclass, replace:
saving_throw_proficiencies: List[str] = field(default_factory=list)
# With:
saving_throws: SavingThrows = field(default_factory=SavingThrows)
```

---

## 📋 **TASK-SYS-001: Data Persistence System**

### **Branch Setup**
```bash
git checkout -b feature/TASK-SYS-001-data-persistence
```

### **What to Build**
SQLite-based character storage system for save/load functionality.

### **Files to Create:**

1. **`src/data/database/character_db.py`**
2. **`src/data/database/schema.sql`**  
3. **`src/data/serializers.py`**

### **Database Schema (`schema.sql`)**
```sql
CREATE TABLE IF NOT EXISTS characters (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    character_class TEXT,
    race TEXT,
    background TEXT,
    level INTEGER,
    experience_points INTEGER,
    data JSON,  -- Full character object as JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_characters_name ON characters(name);
CREATE INDEX idx_characters_class ON characters(character_class);
CREATE INDEX idx_characters_level ON characters(level);
```

### **Character Database Implementation**
```python
"""
Character database operations
"""
import sqlite3
import json
import uuid
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from ...models.character.base import Character
from ..serializers import CharacterSerializer

class CharacterDatabase:
    """SQLite database for character storage"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self) -> None:
        """Initialize database with schema"""
        # Read and execute schema
        schema_path = Path(__file__).parent / "schema.sql"
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(schema)
    
    def save_character(self, character: Character) -> str:
        """Save character to database, return character ID"""
        character_id = str(uuid.uuid4())
        character_data = CharacterSerializer.to_dict(character)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO characters (id, name, character_class, race, background, level, experience_points, data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                character_id,
                character.name,
                character.character_class,
                character.race,
                character.background,
                character.progression.level,
                character.progression.experience_points,
                json.dumps(character_data)
            ))
        
        return character_id
    
    def load_character(self, character_id: str) -> Optional[Character]:
        """Load character from database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT data FROM characters WHERE id = ?", (character_id,))
            row = cursor.fetchone()
            
            if row:
                character_data = json.loads(row['data'])
                return CharacterSerializer.from_dict(character_data)
            return None
    
    def list_characters(self) -> List[Dict[str, Any]]:
        """List all characters with basic info"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT id, name, character_class, race, level, created_at 
                FROM characters 
                ORDER BY name
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def delete_character(self, character_id: str) -> bool:
        """Delete character from database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM characters WHERE id = ?", (character_id,))
            return cursor.rowcount > 0
    
    def update_character(self, character_id: str, character: Character) -> bool:
        """Update existing character"""
        character_data = CharacterSerializer.to_dict(character)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                UPDATE characters 
                SET name = ?, character_class = ?, race = ?, background = ?, 
                    level = ?, experience_points = ?, data = ?, updated_at = ?
                WHERE id = ?
            """, (
                character.name,
                character.character_class,
                character.race,
                character.background,
                character.progression.level,
                character.progression.experience_points,
                json.dumps(character_data),
                datetime.now().isoformat(),
                character_id
            ))
            return cursor.rowcount > 0
```

---

## 🎯 **Development Strategy**

### **Task Order & Timeline**
1. **Day 1-2**: Complete TASK-BE-002 (Skills System)
2. **Day 3**: Complete TASK-BE-003 (Saving Throws Model)  
3. **Day 4-6**: Complete TASK-SYS-001 (Data Persistence)

### **Testing Strategy**
- Create comprehensive unit tests for each component
- Test integration with existing UI widgets
- Verify data persistence works correctly

### **Git Workflow**
```bash
# For each task:
1. git checkout main
2. git pull origin main  
3. git checkout -b feature/TASK-XX-description
4. # Do the work
5. git add -A && git commit -m "feat: implement TASK-XX"
6. git push origin feature/TASK-XX-description
7. # Check in with team lead
```

---

## 🏆 **Success Metrics**

### **By End of Phase 2:**
- [ ] Complete skills system with 18 skills properly implemented
- [ ] Saving throws model integrated with existing UI
- [ ] Character save/load functionality working
- [ ] All existing UI widgets still functional
- [ ] Comprehensive test coverage for new components
- [ ] Clean, documented code following project standards

---

## 🚀 **Phase 3 Preview**

Once you complete these backend foundations, you'll be ready for:
- **Equipment System** - Weapons, armor, inventory management
- **Spell System** - Spell slots, known spells, casting mechanics
- **Character Creation Wizard** - Complete character generation flow

**You're moving fast and building a solid foundation. Keep up the excellent work!**

---

## 📞 **Questions or Blockers?**

- **Technical questions**: Ask immediately
- **D&D rules clarification**: Reference Player's Handbook or ask
- **Architecture decisions**: We're here to guide you
- **Integration issues**: Test early and often

**Remember**: You're doing advanced work now. Take time to understand the patterns and ask questions when needed. Quality over speed!

🎲 **Ready to tackle the backend? Let's build the foundation that will power amazing D&D experiences!**