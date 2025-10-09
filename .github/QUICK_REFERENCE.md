# 🚀 BidNLP CI/CD Quick Reference

**One-page reference for common tasks**

---

## 📋 Setup (One-Time)

```bash
# 1. Push to GitHub
git add .
git commit -m "Add CI/CD pipeline"
git push

# 2. Enable GitHub Actions
# Go to Settings → Actions → Enable workflows

# 3. Set up PyPI Trusted Publishing
# Visit: https://pypi.org/manage/account/publishing/
# Add: Project=bidnlp, Owner=aghabidareh, Repo=bidnlp, Workflow=release.yml
```

---

## 🔄 Daily Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=bidnlp

# Format code
black bidnlp/ tests/
isort bidnlp/ tests/

# Lint
flake8 bidnlp/

# Type check
mypy bidnlp/
```

---

## 🎯 Pre-Commit Checklist

- [ ] All tests pass: `pytest tests/`
- [ ] Code formatted: `black . && isort .`
- [ ] No lint errors: `flake8 bidnlp/`
- [ ] Coverage maintained: `pytest --cov`
- [ ] Documentation updated
- [ ] CHANGELOG updated (for releases)

---

## 🚀 Releasing a New Version

```bash
# 1. Update version
# Edit pyproject.toml: version = "1.0.0"

# 2. Update CHANGELOG.md
# Add release notes under [Unreleased]

# 3. Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "Bump version to 1.0.0"
git push

# 4. Create tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 5. Wait for CI/CD (automatic)
# ✅ Tests run
# ✅ Package builds
# ✅ Publishes to PyPI
# ✅ Creates GitHub release
```

---

## 🐛 Troubleshooting

### Tests fail in CI
```bash
# Run with same Python version as CI
pyenv install 3.11
pyenv local 3.11
pytest tests/
```

### Coverage too low
```bash
# Generate HTML report
pytest tests/ --cov=bidnlp --cov-report=html
# Open htmlcov/index.html
```

### Import errors
```bash
# Ensure package installed
pip install -e .
# Or set PYTHONPATH
export PYTHONPATH=.
```

---

## 📊 Monitoring

### View CI Status
- **GitHub Actions**: `https://github.com/aghabidareh/bidnlp/actions`
- **CodeQL**: Settings → Security → Code scanning
- **Dependabot**: Pull Requests → Filter by `dependencies` label

### Check Coverage
- **Codecov**: `https://codecov.io/gh/aghabidareh/bidnlp`

### PyPI Stats
- **Package**: `https://pypi.org/project/bidnlp/`
- **Downloads**: `https://pepy.tech/project/bidnlp`

---

## 🔒 Security

```bash
# Check dependencies
safety check

# Scan code
bandit -r bidnlp/

# Check for secrets (before commit)
git diff --staged | grep -i 'password\|token\|secret\|api_key'
```

---

## 🤝 Contributing

```bash
# 1. Fork repo on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/bidnlp.git

# 3. Create branch
git checkout -b feature/amazing-feature

# 4. Make changes + tests

# 5. Run checks
pytest tests/
black . && isort .
flake8 bidnlp/

# 6. Commit
git commit -m "Add amazing feature"

# 7. Push
git push origin feature/amazing-feature

# 8. Create PR on GitHub
```

---

## 📝 Workflows Summary

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | Push, PR | Test, lint, security |
| `release.yml` | Tag `v*` | Publish to PyPI |
| `codeql.yml` | Push, Weekly | Security scan |
| `docs.yml` | Push, PR | Doc validation |

---

## 🎨 Badges

```markdown
[![CI](https://github.com/aghabidareh/bidnlp/actions/workflows/ci.yml/badge.svg)](https://github.com/aghabidareh/bidnlp/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/aghabidareh/bidnlp/branch/master/graph/badge.svg)](https://codecov.io/gh/aghabidareh/bidnlp)
[![PyPI version](https://badge.fury.io/py/bidnlp.svg)](https://badge.fury.io/py/bidnlp)
```

---

## 📞 Help & Resources

- **Setup Guide**: `.github/SETUP_GUIDE.md`
- **Contributing**: `CONTRIBUTING.md`
- **Security**: `SECURITY.md`
- **Changelog**: `CHANGELOG.md`
- **Summary**: `CICD_SETUP_SUMMARY.md`

---

## ⚡ Quick Commands

| Command | Purpose |
|---------|---------|
| `pytest tests/ -v` | Run tests verbose |
| `pytest tests/ -n auto` | Parallel tests |
| `pytest tests/ --cov` | With coverage |
| `black .` | Format all code |
| `isort .` | Sort imports |
| `flake8 bidnlp/` | Lint code |
| `mypy bidnlp/` | Type check |
| `safety check` | Security scan |
| `pip install -e ".[dev]"` | Install dev mode |

---

**Remember**: CI/CD runs automatically. Just push code and create tags! 🚀
