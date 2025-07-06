#!/usr/bin/env python3
"""
Main application entry point for D&D Character Sheet
"""
import sys
import tkinter as tk
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config.settings import (
    APP_NAME, 
    WINDOW_WIDTH, 
    WINDOW_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    COLOR_LIGHT
)
from src.models.character.base import Character, AbilityScores
from src.ui.components.character_header import CharacterHeaderWidget
from src.ui.components.ability_scores import AbilityScoresWidget
from src.ui.components.combat_stats import CombatStatsWidget
from src.ui.components.skills import SkillsWidget
from src.ui.components.saving_throws import SavingThrowsWidget
from src.ui.components.equipment import EquipmentWidget

class DnDCharacterSheetApp:
    """Main application class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.character = self.create_default_character()
        self.setup_window()
        self.setup_ui()
    
    def create_default_character(self) -> Character:
        """Create a default character for testing"""
        ability_scores = AbilityScores(
            strength=15,
            dexterity=14,
            constitution=13,
            intelligence=12,
            wisdom=10,
            charisma=8
        )
        
        character = Character(
            name="N.O.V.A.",
            character_class="Artificer",
            race="Warforged",
            background="Guild Artisan",
            ability_scores=ability_scores
        )
        
        character.progression.level = 3
        character.vitals.hit_points = 22
        character.vitals.max_hit_points = 22
        character.vitals.armor_class = 16
        
        return character
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.root.configure(bg=COLOR_LIGHT)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    
    def setup_ui(self):
        """Set up the main user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg=COLOR_LIGHT)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Character header
        header_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=1)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.character_header = CharacterHeaderWidget(
            header_frame, 
            self.character, 
            self.on_character_change
        )
        self.character_header.pack(fill=tk.X)
        
        # Content area
        content_frame = tk.Frame(main_frame, bg=COLOR_LIGHT)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left sidebar - Ability scores
        left_frame = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=1)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        self.ability_scores_widget = AbilityScoresWidget(
            left_frame,
            self.character.ability_scores,
            self.on_ability_score_change
        )
        self.ability_scores_widget.pack(fill=tk.X, padx=15, pady=15)

        # Combat Stats
        combat_stats_frame = tk.Frame(left_frame, bg="white")
        combat_stats_frame.pack(fill=tk.X, padx=15, pady=15)

        self.combat_stats_widget = CombatStatsWidget(
            combat_stats_frame,
            self.character
        )
        self.combat_stats_widget.pack(fill=tk.X)

        # Saving Throws
        saving_throws_frame = tk.Frame(left_frame, bg="white")
        saving_throws_frame.pack(fill=tk.X, padx=15, pady=15)

        self.saving_throws_widget = SavingThrowsWidget(
            saving_throws_frame,
            self.character,
            self.on_character_change
        )
        self.saving_throws_widget.pack(fill=tk.X)
        
        # Right area - Character details
        right_frame = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=1)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.equipment_widget = EquipmentWidget(
            right_frame,
            self.character,
            self.on_character_change
        )
        self.equipment_widget.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    def on_character_change(self, field: str, value):
        """Handle character field changes"""
        print(f"Character {field} changed to: {value}")
        # Here you could save to database, validate, etc.
    
    def on_ability_score_change(self, ability, score):
        """Handle ability score changes"""
        print(f"Ability {ability.value} changed to: {score}")
        # Here you could update dependent values like saves, skills, etc.
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    app = DnDCharacterSheetApp()
    app.run()

if __name__ == "__main__":
    main()