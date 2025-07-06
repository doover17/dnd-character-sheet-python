# Development Workflow and Setup Guide

## Project Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Code editor (VS Code recommended)
- tkinter (usually included with Python)

### Initial Setup
```bash
# Clone the repository
git clone <repository-url>
cd dnd_char_app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e .

# Run tests to verify setup
pytest

# Run the application
python main.py
```

### IDE Configuration

#### VS Code Recommended Extensions
- Python
- Python Docstring Generator
- GitLens
- Black Formatter
- mypy Type Checker

#### VS Code Settings (`.vscode/settings.json`)
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.mypyEnabled": true,
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "editor.formatOnSave": true,
    "files.trimTrailingWhitespace": true
}
```

---

## Git Workflow

### Branch Naming Convention
- **Feature branches**: `feature/TASK-XX-short-description`
- **Bug fixes**: `bugfix/issue-number-description`
- **Hotfixes**: `hotfix/critical-issue-description`
- **Documentation**: `docs/documentation-update`

Examples:
- `feature/TASK-UI-001-combat-stats-widget`
- `bugfix/ability-modifier-calculation`
- `docs/update-api-documentation`

### Development Process

1. **Start New Feature**
   ```bash
   # Create and switch to feature branch
   git checkout -b feature/TASK-UI-001-combat-stats-widget
   
   # Work on your feature
   # Make commits with clear messages
   ```

2. **Commit Guidelines**
   - Use clear, descriptive commit messages
   - Follow conventional commit format when possible
   - Keep commits focused and atomic
   
   ```bash
   # Good commit messages
   git commit -m "feat: add combat stats widget with HP and AC display"
   git commit -m "fix: correct ability modifier calculation for negative scores"
   git commit -m "test: add unit tests for CharacterVitals model"
   git commit -m "docs: update API documentation for spells module"
   ```

3. **Pre-commit Checks**
   ```bash
   # Run tests
   pytest
   
   # Check code formatting
   black --check src/
   
   # Run type checking
   mypy src/
   
   # Check test coverage
   pytest --cov=src --cov-report=term-missing
   ```

4. **Pull Request Process**
   ```bash
   # Push feature branch
   git push origin feature/TASK-UI-001-combat-stats-widget
   
   # Create pull request on GitHub
   # Fill out PR template
   # Request review from relevant team members
   ```

### Pull Request Template
```markdown
## Description
Brief description of changes made.

## Task Reference
- Task ID: TASK-UI-001
- Documentation: Link to task documentation

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] All tests pass

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Code is well documented
- [ ] Tests added for new functionality
- [ ] No breaking changes introduced
```

---

## Code Standards

### Python Style Guide
- Follow PEP 8 style guidelines
- Use Black for code formatting
- Maximum line length: 88 characters (Black default)
- Use type hints for all function parameters and return values
- Write docstrings for all classes and public methods

### Example Code Style
```python
"""
Module for character combat statistics.

This module contains classes and functions for managing
character combat-related statistics like HP, AC, and initiative.
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class CombatStats:
    """
    Character combat statistics.
    
    Attributes:
        hit_points: Current hit points
        max_hit_points: Maximum hit points
        armor_class: Armor class value
        initiative_modifier: Initiative bonus
    """
    hit_points: int
    max_hit_points: int
    armor_class: int
    initiative_modifier: int = 0
    
    def take_damage(self, damage: int) -> None:
        """
        Apply damage to character.
        
        Args:
            damage: Amount of damage to apply
            
        Raises:
            ValueError: If damage is negative
        """
        if damage < 0:
            raise ValueError("Damage cannot be negative")
        
        self.hit_points = max(0, self.hit_points - damage)
    
    def heal(self, healing: int) -> None:
        """
        Apply healing to character.
        
        Args:
            healing: Amount of healing to apply
        """
        if healing > 0:
            self.hit_points = min(self.max_hit_points, self.hit_points + healing)
```

### Documentation Standards
- All public classes and methods must have docstrings
- Use Google-style docstrings
- Include type information in docstrings
- Document parameters, return values, and exceptions
- Include usage examples for complex functions

---

## Testing Guidelines

### Test Organization
```
tests/
├── conftest.py              # Shared fixtures
├── models/                  # Model tests
│   ├── test_character.py
│   ├── test_spells.py
│   └── test_equipment.py
├── ui/                      # UI tests
│   ├── test_components.py
│   └── test_widgets.py
└── integration/             # Integration tests
    └── test_workflows.py
```

### Test Writing Standards
```python
import pytest
from src.models.character.base import Character


class TestCharacter:
    """Test class for Character model."""
    
    def test_character_creation(self):
        """Test character can be created with default values."""
        character = Character(name="Test Character")
        assert character.name == "Test Character"
        assert character.progression.level == 1
    
    @pytest.mark.parametrize("level,expected_bonus", [
        (1, 2), (5, 3), (9, 4), (13, 5), (17, 6), (20, 6)
    ])
    def test_proficiency_bonus_calculation(self, level: int, expected_bonus: int):
        """Test proficiency bonus calculation for different levels."""
        character = Character()
        character.progression.level = level
        assert character.progression.calculate_proficiency_bonus() == expected_bonus
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/models/test_character.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run with verbose output
pytest -v

# Run only fast tests (skip slow integration tests)
pytest -m "not slow"
```

---

## Team Communication

### Daily Standups
**Time**: 9:00 AM daily  
**Duration**: 15 minutes  
**Format**: 
- What did you work on yesterday?
- What will you work on today?
- Any blockers or questions?

### Weekly Planning
**Time**: Monday 10:00 AM  
**Duration**: 1 hour  
**Agenda**:
- Review completed tasks
- Plan tasks for the week
- Discuss any architecture decisions
- Address team questions

### Communication Channels
- **Slack/Teams**: Day-to-day communication
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Architecture and design discussions
- **Email**: Formal announcements

---

## Code Review Process

### Review Guidelines
1. **Automatic Checks**: All automated checks must pass
2. **Code Quality**: Review for readability, maintainability
3. **Architecture**: Ensure changes align with project architecture
4. **Testing**: Verify adequate test coverage
5. **Documentation**: Check for proper documentation

### Review Checklist
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Adequate test coverage for new code
- [ ] Documentation updated if needed
- [ ] No obvious security issues
- [ ] Performance considerations addressed
- [ ] Error handling implemented properly

### Reviewer Assignment
- **Frontend changes**: UI/UX lead reviews
- **Backend changes**: Backend architect reviews
- **System changes**: Systems architect reviews
- **All changes**: Senior developer final approval

---

## Release Process

### Version Numbering
Follow Semantic Versioning (SemVer):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Example: `1.2.3`

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number bumped
- [ ] Release notes prepared
- [ ] Security review completed
- [ ] Performance testing completed

### Deployment Steps
1. Create release branch: `release/v1.2.3`
2. Update version numbers
3. Run full test suite
4. Create release tag
5. Deploy to production
6. Monitor for issues

---

## Troubleshooting

### Common Issues

#### Virtual Environment Issues
```bash
# If venv activation fails
python -m venv --clear venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Import Issues
```bash
# If modules can't be imported
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
# Or add to your .bashrc/.zshrc
```

#### Test Failures
```bash
# If tests fail due to missing dependencies
pip install -e .
pip install -r requirements.txt

# If database tests fail
rm -f data/test.db
pytest tests/data/
```

### Getting Help
1. Check existing documentation
2. Search GitHub issues
3. Ask in team chat
4. Schedule pairing session
5. Escalate to senior developer

---

## Performance Guidelines

### Code Performance
- Profile code before optimizing
- Use appropriate data structures
- Avoid premature optimization
- Cache expensive calculations

### UI Performance
- Keep UI updates under 100ms
- Use lazy loading for large datasets
- Minimize database queries in UI thread
- Profile memory usage regularly

### Database Performance
- Use appropriate indexes
- Batch database operations
- Avoid N+1 query problems
- Monitor query execution time

---

## Security Considerations

### Input Validation
- Validate all user inputs
- Sanitize file paths
- Check data types and ranges
- Use parameterized queries

### Data Protection
- Don't log sensitive information
- Encrypt data at rest
- Use secure file permissions
- Validate plugin code execution

### Dependencies
- Keep dependencies updated
- Monitor security advisories
- Use dependency scanning tools
- Review third-party code changes