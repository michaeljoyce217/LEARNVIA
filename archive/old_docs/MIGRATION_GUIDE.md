# LEARNVIA Migration Guide

## 🚨 IMPORTANT: Files to Delete Immediately

These files are obsolete and should be deleted to avoid confusion:

```bash
# Delete obsolete archive (2.7 MB of old code)
rm -rf archive/_system

# Delete backup files
rm Testing/run_review_BACKUP_before_fixes.py

# Delete test HTML files
rm Testing/test_*.html

# Delete duplicate module
rm Testing/Module_5_6_Exemplary/module_5_6_exemplary.xml

# Delete empty test folder
rm -rf Testing/Module_5_7_Exemplary

# Delete deprecated prompt
rm config/prompts/claude_live_reviewer_system_v2.xml
```

## 📁 New Folder Structure

### Before (Messy)
```
LEARNVIA/
├── archive/              # 2.7 MB obsolete
├── Testing/              # Mixed active/backup
├── config/               # Good
├── docs/                 # Good
├── exemplary_modules/    # Good but wrong location
└── guides/               # Redundant with docs
```

### After (Organized)
```
LEARNVIA/
├── src/                  # All source code
├── config/               # All configuration
├── modules/              # All module content
├── docs/                 # All documentation
├── tests/                # All tests
├── output/               # All generated reports
└── _deprecated/          # Archive (can delete later)
```

## 🔧 Code Refactoring Plan

### Current: Monolithic (2,641 lines)
```python
# Testing/run_review.py
- Everything in one file
- 1,000+ lines of HTML strings
- Global state
- No tests
```

### Target: Modular Architecture
```python
# src/main.py (300 lines)
from core import ConfigLoader, XMLParser, ConsensusAggregator
from detectors import AuthoringDetector, StyleDetector
from reports import HTMLReporter

# src/core/ (utilities)
# src/detectors/ (pattern detection)
# src/reports/ (report generation)
```

## 🚀 Migration Steps

### Step 1: Clean Up (5 minutes)
```bash
# Run the delete commands above
# Move deprecated files
mkdir -p _deprecated
mv archive _deprecated/
mv Testing/*BACKUP* _deprecated/
mv Testing/test_*.html _deprecated/
```

### Step 2: Reorganize Modules (5 minutes)
```bash
# Create new structure
mkdir -p modules/{exemplary,test}

# Move exemplary modules
cp -r exemplary_modules/* modules/exemplary/

# Move test modules
cp -r Testing/Power_Series modules/test/
cp -r Testing/Fund_Thm_of_Calculus modules/test/
```

### Step 3: Update Paths in Code (10 minutes)

Change in `Testing/run_review.py`:

```python
# Line 37-41
# FROM:
LEARNVIA_PATH = Path("/Users/michaeljoyce/Desktop/LEARNVIA")

# TO:
LEARNVIA_PATH = Path(__file__).parent.parent
# OR use environment variable:
import os
LEARNVIA_PATH = Path(os.environ.get("LEARNVIA_PATH", Path.cwd()))
```

### Step 4: Test Everything Still Works
```bash
cd Testing
python run_review.py Power_Series power_series_original.xml
# Should generate report successfully
```

## 📊 Size Impact

### Before
- Total: 7.1 MB
- Obsolete: 2.7 MB (38%)
- Active: 4.4 MB

### After Cleanup
- Total: 4.4 MB
- All active code
- 38% reduction in size

## ⚠️ Breaking Changes

### For Scripts
- Paths to exemplary modules changed
- Archive folder moved to _deprecated

### For Documentation
- Guides merged into docs/guides
- Architecture docs in docs/architecture

## ✅ Validation Checklist

After migration, verify:
- [ ] run_review.py still executes
- [ ] Reports generate correctly
- [ ] LaTeX renders in HTML
- [ ] All 30 agents run
- [ ] Consensus calculation works
- [ ] No hardcoded paths break

## 🔮 Future Improvements

1. **Immediate** (This week)
   - Split run_review.py into modules
   - Add basic unit tests
   - Fix hardcoded paths

2. **Short-term** (This month)
   - Add HTML templates
   - Create test suite
   - Add CI/CD pipeline

3. **Long-term** (Next quarter)
   - Plugin architecture
   - Custom rule system
   - Performance optimization
   - Support for other subjects

## 📝 Notes

- The current system works but is hard to maintain
- Refactoring will make it easier to add new features
- Tests are critical before major refactoring
- Keep CLAUDE_ONBOARDING.md updated with changes

---

**Remember:** The system is architecturally sound. We're just organizing it better for maintainability.