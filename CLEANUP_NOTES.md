# Directory Cleanup - November 2024

## Summary
Reorganized the LEARNVIA repository for clarity and maintainability.

## New Structure
```
LEARNVIA/
├── Testing/          # Main review script
│   └── run_review.py
├── config/           # All configurations
│   ├── prompts/      # Review prompts
│   ├── rubrics/      # XML rubrics
│   └── templates/    # HTML templates
├── modules/          # Content modules
│   ├── exemplary/    # Example modules with review logs
│   └── test/         # Test modules (Power_Series, Fund_Thm_of_Calculus)
├── guides/           # Authoring & style guides
├── archive/          # Historical/unused files
├── run_review.sh     # Wrapper script for reviews
└── README.md         # Main documentation
```

## What Was Moved to Archive
- Old documentation (CODEBASE_ANALYSIS, SESSION_SUMMARY, etc.)
- Unused src/ directory structure
- Old test modules (Module_5_6_Exemplary, Module_5_7_Exemplary)
- Scripts not in active use
- Deprecated files from _deprecated/

## Key Changes
1. **Consolidated modules**: All exemplary modules now in `modules/exemplary/`
2. **Moved test modules**: From `Testing/` to `modules/test/`
3. **Created wrapper script**: `run_review.sh` for easier module reviews
4. **Updated references**: Fixed all paths in CLAUDE_ONBOARDING.md
5. **Archived unused files**: Moved to `archive/` subdirectories

## Running Reviews
Use the new wrapper script:
```bash
./run_review.sh Power_Series power_series_original.xml
```

Output will be in: `modules/test/Power_Series/output/`