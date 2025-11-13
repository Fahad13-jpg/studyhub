# Contributing to StudyHub

First off, thank you for considering contributing to StudyHub! It's people like you that make StudyHub such a great tool for students worldwide.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [contact@studyhub.com](mailto:mohmmadfahad53408@gmail.com).

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots if possible**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and explain the behavior you expected to see**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python/Django style guides
* Include screenshots in your pull request when appropriate
* End all files with a newline
* Write meaningful commit messages

## Development Process

### 1. Fork the Repository

Fork the project on GitHub and clone your fork locally:

```bash
git clone https://github.com/Fahad13-jpg/studyhub.git
cd studyhub
git remote add upstream https://github.com/Fahad13-jpg/studyhub.git
```

### 2. Create a Branch

Create a branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Urgent fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring

### 3. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Make Your Changes

* Write clean, readable code
* Follow PEP 8 style guide
* Add docstrings to functions and classes
* Write unit tests for new features
* Update documentation as needed

### 5. Test Your Changes

```bash
# Run tests
python manage.py test

# Check code style
flake8 .

# Format code
black .

# Run coverage
coverage run --source='.' manage.py test
coverage report
```

### 6. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting)
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

### 7. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 8. Create Pull Request

* Go to the original repository on GitHub
* Click "New Pull Request"
* Select your branch
* Fill in the PR template with details
* Link related issues
* Request review from maintainers

## Style Guides

### Python Style Guide

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use 4 spaces for indentation
* Maximum line length: 100 characters
* Use meaningful variable names
* Add docstrings to all functions

Example:
```python
def calculate_attendance_rate(session, group):
    """
    Calculate the attendance rate for a study session.
    
    Args:
        session (StudySession): The session to calculate rate for
        group (StudyGroup): The group the session belongs to
        
    Returns:
        float: Attendance rate as a percentage
    """
    total_members = group.members.count()
    attending = session.rsvps.filter(status='attending').count()
    return (attending / total_members) * 100 if total_members > 0 else 0
```

### Django Style Guide

* Use class-based views where appropriate
* Keep views thin, models fat
* Use Django's built-in features
* Follow Django's naming conventions
* Write migrations for model changes

### HTML/CSS Style Guide

* Use Bootstrap 5 classes
* Keep inline styles minimal
* Use semantic HTML
* Ensure accessibility (ARIA labels)
* Mobile-first responsive design

### JavaScript Style Guide

* Use ES6+ features
* Avoid jQuery when possible
* Use meaningful variable names
* Add comments for complex logic
* Handle errors gracefully

## Testing Guidelines

### Unit Tests

Write unit tests for all new features:

```python
from django.test import TestCase
from django.contrib.auth.models import User
from groups.models import StudyGroup

class StudyGroupTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_create_group(self):
        group = StudyGroup.objects.create(
            name='Test Group',
            course_code='CS101',
            creator=self.user,
            max_capacity=5
        )
        self.assertEqual(group.name, 'Test Group')
        self.assertEqual(group.current_member_count(), 0)
```

### Integration Tests

Test feature interactions:

```python
def test_join_group_workflow(self):
    # Create group
    # Join group
    # Verify membership
    # Check notifications
    pass
```

## Documentation

* Update README.md for major changes
* Add docstrings to new functions
* Update API documentation
* Include code examples
* Add screenshots for UI changes

## Questions?

Feel free to reach out:
* Open an issue for questions
* Email: mohmmadfahad53408@gmail.com
## Recognition

Contributors will be recognized in:
* README.md Contributors section
* Release notes
* Project website (coming soon)

Thank you for contributing to StudyHub! 🎓✨