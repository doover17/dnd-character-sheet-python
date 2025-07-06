#!/usr/bin/env python3
"""
D&D Character Sheet UI - Python Implementation
Based on D&D Beyond styling patterns

Key design elements extracted:
- Fonts: Tiamat Condensed SC Regular (headers), Roboto (body text)
- Colors: #242527 (dark text), #ddd (borders), #fff (backgrounds)
- Layout: Clean, card-based design with rounded corners
"""

import tkinter as tk
from tkinter import ttk, font
import json
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class AbilityScores:
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    
    def get_modifier(self, ability: str) -> int:
        """Calculate ability modifier"""
        score = getattr(self, ability)
        return (score - 10) // 2

@dataclass
class Character:
    name: str = "N.O.V.A."
    character_class: str = "Artificer"
    level: int = 1
    race: str = "Warforged"
    background: str = "Guild Artisan"
    ability_scores: AbilityScores = None
    hit_points: int = 8
    armor_class: int = 13
    proficiency_bonus: int = 2
    
    def __post_init__(self):
        if self.ability_scores is None:
            self.ability_scores = AbilityScores()

class CharacterSheetUI:
    def __init__(self, root):
        self.root = root
        self.character = Character()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        
    def setup_window(self):
        """Configure main window with D&D Beyond styling"""
        self.root.title("D&D Character Sheet - N.O.V.A.")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f8f9fa")
        
    def setup_styles(self):
        """Configure ttk styles based on D&D Beyond patterns"""
        self.style = ttk.Style()
        
        # Configure card-like frames
        self.style.configure(
            "Card.TFrame",
            background="#ffffff",
            relief="solid",
            borderwidth=1
        )
        
        # Configure header labels
        self.style.configure(
            "Header.TLabel",
            font=("Arial", 12, "bold"),
            foreground="#242527",
            background="#ffffff"
        )
        
        # Configure body text
        self.style.configure(
            "Body.TLabel",
            font=("Arial", 10),
            foreground="#242527",
            background="#ffffff"
        )
        
        # Configure ability score styling
        self.style.configure(
            "Ability.TLabel",
            font=("Arial", 16, "bold"),
            foreground="#242527",
            background="#ffffff",
            anchor="center"
        )
        
    def create_widgets(self):
        """Create main character sheet interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Character header
        self.create_character_header(main_frame)
        
        # Main content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Left column - Ability scores and combat stats
        left_column = ttk.Frame(content_frame)
        left_column.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        self.create_ability_scores(left_column)
        self.create_combat_stats(left_column)
        
        # Right column - Character details
        right_column = ttk.Frame(content_frame)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_character_details(right_column)
        
    def create_character_header(self, parent):
        """Create character name and basic info header"""
        header_frame = ttk.Frame(parent, style="Card.TFrame", padding="15")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Character name
        name_label = ttk.Label(
            header_frame,
            text=self.character.name,
            font=("Arial", 24, "bold"),
            foreground="#242527",
            background="#ffffff"
        )
        name_label.pack(anchor=tk.W)
        
        # Character class and level
        class_info = f"Level {self.character.level} {self.character.race} {self.character.character_class}"
        class_label = ttk.Label(
            header_frame,
            text=class_info,
            style="Header.TLabel"
        )
        class_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Background
        bg_label = ttk.Label(
            header_frame,
            text=f"Background: {self.character.background}",
            style="Body.TLabel"
        )
        bg_label.pack(anchor=tk.W, pady=(2, 0))
        
    def create_ability_scores(self, parent):
        """Create ability scores section"""
        abilities_frame = ttk.Frame(parent, style="Card.TFrame", padding="15")
        abilities_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(abilities_frame, text="Ability Scores", style="Header.TLabel").pack(anchor=tk.W)
        
        abilities = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
        
        for ability in abilities:
            self.create_ability_score_row(abilities_frame, ability)
            
    def create_ability_score_row(self, parent, ability_name):
        """Create individual ability score row"""
        row_frame = ttk.Frame(parent)
        row_frame.pack(fill=tk.X, pady=2)
        
        # Ability name
        name_label = ttk.Label(
            row_frame,
            text=ability_name.capitalize(),
            style="Body.TLabel",
            width=12
        )
        name_label.pack(side=tk.LEFT)
        
        # Score
        score = getattr(self.character.ability_scores, ability_name)
        score_label = ttk.Label(
            row_frame,
            text=str(score),
            style="Ability.TLabel",
            width=3
        )
        score_label.pack(side=tk.LEFT, padx=(10, 5))
        
        # Modifier
        modifier = self.character.ability_scores.get_modifier(ability_name)
        mod_text = f"+{modifier}" if modifier >= 0 else str(modifier)
        mod_label = ttk.Label(
            row_frame,
            text=f"({mod_text})",
            style="Body.TLabel"
        )
        mod_label.pack(side=tk.LEFT)
        
    def create_combat_stats(self, parent):
        """Create combat statistics section"""
        combat_frame = ttk.Frame(parent, style="Card.TFrame", padding="15")
        combat_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(combat_frame, text="Combat Stats", style="Header.TLabel").pack(anchor=tk.W)
        
        # Armor Class
        ac_frame = ttk.Frame(combat_frame)
        ac_frame.pack(fill=tk.X, pady=2)
        ttk.Label(ac_frame, text="Armor Class:", style="Body.TLabel").pack(side=tk.LEFT)
        ttk.Label(ac_frame, text=str(self.character.armor_class), style="Ability.TLabel").pack(side=tk.RIGHT)
        
        # Hit Points
        hp_frame = ttk.Frame(combat_frame)
        hp_frame.pack(fill=tk.X, pady=2)
        ttk.Label(hp_frame, text="Hit Points:", style="Body.TLabel").pack(side=tk.LEFT)
        ttk.Label(hp_frame, text=str(self.character.hit_points), style="Ability.TLabel").pack(side=tk.RIGHT)
        
        # Proficiency Bonus
        prof_frame = ttk.Frame(combat_frame)
        prof_frame.pack(fill=tk.X, pady=2)
        ttk.Label(prof_frame, text="Proficiency Bonus:", style="Body.TLabel").pack(side=tk.LEFT)
        ttk.Label(prof_frame, text=f"+{self.character.proficiency_bonus}", style="Ability.TLabel").pack(side=tk.RIGHT)
        
    def create_character_details(self, parent):
        """Create character details section"""
        details_frame = ttk.Frame(parent, style="Card.TFrame", padding="15")
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(details_frame, text="Character Details", style="Header.TLabel").pack(anchor=tk.W)
        
        # Placeholder for skills, equipment, spells, etc.
        placeholder_text = """
Skills & Proficiencies:
• Arcana (INT)
• Investigation (INT)
• Medicine (WIS)
• Perception (WIS)

Equipment:
• Light Crossbow
• Studded Leather Armor
• Thieves' Tools
• Dungeoneer's Pack

Spells:
• Detect Magic
• Identify
• Cure Wounds
• Guidance

Features & Traits:
• Constructed Resilience
• Sentry's Rest
• Integrated Protection
• Magical Tinkering
        """
        
        details_text = tk.Text(
            details_frame,
            wrap=tk.WORD,
            font=("Arial", 10),
            bg="#ffffff",
            fg="#242527",
            relief="flat",
            padx=10,
            pady=10
        )
        details_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        details_text.insert(tk.END, placeholder_text.strip())
        details_text.config(state=tk.DISABLED)

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = CharacterSheetUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()