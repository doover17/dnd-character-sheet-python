# New Developer Onboarding Guide

## 👋 Welcome to the D&D Character Sheet Project!

This guide will get you up and running with our Python-based D&D Beyond clone. Follow these steps in order for a smooth onboarding experience.

---

## 🚀 Quick Start (5 minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/doover17/dnd-character-sheet-python.git
cd dnd-character-sheet-python
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Test the Application
```bash
# Run the working application
python main.py

# Run tests to verify setup
pytest
```

**✅ Success Check**: You should see the D&D character sheet GUI open with "N.O.V.A." character displayed.

---

## 📋 Project Overview

### What We're Building
A Python desktop application that replicates D&D Beyond's character sheet functionality using tkinter for the UI.

### Current Status
- ✅ Basic character information and ability scores working
- ✅ Modular architecture with clean separation of concerns
- ✅ Professional development workflow established
- 🟡 35 development tasks documented and ready for implementation
- 🔴 Core D&D features (combat stats, skills, spells) need implementation

### Tech Stack
- **Language**: Python 3.8+
- **UI**: tkinter (built-in)
- **Testing**: pytest
- **Data**: SQLite (planned)
- **Architecture**: Modular MVC pattern

---

## 📁 Project Structure

```
dnd-character-sheet-python/
├── src/
│   ├── models/          # Data models (Character, Spells, Equipment)
│   ├── ui/              # User interface components
│   ├── data/            # Data management and persistence
│   ├── utils/           # Utility functions (dice rolling, etc.)
│   └── config/          # Application configuration
├── tests/               # Test files (pytest)
├── docs/                # Project documentation
├── assets/              # Images, fonts, icons
├── main.py              # Application entry point
└── requirements.txt     # Python dependencies
```

---

## 🎯 Your First Task Options

Based on your experience level, choose your first task:

### 🟢 Beginner-Friendly Tasks
1. **TASK-BE-003**: Saving Throws Model (1-2 days)
   - Simple dataclass implementation
   - Basic D&D calculations
   - Good intro to the codebase

2. **TASK-UI-003**: Saving Throws Widget (1-2 days)
   - Follow existing UI patterns
   - Simple tkinter components
   - Visual display of saving throws

### 🟡 Intermediate Tasks
1. **TASK-BE-002**: Skills System Implementation (2-3 days)
   - All 18 D&D skills with calculations
   - Proficiency and expertise tracking
   - Integration with ability scores

2. **TASK-UI-002**: Skills System Interface (3-4 days)
   - Complete skills UI with checkboxes
   - Search/filter functionality
   - Clean, scrollable interface

### 🔴 Advanced Tasks
1. **TASK-BE-001**: Combat Stats Model Enhancement (2-3 days)
   - Complex combat calculations
   - HP management, AC calculation
   - Integration with equipment system

2. **TASK-SYS-001**: Data Persistence System (3-4 days)
   - SQLite database design
   - Character save/load functionality
   - Data migration system

---

## 📖 Essential Reading

**Before coding, please read these docs (in order):**

1. **`DEVELOPMENT_PLAN.md`** - Project overview and team structure
2. **`WORKFLOW_AND_SETUP.md`** - Development workflow and Git standards
3. **Your team's task file**:
   - Frontend: `FRONTEND_TASKS.md`
   - Backend: `BACKEND_TASKS.md`
   - Systems: `SYSTEMS_TASKS.md`
   - QA: `QA_TESTING_TASKS.md`
4. **`TASK_ASSIGNMENT_MATRIX.md`** - All tasks with dependencies

---

## 🛠 Development Workflow

### Branch Naming Convention
```bash
# Feature branches
git checkout -b feature/TASK-BE-003-saving-throws-model

# Bug fixes
git checkout -b bugfix/ability-modifier-calculation

# Documentation
git checkout -b docs/update-api-documentation
```

### Making Changes
1. **Create feature branch** from main
2. **Make small, focused commits** with clear messages
3. **Follow code style guidelines** (Black formatting, type hints)
4. **Add tests** for new functionality
5. **Update documentation** if needed
6. **Create pull request** when ready

### Code Quality Standards
```bash
# Format code
black src/

# Type checking
mypy src/

# Run tests
pytest

# Check coverage
pytest --cov=src --cov-report=term-missing
```

### Example Development Session
```bash
# 1. Start new feature
git checkout -b feature/TASK-BE-003-saving-throws-model

# 2. Make changes
# ... edit files ...

# 3. Test your changes
python main.py  # Test in GUI
pytest tests/models/test_saving_throws.py  # Run specific tests

# 4. Commit with clear message
git add -A
git commit -m "feat: implement saving throws model with proficiency tracking

- Add SavingThrows dataclass in src/models/character/saving_throws.py
- Implement modifier calculations for all 6 ability saves
- Add proficiency bonus integration
- Include unit tests with 90% coverage

Addresses: TASK-BE-003"

# 5. Push and create PR
git push origin feature/TASK-BE-003-saving-throws-model
# Create PR on GitHub
```

---

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/models/test_character.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test markers
pytest -m "not slow"  # Skip slow integration tests
```

### Writing Tests
Every new feature needs tests. Follow this pattern:
```python
# tests/models/test_saving_throws.py
import pytest
from src.models.character.saving_throws import SavingThrows
from src.models.character.base import AbilityType, AbilityScores

class TestSavingThrows:
    def test_saving_throw_calculation(self):
        """Test saving throw modifier calculation."""
        saving_throws = SavingThrows()
        saving_throws.proficiencies = [AbilityType.WISDOM]
        
        ability_scores = AbilityScores(wisdom=16)  # +3 modifier
        proficiency_bonus = 2
        
        # Proficient save: ability modifier + proficiency
        wisdom_save = saving_throws.get_saving_throw_modifier(
            AbilityType.WISDOM, ability_scores, proficiency_bonus
        )
        assert wisdom_save == 5  # 3 + 2
        
        # Non-proficient save: ability modifier only
        strength_save = saving_throws.get_saving_throw_modifier(
            AbilityType.STRENGTH, ability_scores, proficiency_bonus
        )
        assert strength_save == 0  # 10 strength = +0 modifier
```

---

## 🎮 D&D Rules Reference

### Key D&D 5e Concepts You'll Need

**Ability Scores**: 6 core stats (STR, DEX, CON, INT, WIS, CHA)
- Range: 1-30 (typically 8-18 for players)
- Modifier: `(score - 10) // 2`

**Proficiency Bonus**: Based on character level
- Level 1-4: +2
- Level 5-8: +3
- Level 9-12: +4
- Level 13-16: +5
- Level 17-20: +6

**Skills**: 18 skills, each tied to an ability score
- Examples: Athletics (STR), Stealth (DEX), Perception (WIS)
- Modifier: ability modifier + (proficiency bonus if proficient)

**Saving Throws**: One for each ability score
- Most classes get proficiency in 2 saving throws

### Reference Materials
- **Official**: D&D 5e Player's Handbook
- **Online**: D&D Beyond rules reference
- **SRD**: [System Reference Document](https://dnd.wizards.com/resources/systems-reference-document) (free)

---

## 💬 Communication

### Getting Help
1. **Check existing documentation** first
2. **Search GitHub issues** for similar problems
3. **Ask questions** in project discussions
4. **Tag relevant team members** for specific areas:
   - UI questions: @frontend-lead
   - D&D rules: @backend-lead
   - Architecture: @systems-lead
   - Testing: @qa-lead

### Daily Workflow
- **Morning**: Check GitHub notifications, review any new PRs
- **During development**: Commit frequently with clear messages
- **Before pushing**: Run tests and code quality checks
- **End of day**: Push work-in-progress to your feature branch

---

## 🚨 Common Issues & Solutions

### Environment Issues
```bash
# If virtual environment issues
python -m venv --clear venv
source venv/bin/activate
pip install -r requirements.txt

# If import issues
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Git Issues
```bash
# If you need to sync with main
git checkout main
git pull origin main
git checkout your-feature-branch
git rebase main

# If tests fail after pulling
pip install -r requirements.txt  # Update dependencies
pytest  # Run tests to see what's broken
```

### UI Issues
```bash
# If tkinter crashes or doesn't display
# On macOS, you might need:
brew install python-tk

# Test basic tkinter
python -c "import tkinter; tkinter.Tk().mainloop()"
```

---

## 🎯 Your Next Steps

### Day 1 (Today)
1. ✅ Complete environment setup
2. ✅ Run the application successfully  
3. ✅ Read this onboarding guide
4. 📋 Read `DEVELOPMENT_PLAN.md` and `WORKFLOW_AND_SETUP.md`
5. 🎯 Choose your first task from the options above

### Day 2-3
1. 📖 Read your team's specific task documentation
2. 🧑‍💻 Start working on your chosen task
3. 💬 Ask questions early and often
4. 🧪 Write tests for your implementation

### End of Week 1
1. 🔄 Complete your first task and create a PR
2. 📊 Review other team members' work
3. 🎉 Celebrate your first contribution!

---

## 📞 Emergency Contacts

**If you're completely stuck:**
- **Project Lead**: [Contact info TBD]
- **Senior Developer**: Check GitHub for most active contributors
- **GitHub Issues**: Create an issue with `question` label

**For urgent issues:**
- Create GitHub issue with `urgent` label
- Tag `@doover17` (project owner)

---

## 🎉 Welcome to the Team!

You're joining a well-organized project with clear documentation and professional standards. Take your time to understand the architecture, ask questions, and remember that everyone is here to help you succeed.

**The goal**: Build an amazing D&D character sheet that players will love to use!

**Remember**: 
- Quality over speed
- Ask questions early
- Test your code
- Document your work
- Have fun building something awesome!

---

**Ready to start? Pick a task and create your first feature branch!** 🚀