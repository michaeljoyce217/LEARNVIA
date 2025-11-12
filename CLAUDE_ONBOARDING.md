# LEARNVIA - Claude Onboarding Guide
**Master Context for All Claude Sessions**

---

## ⚡ FIRST STEP: Always Use Superpowers

**BEFORE DOING ANYTHING ELSE, TYPE:**
```
/superpowers
```

This activates the skill system that ensures you follow best practices for:
- Brainstorming before coding
- Test-driven development
- Systematic debugging
- Code review workflows
- And more...

**DO NOT SKIP THIS STEP.** Superpowers prevent common mistakes and ensure quality work.

---

## 🎯 Critical Design Principle: GENERIC BY DEFAULT

**THIS SYSTEM MUST WORK WITH ANY CALCULUS 2 MODULE**

### The Non-Negotiable Rule

Every component of this system—prompts, rubrics, and `run_review.py`—MUST be generic enough to handle any newly introduced Calculus 2 module without modification.

❌ **NEVER hardcode content from specific test modules into prompts or detection logic**
✅ **DO use the two exemplary modules for two-shot pattern learning**
✅ **DO keep Calc 2 topic detection (this is domain-specific, not module-specific)**

### The Problem This Prevents

Previous sessions fell into this trap:
1. Tested system with Power Series module
2. Found specific issues (e.g., "radius of convergence" undefined)
3. Started hardcoding "radius of convergence" detection into prompts
4. System now fails on other Calc 2 topics (integrals, sequences, etc.)

**Your job:** Extract PATTERNS from test modules, not CONTENT.

### What "Generic" Means Here

| ✅ ALLOWED (Generic) | ❌ FORBIDDEN (Hardcoded) |
|---------------------|-------------------------|
| Detect undefined technical terms using frequency analysis | Check specifically for "radius of convergence" |
| Identify vague pronouns ("it", "this", "that") | Flag "it" only in Power Series context |
| Flag missing definitions for terms used 3+ times | Hardcode list of "important Calc 2 terms" |
| Use exemplary modules 5.6 & 5.7 as pattern examples | Copy specific content from exemplars into prompts |
| Detect abstract-before-concrete pedagogy issues | Assume all modules start with series convergence |

---

## 📚 What This System Is

A **30-agent AI review system** for Calculus 2 educational content.

### Architecture Overview

**4-Pass Review Structure:**
1. **Pass 1:** 30 agents (15 authoring + 15 style) review content → Author self-review
2. **Pass 2:** 30 agents review revised content → Human reviewer meeting
3. **Pass 3:** 30 agents focus on style only → Author self-review
4. **Pass 4:** 30 agents final style check → Copy editor meeting

**NOTE: Current implementation demonstrates Pass 1 only.** The system architecture shows all 4 passes, but we're currently building and testing the first pass.

**Consensus Mechanism:**
- 4+ agents flag same issue = **Consensus Issue** (high confidence)
- 1-3 agents flag = **Flagged Issue** (may be false positive)
- Priority = Severity × Agent Agreement (1-5 scale)

**Current Implementation:**
- Working directory: `/Users/michaeljoyce/Desktop/LEARNVIA/Testing`
- Main script: `Testing/run_review.py` (2200+ lines)
- Test module: Power Series (Calc 2 content)
- Exemplary modules: 5.6 (Definite Integral) & 5.7 (Net Change) in `exemplary_modules/`

---

## 🧠 Two-Shot Learning with Exemplary Modules

### Purpose: Pattern Recognition, NOT Content Copying

The two exemplary modules (5.6 and 5.7) are **pattern anchors**, not content templates.

**What to learn from exemplars:**
- ✅ How quality pedagogy flows (concrete → abstract, multiple representations)
- ✅ What "accessible writing" looks like (short sentences, defined terms)
- ✅ How assessments align with learning outcomes
- ✅ Priority calibration (what's P1 vs P5 severity)

**What NOT to do with exemplars:**
- ❌ Assume all modules follow the Fundamental Theorem topic structure
- ❌ Check if new modules "define integration" (topic-specific)
- ❌ Hardcode exemplar-specific terms into detection rules
- ❌ Copy architectural decisions that may not apply to other topics

**Location:**
- `exemplary_modules/module_5_6_exemplary.xml` (~270KB)
- `exemplary_modules/module_5_7_exemplary.xml`
- Human review logs: `exemplary_modules/*.csv`

---

## 🛠️ System Components

### 1. Core Review Script
**File:** `Testing/run_review.py`

**Key features:**
- LaTeX preservation pipeline (custom `<m>` and `<me>` tags)
- Line-numbered text extraction from XML
- 30-agent simulation with consensus mechanism
- HTML report generation with MathJax rendering
- 9-tab output:
  1. **Consensus Issues** - Issues flagged by 4+ agents
  2. **Flagged Issues** - Issues flagged by 1-3 agents
  3. **All Findings** - Complete list of 157 findings
  4. **Agent Breakdown** - How each of 30 agents performed
  5. **Category Analysis** - Issues grouped by category
  6. **Original Input** - Line-numbered source with LaTeX
  7. **Next Steps** - Recommended workflow actions
  8. **System Architecture** - Shows all 4 passes (currently demonstrating Pass 1)
  9. **Complete Workflow** - Visual workflow diagram

**Possible improvement:** Consolidate tabs 8 & 9 into single "System Architecture" tab that shows all 4 passes with clear indication we're demonstrating Pass 1.

**Generic design requirements:**
- Must work with any Calc 2 module XML
- Topic detection should be dynamic, not hardcoded
- Rule-based detectors should use universal patterns (undefined terms, vague pronouns, etc.)
- Calc 2 domain knowledge (e.g., `calc2_compound_terms`) is acceptable—this distinguishes Calc 2 from Calc 1/3/4

### 2. Prompt System
**Location:** `ACTIVE_CONFIG/v2_master_prompts/` and `config/prompts/`

**Key prompts:**
- `master_context.md` - Universal review context (27507 chars)
- `authoring_rules.md` - Pedagogical quality rules (11587 chars)
- `style_rules.md` - Writing mechanics rules (16474 chars)
- `exemplar_anchors.md` - Priority calibration examples (4522 chars)

**Critical meta-rule (lines 77-91 in master_review_context_v2.txt):**
> "Do not hardcode specifics from exemplars. Extract patterns."

**Your role when updating prompts:**
- Keep rules abstract and pattern-based
- Use exemplars for calibration examples only
- Ensure prompts work for sequences, series, integrals, convergence tests, Taylor series, etc.

### 3. Rubrics
**Location:** `config/rubrics/*.xml`

15 rubric files covering:
- **Authoring (5):** Conceptual clarity, pedagogical flow, assessment quality, student engagement, structural integrity
- **Style (10):** Grammar, formatting, consistency, accessibility, etc.

**Status:** Currently generic and domain-agnostic

---

## 🚀 When Starting a New Session

### STEP 0: Activate Superpowers
```
/superpowers
```
**DO THIS FIRST. NON-NEGOTIABLE.**

### For `/superpowers:brainstorming` or `/explore`

**Use this workflow:**
1. Read `config/prompts/explore_prompt.txt` for exploration structure
2. Map the repository quickly (key dirs: `Testing/`, `ACTIVE_CONFIG/`, `exemplary_modules/`, `config/`)
3. Run review if appropriate: `python Testing/run_review.py Power_Series power_series_original.xml power_series_original_readable.txt`
4. Analyze HTML report: `Testing/Power_Series/output/test_module_review_report_generic.html`
5. Compare against human review logs in `exemplary_modules/*.csv`
6. Generate prioritized plan with Day 1/Day 2 milestones

**Key questions to ask:**
- Are prompts still generic or have they drifted toward Power Series specifics?
- Is `run_review.py` detecting patterns or hardcoded content?
- Do exemplary modules inform priority calibration without constraining new topics?

### For Live Review Sessions

**Use this workflow:**
1. Read your "brain": `config/prompts/claude_live_reviewer_system.xml`
2. Understand anti-patterns (don't flag correct structures)
3. Review target student profile (struggling Calc 2 students)
4. Apply specificity requirements: Line # + Quote + Impact + Fix
5. Show your work (parse, review sections, flag issues, explain rejections)
6. Generate HTML report using template

---

## 🎓 Target Student Profile

**Every issue you flag must answer: "Does this hurt THIS student?"**

The student:
- Studies alone at home (no teacher available)
- Low confidence in math (fear of failure)
- Limited time (busy life, work, family)
- May use mobile devices
- Needs SUPPORT and clarity, not gatekeeping

**Pedagogical priorities:**
- Concrete before abstract (real-world examples first)
- Define terms before using them (no assumed knowledge)
- Short sentences, simple structure (reduce cognitive load)
- Multiple representations (graphical, numerical, symbolic)
- Assessment aligned with learning outcomes (test what was taught)

---

## 📋 Specificity Requirements (MANDATORY)

**Every issue MUST include ALL FOUR:**
1. **Line number** - Exact location in XML/readable text
2. **Quoted excerpt** - Verbatim problematic text
3. **Student impact** - How does this hurt the struggling student?
4. **Concrete fix** - Exact wording or structural change needed

**If you can't provide all 4, DON'T FLAG IT.**

---

## ✅ Anti-Pattern Guards (DO NOT FLAG)

### Structural Patterns (CORRECT)
- ✅ Modules with `<LearningOutcomes ids="5.5.1"/>` (they REFERENCE LOs, don't define them)
- ✅ Lessons ~5-10 minutes (intentional chunking)
- ✅ 3-5 scenes in animations (standard)
- ✅ 5-10 follow-up questions (target range)

### Style Patterns (CORRECT per guide)
- ✅ "Ex:" instead of "e.g."
- ✅ "specifically" instead of "i.e."
- ✅ "so" instead of "therefore/thus"
- ✅ Possessives: "function's derivative" (NOT a contraction)

### Assessment Patterns (CORRECT)
- ✅ Multiple choice with 3 choices (intentional)
- ✅ Explanations for ALL choices (including correct answer)

### Out of Scope (DO NOT REVIEW)
- ❌ Images, graphics, visual elements
- ❌ Animations, scenes, figures
- ❌ Visual design, layout, aesthetics

**These are handled by a separate visual reviewer.**

---

## 📁 REORGANIZED STRUCTURE (Nov 11, 2024 - Evening)

### New Folder Organization
```
LEARNVIA/
├── src/           # Modular source code (future)
├── config/        # All configurations
├── modules/       # exemplary/ and test/
├── docs/          # architecture/ and guides/
├── tests/         # Unit tests (future)
├── output/        # Generated reports
├── _deprecated/   # Old files (can delete)
└── Testing/       # Current working directory
```

### Files Moved to _deprecated/
- `archive/` (2.7 MB of obsolete code)
- Backup scripts and test HTML files
- Duplicate modules

## 🔍 Current Status

### ✅ Completed (Session Nov 11, 2024 - Evening)
- **FULL SYSTEM REVIEW** conducted (bottom-up and top-down)
- **CODEBASE_ANALYSIS.md** created (1,063 lines of detailed analysis)
- **Folder reorganization** completed
- **Style agent enhancements** (+3 new detectors)
- **LaTeX rendering** fixed (using $ delimiters)
- **Agent balance** improved (1.4:1 ratio vs 4:1 before)

### ✅ Completed (Session Nov 11, 2024 - Morning)
- LaTeX rendering pipeline fixed (preserves `<m>` and `<me>` tags)
- Line-numbered Original Input tab working
- Workflow diagram colors improved (dark bubbles, white text)
- Successful Power Series review: 157 findings, 15 consensus issues, 5 flagged issues
- Opus exploration of entire codebase completed
- Prompts verified as generic (not hardcoded to Power Series)

### ✅ Completed (Session Nov 11, 2025 - Afternoon)
**CRITICAL: Source Guide Adherence Fixes**

After discovering authoring/style guides were deleted and re-uploaded, conducted comprehensive Opus analysis revealing adherence score of 7.5/10 with critical gaps. Implemented all critical fixes:

**1. Units of Measure (CRITICAL GAP #1)**
- Added complete units table to `style_prompt_rules_v3.xml` (80+ abbreviations across 6 categories)
- Added enforcement criteria to `style_mechanical_compliance.xml` rubric
- Rules: No periods, identical singular/plural, spell out when not preceded by number
- Impact: Agents now flag "5 meters" → "5 m", "2 secs" → "2 sec", etc.

**2. Hint Quality Requirements (CRITICAL GAP #2)**
- Strengthened hint requirements in `authoring_prompt_rules_v3.xml`
- Two-hint minimum now marked MANDATORY with detailed examples
- Added "must concretely lead" principle with good/bad/frustrating examples
- Added explicit prohibitions: no error suggestions, no redirects, declarative form
- Added enforcement to `authoring_assessment_quality.xml` rubric as Severity 4
- Impact: Agents now flag vague hints ("Remember the rules") and missing 2nd hints

**3. Backward Design Alignment (CRITICAL GAP #3)**
- Added backward design principle to `master_review_context_v3.xml`
- 4-step sequence: Exam → Quiz → Homework → Lessons
- Added to `authoring_pedagogical_flow.xml` rubric as Severity 4 criteria
- 4 diagnostic questions for alignment checks
- Impact: Agents now flag tangent content not in homework and homework gaps not in lessons

**4. Seven Common Authoring Mistakes (HIGH PRIORITY)**
- Expanded section in `authoring_prompt_rules_v3.xml` with detailed patterns
- Each mistake has: ID, pattern, description, impact, severity, flag_when guidance
- Includes: too many questions, big jumps, missing conceptual questions, etc.
- Impact: Agents have clear criteria for flagging common pedagogical errors

**Files Modified:** 6 total (3 prompts, 3 rubrics) - All validated as valid XML

**Adherence Score Impact:** 7.5/10 → ~9.0/10 (estimated)

### ⏭️ Immediate Next Steps
- ✅ Run Power Series review with updated prompts (IN PROGRESS)
- Compare before/after review outputs
- Analyze impact on consensus issues and false positive reduction
- Test with another Calc 2 module (Fundamental Theorem available)
- Consolidate System Architecture and Complete Workflow tabs into one

---

## 📊 Success Metrics

**Quality indicators:**
- 95%+ issues have all 4 required components (line #, quote, impact, fix)
- <20% false positive rate (flagged but not actually problematic)
- Zero flagging of correct patterns (anti-patterns)
- Zero flagging of visual elements (out of scope)
- Author feedback: "specific", "actionable", "helpful"

**Genericity indicators:**
- System works on ANY Calc 2 module without code changes
- Prompts contain no hardcoded module-specific content checks
- Detection logic uses universal patterns (undefined terms, vague pronouns, etc.)
- Only exemplary modules referenced are 5.6 and 5.7 (for calibration)

---

## 🗂️ Quick File Reference

### When exploring/brainstorming:
- **This file:** `/Users/michaeljoyce/Desktop/LEARNVIA/CLAUDE_ONBOARDING.md` ⭐
- Explore prompt: `config/prompts/explore_prompt.txt`
- Project README: `README.md`

### When reviewing content:
- Your brain (XML): `config/prompts/claude_live_reviewer_system.xml` ⭐
- Master context: `ACTIVE_CONFIG/v2_master_prompts/master_context.md`
- Authoring rules: `ACTIVE_CONFIG/v2_master_prompts/authoring_rules.md`
- Style rules: `ACTIVE_CONFIG/v2_master_prompts/style_rules.md`

### When running reviews:
- Main script: `Testing/run_review.py`
- Test module: `Testing/Power_Series/power_series_original.xml`
- Latest report: `Testing/Power_Series/output/test_module_review_report_generic.html`

### For pattern learning:
- Exemplar 1: `exemplary_modules/module_5_6_exemplary.xml`
- Exemplar 2: `exemplary_modules/module_5_7_exemplary.xml`
- Human review logs: `exemplary_modules/*.csv`

### Don't waste time on:
- `archive/` - Historical artifacts, not current system
- `.DS_Store`, temp files

---

## 💭 Remember

**Superpowers First**

Always `/superpowers` before starting work. This prevents mistakes.

**Generic > Specific**

The system is only valuable if it works on the NEXT module, not just the test module.

**Patterns > Content**

Extract what makes good pedagogy, not what makes a good Power Series module.

**Quality > Quantity**

Ten specific, actionable issues beat fifty vague observations.

**When in doubt, DON'T FLAG**

You're helping authors improve, not demonstrating your reviewing prowess.

---

## 🧭 Navigation Commands

**Activate superpowers (DO THIS FIRST):**
```
/superpowers
```

**Explore the repository:**
```
/explore
```
Uses `config/prompts/explore_prompt.txt` to map repo and generate prioritized plan.

**Run a review:**
```bash
cd Testing
python run_review.py Power_Series power_series_original.xml power_series_original_readable.txt
```

**Open latest report:**
```bash
open Testing/Power_Series/output/test_module_review_report_generic.html
```

---

**REMEMBER: /superpowers FIRST, THEN WORK. 🚀**
