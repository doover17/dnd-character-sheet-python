"""
Dice rolling utilities
"""
import random
import re
from typing import List, Tuple

class DiceRoller:
    """Utility class for rolling dice"""
    
    @staticmethod
    def roll_die(sides: int) -> int:
        """Roll a single die with specified number of sides"""
        return random.randint(1, sides)
    
    @staticmethod
    def roll_dice(count: int, sides: int, modifier: int = 0) -> Tuple[int, List[int]]:
        """
        Roll multiple dice and return total and individual rolls
        
        Args:
            count: Number of dice to roll
            sides: Number of sides on each die
            modifier: Modifier to add to total
            
        Returns:
            Tuple of (total, individual_rolls)
        """
        rolls = [DiceRoller.roll_die(sides) for _ in range(count)]
        total = sum(rolls) + modifier
        return total, rolls
    
    @staticmethod
    def parse_dice_string(dice_string: str) -> Tuple[int, List[int]]:
        """
        Parse dice notation string (e.g., "2d6+3") and roll
        
        Args:
            dice_string: String in format "XdY+Z" or "XdY-Z"
            
        Returns:
            Tuple of (total, individual_rolls)
        """
        # Match patterns like "2d6+3", "1d20", "1d8-1"
        pattern = r'(\d+)d(\d+)([+-]\d+)?'
        match = re.match(pattern, dice_string.strip())
        
        if not match:
            raise ValueError(f"Invalid dice string: {dice_string}")
        
        count = int(match.group(1))
        sides = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0
        
        return DiceRoller.roll_dice(count, sides, modifier)
    
    @staticmethod
    def ability_score_roll() -> int:
        """Roll ability scores using 4d6 drop lowest method"""
        rolls = [DiceRoller.roll_die(6) for _ in range(4)]
        rolls.sort(reverse=True)
        return sum(rolls[:3])  # Take the 3 highest
    
    @staticmethod
    def generate_ability_scores() -> List[int]:
        """Generate a full set of ability scores"""
        return [DiceRoller.ability_score_roll() for _ in range(6)]