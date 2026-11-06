# Contributing to Plan Subdivider

Thank you for your interest in contributing to Plan Subdivider! This document provides guidelines for contributing to the project.

---

## 📋 Development Workflow

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR-USERNAME/plan-subdivider.git
cd plan-subdivider
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 3. Make Changes

- Write clear, concise code
- Follow existing code style
- Add tests if applicable
- Update documentation as needed

### 4. Update CHANGELOG

**⚠️ IMPORTANT**: Always update `CHANGELOG.md` when making changes!

Add your changes under the `[Unreleased]` section:

```markdown
## [Unreleased]

### Added
- New feature description

### Changed
- Modified behavior description

### Fixed
- Bug fix description
```

**Categories**:
- `Added`: New features
- `Changed`: Changes to existing functionality
- `Deprecated`: Soon-to-be removed features
- `Removed`: Removed features
- `Fixed`: Bug fixes
- `Security`: Security improvements

### 5. Commit Changes

```bash
git add .
git commit -m "feat: Add new feature

Detailed description of changes.

Co-Authored-By: Your Name <your.email@example.com>"
```

**Commit Message Format**:
```
<type>: <subject>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

---

## 📝 CHANGELOG Management

### Why We Maintain CHANGELOG

CHANGELOG.md helps users understand:
- What changed between versions
- Whether they need to update
- What new features are available
- What bugs were fixed

### When to Update CHANGELOG

**Always update CHANGELOG.md when you**:
- ✅ Add a new feature
- ✅ Fix a bug
- ✅ Change existing behavior
- ✅ Remove a feature
- ✅ Update documentation (major changes only)

**Don't update CHANGELOG for**:
- ❌ Typo fixes
- ❌ Code style changes
- ❌ Internal refactoring (unless it affects users)

### CHANGELOG Format

Follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Feature description [#PR_NUMBER](link)

### Fixed
- Bug fix description [#PR_NUMBER](link)

## [1.0.0] - 2026-02-09

### Added
- Initial release
- Automatic plan subdivision
- Task navigation
- Pre-work workflow
```

### Release Process

When releasing a new version:

1. **Update version** in `plugin.json` and `marketplace.json`
2. **Move Unreleased to version** in CHANGELOG.md:
   ```markdown
   ## [1.1.0] - 2026-02-15

   ### Added
   - New feature from unreleased
   ```
3. **Create release tag**:
   ```bash
   git tag -a v1.1.0 -m "Release v1.1.0"
   git push origin v1.1.0
   ```
4. **Create GitHub Release** with CHANGELOG excerpt

---

## 🧪 Testing

### Manual Testing

Test your changes locally:

```bash
# In Claude Code, use --plugin-dir to load from local directory
claude --plugin-dir /path/to/your/plan-subdivider

# Or reinstall from your fork's marketplace
/plugin marketplace add YOUR-USERNAME/plan-subdivider
/plugin install plan-subdivider@sanghyun-skills

# Verify
/plugin list
/subdivide
```

### Test Checklist

Before submitting PR:
- [ ] Plugin installs successfully
- [ ] `/subdivide` command works
- [ ] Rules are installed correctly
- [ ] No errors in Claude Code debug mode
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated

---

## 📚 Documentation

### README Updates

Update README.md if you:
- Add new features
- Change installation process
- Add new configuration options
- Change usage examples

Update both:
- `README.md` (English)
- `README.ko.md` (Korean)

### Code Comments

Add comments for:
- Complex logic
- Non-obvious decisions
- Public APIs
- Configuration options

---

## 🎨 Code Style

### File Structure

```
plan-subdivider/
├── .claude-plugin/       # Plugin metadata only
├── rules/                # At root level
├── skills/               # At root level
└── scripts/              # At root level
```

### Naming Conventions

- **Files**: kebab-case (`my-feature.md`)
- **Directories**: kebab-case (`my-plugin/`)
- **Variables**: camelCase (in scripts)

---

## 🐛 Bug Reports

### Before Reporting

1. Search existing issues
2. Update to latest version
3. Check CHANGELOG for known issues

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- Claude Code version:
- OS:
- Plugin version:
```

---

## 💡 Feature Requests

### Feature Request Template

```markdown
**Problem**
What problem does this solve?

**Proposed Solution**
How should it work?

**Alternatives**
Other solutions considered

**Additional Context**
Screenshots, examples, etc.
```

---

## 📞 Questions?

- **GitHub Issues**: Technical questions
- **GitHub Discussions**: General discussion
- **Email**: ppkimsanh@gmail.com

---

## 🙏 Recognition

Contributors will be:
- Listed in release notes
- Mentioned in CHANGELOG.md
- Added to GitHub contributors list

Thank you for contributing! 🎉
