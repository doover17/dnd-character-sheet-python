"""
Ability scores UI component
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from ...models.character.base import AbilityScores, AbilityType

class AbilityScoresWidget(ttk.Frame):
    """Widget for displaying and editing ability scores"""
    
    def __init__(self, parent, ability_scores: AbilityScores, on_change: Optional[Callable] = None):
        super().__init__(parent)
        self.ability_scores = ability_scores
        self.on_change = on_change
        self.score_vars = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the ability scores UI"""
        # Title
        title_label = ttk.Label(self, text="Ability Scores", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Create ability score rows
        for ability in AbilityType:
            self.create_ability_row(ability)
    
    def create_ability_row(self, ability: AbilityType):
        """Create a row for a single ability score"""
        row_frame = ttk.Frame(self)
        row_frame.pack(fill=tk.X, pady=2)
        
        # Ability name
        name_label = ttk.Label(row_frame, text=ability.value.capitalize(), width=12)
        name_label.pack(side=tk.LEFT)
        
        # Score entry
        score_var = tk.IntVar(value=getattr(self.ability_scores, ability.value))
        self.score_vars[ability.value] = score_var
        
        score_entry = ttk.Entry(row_frame, textvariable=score_var, width=5)
        score_entry.pack(side=tk.LEFT, padx=(10, 5))
        score_entry.bind('<KeyRelease>', lambda e, ab=ability: self.on_score_change(ab))
        
        # Modifier display
        modifier = self.ability_scores.get_modifier(ability)
        mod_text = f"+{modifier}" if modifier >= 0 else str(modifier)
        mod_label = ttk.Label(row_frame, text=f"({mod_text})", width=6)
        mod_label.pack(side=tk.LEFT)
        
        # Store reference for updates
        setattr(self, f"{ability.value}_modifier_label", mod_label)
    
    def on_score_change(self, ability: AbilityType):
        """Handle ability score change"""
        try:
            new_score = self.score_vars[ability.value].get()
            setattr(self.ability_scores, ability.value, new_score)
            
            # Update modifier display
            modifier = self.ability_scores.get_modifier(ability)
            mod_text = f"+{modifier}" if modifier >= 0 else str(modifier)
            mod_label = getattr(self, f"{ability.value}_modifier_label")
            mod_label.config(text=f"({mod_text})")
            
            # Notify parent of change
            if self.on_change:
                self.on_change(ability, new_score)
        except tk.TclError:
            # Invalid input, ignore
            pass
    
    def update_scores(self, ability_scores: AbilityScores):
        """Update displayed scores"""
        self.ability_scores = ability_scores
        for ability in AbilityType:
            self.score_vars[ability.value].set(getattr(ability_scores, ability.value))
            self.on_score_change(ability)