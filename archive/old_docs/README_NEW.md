# LEARNVIA - AI-Powered Calculus Content Review System

## 🎯 Overview

LEARNVIA is a 30-agent AI review system that helps calculus content authors improve their work through educational feedback. The system reviews Calculus I-IV educational content using specialized AI agents focused on calculus pedagogy and writing quality.

## 📁 Project Structure (Reorganized)

```
LEARNVIA/
│
├── src/                      # Source code (refactored from monolithic script)
│   ├── core/                 # Core functionality
│   │   ├── __init__.py
│   │   ├── config_loader.py  # Load XML configurations
│   │   ├── xml_parser.py     # Extract text from module XML
│   │   └── consensus.py      # Aggregate agent findings
│   │
│   ├── detectors/           # Pattern detection modules
│   │   ├── __init__.py
│   │   ├── base.py          # RuleBasedDetector base class
│   │   ├── authoring.py     # Pedagogical issue detectors
│   │   └── style.py         # Mechanical issue detectors
│   │
│   ├── reports/             # Report generation
│   │   ├── __init__.py
│   │   ├── html_generator.py # HTML report generation
│   │   └── templates/       # HTML templates (future)
│   │
│   └── main.py              # Main orchestration script
│
├── config/                  # Configuration files
│   ├── prompts/            # V3 XML layered prompts
│   │   ├── master_review_context_v3.xml
│   │   ├── authoring_prompt_rules_v3.xml
│   │   ├── style_prompt_rules_v3.xml
│   │   └── exemplar_anchors_v3.xml
│   │
│   ├── rubrics/            # Competency rubrics (10 files)
│   │   ├── authoring_*.xml (5 files)
│   │   └── style_*.xml (5 files)
│   │
│   └── agent_configuration.xml  # 30-agent setup
│
├── modules/                # Module content
│   ├── exemplary/          # Gold-standard reference modules
│   │   ├── module_5_6_exemplary.xml
│   │   ├── module_5_7_exemplary.xml
│   │   └── *.csv          # Human review logs
│   │
│   └── test/              # Test modules for review
│       ├── Power_Series/
│       └── Fund_Thm_of_Calculus/
│
├── docs/                   # Documentation
│   ├── architecture/       # System design docs
│   │   ├── layered_prompt_architecture.md
│   │   ├── OPUS_REVIEW_*.md
│   │   └── implementation_next_steps.md
│   │
│   └── guides/            # Authoring & style guides
│       ├── Learnvia authoring guidelines (2025).md
│       └── Learnvia style guide_103125.docx.md
│
├── tests/                  # Unit tests (to be created)
│   ├── test_detectors.py
│   ├── test_consensus.py
│   └── test_integration.py
│
├── output/                 # Generated reports go here
│
├── _deprecated/            # Archived/obsolete files
│   ├── archive/           # Old monolithic system
│   └── *.backup           # Backup files
│
├── Testing/               # Current working directory (legacy)
│   └── run_review.py      # Current monolithic script (2,641 lines)
│
├── CLAUDE_ONBOARDING.md   # Session context for Claude
├── CODEBASE_ANALYSIS.md   # Detailed system analysis
└── README.md              # This file
```

## 🚀 Quick Start

### Running a Review (Current System)

```bash
cd Testing
python run_review.py Power_Series power_series_original.xml
```

### Output

The system generates:
- **HTML Report** with 9 tabs of analysis
- **JSON Data** with all findings
- **Line-numbered source** with rendered LaTeX

## 🏗️ System Architecture

### 4-Layer Prompt System

```
Layer 0: Exemplar Anchors      # Priority calibration examples
Layer 1: Master Context        # Universal review principles
Layer 2: Domain Rules          # Authoring & Style guidelines
Layer 3: Competency Rubrics    # Specific evaluation criteria
```

### 30-Agent Consensus Model

```
15 Authoring Agents            15 Style Agents
├─ 9 Specialists               ├─ 9 Specialists
│  (Deep expertise)            │  (Deep expertise)
└─ 6 Generalists               └─ 6 Generalists
   (Holistic view)                (Holistic view)

Consensus = Issues flagged by 4+ agents (high confidence)
```

### Detection Methods (15 total)

**Authoring Detectors:**
- Vague pronouns
- Missing definitions
- Todo placeholders
- Conceptual issues
- Pedagogical flow

**Style Detectors:**
- Contractions
- Missing LaTeX
- Lazy starts
- Complex sentences
- Passive voice (NEW)
- Imperative hints (NEW)
- Interval notation (NEW)

## 📊 Key Metrics

| Metric | Value |
|--------|-------|
| Agents | 30 |
| Detection Methods | 15 |
| Regex Patterns | 100+ |
| Lines of Code | 2,641 |
| Consensus Threshold | 4 agents |
| Priority Scale | 1-5 |
| Typical Findings | 150-200 per module |

## 🎯 Design Principles

1. **GENERIC BY DEFAULT** - Works with ANY Calc 2 module
2. **Pattern extraction over content** - Learn patterns, not specifics
3. **Educational feedback** - Support authors, don't gatekeep
4. **Target struggling students** - Every decision considers impact

## 🔧 Recent Improvements

### LaTeX Rendering Fix (Nov 2024)
- Changed from `\(` delimiters to `$` for MathJax
- Math now renders correctly in Original Input tab

### Style Agent Enhancement (Nov 2024)
- Added passive voice detection (+28 findings)
- Added interval notation checking (+18 findings)
- Added imperative hint detection
- Improved authoring:style ratio from 4:1 to 1.4:1

## 📝 TODO: Refactoring Plan

### Phase 1: Code Modularization
- [ ] Split run_review.py into modules
- [ ] Create proper class hierarchy
- [ ] Add configuration management

### Phase 2: Testing
- [ ] Add unit tests for detectors
- [ ] Add integration tests
- [ ] Add performance benchmarks

### Phase 3: Templates
- [ ] Replace HTML concatenation with Jinja2
- [ ] Create reusable report components
- [ ] Add PDF export option

## 👥 Contributing

See `CLAUDE_ONBOARDING.md` for development setup and guidelines.

## 📄 License

Internal LEARNVIA use only.

---

**Current Status:** Production-ready but needs refactoring for maintainability.