# LEARNVIA Codebase - Comprehensive Structural Analysis

**Date**: November 11, 2025  
**Repository**: /Users/michaeljoyce/Desktop/LEARNVIA  
**Current Branch**: feature/cold_example2

---

## Executive Summary

The LEARNVIA codebase shows **significant organizational debt** with extensive duplication, obsolete archived systems, and a monolithic main script (2,641 lines). The repository has evolved from an earlier complex architecture into a simpler rule-based system, but the old architecture remains in the `/archive` directory creating confusion and maintenance burden.

**Critical Issues**:
- **File duplication**: Same exemplary modules exist in 2 locations
- **Obsolete versions**: Old monolithic Python code (~9,000 lines) in archive no longer used
- **Architectural confusion**: V2 and V3 prompt versions mixed without clear deprecation
- **Code organization**: Single 2,641-line script handling all concerns (parsing, rules, HTML generation)
- **Testing fragmentation**: Multiple output directories with no clear purpose
- **Naming inconsistency**: Files named with generic "test_module_*" patterns across 4 test folders

**Repository Size Breakdown**:
- Total: ~7.1 MB
- Archive (obsolete): 2.7 MB (38%)
- Testing (active): 4.0 MB (56%)
- Config/Guides: ~800 KB (11%)

---

## 1. Current Folder Organization

### Top-Level Structure

```
/Users/michaeljoyce/Desktop/LEARNVIA/
├── archive/              (2.7 MB) - OBSOLETE SYSTEM
├── config/               (256 KB) - ACTIVE config (prompts, rubrics, templates)
├── docs/                 (124 KB) - Architecture documentation
├── exemplary_modules/    (396 KB) - Exemplary content (duplicate location #1)
├── guides/               (412 KB) - Educational guidelines
├── scripts/              (16 KB)  - Utility scripts
├── Testing/              (4.0 MB) - ACTIVE test system (duplicate location #2)
├── .claude/              - Claude Code configuration
├── .git/                 - Version control
├── README.md             - Project overview
├── CLAUDE_ONBOARDING.md  - Integration guide
└── .gitignore            - Git exclusions
```

### 1.1 Active Directories (Currently Used)

#### `/config/` - System Configuration (256 KB)
**Purpose**: Central configuration for all reviews

**Contents**:
```
config/
├── agent_configuration.xml          (8.5 KB) - 30-agent setup (15 auth + 15 style)
├── prompts/                         (v3 XML layer system)
│   ├── authoring_prompt_rules_v3.xml     (32 KB) - Authoring quality rules
│   ├── style_prompt_rules_v3.xml         (19 KB) - Style compliance rules
│   ├── master_review_context_v3.xml      (22 KB) - Universal review guidelines
│   ├── exemplar_anchors_v3.xml           (18 KB) - Layer 0 reference examples
│   └── claude_live_reviewer_system_v2.xml (25 KB) - [UNUSED - should be archived]
├── rubrics/                         (10 files, 1.4 KB each)
│   ├── authoring_*.xml              (5 files) - Pedagogical quality rubrics
│   └── style_*.xml                  (5 files) - Writing quality rubrics
└── templates/                       [EMPTY except for .DS_Store]
```

**Status**: Well-organized with clear V3 versioning. One deprecated file (`claude_live_reviewer_system_v2.xml`) should be archived.

---

#### `/Testing/` - Active Review System (4.0 MB)
**Purpose**: Test modules and generated review reports

**Contents**:
```
Testing/
├── run_review.py                    (2,641 lines) - MAIN EXECUTION SCRIPT
├── run_review_BACKUP_before_fixes.py (2,342 lines) - [OBSOLETE BACKUP]
├── GENERIC_REVIEW_SUMMARY.md        - Review session notes
├── test_*.html                      (2 files) - [TEST FILES - should be deleted]
├── Fund_Thm_of_Calculus/
│   ├── module_5_6.xml               - Test module (XML)
│   └── output/
│       ├── test_module_review_data_generic.json
│       └── test_module_review_report_generic.html
├── Module_5_6_Exemplary/
│   ├── module_5_6_exemplary.xml     - DUPLICATE of exemplary_modules/
│   └── output/
│       ├── test_module_review_data_generic.json
│       └── test_module_review_report_generic.html
├── Module_5_7_Exemplary/
│   ├── [no input module]
│   └── output/ [empty]
├── Power_Series/
│   ├── power_series_original.xml
│   └── output/
│       ├── test_module_review_data_generic.json
│       ├── test_module_review_data_generic_BEFORE_FIXES.json
│       └── test_module_review_report_generic.html
└── __pycache__/
```

**Status**: 
- Disorganized with leftover test files and backup scripts
- Module_5_6 exists in 2 locations (Testing/ and exemplary_modules/)
- Module_5_7 has folder but no input module to test
- Output files use generic naming making it hard to track what they're from

---

#### `/config/prompts/` - Layered Prompt System (v3 XML Architecture)
**V3 Structure** (Active as of Nov 11, 4bfa1c6):

```
prompts/
├── master_review_context_v3.xml      (22 KB) Layer 1: Universal context
├── authoring_prompt_rules_v3.xml     (32 KB) Layer 2a: Authoring guidelines  
├── style_prompt_rules_v3.xml         (19 KB) Layer 2b: Style guidelines
├── exemplar_anchors_v3.xml           (18 KB) Layer 0: Gold-standard examples
└── claude_live_reviewer_system_v2.xml (25 KB) [DEPRECATED - unused]
```

**Layered Architecture**:
- **Layer 0** (Exemplar Anchors): Reference modules showing quality standards
- **Layer 1** (Master Context): Universal review principles and agent role
- **Layer 2** (Domain Prompts): Authoring quality + Style quality rules
- **Layer 3** (Rubrics): Competency-specific evaluation criteria (10 rubrics)

**Status**: Well-structured. The V2 system file should be removed or clearly marked as deprecated.

---

#### `/exemplary_modules/` - Exemplary Content (396 KB)
**Purpose**: Reference modules demonstrating quality standards

**Contents**:
```
exemplary_modules/
├── module_5_6_exemplary.xml    (164 KB) Chapter 5.6: FTC (Exemplar)
├── module_5_7_exemplary.xml    (196 KB) Chapter 5.7: Net Change (Exemplar)
└── strip_animations.py         (95 lines) Utility to remove animations from XML
```

**DUPLICATE LOCATION ISSUE**:
- `module_5_6_exemplary.xml` also exists at `/Testing/Module_5_6_Exemplary/module_5_6_exemplary.xml`
- Same file, two locations = maintenance burden and confusion
- **Recommendation**: Keep exemplary_modules/ as single source; remove from Testing/

---

#### `/guides/` - Human-Readable Guidelines (412 KB)
**Purpose**: Educational content standards for human reviewers

**Contents**:
```
guides/
├── Learnvia authoring guidelines (2025).md    (342 KB) 
├── Learnvia style guide_103125.docx.md        (61 KB)
└── README.md (905 bytes)
```

**Status**: Comprehensive guides for content authors. Files are untracked (in git status as `??`).

---

#### `/docs/` - Architecture & Documentation (124 KB)
**Purpose**: Design decisions, analysis, and implementation guidance

**Contents**:
```
docs/
├── layered_prompt_architecture.md           (16 KB) Design rationale
├── categorized_examples_from_logs.md        (9.5 KB) Real review examples
├── OPUS_REVIEW_1_SUMMARY.md                 (8.1 KB) Expert review feedback
├── OPUS_REVIEW_2_SUMMARY.md                 (5.6 KB) Follow-up review
├── OPUS_REVIEW_PACKAGE.md                   (6.7 KB) Review submission
├── implementation_next_steps.md             (7.1 KB) TODO list
├── prompt_loading_order.md                  (2.5 KB) Prompt sequencing
├── review_log_analysis.md                   (3.9 KB) Data analysis
└── plans/
    └── 2025-11-06-tabbed-html-report-design.md
```

**Status**: Well-documented architecture. Documentation is current and detailed.

---

#### `/scripts/` - Utility Scripts (16 KB)
**Purpose**: Log analysis and testing utilities

**Contents**:
```
scripts/
├── analyze_review_logs.py      (282 lines) - Parse review data
└── run_iteration_test.sh       (43 lines)  - Shell test runner
```

**Status**: Minimal utilities. Most functionality is in the main run_review.py.

---

### 1.2 Obsolete/Archive Directories

#### `/archive/_system/` - OLD MONOLITHIC SYSTEM (2.7 MB)
**Status**: COMPLETELY OBSOLETE - Do not use

**History**: This was the original multi-file architecture. Replaced with current system on commit d1ba9f9 (Clean up repository structure, Nov 9).

**Contains** (not actively used):
```
archive/_system/
├── CODE/                    (~3,300 lines Python)
│   ├── reviewers.py        (1,133 lines) - Individual reviewer logic
│   ├── report_generator.py (591 lines)   - HTML report generation  
│   ├── aggregator.py       (379 lines)   - Consensus aggregation
│   ├── orchestrator.py     (420 lines)   - Workflow coordination
│   ├── models.py           (315 lines)   - Data models
│   ├── feedback_loop.py    (455 lines)   - Revision management
│   └── [7 more files]
├── tests/                   (4 test files, ~1,300 lines)
├── ACTIVE_CONFIG/          (OLD v1 config - 10 rubrics + templates)
│   ├── agent_configuration.xml
│   ├── prompts/ [EMPTY - v1 prompts deleted]
│   ├── rubrics/ (10 XML files - OLDER versions)
│   └── templates/ (2 XML templates for agents)
├── REALISTIC_WORKFLOW/     (~6,000 lines scripts)
│   ├── scripts/            (9 Python scripts for different review passes)
│   ├── outputs/            (Workflow output examples)
│   └── [various demo files]
├── DOCUMENTATION/          (MD versions of rubrics)
├── FOUNDATION/            (Old guides)
├── tests/                 (Old unit tests)
└── scripts/              (Older utility scripts)
```

**Why Obsolete**:
- Original architecture split concerns across 8+ Python modules
- Hard to maintain and scale - replaced with unified run_review.py
- Old "ACTIVE_CONFIG" v1 prompts no longer used (superseded by v3 XML system)
- Realistic workflow examples are educational but system is not used operationally

**Recommendation**: Move entire `/archive/_system/` to a `_deprecated/` folder or delete if not needed for historical reference.

---

## 2. Active vs Obsolete Files

### 2.1 Files Currently Used

| File | Purpose | Status |
|------|---------|--------|
| `Testing/run_review.py` | Main execution script | ✅ ACTIVE |
| `config/prompts/*_v3.xml` | Layered prompts (5 files) | ✅ ACTIVE |
| `config/rubrics/*.xml` | Competency rubrics (10 files) | ✅ ACTIVE |
| `config/agent_configuration.xml` | Agent setup | ✅ ACTIVE |
| `exemplary_modules/*.xml` | Reference content (2 files) | ✅ ACTIVE |
| `Testing/<module>/` | Test modules (3 folders) | ✅ ACTIVE |
| `Testing/<module>/output/` | Review reports | ✅ ACTIVE |
| `guides/*.md` | Educational guidelines (2 files) | ✅ ACTIVE |
| `docs/*.md` | Architecture documentation | ✅ ACTIVE |
| `README.md` | Project overview | ✅ ACTIVE |

### 2.2 Obsolete/Deprecated Files

| File | Reason | Action |
|------|--------|--------|
| `archive/_system/` | Old monolithic system (entire folder) | **DELETE or rename to _deprecated/** |
| `archive/_system/ACTIVE_CONFIG/` | V1 prompt system (superseded by config/prompts/) | **DELETE** |
| `Testing/run_review_BACKUP_before_fixes.py` | Backup from previous fix attempt | **DELETE** |
| `config/prompts/claude_live_reviewer_system_v2.xml` | Old v2 system, replaced by v3 architecture | **DELETE or archive** |
| `Testing/*.html` (test_exact_structure.html, test_mathjax.html) | Temporary test files | **DELETE** |
| `Testing/Module_5_7_Exemplary/` | Test folder with no input module | **DELETE or add proper test module** |
| `exemplary_modules/` (duplicate location) | Same files in Testing/Module_5_6_Exemplary/ | **KEEP exemplary_modules/, DELETE from Testing/** |

### 2.3 Duplicate Files

| File | Locations | Issue |
|------|-----------|-------|
| `module_5_6_exemplary.xml` | exemplary_modules/ AND Testing/Module_5_6_Exemplary/ | Same 164 KB file in 2 places - maintain confusion about single source |

---

## 3. Code Quality Issues in run_review.py

### 3.1 Scale & Complexity (2,641 lines)

**File**: `/Users/michaeljoyce/Desktop/LEARNVIA/Testing/run_review.py`

**Issues**:
- Single file handles: XML parsing, pattern detection, consensus aggregation, HTML report generation
- 17 public functions + 1 class with 15 methods
- Monolithic design makes testing and refactoring difficult
- Any change affects the entire review pipeline

**Functions by Category**:

```
Loading & Parsing (3 functions):
  - load_prompt_file()
  - load_rubric_file()
  - load_module_content()

Text Extraction (1 function):
  - extract_text_from_module()        ← 70+ lines, complex nested function

Pattern Detection (1 class):
  - RuleBasedDetector                 ← 15 detection methods
    ├── detect_todo_placeholders()
    ├── detect_contractions()
    ├── detect_missing_latex()
    ├── detect_lazy_starts()
    ├── detect_complex_sentences()
    ├── detect_passive_voice()
    ├── detect_imperative_in_hints()
    ├── detect_interval_notation_issues()
    ├── detect_vague_pronouns()
    ├── detect_missing_definitions()
    └── detect_authoring_issues()      ← ~250 lines of pattern matching

Prompt Building (1 function):
  - build_agent_prompt()              ← ~70 lines, complex string formatting

Simulation (2 functions):
  - simulate_agent_review()           ← ~110 lines
  - aggregate_consensus_issues()      ← ~80 lines

Reporting (7 functions):
  - generate_html_report()            ← ~1,000+ lines of HTML generation
  - _format_issues_html()
  - _format_category_table_html()
  - _format_issues_by_category_html()
  - _format_category_details_html()
  - _format_top_issues_list()

Main (1 function):
  - main()                            ← ~200 lines of orchestration
```

### 3.2 Code Organization Issues

#### Issue 1: Oversized Functions
```python
extract_text_from_module()    # 70 lines with nested function definitions
generate_html_report()         # 1,000+ lines of HTML concatenation
detect_authoring_issues()      # ~250 lines, should be split into 5-10 functions
```

#### Issue 2: Inlined HTML Generation
Lines 1,250-2,270: Massive HTML report generation (1,000+ lines) mixed with logic:
```python
def generate_html_report(...):
    # Logic checking, data formatting
    html = """
    <!DOCTYPE html>
    <html>
    ...
    """ + conditional_sections + """
    ...
    """  # ~1,000 lines of string concatenation
```

**Better approach**: Use a template library (Jinja2) or separate HTML templates.

#### Issue 3: Magic Numbers & Hardcoded Values
- Lines 48-73: Agent config hardcoded in dict (should be in config/agent_configuration.xml)
- Lines 37-41: LEARNVIA_PATH hardcoded to specific user's desktop
- Lines 258-265: Probability map in should_flag() method (good comment, but could be config)

#### Issue 4: Regex Patterns Scattered Throughout
Lines 285-996: Multiple detect_*() methods each contain 5-50 regex patterns:
- No centralized regex library
- Patterns repeated (contractions appears in 2 methods)
- Hard to validate or test patterns in isolation
- Missing many edge cases (e.g., "its" vs "it's" partially handled on line 343)

#### Issue 5: Poor Separation of Concerns
```
Parsing:     extract_text_from_module() + XML parsing inline
Rules:       15 detection methods in single class
Consensus:   aggregate_consensus_issues() mixed with rule logic
Reporting:   1,000+ lines of HTML in generate_html_report()
Execution:   main() orchestrates everything
```

### 3.3 Global State Issues

```python
# Lines 37-45: Global mutable state
LEARNVIA_PATH = Path(...)
CONFIG_PATH = ...
PROMPTS_PATH = ...
RUBRICS_PATH = ...
TESTING_PATH = ...

TEST_MODULE_PATH = None        # ← Mutable global set in main()
OUTPUT_PATH = None             # ← Mutable global set in main()

AGENT_CONFIG = { ... }         # ← Hardcoded configuration dict
```

**Issues**:
- Global paths make testing impossible (can't test with different modules)
- Global AGENT_CONFIG should be loaded from XML
- Mutation of globals in main() makes code flow hard to follow

### 3.4 Error Handling Issues

**Poor error handling**:
```python
Line 281-282:
    try:
        return int(line.split('|')[0].strip())
    except:  # ← Bare except clause (bad practice)
        pass

Line 144-162:
    except ET.ParseError as e:
        print(f"Warning: XML parsing error: {e}")
        # Silent fallback - could hide real problems

Line 2523-2525:
    try:
        OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    except Exception:  # ← Too broad
        pass
```

### 3.5 Type Hints & Documentation

**Good**:
- Type hints on function signatures: `def load_prompt_file(filename: str) -> str:`
- Docstrings on classes and public functions
- Comments explaining complex logic (e.g., LaTeX preservation)

**Issues**:
- Incomplete type hints on some parameters
- Internal helper functions lack docstrings
- HTML generation completely lacks documentation of output structure

### 3.6 Testing & Validation

**No automated tests**:
- archive/_system/tests/ exists but isn't used with current code
- Test files in Testing/ are manual (run_review.py with different modules)
- No unit tests for individual detection methods
- No regression tests for HTML output format

### 3.7 Performance Concerns

**Potential issues**:
- `generate_html_report()` concatenates 1,000+ line strings (memory inefficient)
- Regex patterns recompiled on every detection (should be compiled once)
- No caching for repeated operations
- JSON serialization in memory for large reports (282-346 KB files)

---

## 4. Prompt Files & Relationships

### 4.1 Prompt Loading Architecture

**Layered System** (Commit 85429e0):

```
Layer 0: Exemplar Anchors
    ├─ exemplar_anchors_v3.xml       ← Gold-standard reference modules
    └─ Purpose: Calibrate judgments, reduce false positives

    ↓ (build_agent_prompt includes all layers)

Layer 1: Master Review Context
    ├─ master_review_context_v3.xml  ← Universal principles
    └─ Purpose: Agent role, mission, output format

    ↓

Layer 2a: Authoring Rules
    ├─ authoring_prompt_rules_v3.xml ← Pedagogical quality
    └─ Purpose: Content organization, clarity, engagement

    ↓

Layer 2b: Style Rules  
    ├─ style_prompt_rules_v3.xml     ← Writing quality
    └─ Purpose: Grammar, mechanics, math formatting

    ↓

Layer 3: Rubric Competencies
    ├─ config/rubrics/*.xml          ← 10 detailed rubrics
    └─ Purpose: Specialized evaluation criteria
```

### 4.2 Prompt Files in Detail

**Active V3 System** (`config/prompts/`):

| File | Size | Purpose | Status |
|------|------|---------|--------|
| `master_review_context_v3.xml` | 22 KB | Layer 1: Core review principles, agent role, output format | ✅ ACTIVE |
| `authoring_prompt_rules_v3.xml` | 32 KB | Layer 2a: 6 authoring principles + common issues | ✅ ACTIVE |
| `style_prompt_rules_v3.xml` | 19 KB | Layer 2b: 5 style principles + common issues | ✅ ACTIVE |
| `exemplar_anchors_v3.xml` | 18 KB | Layer 0: 2 exemplary modules + positive patterns | ✅ ACTIVE |
| `claude_live_reviewer_system_v2.xml` | 25 KB | OLD v2 system (unused) | ❌ DEPRECATED |

**Rubrics** (`config/rubrics/`):

**Authoring Rubrics** (5 files, 142-151 lines each):
1. `authoring_pedagogical_flow.xml` (142 lines) - Content flow and coherence
2. `authoring_assessment_quality.xml` (151 lines) - Assessment alignment
3. `authoring_conceptual_clarity.xml` (149 lines) - Concept clarity
4. `authoring_structural_integrity.xml` (118 lines) - Content organization
5. `authoring_student_engagement.xml` (125 lines) - Student motivation

**Style Rubrics** (5 files, 124-142 lines each):
6. `style_mechanical_compliance.xml` (144 lines) - Grammar, punctuation
7. `style_accessibility.xml` (142 lines) - Readability, accessibility
8. `style_mathematical_formatting.xml` (124 lines) - Math notation
9. `style_consistency.xml` (134 lines) - Terminology consistency
10. `style_punctuation_grammar.xml` (129 lines) - Grammar details

### 4.3 Data Flow Through Prompts

```
run_review.py main()
    │
    ├─→ load_prompt_file("master_review_context_v3.xml")
    │
    ├─→ load_prompt_file("authoring_prompt_rules_v3.xml")
    │
    ├─→ load_prompt_file("style_prompt_rules_v3.xml")
    │
    ├─→ load_prompt_file("exemplar_anchors_v3.xml")
    │
    └─→ For each of 30 agents:
        │
        ├─→ Determine agent type (authoring/style) and specialty
        │
        ├─→ load_rubric_file(selected_rubric.xml)
        │
        ├─→ build_agent_prompt(
        │       agent_type, focus, 
        │       exemplar_anchors,      ← Layer 0
        │       master_prompt,         ← Layer 1
        │       domain_prompt,         ← Layer 2 (authoring or style)
        │       rubric_content         ← Layer 3
        │   )
        │
        ├─→ simulate_agent_review(agent_id, full_prompt)
        │       │
        │       └─→ RuleBasedDetector.detect_*()  ← 11 pattern detectors
        │
        └─→ Store findings[]

    └─→ aggregate_consensus_issues(all_findings)
        │
        └─→ generate_html_report(consensus_issues)
```

### 4.4 Prompt Loading Issues

**Issue 1: Hardcoded config paths**
```python
# Line 37-41
LEARNVIA_PATH = Path("/Users/michaeljoyce/Desktop/LEARNVIA")
CONFIG_PATH = LEARNVIA_PATH / "config"
PROMPTS_PATH = CONFIG_PATH / "prompts"
RUBRICS_PATH = CONFIG_PATH / "rubrics"
```
- Hardcoded to specific user's desktop
- Breaks if repository moves or is cloned elsewhere
- Should use relative paths or environment variables

**Issue 2: Silent file not found**
```python
# Lines 2499-2503
try:
    exemplar_anchors = load_prompt_file("exemplar_anchors_v3.xml")
except FileNotFoundError:
    exemplar_anchors = ""
    print("Warning: exemplar_anchors_v3.xml not found")
```
- Missing prompt silently degrades performance
- No validation that all required prompts exist
- Should fail fast if critical files missing

**Issue 3: Mixed v2/v3 system**
- `claude_live_reviewer_system_v2.xml` still in directory but not used
- Could confuse developers about which system is active
- Clear deprecation marker needed

---

## 5. Data Flow Through the System

### 5.1 Complete Execution Flow

```
INPUT: User runs: python run_review.py <module_folder> <xml_file>
        │
        ├─ Parse command-line args → (module_folder, xml_file)
        │
        ├─ Set paths:
        │   MODULE_PATH = TESTING_PATH / module_folder
        │   TEST_MODULE_PATH = MODULE_PATH / xml_file
        │   OUTPUT_PATH = MODULE_PATH / "output"
        │
        └─ Validate:
           if not TEST_MODULE_PATH.exists() → exit with error
        
PHASE 1: LOAD CONFIGURATION
        │
        ├─ Load 4 layered prompts (V3 XML system)
        │   ├─ master_review_context_v3.xml
        │   ├─ authoring_prompt_rules_v3.xml
        │   ├─ style_prompt_rules_v3.xml
        │   └─ exemplar_anchors_v3.xml (optional, silent fallback)
        │
        └─ Load agent configuration
            └─ AGENT_CONFIG dict (hardcoded 30 agents: 15 auth + 15 style)

PHASE 2: LOAD MODULE
        │
        ├─ Read XML file: module_xml = load_module_content(TEST_MODULE_PATH)
        │
        └─ Extract text (in-memory only, transient):
           module_text = extract_text_from_module(module_xml)
               │
               └─ Parse XML → recursive text extraction
               ├─ Preserve <m> and <me> LaTeX tags
               ├─ Normalize whitespace in LaTeX
               ├─ Add line numbers (0001|, 0002|, etc.)
               └─ Return: numbered_text_lines string

PHASE 3: SIMULATE 30 AGENT REVIEWS
        │
        ├─ Agent 1-9 (Authoring Specialists):
        │   Each i from 0 to 8:
        │   │
        │   ├─ Load competency-specific rubric
        │   │   Competencies: Pedagogical Flow, Structural Integrity,
        │   │                 Student Engagement, Conceptual Clarity,
        │   │                 Assessment Quality (cycling)
        │   │
        │   ├─ agent_id = f"Authoring-Specialist-{competency}-{i+1}"
        │   │
        │   ├─ build_agent_prompt(
        │   │       "authoring", competency,
        │   │       exemplar_anchors, master_prompt,
        │   │       authoring_prompt, rubric_content
        │   │   )
        │   │
        │   └─ simulate_agent_review(agent_id, full_prompt)
        │       │
        │       ├─ Extract module content from prompt
        │       │   (find "# MODULE TO REVIEW" section)
        │       │
        │       ├─ Create RuleBasedDetector(module_text, "authoring", agent_id)
        │       │
        │       ├─ Detect authoring issues:
        │       │   ├─ detect_todo_placeholders()     ← Unfinished markers
        │       │   ├─ detect_vague_pronouns()        ← Grammar clarity
        │       │   ├─ detect_missing_definitions()   ← Concept setup
        │       │   └─ detect_authoring_issues()      ← Pedagogical patterns
        │       │
        │       └─ Return: findings[] (issue objects)
        │
        ├─ Agent 10-15 (Authoring Generalists):
        │   Each i from 9 to 14:
        │   │
        │   ├─ No rubric (generalist role)
        │   │
        │   ├─ agent_id = f"Authoring-Generalist-{i+1}"
        │   │
        │   └─ simulate_agent_review() with all detection methods
        │       (but with lower detection probability for specialization)
        │
        ├─ Agent 16-24 (Style Specialists):
        │   Each i from 0 to 8:
        │   │
        │   ├─ Load competency-specific rubric
        │   │   Competencies: Mechanical Compliance, Mathematical Formatting,
        │   │                 Punctuation & Grammar, Accessibility,
        │   │                 Consistency (cycling)
        │   │
        │   └─ simulate_agent_review() with style detections:
        │       ├─ detect_contractions()            ← Formality
        │       ├─ detect_missing_latex()           ← Math formatting
        │       ├─ detect_lazy_starts()             ← Writing quality
        │       ├─ detect_complex_sentences()       ← Readability
        │       ├─ detect_passive_voice()           ← Active voice
        │       ├─ detect_imperative_in_hints()     ← Tone
        │       └─ detect_interval_notation_issues() ← Math notation
        │
        └─ Agent 25-30 (Style Generalists):
            Each i from 9 to 14:
            │
            └─ simulate_agent_review() with all style detections

PHASE 4: AGGREGATE CONSENSUS
        │
        ├─ Collect all findings from 30 agents → all_findings[]
        │   (each finding: issue_description, line_numbers, severity,
        │    category, confidence, student_impact, suggested_fix)
        │
        └─ aggregate_consensus_issues(all_findings, total_agents=30)
            │
            ├─ Group findings by similar description (first 50 chars)
            │
            ├─ For each group:
            │   ├─ agent_count = agents reporting this issue
            │   ├─ consensus_score = agent_count / 30
            │   ├─ priority = severity × consensus (combines metrics)
            │   │
            │   └─ If consensus_score >= 2/30 (2+ agents):
            │       └─ Add to consensus_issues[]
            │       Else:
            │       └─ Add to non_consensus_issues[]
            │
            └─ Return: (consensus_issues, non_consensus_issues)

PHASE 5: GENERATE HTML REPORT
        │
        ├─ generate_html_report(
        │       consensus_issues, non_consensus_issues,
        │       all_findings, module_xml, module_text
        │   )
        │
        └─ Assemble 8-tab HTML report:
            │
            ├─ Tab 1: DASHBOARD
            │   ├─ Summary stats (total issues, by type, by priority)
            │   ├─ Top issues list
            │   └─ Agent participation chart
            │
            ├─ Tab 2: FINDINGS BY PRIORITY (sorted 1-5)
            │   └─ Consensus issues with line numbers + suggested fixes
            │
            ├─ Tab 3: ALL ISSUES (consensus + non-consensus)
            │   └─ Detailed table of all 400+ findings
            │
            ├─ Tab 4: ISSUES BY CATEGORY
            │   ├─ Authoring issues (Pedagogical, Structural, etc.)
            │   └─ Style issues (Mechanical, Math Formatting, etc.)
            │
            ├─ Tab 5: ORIGINAL INPUT (with line numbers)
            │   └─ Module text extracted from XML (read-only, reference only)
            │
            ├─ Tab 6: AGENT FINDINGS
            │   ├─ Authoring agents' findings
            │   └─ Style agents' findings
            │
            ├─ Tab 7: AGENT PARTICIPATION
            │   └─ Which agents flagged which issues
            │
            └─ Tab 8: DETAILED ANALYSIS
                ├─ Full issue descriptions
                ├─ Student impact analysis
                └─ Suggested fixes

OUTPUT: Write to disk
        │
        ├─ OUTPUT_PATH/test_module_review_data_generic.json
        │   (All findings in JSON format)
        │
        └─ OUTPUT_PATH/test_module_review_report_generic.html
            (Complete 8-tab interactive report)
```

### 5.2 Data Structures

**Issue Finding Object**:
```python
{
    "issue_description": str,      # Specific finding with context
    "line_numbers": [int, ...],    # Which lines affected
    "quoted_text": str,            # Exact problematic text
    "category": str,               # Pedagogical Flow | Structural Integrity | etc.
    "severity": int,               # 1-5 scale
    "student_impact": str,         # How affects learning
    "suggested_fix": str,          # Actionable remedy
    "confidence": float            # 0.0-1.0 (agent certainty)
}
```

**Consensus Issue Object** (enhanced):
```python
{
    ... (all fields from Issue Finding)
    "agent_count": int,            # How many agents flagged this
    "consensus_score": float,      # agent_count / 30
    "max_severity": int,           # Highest severity reported
    "priority": int                # severity × consensus (1-5)
}
```

**Agent Detection Process**:
```
Input: prompt (full 8,000+ character prompt with module embedded)
│
├─ Extract module content (search for "# MODULE TO REVIEW" marker)
├─ Create RuleBasedDetector instance
├─ Run 11 detection methods (depending on agent type)
├─ Each detection method:
│   └─ Regex pattern matching on module lines
│       ├─ Check for match
│       ├─ Calculate severity
│       ├─ Determine agent-specific probability of flagging
│       │   (90% for severity 5, 20% for severity 1)
│       ├─ If should_flag(), create finding object
│       └─ Add to findings list
│
└─ Remove duplicates (same line + category + description)
   └─ Return: [finding, finding, ...]
```

---

## 6. Organization & Structure Recommendations

### CRITICAL PRIORITY (Immediately)

**1. Remove Duplicate Files** (5 min)
```bash
# Keep exemplary_modules/ as the single source
rm /Users/michaeljoyce/Desktop/LEARNVIA/Testing/Module_5_6_Exemplary/module_5_6_exemplary.xml

# Update Testing/Module_5_6_Exemplary/input link or copy reference
# Document which exemplary files Testing/ should reference
```

**2. Delete Obsolete Files** (5 min)
```bash
# Remove backup and test files
rm /Users/michaeljoyce/Desktop/LEARNVIA/Testing/run_review_BACKUP_before_fixes.py
rm /Users/michaeljoyce/Desktop/LEARNVIA/Testing/test_exact_structure.html
rm /Users/michaeljoyce/Desktop/LEARNVIA/Testing/test_mathjax.html

# Remove deprecated prompt
rm /Users/michaeljoyce/Desktop/LEARNVIA/config/prompts/claude_live_reviewer_system_v2.xml
```

**3. Archive Old System** (10 min)
```bash
# Move archive/_system to _deprecated or delete entirely
mv /Users/michaeljoyce/Desktop/LEARNVIA/archive/_system \
   /Users/michaeljoyce/Desktop/LEARNVIA/_deprecated_system
```

**4. Fix Hardcoded Paths** (20 min)
```python
# In Testing/run_review.py:
# Replace line 37-41 with:
import os
LEARNVIA_PATH = Path(__file__).parent.parent  # Relative to script location
# OR
LEARNVIA_PATH = Path(os.environ.get("LEARNVIA_PATH", Path.cwd()))
```

### HIGH PRIORITY (Next 1-2 hours)

**5. Refactor run_review.py** (2-3 hours)

Split into modules:
```
Testing/
├── run_review.py          (Main orchestration - 300 lines)
├── lib/
│   ├── __init__.py
│   ├── config_loader.py   (Load prompts, rubrics, config)
│   ├── xml_parser.py      (Extract text from module XML)
│   ├── detector.py        (RuleBasedDetector class - keep intact)
│   ├── consensus.py       (aggregate_consensus_issues)
│   ├── html_report.py     (generate_html_report - use Jinja2)
│   └── models.py          (Finding, ConsensusIssue data classes)
└── tests/
    ├── test_detector.py
    ├── test_html_output.py
    └── test_integration.py
```

**6. Create HTML Templates** (1 hour)
```
Testing/
└── templates/
    ├── base.html          (Main 8-tab structure)
    ├── dashboard_tab.html
    ├── issues_tab.html
    ├── original_input_tab.html
    └── [5 more templates]
```

**7. Extract Configuration to XML** (30 min)
```
config/
└── agent_configuration.xml  (Already exists - just use it!)
    Currently loaded but not parsed - fix load_agent_config()
```

### MEDIUM PRIORITY (Code Quality)

**8. Fix Error Handling** (30 min)
```python
# Remove bare except clauses
# Add validation for all required config files
# Fail fast on configuration errors instead of silent fallback
```

**9. Add Unit Tests** (2 hours)
```
Testing/tests/
├── test_detection_rules.py      (Test each regex independently)
├── test_consensus_logic.py       (Test aggregation algorithm)
├── test_html_output.py          (Verify report structure)
└── test_end_to_end.py           (Integration tests)
```

**10. Document Code** (1 hour)
```python
# Add comprehensive docstrings to:
# - RuleBasedDetector class (explain each detection method)
# - generate_html_report() function
# - Consensus algorithm explanation
```

### LOW PRIORITY (Optimization)

**11. Performance** (1-2 hours)
- Compile regex patterns once (not on every detection)
- Use template rendering instead of string concatenation
- Consider JSON caching for large reports

**12. Extend Functionality** (Ongoing)
- Add custom rules system
- Support for additional content types beyond Calculus
- Plugin system for detection methods

---

## 7. Summary Table: File Status & Action Items

| Path | Type | Size | Status | Action |
|------|------|------|--------|--------|
| config/ | DIR | 256 KB | ✅ ACTIVE | Keep, add missing v3 prompts if any |
| config/prompts/*_v3.xml | FILE | 111 KB | ✅ ACTIVE | Keep all 4 v3 files |
| config/prompts/claude_*_v2.xml | FILE | 25 KB | ❌ DEPRECATED | **DELETE** |
| config/rubrics/*.xml | FILE | 1.4 KB | ✅ ACTIVE | Keep all 10 rubrics |
| config/agent_configuration.xml | FILE | 8.5 KB | ✅ ACTIVE | Keep, load properly in code |
| config/templates/ | DIR | - | EMPTY | Delete or document purpose |
| Testing/ | DIR | 4.0 MB | ✅ ACTIVE | Clean up output files |
| Testing/run_review.py | FILE | 110 KB | ✅ ACTIVE | **REFACTOR into modules** |
| Testing/run_review_BACKUP_before_fixes.py | FILE | 94 KB | ❌ DEPRECATED | **DELETE** |
| Testing/*.html | FILE | 4 KB | ❌ TEMP | **DELETE** |
| Testing/Module_5_6_Exemplary/module_5_6_exemplary.xml | FILE | 164 KB | ❌ DUPLICATE | **DELETE** (keep exemplary_modules/) |
| Testing/Module_5_7_Exemplary/ | DIR | - | INCOMPLETE | **Delete or add test module** |
| Testing/*/output/*.json | FILE | 282-1.3 MB | ✅ ACTIVE | Keep, document naming convention |
| Testing/*/output/*.html | FILE | 346 KB | ✅ ACTIVE | Keep, verify output names |
| exemplary_modules/ | DIR | 396 KB | ✅ ACTIVE | Keep as single source |
| exemplary_modules/*.xml | FILE | 180 KB | ✅ ACTIVE | Keep all exemplary modules |
| guides/ | DIR | 412 KB | ✅ ACTIVE | Keep, add to .gitignore if needed |
| guides/*.md | FILE | 403 KB | ✅ ACTIVE | Keep comprehensive guides |
| docs/ | DIR | 124 KB | ✅ ACTIVE | Keep architecture docs |
| scripts/ | DIR | 16 KB | ✅ ACTIVE | Keep utilities |
| archive/_system/ | DIR | 2.7 MB | ❌ OBSOLETE | **Move to _deprecated/ or DELETE** |
| archive/_system/ACTIVE_CONFIG/ | DIR | 48 KB | ❌ OBSOLETE | **DELETE** (config/ is newer) |
| archive/_system/CODE/ | DIR | 3.3 KB | ❌ OBSOLETE | **DELETE** (monolithic now) |
| archive/_system/* (all) | DIR | 2.7 MB | ❌ OBSOLETE | **DELETE or ARCHIVE** |
| .claude/ | DIR | - | ✅ ACTIVE | Keep, Claude Code config |
| .gitignore | FILE | - | ✅ ACTIVE | Keep version control config |
| README.md | FILE | 11 KB | ✅ ACTIVE | Keep updated |
| CLAUDE_ONBOARDING.md | FILE | 15 KB | ✅ ACTIVE | Keep project context |

---

## 8. Data Flow Diagram

```
XML Input Module
    │
    ├─→ XML Parser
    │   └─→ Line-numbered text (with LaTeX preservation)
    │
    ├─→ Load 4-Layer Prompts
    │   ├─ Layer 0: Exemplars (calibration)
    │   ├─ Layer 1: Master context (role/mission)
    │   ├─ Layer 2: Domain rules (authoring/style)
    │   └─ Layer 3: Rubrics (competencies)
    │
    ├─→ Build 30 Agent Prompts (full prompts with embedded module)
    │
    ├─→ Simulate 30 Agent Reviews
    │   ├─ 15 Authoring Agents (9 specialist + 6 generalist)
    │   ├─ 15 Style Agents (9 specialist + 6 generalist)
    │   └─ Each runs 11 pattern detection methods
    │
    ├─→ Collect ~400-800 Individual Findings
    │   (Each: line#, severity, category, confidence, suggested fix)
    │
    ├─→ Aggregate Consensus
    │   ├─ Group similar issues
    │   ├─ Count how many agents flagged each
    │   ├─ Calculate consensus score (agents/30)
    │   ├─ Calculate priority (severity × consensus)
    │   └─ Separate into: consensus_issues + non_consensus_issues
    │
    ├─→ Generate HTML Report (8 tabs)
    │   ├─ Dashboard (summary)
    │   ├─ By Priority (1-5)
    │   ├─ All Issues
    │   ├─ By Category
    │   ├─ Original Input (line numbers)
    │   ├─ Agent Findings
    │   ├─ Agent Participation
    │   └─ Detailed Analysis
    │
    └─→ Output Files
        ├─ test_module_review_data_generic.json  (structured data)
        └─ test_module_review_report_generic.html (interactive report)
```

---

## CONCLUSION

The LEARNVIA codebase is **functionally complete but organizationally messy**:

**Strengths**:
- Sophisticated 4-layer prompt architecture (v3 XML system)
- 30-agent consensus mechanism well-designed
- Comprehensive rubrics for all quality dimensions
- Good separation of concerns in prompt design

**Weaknesses**:
- **Monolithic run_review.py** (2,641 lines, needs splitting)
- **Extensive archive** (2.7 MB obsolete code, should be deleted)
- **Duplicate files** (exemplary modules in 2 locations)
- **Hardcoded paths** (desktop-specific, breaks on clone)
- **Poor HTML generation** (1,000 lines of string concatenation)
- **No unit tests** (hard to refactor with confidence)
- **Deprecated files** (v2 prompts still in directory)

**Immediate Actions** (Priority):
1. Delete 2.7 MB archive/_system/ directory
2. Remove duplicate module_5_6_exemplary.xml from Testing/
3. Delete obsolete backup scripts and temporary test files
4. Delete deprecated v2 prompt file
5. Fix hardcoded paths to be relative

**Short-term Refactoring** (1-2 weeks):
1. Split run_review.py into 6-7 focused modules
2. Move HTML generation to Jinja2 templates
3. Load agent configuration from XML (not hardcoded)
4. Add comprehensive unit tests
5. Document each module's responsibility

**Long-term Improvements** (ongoing):
1. Plugin system for custom detection rules
2. Support for non-calculus content
3. Performance optimizations
4. Automated regression testing for HTML output format
