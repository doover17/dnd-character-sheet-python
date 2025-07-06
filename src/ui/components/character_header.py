"""
Character header UI component
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from ...models.character.base import Character

class CharacterHeaderWidget(ttk.Frame):
    """Widget for displaying character basic information"""
    
    def __init__(self, parent, character: Character, on_change: Optional[Callable] = None):
        super().__init__(parent)
        self.character = character
        self.on_change = on_change
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the character header UI"""
        # Main frame with padding
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Character name
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=(0, 10))
        
        name_label = ttk.Label(name_frame, text="Character Name:", font=("Arial", 10))
        name_label.pack(side=tk.LEFT)
        
        self.name_var = tk.StringVar(value=self.character.name)
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var, font=("Arial", 16, "bold"))
        name_entry.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        name_entry.bind('<KeyRelease>', self.on_name_change)
        
        # Character details row
        details_frame = ttk.Frame(main_frame)
        details_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Class
        class_frame = ttk.Frame(details_frame)
        class_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(class_frame, text="Class:", font=("Arial", 10)).pack(anchor=tk.W)
        self.class_var = tk.StringVar(value=self.character.character_class)
        class_entry = ttk.Entry(class_frame, textvariable=self.class_var, width=15)
        class_entry.pack(anchor=tk.W)
        class_entry.bind('<KeyRelease>', self.on_class_change)
        
        # Level
        level_frame = ttk.Frame(details_frame)
        level_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(level_frame, text="Level:", font=("Arial", 10)).pack(anchor=tk.W)
        self.level_var = tk.IntVar(value=self.character.progression.level)
        level_spinbox = ttk.Spinbox(level_frame, from_=1, to=20, textvariable=self.level_var, width=5)
        level_spinbox.pack(anchor=tk.W)
        level_spinbox.bind('<KeyRelease>', self.on_level_change)
        
        # Race
        race_frame = ttk.Frame(details_frame)
        race_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(race_frame, text="Race:", font=("Arial", 10)).pack(anchor=tk.W)
        self.race_var = tk.StringVar(value=self.character.race)
        race_entry = ttk.Entry(race_frame, textvariable=self.race_var, width=15)
        race_entry.pack(anchor=tk.W)
        race_entry.bind('<KeyRelease>', self.on_race_change)
        
        # Background
        background_frame = ttk.Frame(details_frame)
        background_frame.pack(side=tk.LEFT)
        
        ttk.Label(background_frame, text="Background:", font=("Arial", 10)).pack(anchor=tk.W)
        self.background_var = tk.StringVar(value=self.character.background)
        background_entry = ttk.Entry(background_frame, textvariable=self.background_var, width=15)
        background_entry.pack(anchor=tk.W)
        background_entry.bind('<KeyRelease>', self.on_background_change)
    
    def on_name_change(self, event=None):
        """Handle character name change"""
        self.character.name = self.name_var.get()
        if self.on_change:
            self.on_change("name", self.character.name)
    
    def on_class_change(self, event=None):
        """Handle character class change"""
        self.character.character_class = self.class_var.get()
        if self.on_change:
            self.on_change("class", self.character.character_class)
    
    def on_level_change(self, event=None):
        """Handle level change"""
        try:
            self.character.progression.level = self.level_var.get()
            # Update proficiency bonus
            self.character.progression.proficiency_bonus = self.character.progression.calculate_proficiency_bonus()
            if self.on_change:
                self.on_change("level", self.character.progression.level)
        except tk.TclError:
            pass
    
    def on_race_change(self, event=None):
        """Handle race change"""
        self.character.race = self.race_var.get()
        if self.on_change:
            self.on_change("race", self.character.race)
    
    def on_background_change(self, event=None):
        """Handle background change"""
        self.character.background = self.background_var.get()
        if self.on_change:
            self.on_change("background", self.character.background)
    
    def update_character(self, character: Character):
        """Update displayed character information"""
        self.character = character
        self.name_var.set(character.name)
        self.class_var.set(character.character_class)
        self.level_var.set(character.progression.level)
        self.race_var.set(character.race)
        self.background_var.set(character.background)