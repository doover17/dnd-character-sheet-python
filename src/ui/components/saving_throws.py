"""
Saving Throws UI component
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from ...models.character.base import Character, AbilityType

class SavingThrowsWidget(ttk.Frame):
    """Widget for displaying and managing saving throws"""

    def __init__(self, parent, character: Character, on_change: Optional[Callable] = None):
        super().__init__(parent)
        self.character = character
        self.on_change = on_change
        self.saving_throw_vars = {}
        self.setup_ui()

    def setup_ui(self):
        """Set up the saving throws UI"""
        title_label = ttk.Label(self, text="Saving Throws", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))

        for ability in AbilityType:
            self.create_saving_throw_row(ability)

    def create_saving_throw_row(self, ability: AbilityType):
        """Create a row for a single saving throw"""
        row_frame = ttk.Frame(self)
        row_frame.pack(fill=tk.X, pady=1)

        # Proficiency Checkbox
        prof_var = tk.BooleanVar(value=ability.value in self.character.saving_throw_proficiencies)
        self.saving_throw_vars[ability.value] = prof_var
        prof_check = ttk.Checkbutton(row_frame, variable=prof_var, command=lambda a=ability: self.on_proficiency_change(a))
        prof_check.pack(side=tk.LEFT)

        # Ability Name
        ability_label = ttk.Label(row_frame, text=ability.value.capitalize(), width=15)
        ability_label.pack(side=tk.LEFT, padx=(5, 0))

        # Saving Throw Modifier
        modifier = self.calculate_modifier(ability)
        mod_text = f"+{modifier}" if modifier >= 0 else str(modifier)
        mod_label = ttk.Label(row_frame, text=mod_text, width=4)
        mod_label.pack(side=tk.LEFT, padx=(5, 0))
        setattr(self, f"{ability.value}_modifier_label", mod_label)

    def calculate_modifier(self, ability: AbilityType) -> int:
        """Calculate the saving throw modifier"""
        ability_modifier = self.character.ability_scores.get_modifier(ability)
        proficiency_bonus = self.character.progression.proficiency_bonus
        is_proficient = self.saving_throw_vars[ability.value].get()

        if is_proficient:
            return ability_modifier + proficiency_bonus
        else:
            return ability_modifier

    def on_proficiency_change(self, ability: AbilityType):
        """Handle proficiency checkbox change"""
        is_proficient = self.saving_throw_vars[ability.value].get()
        if is_proficient:
            if ability.value not in self.character.saving_throw_proficiencies:
                self.character.saving_throw_proficiencies.append(ability.value)
        else:
            if ability.value in self.character.saving_throw_proficiencies:
                self.character.saving_throw_proficiencies.remove(ability.value)

        self.update_modifier_label(ability)

        if self.on_change:
            self.on_change("saving_throw_proficiencies", self.character.saving_throw_proficiencies)

    def update_modifier_label(self, ability: AbilityType):
        """Update the displayed modifier for a saving throw"""
        modifier = self.calculate_modifier(ability)
        mod_text = f"+{modifier}" if modifier >= 0 else str(modifier)
        mod_label = getattr(self, f"{ability.value}_modifier_label")
        mod_label.config(text=mod_text)

    def update_all_modifiers(self):
        """Update all saving throw modifiers"""
        for ability in AbilityType:
            self.update_modifier_label(ability)
