# Contributing to NFL Stats Dashboard

Thank you for your interest in contributing to the NFL Stats Dashboard! This document provides guidelines and information for contributors.

## 🏈 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork locally**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/nfL-stats-dashboard.git
   cd nfL-stats-dashboard
   ```

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install flake8 pytest  # Development dependencies
   ```

5. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Code Style Guidelines

### Python Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Maximum line length: 120 characters

### Linting

Before submitting, run the linter:
```bash
flake8 --max-line-length=120 --ignore=E501,W503 src/
```

### Testing

Run the test suite before submitting:
```bash
pytest tests/
```

## 🔄 Contribution Workflow

1. **Create an issue** first for major changes to discuss the approach
2. **Make your changes** in a feature branch
3. **Test your changes** locally
4. **Commit with clear messages**:
   ```bash
   git commit -m "Add feature: brief description"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request** against the main branch

## 📋 Pull Request Guidelines

### PR Title Format
- `feat: Add new feature description`
- `fix: Fix bug description`
- `docs: Update documentation`
- `refactor: Code refactoring description`
- `test: Add or update tests`

### PR Description Should Include
- Clear description of changes
- Related issue number (if applicable)
- Screenshots for UI changes
- Test results

## 🧪 Adding Tests

When adding new features:
1. Create test files in the `tests/` directory
2. Follow the naming convention `test_*.py`
3. Use pytest for writing tests
4. Aim for meaningful test coverage

## 📊 Data Processing Guidelines

When modifying data processors:
1. Ensure graceful error handling
2. Add appropriate logging
3. Test with sample/mock data
4. Be mindful of API rate limits when scraping

## 🐛 Reporting Bugs

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces

## 💡 Feature Requests

For feature requests, please:
- Check existing issues first
- Provide a clear use case
- Describe the expected behavior

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Your contributions help make this project better for the NFL analytics community!
