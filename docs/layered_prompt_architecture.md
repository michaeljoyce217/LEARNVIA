# Layered Prompt Architecture

## Overview

The AI review system uses a 3-layer prompt architecture to improve review quality through:
1. **Master guardrails** - Specificity, anti-patterns, severity calibration
2. **Domain guidelines** - Authoring and style rules
3. **Competency rubrics** - Specific evaluation criteria

**Key Constraint:** Visual elements (images, animations) are excluded from text review scope.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Master Review Context                         │
│  ─────────────────────────────────────────────────────  │
│  • Out of scope (images/animations)                     │
│  • Content structure facts                              │
│  • Specificity requirements (line, quote, impact, fix)  │
│  • Chain-of-thought severity assignment                 │
│  • Anti-pattern guards (correct patterns)               │
│  • Confidence scoring (≥0.6 to flag)                    │
│                                                          │
│  Purpose: Establish guardrails for ALL reviews          │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 2: Domain Prompts                                │
│  ─────────────────────────────────────────────────────  │
│  Authoring Rules:                                       │
│  • 6 core principles (ORGANIZED, CONCISE, etc.)         │
│  • Module/lesson structure requirements                 │
│  • Critical writing rules (no synonyms, simple sent.)   │
│  • Learning questions design                            │
│                                                          │
│  Style Rules:                                           │
│  • Mechanical rules (no contractions, pronouns)         │
│  • Mathematical style (LaTeX, functions, fractions)     │
│  • Accessibility (8th grade level, inclusive language)  │
│                                                          │
│  Purpose: Provide domain-specific guidelines            │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 3: Competency Rubrics                            │
│  ─────────────────────────────────────────────────────  │
│  15 rubrics covering:                                   │
│  • Pedagogical Flow (scaffolding, practice)             │
│  • Structural Integrity (organization, chunking)        │
│  • Student Engagement (motivation, relevance)           │
│  • Conceptual Clarity (definitions, examples)           │
│  • Assessment Quality (questions, feedback)             │
│  • Mathematical Accuracy (correctness, precision)       │
│  • Language Accessibility (reading level, clarity)      │
│  • (8 more...)                                          │
│                                                          │
│  Each rubric:                                           │
│  • Severity criteria (1-5) with real examples           │
│  • Diagnostic questions                                 │
│  • Good practices and failure modes                     │
│                                                          │
│  Purpose: Evaluate specific competency dimensions       │
└─────────────────────────────────────────────────────────┘
```

## Component Details

### Layer 1: Master Review Context

**File:** `config/prompts/master_review_context.txt`

**Critical Sections:**

1. **Out of Scope** - Explicitly excludes:
   - Images, graphics, visual elements
   - Animated figures and animations
   - Static figures and diagrams
   - Scene transitions, visual design

   *Rationale:* Separate specialized model handles visual review

2. **Content Structure Facts** - Prevents misconceptions:
   - Modules reference LOs, don't define them
   - Lessons contain questions, not homework
   - Standard structures are intentional (3-5 scenes, 5-10 questions)

3. **Specificity Requirements** - Every issue MUST have:
   - Line number(s)
   - Quoted excerpt (verbatim)
   - Student impact explanation
   - Concrete suggestion (specific wording)

   *Rationale:* Forces actionable feedback, eliminates vague opinions

4. **Chain-of-Thought** - Before severity assignment:
   - Quote text + line number
   - Explain rule violation
   - Explain student impact
   - Propose fix
   - THEN assign severity

   *Rationale:* Prevents intuitive/arbitrary severity judgments

5. **Anti-Pattern Guards** - Explicit "DO NOT FLAG" list:
   - Correct structural patterns (LO references, short lessons)
   - Style guide compliance (Ex: not e.g., "so" not "therefore")
   - Pedagogical patterns (simple before complex examples)
   - Assessment patterns (3 MC choices, leading hints)

   *Rationale:* Eliminates false positives from common misconceptions

6. **Confidence Scoring** - Threshold: ≥0.6 to flag
   - 1.0 = Unambiguous violation
   - 0.8 = Clear violation, minor interpretation
   - 0.6 = Violation with guideline flexibility
   - <0.6 = Do not flag

   *Rationale:* Reduces noise from uncertain judgments

### Layer 2: Domain Prompts

**Authoring Rules:** `config/prompts/authoring_prompt_rules.txt`

Key principles:
- ORGANIZED: Chunking, scaffolding, alignment
- CONCISE: Simplest words and explanations
- PRECISE: No synonyms/homonyms, no vague references
- INTUITIVE: Clearest illustrations and explanations
- CONCRETE: Student-relevant examples throughout
- INTERACTIVE: Frequent short activities

**Style Rules:** `config/prompts/style_prompt_rules.txt`

Key mechanics:
- No contractions (what's → what is)
- Restricted imperative voice
- No pronouns (you, it, they)
- LaTeX for all math/numerals
- Serial comma always
- 8th grade reading level

### Layer 3: Competency Rubrics

**Location:** `config/rubrics/*.xml`

**Structure:**
```xml
<rubric>
  <metadata>
    <name>Competency Name</name>
    <category>authoring|style</category>
    <version>1.0</version>
  </metadata>

  <evaluation_criteria>
    <severity level="5|4|3|2|1">
      <criteria>
        <criterion>Description</criterion>
      </criteria>
      <examples>
        <example type="violation">Generic example</example>
        <example type="real" source="human_review_log">
          Actual issue from module 5.6/5.7 review
        </example>
      </examples>
    </severity>
  </evaluation_criteria>

  <diagnostic_questions>
    <question>Guiding question for reviewers</question>
  </diagnostic_questions>
</rubric>
```

**Real Examples:** Sourced from human review logs for severity calibration

## Exemplar Grounding

**Fully Reviewed Modules:**
- `modules/module_5.6_exemplary.xml` - The definite integral (~270KB)
- `modules/module_5.7_exemplary.xml` - Net Change Theorem

**Human Review Logs:**
- `modules/Chapter 5 Review Log - 5.6 Beta.csv`
- `modules/Chapter 5 Review Log - 5.6 CE + Other.csv`
- `modules/Chapter 5 Review Log - 5.7 Beta.csv`
- `modules/Chapter 5 Review Log - 5.7 CE + Other.csv`

**Usage:**
1. Extract good catches → inform severity examples
2. Extract false positives → add to anti-pattern guards
3. Extract severity distribution → calibrate severity scale
4. Separate visual issues → confirm out-of-scope items

## Iteration Process

```
┌─────────────────────┐
│  Run AI Review      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  Compare with Human Review Log  │
└──────┬──────────────────────────┘
       │
       ├─────────────────────┐
       │                     │
       ▼                     ▼
┌─────────────────┐   ┌─────────────────┐
│  False          │   │  False          │
│  Positives      │   │  Negatives      │
└──────┬──────────┘   └──────┬──────────┘
       │                     │
       ▼                     ▼
┌─────────────────┐   ┌─────────────────┐
│  Update Anti-   │   │  Add Severity   │
│  Pattern Guards │   │  Examples       │
└──────┬──────────┘   └──────┬──────────┘
       │                     │
       └─────────┬───────────┘
                 │
                 ▼
       ┌─────────────────┐
       │  Re-run Review  │
       └──────┬──────────┘
              │
              ▼
       ┌─────────────────┐      Yes    ┌─────────────────┐
       │  Metrics        │────────────▶│  Test Next      │
       │  Improved?      │              │  Module         │
       └──────┬──────────┘              └──────┬──────────┘
              │ No                             │
              └────────────────────────────────┘
                                               │
                                               ▼
                                        ┌─────────────────┐
                                        │  Production     │
                                        │  Ready?         │
                                        └──────┬──────────┘
                                               │ Yes
                                               ▼
                                        ┌─────────────────┐
                                        │  Deploy         │
                                        └─────────────────┘
```

**Metrics to Track:**
- False positive rate (target: <20%)
- Specificity compliance (target: >95% with all 4 components)
- Severity alignment (target: >70% within ±1 level)
- Visual scope compliance (target: 100% no visual issues flagged)

## Usage Guide

### Running a Review

```bash
# Single module review
python scripts/test_sonnet_review.py \
  --module modules/your_module.xml \
  --output outputs/review_results.json
```

### Comparing with Human Review

```bash
# Compare AI vs human
python scripts/compare_reviews.py \
  --ai outputs/review_results.json \
  --human "modules/Your Review Log.csv" \
  --output docs/comparison.md
```

### Full Iteration Test

```bash
# Automated pipeline
./scripts/run_iteration_test.sh \
  modules/module_5.6_exemplary.xml \
  "modules/Chapter 5 Review Log - 5.6 Beta.csv"
```

## Design Rationale

**Why 3 layers?**
- Layer 1 (Master): Universal guardrails prevent common failure modes
- Layer 2 (Domain): Subject expertise without repetition across rubrics
- Layer 3 (Rubrics): Specific evaluation criteria for targeted competencies

**Why specificity requirements?**
- Vague feedback is not actionable for authors
- Specificity forces reviewers to engage with actual content
- Line numbers + quotes make issues verifiable

**Why chain-of-thought?**
- Prevents arbitrary severity inflation/deflation
- Forces explicit reasoning
- Makes severity judgments auditable

**Why anti-pattern guards?**
- Most false positives come from misconceptions about correct patterns
- Explicit "do not flag" list eliminates entire classes of errors
- Grounded in real false positives from human review logs

**Why exclude visual elements?**
- Requires different evaluation criteria (composition, clarity, accessibility)
- Better handled by specialized vision model
- Prevents text reviewers from commenting on aspects they can't fully evaluate

## Results

**Baseline (before implementation):**
- Confidence: 25-32%
- Many false positives (missing LOs, etc.)
- Vague feedback without line numbers
- Visual elements incorrectly flagged

**Expected After Implementation:**
- Confidence: >60% (threshold enforcement)
- False positive rate: <20%
- 95%+ specificity compliance
- Zero visual elements flagged

**To Be Measured:** Run iteration tests and populate actual metrics

## Next Steps

See `docs/implementation_next_steps.md` for detailed task list.

**Immediate priorities:**
1. Create test review scripts (test_sonnet_review.py, compare_reviews.py)
2. Run first iteration test with module 5.6
3. Extract false positive patterns and refine master prompt
4. Run second iteration with module 5.7
5. Document improvement metrics

## Integration with Multi-Agent System

The layered prompt architecture integrates with the existing agent configuration (`config/agent_configuration.xml`):

**Agent Pool Structure:**
- 76 total agents across 4 passes
- 60% rubric-focused (assigned specific competencies)
- 40% generalists (holistic review)

**Prompt Assignment:**
- All agents receive Layer 1 (Master Context)
- All agents receive Layer 2 (Domain Rules)
- Rubric-focused agents receive Layer 3 (Specific Rubric)
- Generalists receive all rubrics for holistic evaluation

**Consensus Mechanism:**
- Cross-validation bonus when rubric-focused AND generalist agents agree
- Severity escalation when multiple agents flag same area
- Confidence threshold: 0.7 for automatic fixes, <0.6 escalates to human review

This ensures consistency while leveraging specialized and generalist perspectives.
