"""
Combat stats UI component
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional
from ...models.character.base import Character, AbilityType

class CombatStatsWidget(ttk.Frame):
    """Widget for displaying combat statistics"""

    def __init__(self, parent, character: Character):
        super().__init__(parent)
        self.character = character
        self.setup_ui()

    def setup_ui(self):
        """Set up the combat stats UI"""
        # Title
        title_label = ttk.Label(self, text="Combat Stats", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))

        # Armor Class
        ac_frame = ttk.Frame(self)
        ac_frame.pack(fill=tk.X, pady=2)
        ttk.Label(ac_frame, text="Armor Class:", width=15).pack(side=tk.LEFT)
        self.ac_label = ttk.Label(ac_frame, text=str(self.character.vitals.armor_class), font=("Arial", 16, "bold"))
        self.ac_label.pack(side=tk.LEFT)

        # Hit Points
        hp_frame = ttk.Frame(self)
        hp_frame.pack(fill=tk.X, pady=2)
        ttk.Label(hp_frame, text="Hit Points:", width=15).pack(side=tk.LEFT)
        self.hp_label = ttk.Label(hp_frame, text=f"{self.character.vitals.hit_points} / {self.character.vitals.max_hit_points}", font=("Arial", 16, "bold"))
        self.hp_label.pack(side=tk.LEFT)

        # Speed
        speed_frame = ttk.Frame(self)
        speed_frame.pack(fill=tk.X, pady=2)
        ttk.Label(speed_frame, text="Speed:", width=15).pack(side=tk.LEFT)
        self.speed_label = ttk.Label(speed_frame, text=f"{self.character.vitals.speed} ft.", font=("Arial", 16, "bold"))
        self.speed_label.pack(side=tk.LEFT)

        # Initiative
        initiative_frame = ttk.Frame(self)
        initiative_frame.pack(fill=tk.X, pady=2)
        ttk.Label(initiative_frame, text="Initiative:", width=15).pack(side=tk.LEFT)
        dex_mod = self.character.ability_scores.get_modifier(AbilityType.DEXTERITY)
        initiative = self.character.vitals.calculate_initiative(dex_mod)
        self.initiative_label = ttk.Label(initiative_frame, text=f"{initiative:+}", font=("Arial", 16, "bold"))
        self.initiative_label.pack(side=tk.LEFT)

        # Death Saves
        death_saves_frame = ttk.Frame(self)
        death_saves_frame.pack(fill=tk.X, pady=2)
        ttk.Label(death_saves_frame, text="Death Saves:", width=15).pack(side=tk.LEFT)
        self.death_saves_success_label = ttk.Label(death_saves_frame, text=f"Successes: {self.character.vitals.death_saves_successes}")
        self.death_saves_success_label.pack(side=tk.LEFT)
        self.death_saves_failure_label = ttk.Label(death_saves_frame, text=f"Failures: {self.character.vitals.death_saves_failures}")
        self.death_saves_failure_label.pack(side=tk.LEFT, padx=(5,0))


    def update_vitals(self, character: Character):
        """Update displayed vitals"""
        self.character = character
        self.ac_label.config(text=str(self.character.vitals.armor_class))
        self.hp_label.config(text=f"{self.character.vitals.hit_points} / {self.character.vitals.max_hit_points}")
        self.speed_label.config(text=f"{self.character.vitals.speed} ft.")
        dex_mod = self.character.ability_scores.get_modifier(AbilityType.DEXTERITY)
        initiative = self.character.vitals.calculate_initiative(dex_mod)
        self.initiative_label.config(text=f"{initiative:+}")
        self.death_saves_success_label.config(text=f"Successes: {self.character.vitals.death_saves_successes}")
        self.death_saves_failure_label.config(text=f"Failures: {self.character.vitals.death_saves_failures}")