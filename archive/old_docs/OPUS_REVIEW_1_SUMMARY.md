# Opus Review #1 - Pre-Augmentation Structure Review

## Session Context

This is the **first of two Opus reviews**. We're reviewing the foundation before adding real examples from review logs.

**Current State:**
- ✅ Master review context prompt created
- ✅ Domain prompts exist (authoring & style)
- ✅ 10 rubrics exist (5 authoring, 5 style)
- ✅ 22 real examples extracted and categorized
- ⏳ Real examples NOT YET added to rubrics (waiting for this review)

**Goal:** Validate structure and criteria before augmentation

---

## What Needs Review

### 1. Master Review Context (NEW - Created This Session)

**File:** `config/prompts/master_review_context.txt`

**What it does:**
- Layer 1 of 3-layer architecture
- Provides universal guardrails for ALL reviews
- Excludes visual elements (images/animations) from scope
- Requires specificity (line #, quote, impact, suggestion)
- Enforces chain-of-thought severity assignment
- Contains anti-pattern guards for common false positives
- Sets confidence threshold (0.6 minimum to flag)

**Key Review Questions:**
1. Are the out-of-scope exclusions clear enough to prevent AI from reviewing visuals?
2. Will the 4-component specificity requirement (line, quote, impact, fix) actually prevent vague feedback?
3. Are the anti-pattern guards comprehensive enough?
4. Is the chain-of-thought process well-structured?
5. Is confidence threshold of 0.6 appropriate?

**Priority:** HIGH - This governs everything else

---

### 2. Authoring Rules Prompt

**File:** `config/prompts/authoring_prompt_rules.txt`

**What it does:**
- Layer 2 (domain knowledge)
- Defines 6 core principles: ORGANIZED, CONCISE, PRECISE, INTUITIVE, CONCRETE, INTERACTIVE
- Module/lesson structure requirements
- Critical writing rules
- Learning questions requirements

**Key Review Questions:**
1. Do the 6 principles adequately cover authoring quality?
2. Are structure requirements clear?
3. Do rules support struggling students learning alone?
4. Any missing critical authoring guidance?

**Source:** Derived from `guides/authoring_guide_full.txt`

---

### 3. Style Rules Prompt

**File:** `config/prompts/style_prompt_rules.txt`

**What it does:**
- Layer 2 (domain knowledge)
- Mechanical rules (no contractions, pronouns)
- Mathematical style (LaTeX, notation)
- Accessibility (8th grade level)

**Key Review Questions:**
1. Are mechanical rules clear and checkable?
2. Do LaTeX rules cover common calculus errors?
3. Is "8th grade level" operationalized well enough?
4. Balance between correctness and readability?

**Source:** Derived from `guides/style_guide_full.txt`

---

### 4. Ten Competency Rubrics

**Location:** `config/rubrics/`

**Structure (All follow this):**
```xml
<rubric>
  <metadata>
    <name>Competency Name</name>
    <category>authoring|style</category>
  </metadata>
  
  <evaluation_criteria>
    <severity level="1-5">
      <criteria>
        <criterion>Description</criterion>
      </criteria>
      <examples>
        <example type="violation">Generic example</example>
      </examples>
    </severity>
  </evaluation_criteria>
  
  <diagnostic_questions>
    <question>Guiding question</question>
  </diagnostic_questions>
</rubric>
```

#### Authoring Rubrics (5)

1. **authoring_pedagogical_flow.xml**
   - Focus: Scaffolding, practice, knowledge building
   - Key: Does it catch conceptual jumps? Missing practice?

2. **authoring_structural_integrity.xml**
   - Focus: Organization, chunking, alignment
   - Key: Does it identify structural confusion?

3. **authoring_student_engagement.xml**
   - Focus: Motivation, relevance, interest
   - Key: Distinguishes engagement from entertainment?

4. **authoring_conceptual_clarity.xml**
   - Focus: Definitions, explanations, examples
   - Key: Catches vague/circular definitions?

5. **authoring_assessment_quality.xml**
   - Focus: Questions, hints, explanations
   - Key: Tests understanding vs memorization?

#### Style Rubrics (5)

6. **style_mechanical_compliance.xml**
   - Focus: LaTeX, contractions, formatting
   - Key: Rules specific enough to check?

7. **style_mathematical_formatting.xml**
   - Focus: Mathematical notation, LaTeX
   - Key: Covers common calculus LaTeX errors?

8. **style_punctuation_grammar.xml**
   - Focus: Grammar, punctuation, sentences
   - Key: Balances correctness with readability?

9. **style_accessibility.xml**
   - Focus: Reading level, inclusive language
   - Key: Operationalizes 8th grade level?

10. **style_consistency.xml**
    - Focus: Terminology, voice, formatting
    - Key: Meaningful inconsistencies vs nitpicking?

**For Each Rubric, Review:**
1. XML structure valid?
2. Severity criteria (1-5) clear and distinct?
3. Diagnostic questions guide reviewers effectively?
4. Current examples (generic) helpful?
5. Ready to receive real examples from logs?

---

## Cross-Cutting Review Questions

After reviewing individual components:

1. **Alignment:** Do all three layers work together coherently?
2. **Conflicts:** Any contradictory instructions across components?
3. **Completeness:** Missing critical competencies or guidance?
4. **Usability:** Will AI reviewers be able to follow combined guidance?
5. **Balance:** Over-specified or under-specified?

---

## Available Reference Materials

**For context during review:**

1. **`docs/OPUS_REVIEW_PACKAGE.md`** - Detailed review criteria and process
2. **`docs/categorized_examples_from_logs.md`** - 22 real examples ready to add
3. **`docs/layered_prompt_architecture.md`** - System architecture overview
4. **`docs/implementation_next_steps.md`** - What happens after this review
5. **`guides/authoring_guide_full.txt`** - Source document for authoring rules
6. **`guides/style_guide_full.txt`** - Source document for style rules

---

## Expected Outputs

For each reviewed component, please provide:

### Overall Assessment
- **Ready** (no changes needed)
- **Minor Fixes** (small adjustments, can proceed)
- **Major Revision** (significant issues, blocks progress)

### Specific Issues
- Line numbers or section references
- What's wrong/missing/unclear
- Why it matters

### Recommendations
- Concrete suggestions for improvement
- Alternative approaches if applicable

### Priority
- **High** (blocks adding examples and testing)
- **Medium** (should fix but not blocking)
- **Low** (nice-to-have, future improvement)

---

## After This Review

**Immediate next steps:**
1. Address High priority issues
2. Incorporate Medium priority suggestions  
3. Add real examples from `categorized_examples_from_logs.md` to rubrics
4. Second Opus review of complete system with examples
5. Then test on NEW unreviewed modules

---

## Key Constraint Reminder

**Visual elements (images, animations, graphs) are OUT OF SCOPE for text reviewers.**

This is critical. A separate specialized model handles visual review. Text reviewers must NEVER comment on:
- Image quality or clarity
- Animation pacing or transitions
- Graph formatting or visual design
- Figure labels or visual annotations
- Color choices or aesthetics

Ensure all prompts/rubrics clearly enforce this boundary.

---

## Questions for Reviewer

As you review, please also consider:

1. Are we missing any critical competencies for calculus content?
2. Do severity definitions (1-5) make sense for educational content?
3. Will these prompts help or confuse AI reviewers (Sonnet-level)?
4. Are we appropriately calibrated for struggling students learning alone?
5. What would make these components more effective?

---

## Review Approach Suggestion

**Recommended order:**

1. Start with **master_review_context.txt** (governs everything)
2. Then **authoring_prompt_rules.txt** and **style_prompt_rules.txt**
3. Then **rubrics** (can sample rather than all 10 if similar)
4. Finally **cross-cutting analysis**

**Time estimate:** 30-60 minutes for thorough review

---

## Ready to Begin

All files are in place and committed to git. The repository is on branch `feature/evaluate_real_examples`.

**Primary files to review:**
- `config/prompts/master_review_context.txt` (NEW, 199 lines)
- `config/prompts/authoring_prompt_rules.txt` (existing)
- `config/prompts/style_prompt_rules.txt` (existing)
- `config/rubrics/*.xml` (10 files, existing)

Thank you for the expert review!
