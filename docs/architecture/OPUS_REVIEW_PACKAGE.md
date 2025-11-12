# Opus Review Package - Prompt & Rubric Quality Evaluation

## Purpose

This document identifies all prompts and rubrics that need expert (Opus) evaluation before we proceed with testing on new modules. These components form the foundation of our AI review system and must be solid.

## Review Criteria

For each component, evaluate:
1. **Clarity** - Are instructions unambiguous?
2. **Completeness** - Are there gaps or missing cases?
3. **Consistency** - Do components align with each other?
4. **Actionability** - Will this produce specific, useful feedback?
5. **Pedagogical Soundness** - Do these serve struggling calculus students?

---

## Components for Review

### Layer 1: Master Review Context

**File:** `config/prompts/master_review_context.txt`

**Purpose:** Universal guardrails for ALL reviews

**Key Questions:**
- Are the out-of-scope exclusions (images/animations) clear enough?
- Do the specificity requirements (line #, quote, impact, fix) cover all bases?
- Are the anti-pattern guards comprehensive?
- Will the chain-of-thought requirement actually prevent arbitrary judgments?
- Is the confidence scoring threshold (0.6) appropriate?

**Status:** Created in this session, needs validation

---

### Layer 2: Domain Prompts

#### Authoring Rules

**File:** `config/prompts/authoring_prompt_rules.txt`

**Purpose:** Pedagogical and structural guidelines

**Key Questions:**
- Do the 6 core principles (ORGANIZED, CONCISE, PRECISE, INTUITIVE, CONCRETE, INTERACTIVE) adequately cover authoring quality?
- Are the module/lesson structure requirements clear?
- Do the critical writing rules support struggling students?
- Is anything missing that would help AI reviewers catch pedagogical issues?

**Status:** Exists, derived from guides/authoring_guide_full.txt

---

#### Style Rules

**File:** `config/prompts/style_prompt_rules.txt`

**Purpose:** Writing mechanics and formatting

**Key Questions:**
- Are mechanical rules (contractions, pronouns) clearly stated?
- Do mathematical style rules cover LaTeX, functions, fractions adequately?
- Are accessibility requirements (8th grade level) operationalized?
- Will these rules help or hinder readability?

**Status:** Exists, derived from guides/style_guide_full.txt

---

### Layer 3: Competency Rubrics

All rubrics follow this structure:
```xml
<rubric>
  <metadata>
    <name>Competency Name</name>
    <category>authoring|style</category>
  </metadata>
  
  <evaluation_criteria>
    <severity level="1-5">
      <criteria>...</criteria>
      <examples>...</examples>
    </severity>
  </evaluation_criteria>
  
  <diagnostic_questions>...</diagnostic_questions>
</rubric>
```

#### Authoring Rubrics (5 total)

1. **`config/rubrics/authoring_pedagogical_flow.xml`**
   - Focus: Scaffolding, practice opportunities, knowledge building
   - Questions: Does it catch conceptual jumps? Missing practice?

2. **`config/rubrics/authoring_structural_integrity.xml`**
   - Focus: Organization, chunking, alignment
   - Questions: Does it identify structural problems that confuse students?

3. **`config/rubrics/authoring_student_engagement.xml`**
   - Focus: Motivation, relevance, interest
   - Questions: Does it distinguish engagement from entertainment?

4. **`config/rubrics/authoring_conceptual_clarity.xml`**
   - Focus: Definitions, explanations, examples
   - Questions: Does it catch vague or circular definitions?

5. **`config/rubrics/authoring_assessment_quality.xml`**
   - Focus: Questions, hints, explanations, feedback
   - Questions: Does it evaluate whether questions test understanding vs memorization?

#### Style Rubrics (5 total)

6. **`config/rubrics/style_mechanical_compliance.xml`**
   - Focus: LaTeX, contractions, formatting errors
   - Questions: Are rules specific enough to be checkable?

7. **`config/rubrics/style_mathematical_formatting.xml`**
   - Focus: Mathematical notation, LaTeX consistency
   - Questions: Does it cover common LaTeX errors in calculus?

8. **`config/rubrics/style_punctuation_grammar.xml`**
   - Focus: Grammar, punctuation, sentence structure
   - Questions: Does it balance correctness with readability?

9. **`config/rubrics/style_accessibility.xml`**
   - Focus: Reading level, inclusive language, clarity
   - Questions: Does it operationalize "8th grade level"?

10. **`config/rubrics/style_consistency.xml`**
    - Focus: Terminology, voice, formatting consistency
    - Questions: Does it catch meaningful inconsistencies vs nitpicking?

---

## Review Process

### Step 1: Master Prompt Review

Start with `master_review_context.txt` since it governs everything else:
1. Read completely
2. Identify ambiguities or gaps
3. Check if anti-pattern guards cover common false positives
4. Verify severity guidance makes sense

### Step 2: Domain Prompt Review

Review both authoring and style prompts:
1. Check alignment with master prompt
2. Verify no contradictions
3. Assess completeness for their domains
4. Ensure they support the 6 core principles

### Step 3: Rubric Review

For each of the 10 rubrics:
1. Verify XML structure is valid
2. Check severity levels have clear criteria
3. Confirm diagnostic questions guide reviewers effectively
4. Assess if examples (when present) are helpful

### Step 4: Cross-Component Check

After individual reviews:
1. Do all components work together?
2. Are there conflicting instructions?
3. Do the layers properly build on each other?
4. Will an AI reviewer be able to follow the combined guidance?

---

## Outputs Needed

For each reviewed component, provide:

1. **Overall Assessment:** Ready / Needs Minor Fixes / Needs Major Revision
2. **Specific Issues:** Line numbers or section references with problems
3. **Recommendations:** Concrete suggestions for improvement
4. **Priority:** High (blocks testing) / Medium (should fix) / Low (nice-to-have)

---

## Context for Reviewer

**Target Audience:** Non-traditional calculus students studying alone at home with low confidence

**Review Goals:**
- Help authors improve content (not gatekeep)
- Provide specific, actionable feedback
- Focus on student learning outcomes
- Avoid false positives that waste author time

**Key Constraint:** Visual elements (images, animations) are reviewed separately - text reviewers should NEVER comment on these

---

## Next Steps After Review

1. Address High priority issues immediately
2. Incorporate Medium priority suggestions
3. Note Low priority items for future improvement
4. Then proceed to: Extract real examples from 5.6/5.7 logs and populate rubrics
5. Finally: Test system on NEW, unreviewed modules

---

## Questions for Opus

As you review, please consider:
1. Are we missing any critical competencies?
2. Do severity definitions make sense for educational content?
3. Will these prompts help or confuse AI reviewers?
4. Are we over-specifying or under-specifying?
5. What would make these components more effective?
