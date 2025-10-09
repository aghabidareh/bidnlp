# GitHub Actions CI/CD Setup Guide

This guide explains the CI/CD pipeline configuration for BidNLP and how to set it up.

## 📋 Overview

BidNLP uses a comprehensive GitHub Actions workflow that includes:

1. **Continuous Integration (CI)** - Automated testing, linting, and security checks
2. **Release Automation** - Automated PyPI publishing and GitHub releases
3. **Code Quality** - Security scanning with CodeQL
4. **Documentation** - Link checking and validation

## 🔧 Workflows

### 1. CI Workflow (`.github/workflows/ci.yml`)

**Triggers**: Push to master/main/develop, Pull Requests

**Jobs**:

#### Test Job
- Runs on: Ubuntu, macOS, Windows
- Python versions: 3.7, 3.8, 3.9, 3.10, 3.11, 3.12
- Actions:
  - Install dependencies
  - Run tests with pytest
  - Generate coverage reports
  - Upload coverage to Codecov (Ubuntu + Python 3.11 only)

#### Lint Job
- Code formatting check with Black
- Import sorting check with isort
- Linting with flake8
- Type checking with mypy
- All checks run with `continue-on-error: true` to not block PRs

#### Security Job
- Dependency vulnerability scanning with Safety
- Code security analysis with Bandit

#### Build Job
- Builds distribution packages (wheel and source)
- Validates package with twine
- Uploads artifacts

### 2. Release Workflow (`.github/workflows/release.yml`)

**Triggers**: Push tags matching `v*.*.*` (e.g., v1.0.0)

**Jobs**:

#### Test Job
- Runs full test suite before releasing

#### Build Job
- Builds distribution packages
- Validates packages

#### Publish to PyPI
- Uses trusted publishing (no API tokens needed!)
- Publishes to PyPI automatically

#### Create GitHub Release
- Generates changelog
- Creates GitHub release
- Attaches distribution files

### 3. CodeQL Workflow (`.github/workflows/codeql.yml`)

**Triggers**: Push to master/main/develop, PRs, Weekly schedule

**Actions**:
- Advanced security scanning
- Detects security vulnerabilities
- Analyzes code quality issues

### 4. Documentation Workflow (`.github/workflows/docs.yml`)

**Triggers**: Push to master/main, PRs

**Actions**:
- Checks documentation links
- Validates example files
- Ensures documentation quality

## 🚀 Setup Instructions

### Step 1: Enable GitHub Actions

1. Go to your repository settings
2. Navigate to **Actions** → **General**
3. Ensure "Allow all actions and reusable workflows" is selected

### Step 2: Set Up PyPI Publishing (Trusted Publishing)

**This is the modern, secure way - no API tokens needed!**

1. Go to [PyPI](https://pypi.org/) and log in
2. Create the project (if it doesn't exist):
   - Navigate to "Your projects" → "Publishing" → "Add a new pending publisher"
   - Or go to: https://pypi.org/manage/account/publishing/

3. Fill in the form:
   - **PyPI Project Name**: `bidnlp`
   - **Owner**: `aghabidareh` (your GitHub username)
   - **Repository name**: `bidnlp`
   - **Workflow name**: `release.yml`
   - **Environment name**: `pypi` (must match the environment in release.yml)

4. Click "Add"

**Note**: You can also use traditional API tokens if preferred - see "Alternative: API Token Method" below.

### Step 3: Set Up Codecov (Optional but Recommended)

1. Go to [Codecov](https://codecov.io/)
2. Sign in with GitHub
3. Add your repository
4. Copy the upload token (if needed)
5. Add as repository secret:
   - Name: `CODECOV_TOKEN`
   - Value: Your token

**Note**: For public repositories, the token is optional.

### Step 4: Configure Dependabot

Dependabot is already configured via `.github/dependabot.yml`. It will:
- Check for dependency updates weekly
- Create PRs for Python packages
- Update GitHub Actions versions

To enable:
1. Go to repository **Settings** → **Security** → **Dependabot**
2. Enable "Dependabot alerts"
3. Enable "Dependabot security updates"
4. Enable "Dependabot version updates"

### Step 5: Enable CodeQL

1. Go to repository **Settings** → **Security** → **Code scanning**
2. Click "Set up code scanning"
3. Select "CodeQL Analysis"
4. The workflow file is already created, so just enable it

## 📦 Creating a Release

### Method 1: Git Tags (Recommended)

```bash
# Ensure you're on master/main
git checkout master
git pull

# Update version in pyproject.toml
# Update CHANGELOG.md

# Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "Bump version to 1.0.0"
git push

# Create and push tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

The release workflow will automatically:
1. Run tests
2. Build packages
3. Publish to PyPI
4. Create GitHub release

### Method 2: Manual Workflow Dispatch

1. Go to **Actions** → **Release**
2. Click "Run workflow"
3. Enter the version (e.g., v1.0.0)
4. Click "Run workflow"

## 🛡️ Security Features

### Automated Security Scanning

- **Bandit**: Scans for common security issues in Python code
- **Safety**: Checks dependencies for known vulnerabilities
- **CodeQL**: Advanced semantic code analysis
- **Dependabot**: Automated dependency updates

### Secrets Management

Required secrets (add in repository Settings → Secrets):

1. **CODECOV_TOKEN** (optional for public repos)
   - Coverage reporting token

No PyPI token needed if using trusted publishing!

### Alternative: API Token Method

If you prefer using API tokens instead of trusted publishing:

1. Generate PyPI API token:
   - Go to PyPI Account Settings
   - Create new API token for the project
   - Copy the token (starts with `pypi-`)

2. Add as repository secret:
   - Name: `PYPI_API_TOKEN`
   - Value: Your token

3. Update `.github/workflows/release.yml`:
   ```yaml
   - name: Publish to PyPI
     env:
       TWINE_USERNAME: __token__
       TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
     run: twine upload dist/*
   ```

## ✅ Testing the Workflows

### Test CI Workflow

```bash
# Create a test branch
git checkout -b test-ci

# Make a small change
echo "# Test" >> README.md

# Commit and push
git add README.md
git commit -m "Test CI"
git push origin test-ci

# Create PR and watch workflows run
```

### Test Release Workflow (Dry Run)

Use TestPyPI for testing:

1. Create TestPyPI account
2. Set up trusted publishing for TestPyPI
3. Create a test tag:
   ```bash
   git tag -a v0.0.1-test -m "Test release"
   git push origin v0.0.1-test
   ```

## 📊 Monitoring

### View Workflow Runs
- Go to repository **Actions** tab
- Click on any workflow to see details
- View logs for debugging

### Badges

Add these badges to README (already done):
```markdown
[![CI](https://github.com/aghabidareh/bidnlp/actions/workflows/ci.yml/badge.svg)](https://github.com/aghabidareh/bidnlp/actions/workflows/ci.yml)
[![CodeQL](https://github.com/aghabidareh/bidnlp/actions/workflows/codeql.yml/badge.svg)](https://github.com/aghabidareh/bidnlp/actions/workflows/codeql.yml)
[![codecov](https://codecov.io/gh/aghabidareh/bidnlp/branch/master/graph/badge.svg)](https://codecov.io/gh/aghabidareh/bidnlp)
```

## 🔧 Troubleshooting

### Common Issues

**1. Tests fail in CI but pass locally**
- Check Python version differences
- Ensure all dependencies are in pyproject.toml
- Check for environment-specific issues

**2. PyPI publishing fails**
- Verify trusted publishing is set up correctly
- Check project name matches exactly
- Ensure version hasn't been published before

**3. Coverage upload fails**
- Check CODECOV_TOKEN is set (if private repo)
- Ensure coverage.xml is generated
- Check Codecov is enabled for the repo

**4. CodeQL fails**
- Check for syntax errors in code
- Review CodeQL logs for specific issues
- May need to exclude certain files

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Trusted Publishing Guide](https://docs.pypi.org/trusted-publishers/)
- [Codecov Documentation](https://docs.codecov.com/)
- [CodeQL Documentation](https://codeql.github.com/docs/)

## 🎯 Best Practices

1. **Never commit secrets** - Use GitHub Secrets
2. **Test before releasing** - Always run CI checks
3. **Use semantic versioning** - Follow semver.org
4. **Write good commit messages** - Clear and descriptive
5. **Update CHANGELOG** - Document all changes
6. **Review dependencies** - Keep them updated
7. **Monitor workflows** - Check for failures regularly

---

**Need help?** Open an issue or check the GitHub Actions documentation.
