# New Developer Onboarding Guide

## 👋 Welcome to the D&D Character Sheet Project

This guide will get you up and running with our Python-based D&D Beyond clone. You'll be working in the shared project directory, so follow these steps to get started.

---

## 🚀 Quick Start (2 minutes)

### 1. Navigate to Project Directory

```bash
cd /Users/davidhoover/Desktop/nova_dnd_dashboard/dnd_char_app
```

### 2. Activate Development Environment

```bash
# Activate the existing virtual environment
source venv/bin/activate

# Verify dependencies are installed
pip list | grep pytest
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

```markdown

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

## 🎯 Your First Task: TASK-UI-003

### Your initial assignment is TASK-UI-003: Saving Throws Widget

This is a beginner-friendly task that will get you familiar with the codebase:

### Task Details

- **Estimated Time**: 1-2 days
- **Difficulty**: Beginner-friendly
- **What You'll Build**: A UI widget displaying saving throws with proficiency tracking
- **Skills Learned**: tkinter widgets, following UI patterns, D&D mechanics

### Task Requirements

1. **Follow existing UI patterns** from `src/ui/components/ability_scores.py`
2. **Create saving throws widget** with all 6 ability-based saves
3. **Add proficiency checkboxes** for each saving throw
4. **Calculate and display modifiers** (ability modifier + proficiency bonus if applicable)
5. **Integrate with character model** to show real data

### Success Criteria

- [ ] Widget displays all 6 saving throws (STR, DEX, CON, INT, WIS, CHA)
- [ ] Proficiency checkboxes are functional
- [ ] Modifiers calculate correctly
- [ ] Widget integrates into main application
- [ ] Code follows project style guidelines

### Check-in Point

**Complete TASK-UI-003 and check in with the team lead before moving to additional tasks.**

---

## 📖 Essential Reading for TASK-UI-003

**Before starting your task, read these specific sections:**

1. **`FRONTEND_TASKS.md`** - Find TASK-UI-003 for detailed requirements
2. **`WORKFLOW_AND_SETUP.md`** - Git workflow and coding standards (sections on branch naming and code quality)
3. **Existing code pattern**: Study `src/ui/components/ability_scores.py` to understand the widget pattern

**Optional reading** (for broader context):

- `DEVELOPMENT_PLAN.md` - Project overview
- `TASK_ASSIGNMENT_MATRIX.md` - How your task fits into the bigger picture

---

## 🛠 Development Workflow

### Branch Naming Convention

```bash
# For your task (TASK-UI-003)
git checkout -b feature/TASK-UI-003-saving-throws-widget

# General pattern for future tasks
git checkout -b feature/TASK-XX-short-description
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

### Example Development Session for TASK-UI-003

```bash
# 1. Start new feature
git checkout -b feature/TASK-UI-003-saving-throws-widget

# 2. Create the widget file
# Create src/ui/components/saving_throws.py
# Follow the pattern from ability_scores.py

# 3. Test your changes frequently
python main.py  # Test in GUI - see your widget appear
pytest  # Run tests to make sure nothing broke

# 4. Commit when widget is working
git add -A
git commit -m "feat: implement saving throws widget with proficiency checkboxes

- Add SavingThrowsWidget in src/ui/components/saving_throws.py
- Display all 6 saving throws with ability-based modifiers
- Include proficiency checkboxes for each save
- Calculate modifiers correctly (ability + proficiency if applicable)
- Integrate widget into main application

Addresses: TASK-UI-003"

# 5. Push when complete and ready for review
git push origin feature/TASK-UI-003-saving-throws-widget
# Check in with team lead for review
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

### Testing for TASK-UI-003

For your saving throws widget, focus on testing that:

1. **The widget displays correctly** (all 6 saves shown)
2. **Checkboxes work** (can be checked/unchecked)
3. **Modifiers calculate correctly** (ability modifier + proficiency if checked)

**Note**: UI testing can be tricky with tkinter. For now, focus on manual testing:

```bash
# Run the app and verify:
python main.py

# Check that your widget:
# - Shows all 6 saving throws
# - Has working checkboxes
# - Displays correct modifiers
# - Updates when ability scores change
```

**Advanced testing** (optional): You can add widget tests later following the pattern in existing test files.

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

**Saving Throws**: One for each ability score (STR, DEX, CON, INT, WIS, CHA)

- Calculation: ability modifier + (proficiency bonus if proficient)
- Most classes get proficiency in 2 saving throws
- Examples: Fighters get STR and CON, Wizards get INT and WIS

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

### Today (Setup & Research)

1. ✅ Complete environment setup and test the app
2. ✅ Read this onboarding guide  
3. 📋 Read TASK-UI-003 details in `FRONTEND_TASKS.md`
4. 🔍 Study the existing pattern in `src/ui/components/ability_scores.py`
5. 🌿 Create your feature branch: `feature/TASK-UI-003-saving-throws-widget`

### Day 1-2 (Implementation)

1. 🧑‍💻 Implement the saving throws widget following the existing pattern
2. 🧪 Test frequently by running `python main.py`
3. 💬 Ask questions if you get stuck
4. ✅ Verify all success criteria are met

### Check-in Point 2

1. 🔄 Complete TASK-UI-003 implementation
2. 🚀 Push your feature branch
3. 👥 **Check in with team lead for review**
4. 🎉 Get approval before taking on additional tasks

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

## 🎉 Welcome to the Team

You're joining a well-organized project with clear documentation and professional standards. Take your time to understand the architecture, ask questions, and remember that everyone is here to help you succeed.

**The goal**: Build an amazing D&D character sheet that players will love to use!

**Remember**:

- Quality over speed
- Ask questions early
- Test your code
- Document your work
- Have fun building something awesome!

---

**Ready to start? Begin with TASK-UI-003 and we'll see you at the check-in point!** 🚀

## 📝 Quick Reference for TASK-UI-003

**What to create**: `src/ui/components/saving_throws.py`
**Pattern to follow**: `src/ui/components/ability_scores.py`
**Integration point**: Add widget to `main.py` in the left sidebar
**Branch name**: `feature/TASK-UI-003-saving-throws-widget`

**Key requirements**:

- Display all 6 saving throws (STR, DEX, CON, INT, WIS, CHA)
- Add checkboxes for proficiency selection
- Calculate modifiers: ability modifier + (proficiency bonus if checked)
- Follow existing UI styling and layout patterns
