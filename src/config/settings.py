"""
Application settings and configuration
"""
import os
from pathlib import Path

# Application metadata
APP_NAME = "D&D Character Sheet"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Nova DND Dashboard"

# File paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ASSETS_DIR = PROJECT_ROOT / "assets"
CONFIG_DIR = PROJECT_ROOT / "config"

# Database settings
DATABASE_PATH = DATA_DIR / "characters.db"

# UI settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# Styling
FONT_FAMILY = "Arial"
FONT_SIZE_NORMAL = 10
FONT_SIZE_HEADER = 12
FONT_SIZE_LARGE = 16
FONT_SIZE_TITLE = 20

# Colors (based on D&D Beyond theme)
COLOR_PRIMARY = "#242527"
COLOR_SECONDARY = "#6c757d"
COLOR_SUCCESS = "#28a745"
COLOR_INFO = "#17a2b8"
COLOR_WARNING = "#ffc107"
COLOR_DANGER = "#dc3545"
COLOR_LIGHT = "#f8f9fa"
COLOR_DARK = "#343a40"
COLOR_WHITE = "#ffffff"
COLOR_BORDER = "#dee2e6"

# D&D Rules
MAX_LEVEL = 20
ABILITY_SCORE_MIN = 1
ABILITY_SCORE_MAX = 30
ABILITY_SCORE_DEFAULT = 10

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)