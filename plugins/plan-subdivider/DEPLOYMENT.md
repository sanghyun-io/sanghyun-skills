# Deployment Guide

This guide explains how to deploy the Plan Subdivider Plugin to GitHub and make it available via Claude Code Marketplace.

## 📦 Plugin Structure (Complete)

```
plan-subdivider/
├── .claude-plugin/
│   ├── plugin.json           ✅ Plugin metadata
│   └── marketplace.json      ✅ Marketplace configuration
├── .gitignore                ✅ Git ignore rules
├── README.md                 ✅ Installation & usage guide
├── CHANGELOG.md              ✅ Version history
├── LICENSE                   ✅ MIT License
├── DEPLOYMENT.md             ✅ This file
├── hooks/
│   └── hooks.json            ✅ Post-install automation
├── scripts/
│   └── install-rules.sh      ✅ Rule installation script
├── rules/
│   ├── plan-structure.md     ✅ Main plan structure rules
│   └── rule-format.md        ✅ Rule format standard
├── skills/
│   └── plan-subdivide/
│       └── SKILL.md          ✅ Subdivision skill
└── examples/
    └── sample-plan.md        ✅ Example plan file
```

## 🚀 Deployment Steps

### 1. Create GitHub Repository

```bash
cd C:/Users/QESG/Desktop/plan-subdivider

# Initialize git repository
git init

# Add all files
git add .

# First commit
git commit -m "Initial release: Plan Subdivider Plugin v1.0.0

- Automatic plan subdivision with /subdivide skill
- Rule files for structured planning
- Pre-work workflow integration
- Task navigation and verification
- AskUserQuestion pattern for confirmations
"

# Create repository on GitHub (via web or gh CLI)
# Option A: Using gh CLI
gh repo create plan-subdivider --public --source=. --remote=origin

# Option B: Manual
# 1. Go to https://github.com/new
# 2. Create repository named "plan-subdivider"
# 3. Add remote:
git remote add origin https://github.com/sanghyun-io/sanghyun-skills.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 2. Create Release

```bash
# Tag version 1.0.0
git tag -a v1.0.0 -m "Version 1.0.0

First stable release of Plan Subdivider Plugin.

Features:
- Automatic plan subdivision
- Structured task files with checklists
- Pre-work workflow
- Rule-based formatting
- AskUserQuestion integration
"

# Push tag
git push origin v1.0.0

# Create GitHub release (via gh CLI)
gh release create v1.0.0 \
  --title "Plan Subdivider Plugin v1.0.0" \
  --notes-file CHANGELOG.md

# Or create release manually at:
# https://github.com/sanghyun-io/sanghyun-skills/releases/new
```

### 3. Update Plugin Configuration

Before deploying, update these files with your actual GitHub information:

#### `.claude-plugin/plugin.json`
```json
{
  "homepage": "https://github.com/sanghyun-io/sanghyun-skills",
  "repository": "https://github.com/sanghyun-io/sanghyun-skills"
}
```

#### `.claude-plugin/marketplace.json`
```json
{
  "name": "plan-subdivider",
  "owner": {
    "name": "sanghyun-io",
    "email": "ppkimsanh@gmail.com"
  },
  "plugins": [{
    "name": "plan-subdivider",
    "source": "./",
    "description": "Automatically breaks down large plans into manageable, sequential tasks",
    "category": "productivity",
    "tags": ["planning", "workflow", "task-management", "subdivision"]
  }]
}
```

#### `README.md`
Replace all instances of:
- `sanghyun-io` → Your GitHub username
- `ppkimsanh@gmail.com` → Your email

### 4. Test Installation Locally

Before publishing, test the plugin via marketplace:

```bash
# In Claude Code session:

# 1. Add marketplace
/plugin marketplace add sanghyun-io/sanghyun-skills

# 2. Install plugin
/plugin install plan-subdivider@sanghyun-skills

# 3. Verify installation
/plugin list
# Should show "plan-subdivider"

# 4. Test subdivision
/subdivide
```

### 5. Install from Marketplace

Users install with two commands:

```bash
# 1. Add marketplace (one-time)
/plugin marketplace add sanghyun-io/sanghyun-skills

# 2. Install the plugin
/plugin install plan-subdivider@sanghyun-skills
```

Or via the UI:

1. Run `/plugin`
2. Go to **Marketplaces** tab → **Add Marketplace**
3. Enter: `https://github.com/sanghyun-io/sanghyun-skills.git`
4. Then install `plan-subdivider` from the plugin list

## 🧪 Testing Checklist

Before publishing, verify:

- [ ] All files are present (check structure above)
- [ ] GitHub URLs updated in all files
- [ ] Plugin installs successfully locally
- [ ] Rules are auto-installed to `.claude/rules/`
- [ ] `/subdivide` skill works correctly
- [ ] AskUserQuestion prompts appear
- [ ] Example plan can be subdivided
- [ ] README documentation is clear
- [ ] License is correct

## 📣 Promotion

After deployment, share your plugin:

### Claude Code Community
- Post in Claude Code Discord/Slack
- Share on relevant forums

### Documentation
- Update your project's documentation
- Add usage examples
- Create tutorial videos (optional)

### Social Media
```markdown
🚀 Just released Plan Subdivider Plugin for Claude Code!

✅ Auto-subdivide complex plans
✅ Structured task checklists
✅ Sequential navigation
✅ Built-in verification

Install: /plugin marketplace add sanghyun-io/sanghyun-skills && /plugin install plan-subdivider@sanghyun-skills

#ClaudeCode #ProductivityTools
```

## 🔄 Future Updates

When releasing new versions:

```bash
# Update version in plugin.json and marketplace.json
# Update CHANGELOG.md
# Commit changes
git add .
git commit -m "Release v1.1.0: [describe changes]"

# Tag new version
git tag -a v1.1.0 -m "Version 1.1.0"
git push origin main
git push origin v1.1.0

# Create GitHub release
gh release create v1.1.0 --title "v1.1.0" --notes-file CHANGELOG.md
```

## 📞 Support

- **Issues**: https://github.com/sanghyun-io/sanghyun-skills/issues
- **Discussions**: https://github.com/sanghyun-io/sanghyun-skills/discussions
- **Email**: ppkimsanh@gmail.com

---

**Happy deploying! 🎉**
