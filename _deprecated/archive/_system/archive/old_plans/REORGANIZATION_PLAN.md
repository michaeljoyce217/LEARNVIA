# LEARNVIA Directory Reorganization Plan

**Current State:** 40 items in root directory - too cluttered
**Goal:** Clean, logical structure that's easy to navigate

---

## 📁 PROPOSED NEW STRUCTURE

```
/Users/michaeljoyce/Desktop/LEARNVIA/
│
├── README.md                          # Main project overview (KEEP IN ROOT)
├── requirements.txt                   # Python dependencies (KEEP IN ROOT)
│
├── 📂 src/                            # Core system code (ALREADY GOOD)
│   ├── __init__.py
│   ├── models.py
│   ├── orchestrator.py
│   ├── reviewers.py
│   ├── aggregator.py
│   ├── report_generator.py
│   ├── feedback_loop.py
│   ├── reviewer_feedback_loop.py
│   ├── claude_api.py
│   └── mock_api.py
│
├── 📂 tests/                          # Unit tests (ALREADY GOOD)
│   ├── test_models.py
│   ├── test_reviewers.py
│   ├── test_aggregator.py
│   └── test_report_generator.py
│
├── 📂 scripts/                        # Utility scripts (NEW - consolidate)
│   ├── run_tests.py                   # MOVE from root
│   ├── test_claude_workflow.py        # MOVE from root
│   ├── test_feedback_loop.py          # MOVE from root
│   ├── test_reviewer_feedback.py      # MOVE from root
│   ├── example_usage.py               # MOVE from root
│   ├── dispute_issue.py               # MOVE from root
│   ├── validate_disputes.py           # MOVE from root
│   └── log_missed_issues.py           # MOVE from root
│
├── 📂 config/                         # Configuration & guidelines (NEW)
│   ├── authoring_prompt_rules.txt     # MOVE from root
│   ├── style_prompt_rules.txt         # MOVE from root
│   └── product_vision_context.txt     # MOVE from root
│
├── 📂 docs/                           # All documentation (EXPAND EXISTING)
│   ├── 📂 reports/                    # Project reports
│   │   ├── POC_PHASE1_REPORT.md       # MOVE from root
│   │   ├── SYSTEM_REPORT.md           # MOVE from root
│   │   ├── SYSTEM_REPORT_READABLE.txt # MOVE from root
│   │   └── SESSION_COMPLETE_SUMMARY.md # MOVE from root
│   │
│   ├── 📂 summaries/                  # Executive summaries
│   │   ├── EXECUTIVE_SUMMARY.md       # MOVE from root
│   │   ├── EXECUTIVE_SUMMARY_EMAIL.txt # MOVE from root
│   │   └── QUICK_REFERENCE.md         # MOVE from root
│   │
│   ├── 📂 handoffs/                   # Session handoff prompts
│   │   ├── PHASE2_HANDOFF_PROMPT.md   # MOVE from root
│   │   └── PILOT_HANDOFF_PROMPT.md    # MOVE from root
│   │
│   └── 📂 team_review/                # Team review materials
│       ├── REPORT_ANALYSIS_FOR_TEAM_REVIEW.md # MOVE from root
│       ├── EXECUTIVE_SUMMARY_REPORT_REVIEW.md # MOVE from root
│       ├── PRESENTATION_SLIDES.md      # MOVE from root
│       └── TEAM_MEETING_TALKING_POINTS.md # MOVE from root
│
├── 📂 reports/                        # Generated HTML reports (ALREADY GOOD)
│   ├── demonstration_report_with_issues.html
│   └── final_report.html
│
├── 📂 feedback/                       # Feedback loop storage (ALREADY GOOD)
│   ├── disputes/
│   ├── validations/
│   ├── patterns/
│   ├── metrics/
│   └── missed_issues/
│
├── 📂 modules/                        # Test modules (RENAME from module_examples)
│   └── Module 3.4 Basic Rules of Finding Derivatives.txt
│
└── 📂 archive/                        # Old/unused files (NEW)
    ├── txt_guides/                    # MOVE entire dir (if not used)
    └── claude-test/                   # MOVE entire dir (if not used)
```

---

## 🎯 BENEFITS OF THIS STRUCTURE

### 1. Clear Separation of Concerns
- **src/** = Production code
- **tests/** = Test code
- **scripts/** = Utility/workflow scripts
- **config/** = Guidelines and rules
- **docs/** = All documentation organized by type
- **reports/** = Generated output
- **feedback/** = System learning data
- **modules/** = Test content

### 2. Easy Navigation
- New team members know where to find things
- Related files are grouped together
- Root directory is clean (only README + requirements)

### 3. Scalability
- Easy to add new docs without cluttering root
- Clear place for new scripts
- Documentation organized by purpose

---

## 📋 REORGANIZATION COMMANDS

Run these commands to reorganize:

```bash
# Navigate to project
cd /Users/michaeljoyce/Desktop/LEARNVIA

# Create new directories
mkdir -p scripts
mkdir -p config
mkdir -p docs/reports
mkdir -p docs/summaries
mkdir -p docs/handoffs
mkdir -p docs/team_review
mkdir -p archive

# Move scripts
mv run_tests.py scripts/
mv test_claude_workflow.py scripts/
mv test_feedback_loop.py scripts/
mv test_reviewer_feedback.py scripts/
mv example_usage.py scripts/
mv dispute_issue.py scripts/
mv validate_disputes.py scripts/
mv log_missed_issues.py scripts/

# Move config files
mv authoring_prompt_rules.txt config/
mv style_prompt_rules.txt config/
mv product_vision_context.txt config/

# Move documentation - reports
mv POC_PHASE1_REPORT.md docs/reports/
mv SYSTEM_REPORT.md docs/reports/
mv SYSTEM_REPORT_READABLE.txt docs/reports/
mv SESSION_COMPLETE_SUMMARY.md docs/reports/

# Move documentation - summaries
mv EXECUTIVE_SUMMARY.md docs/summaries/
mv EXECUTIVE_SUMMARY_EMAIL.txt docs/summaries/
mv QUICK_REFERENCE.md docs/summaries/

# Move documentation - handoffs
mv PHASE2_HANDOFF_PROMPT.md docs/handoffs/
mv PILOT_HANDOFF_PROMPT.md docs/handoffs/

# Move documentation - team review
mv REPORT_ANALYSIS_FOR_TEAM_REVIEW.md docs/team_review/
mv EXECUTIVE_SUMMARY_REPORT_REVIEW.md docs/team_review/
mv PRESENTATION_SLIDES.md docs/team_review/
mv TEAM_MEETING_TALKING_POINTS.md docs/team_review/

# Rename module_examples to modules (cleaner name)
mv module_examples modules

# Archive unused directories (if not needed)
mv txt_guides archive/ 2>/dev/null || true
mv claude-test archive/ 2>/dev/null || true

# Clean up empty docs folder if it exists
rmdir docs/plans 2>/dev/null || true

# Show new structure
echo "✅ Reorganization complete!"
echo ""
echo "New directory structure:"
echo ""
ls -d */ 2>/dev/null | sort
echo ""
echo "Root files:"
ls -1 *.md *.txt 2>/dev/null | sort
```

**Note:** The `tree` command isn't installed by default on macOS. The commands above use standard Unix utilities (`ls`, `sort`) that work everywhere. If you want a tree view, you can install tree with: `brew install tree`

---

## 🔄 UPDATED README PATHS

After reorganization, update README.md with new paths:

```markdown
# LEARNVIA AI Review System

## Quick Start

### Installation
pip install -r requirements.txt

### Run Tests
python scripts/run_tests.py

### Run Workflow Test
python scripts/test_claude_workflow.py

### Configuration
- Authoring Guidelines: `config/authoring_prompt_rules.txt`
- Style Guidelines: `config/style_prompt_rules.txt`

### Documentation
- Executive Summary: `docs/summaries/EXECUTIVE_SUMMARY.md`
- Quick Reference: `docs/summaries/QUICK_REFERENCE.md`
- System Report: `docs/reports/SYSTEM_REPORT.md`
- Team Review Materials: `docs/team_review/`
```

---

## ⚠️ IMPORTANT NOTES

### Files That Reference Other Files

After moving files, check these for broken paths:

1. **scripts/test_claude_workflow.py**
   - Update: `authoring_prompt_rules.txt` → `../config/authoring_prompt_rules.txt`
   - Update: `style_prompt_rules.txt` → `../config/style_prompt_rules.txt`
   - Update: Module path if needed

2. **src/claude_api.py**
   - Update guideline file paths in `_load_guidelines()`
   - Change to: `base_path / "config" / "authoring_prompt_rules.txt"`

3. **src/reviewers.py**
   - Check if it loads guidelines
   - Update paths if needed

4. **Any other scripts that reference files**

---

## 🚀 NEXT STEPS

### After Reorganization:

1. **Test Everything**
   ```bash
   python scripts/run_tests.py
   python scripts/test_claude_workflow.py
   ```

2. **Update Git**
   ```bash
   git add .
   git commit -m "Reorganize project structure for clarity"
   ```

3. **Update Documentation**
   - Update README.md with new paths
   - Update any handoff prompts with new structure
   - Update team review materials if needed

4. **Create .gitignore if not exists**
   ```
   # Python
   __pycache__/
   *.pyc
   .pytest_cache/

   # System
   .DS_Store
   .claude/

   # Generated
   reports/*.html
   feedback/disputes/*.json
   feedback/validations/*.json
   feedback/patterns/*.json
   feedback/metrics/*.json

   # Archive
   archive/
   ```

---

## 📊 BEFORE vs AFTER

### BEFORE (40 items in root)
```
├── authoring_prompt_rules.txt
├── dispute_issue.py
├── EXECUTIVE_SUMMARY.md
├── EXECUTIVE_SUMMARY_EMAIL.txt
├── EXECUTIVE_SUMMARY_REPORT_REVIEW.md
├── example_usage.py
├── log_missed_issues.py
├── PHASE2_HANDOFF_PROMPT.md
├── PILOT_HANDOFF_PROMPT.md
├── POC_PHASE1_REPORT.md
├── PRESENTATION_SLIDES.md
├── product_vision_context.txt
├── QUICK_REFERENCE.md
├── README.md
├── REPORT_ANALYSIS_FOR_TEAM_REVIEW.md
├── requirements.txt
├── run_tests.py
├── SESSION_COMPLETE_SUMMARY.md
├── style_prompt_rules.txt
├── SYSTEM_REPORT.md
├── SYSTEM_REPORT_READABLE.txt
├── TEAM_MEETING_TALKING_POINTS.md
├── test_claude_workflow.py
├── test_feedback_loop.py
├── test_reviewer_feedback.py
├── validate_disputes.py
├── src/
├── tests/
├── reports/
├── feedback/
├── module_examples/
├── docs/
├── txt_guides/
└── claude-test/
```

### AFTER (9 items in root)
```
├── README.md
├── requirements.txt
├── src/
├── tests/
├── scripts/
├── config/
├── docs/
├── reports/
├── feedback/
├── modules/
└── archive/
```

**Much cleaner!** ✨

---

## 💡 ALTERNATIVE: Minimal Reorganization

If you want a lighter touch, just do these moves:

```bash
# Minimum cleanup - just move obvious clutter
mkdir -p scripts docs/reports config

# Scripts
mv *_test*.py run_tests.py example_usage.py dispute_issue.py validate_disputes.py log_missed_issues.py scripts/

# Config
mv *_rules.txt product_vision_context.txt config/

# Docs
mv *SUMMARY*.md *REPORT*.md *HANDOFF*.md *REFERENCE.md *SLIDES.md *TALKING*.md docs/

# Done - root is now much cleaner
```

This gets you 80% of the benefit with 20% of the work.

---

## ✅ RECOMMENDATION

**I recommend the FULL reorganization** because:
1. Project is still early - easy to change now
2. Scales better as project grows
3. Easier for new team members
4. Professional structure for potential pilot/production

**But if you're short on time:** Do the minimal reorganization above.

---

## 🎯 WHAT TO DO BEFORE NEXT CHAT SESSION

After reorganization:

1. ✅ Test that scripts still run
2. ✅ Update README with new paths
3. ✅ Git commit the reorganization
4. ✅ Note any issues for next session

That way next Claude session starts with a clean, organized codebase!
