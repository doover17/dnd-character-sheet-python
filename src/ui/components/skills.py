"""
Skills UI component
"""
import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Callable
from ...models.character.base import Character, AbilityType

class SkillsWidget(ttk.Frame):
    """Widget for displaying and managing character skills"""

    def __init__(self, parent, character: Character, on_change: Optional[Callable] = None):
        super().__init__(parent)
        self.character = character
        self.on_change = on_change
        self.skill_vars = {}
        self.setup_ui()

    def setup_ui(self):
        """Set up the skills UI"""
        title_label = ttk.Label(self, text="Skills", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))

        # Define all 18 skills and their associated abilities
        self.skills = {
            "Acrobatics": AbilityType.DEXTERITY,
            "Animal Handling": AbilityType.WISDOM,
            "Arcana": AbilityType.INTELLIGENCE,
            "Athletics": AbilityType.STRENGTH,
            "Deception": AbilityType.CHARISMA,
            "History": AbilityType.INTELLIGENCE,
            "Insight": AbilityType.WISDOM,
            "Intimidation": AbilityType.CHARISMA,
            "Investigation": AbilityType.INTELLIGENCE,
            "Medicine": AbilityType.WISDOM,
            "Nature": AbilityType.INTELLIGENCE,
            "Perception": AbilityType.WISDOM,
            "Performance": AbilityType.CHARISMA,
            "Persuasion": AbilityType.CHARISMA,
            "Religion": AbilityType.INTELLIGENCE,
            "Sleight of Hand": AbilityType.DEXTERITY,
            "Stealth": AbilityType.DEXTERITY,
            "Survival": AbilityType.WISDOM,
        }

        for skill, ability in self.skills.items():
            self.create_skill_row(skill, ability)

    def create_skill_row(self, skill: str, ability: AbilityType):
        """Create a row for a single skill"""
        row_frame = ttk.Frame(self)
        row_frame.pack(fill=tk.X, pady=1)

        # Proficiency Checkbox
        prof_var = tk.BooleanVar(value=skill in self.character.skill_proficiencies)
        self.skill_vars[skill] = prof_var
        prof_check = ttk.Checkbutton(row_frame, variable=prof_var, command=lambda s=skill: self.on_proficiency_change(s))
        prof_check.pack(side=tk.LEFT)

        # Skill Name
        skill_label = ttk.Label(row_frame, text=skill, width=15)
        skill_label.pack(side=tk.LEFT, padx=(5, 0))

        # Ability Association
        ability_label = ttk.Label(row_frame, text=f"({ability.value[:3].upper()})", width=5)
        ability_label.pack(side=tk.LEFT)

        # Skill Modifier
        modifier = self.calculate_skill_modifier(skill, ability)
        mod_text = f"+{modifier}" if modifier >= 0 else str(modifier)
        mod_label = ttk.Label(row_frame, text=mod_text, width=4)
        mod_label.pack(side=tk.LEFT, padx=(5, 0))
        setattr(self, f"{skill.replace(' ', '_')}_modifier_label", mod_label)

    def calculate_skill_modifier(self, skill: str, ability: AbilityType) -> int:
        """Calculate the modifier for a given skill"""
        ability_modifier = self.character.ability_scores.get_modifier(ability)
        proficiency_bonus = self.character.progression.proficiency_bonus
        is_proficient = self.skill_vars[skill].get()

        if is_proficient:
            return ability_modifier + proficiency_bonus
        else:
            return ability_modifier

    def on_proficiency_change(self, skill: str):
        """Handle proficiency checkbox change"""
        is_proficient = self.skill_vars[skill].get()
        if is_proficient:
            if skill not in self.character.skill_proficiencies:
                self.character.skill_proficiencies.append(skill)
        else:
            if skill in self.character.skill_proficiencies:
                self.character.skill_proficiencies.remove(skill)

        self.update_skill_modifier(skill)

        if self.on_change:
            self.on_change("skill_proficiencies", self.character.skill_proficiencies)

    def update_skill_modifier(self, skill: str):
        """Update the displayed modifier for a skill"""
        ability = self.skills[skill]
        modifier = self.calculate_skill_modifier(skill, ability)
        mod_text = f"+{modifier}" if modifier >= 0 else str(modifier)
        mod_label = getattr(self, f"{skill.replace(' ', '_')}_modifier_label")
        mod_label.config(text=mod_text)

    def update_all_modifiers(self):
        """Update all skill modifiers"""
        for skill in self.skills:
            self.update_skill_modifier(skill)
