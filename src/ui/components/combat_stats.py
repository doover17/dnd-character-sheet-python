"""
Combat stats UI component
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional
from ...models.character.base import CharacterVitals

class CombatStatsWidget(ttk.Frame):
    """Widget for displaying combat statistics"""

    def __init__(self, parent, vitals: CharacterVitals):
        super().__init__(parent)
        self.vitals = vitals
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
        self.ac_label = ttk.Label(ac_frame, text=str(self.vitals.armor_class), font=("Arial", 16, "bold"))
        self.ac_label.pack(side=tk.LEFT)

        # Hit Points
        hp_frame = ttk.Frame(self)
        hp_frame.pack(fill=tk.X, pady=2)
        ttk.Label(hp_frame, text="Hit Points:", width=15).pack(side=tk.LEFT)
        self.hp_label = ttk.Label(hp_frame, text=f"{self.vitals.hit_points} / {self.vitals.max_hit_points}", font=("Arial", 16, "bold"))
        self.hp_label.pack(side=tk.LEFT)

        # Speed
        speed_frame = ttk.Frame(self)
        speed_frame.pack(fill=tk.X, pady=2)
        ttk.Label(speed_frame, text="Speed:", width=15).pack(side=tk.LEFT)
        self.speed_label = ttk.Label(speed_frame, text=f"{self.vitals.speed} ft.", font=("Arial", 16, "bold"))
        self.speed_label.pack(side=tk.LEFT)

    def update_vitals(self, vitals: CharacterVitals):
        """Update displayed vitals"""
        self.vitals = vitals
        self.ac_label.config(text=str(self.vitals.armor_class))
        self.hp_label.config(text=f"{self.vitals.hit_points} / {self.vitals.max_hit_points}")
        self.speed_label.config(text=f"{self.vitals.speed} ft.")
