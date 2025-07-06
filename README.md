# D&D Character Sheet - Python Clone

A Python-based D&D Beyond character sheet clone built with tkinter.

## Features

- **Character Management**: Create and manage D&D 5e characters
- **Ability Scores**: Track and calculate ability scores and modifiers
- **Combat Stats**: Manage HP, AC, and other combat statistics
- **Equipment**: Track weapons, armor, and other equipment
- **Spells**: Manage spell lists and spell slots
- **Clean UI**: Inspired by D&D Beyond's clean design

## Project Structure

```markdown

dnd_char_app/
├── src/
│   ├── models/          # Data models
│   │   ├── character/   # Character-related models
│   │   ├── spells/      # Spell models
│   │   └── equipment/   # Equipment models
│   ├── ui/              # User interface
│   │   ├── components/  # Reusable UI components
│   │   ├── views/       # Main application views
│   │   ├── dialogs/     # Dialog windows
│   │   └── widgets/     # Custom widgets
│   ├── data/            # Data management
│   │   ├── database/    # Database operations
│   │   ├── api/         # API integrations
│   │   └── loaders/     # Data loaders
│   ├── utils/           # Utility functions
│   └── config/          # Configuration
├── tests/               # Test files
├── docs/                # Documentation
├── assets/              # Images, fonts, icons
├── scripts/             # Build/deployment scripts
└── character_sheet_ui.py # Legacy UI (will be refactored)
```

## Installation

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:

```bash
python main.py
```

Or run the legacy UI:

```bash
python character_sheet_ui.py
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/
```

### Type Checking

```bash
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is for educational purposes and is not affiliated with D&D Beyond or Wizards of the Coast.
