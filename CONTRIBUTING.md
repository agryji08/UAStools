# Contributing to UAStools

Thank you for your interest in contributing to UAStools! This document provides guidelines for contributing to both the R and Python packages.

## 🏗️ Repository Structure

This is a monorepo containing two packages:
- **r-package/** - R implementation
- **python-package/** - Python implementation

Both packages maintain feature parity, so changes to functionality should ideally be implemented in both versions.

## 🚀 Getting Started

### For R Package Development

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/UAStools.git
   cd UAStools/r-package
   ```

2. **Install development dependencies**
   ```r
   install.packages("devtools")
   install.packages("testthat")
   install.packages("roxygen2")
   ```

3. **Load the package**
   ```r
   devtools::load_all()
   ```

4. **Run tests**
   ```r
   devtools::test()
   ```

5. **Check package**
   ```r
   devtools::check()
   ```

### For Python Package Development

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/UAStools.git
   cd UAStools/python-package
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   pip install pytest pytest-cov black flake8
   ```

4. **Run tests**
   ```bash
   pytest tests/ -v
   ```

5. **Check code style**
   ```bash
   black uastools/
   flake8 uastools/
   ```

## 📝 Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-hexagonal-plots` - New features
- `fix/buffer-calculation` - Bug fixes
- `docs/update-readme` - Documentation
- `refactor/improve-rotation` - Code refactoring

### Commit Messages

Follow conventional commit format:
```
type(scope): brief description

Detailed explanation if needed

Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat(r): add support for hexagonal plot patterns`
- `fix(python): correct buffer calculation for metric units`
- `docs: update installation instructions`

## 🧪 Testing

### R Package Tests

- Add tests in `r-package/tests/testthat/`
- Use `testthat` framework
- Run with `devtools::test()`

### Python Package Tests

- Add tests in `python-package/tests/`
- Use `pytest` framework
- Aim for >80% code coverage
- Run with `pytest tests/ -v --cov=uastools`

## 📚 Documentation

### R Package Documentation

- Use roxygen2 comments in R source files
- Update documentation with `devtools::document()`
- Add examples to function documentation
- Update `NEWS.md` for user-facing changes

### Python Package Documentation

- Use docstrings (Google style) in Python source files
- Update `CHANGELOG.md` for user-facing changes
- Add examples to function docstrings
- Update `README.md` if needed

## 🔄 Pull Request Process

1. **Update your fork**
   ```bash
   git checkout main
   git pull upstream main
   ```

2. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write code
   - Add tests
   - Update documentation
   - Ensure all tests pass

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

### Pull Request Checklist

- [ ] Tests pass for affected package(s)
- [ ] Documentation updated
- [ ] CHANGELOG/NEWS updated
- [ ] Code follows style guidelines
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] Changes work in both R and Python (if applicable)

## 🎯 Feature Parity

When adding new features, consider implementing them in both packages to maintain feature parity. If a feature is language-specific, document why in the PR.

## 🐛 Reporting Bugs

Use GitHub Issues with the bug report template:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- System information (R/Python version, OS, package version)
- Minimal reproducible example

## 💡 Suggesting Features

Use GitHub Issues with the feature request template:
- Clear description of the feature
- Use case and motivation
- Proposed implementation (if any)
- Consider impact on both R and Python versions

## 📋 Code Style

### R Package
- Follow [tidyverse style guide](https://style.tidyverse.org/)
- Use `<-` for assignment
- Maximum line length: 80 characters
- Use roxygen2 for documentation

### Python Package
- Follow [PEP 8](https://pep8.org/)
- Use `black` for formatting
- Use `flake8` for linting
- Maximum line length: 100 characters
- Use type hints where appropriate
- Use Google-style docstrings

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Follow GitHub's community guidelines

## 📞 Questions?

If you have questions about contributing:
- Open a GitHub Discussion
- Email: zji7@unl.edu or andersst@tamu.edu
- Check existing Issues and PRs

## 🏆 Contributors

Thank you to all contributors! Your contributions are greatly appreciated.

---

## Quick Links

- [Main README](README.md)
- [R Package README](r-package/README.md)
- [Python Package README](python-package/README.md)
- [License](LICENSE)
