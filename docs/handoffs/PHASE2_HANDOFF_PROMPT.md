# PHASE 2 HANDOFF PROMPT
**Use this to start your next Claude Code session**

---

## CONTEXT FOR NEW CLAUDE SESSION

I need help continuing the LEARNVIA AI-Powered Content Revision System pilot.

### What's Been Completed

**Phase 1 POC Test (COMPLETE):**
- ✅ Ran Pass 1: 5 authoring + 5 style reviewers on Module 3.4
- ✅ Ran Pass 2: Different 5 authoring + 5 style reviewers (same module)
- ✅ Generated comprehensive comparison analysis
- ✅ Created POC Phase 1 Report

**Key Finding:** Technical architecture validated, but we skipped the author revision step between passes (workflow deviation).

**Files to Read:**
1. `/Users/michaeljoyce/Desktop/LEARNVIA/POC_PHASE1_REPORT.md` - Complete findings
2. `/Users/michaeljoyce/Desktop/LEARNVIA/module_examples/Module 3.4 Basic Rules of Finding Derivatives.txt` - Test module

---

## WHERE WE ARE NOW

**Status:** Phase 1 POC Complete, awaiting Phase 2 decision

**Immediate Next Steps (Priority Order):**

### Option A: Expert Validation (RECOMMENDED FIRST)
```
Help me prepare materials for expert validation of the 21 flagged issues:
- Extract all issues into validation-friendly format
- Create expert review form/checklist
- Calculate preliminary metrics once expert provides input
```

### Option B: Fix Critical Issues
```
Help me fix the 3 critical LaTeX errors identified:
- Close unclosed tags (Lines 130, 131, 136, 137, 141, 142, 154, 155, 296, 338, 518, 535)
- Correct syntax Line 105
- Complete limit Line 171

Then we can test Pass 3-4 on the REVISED module.
```

### Option C: Phase 2 Planning
```
Help me plan Phase 2 proper workflow testing:
- Select 3-5 diverse modules for testing
- Design workflow tracking
- Prepare author materials
- Define success metrics
```

### Option D: Different Module Test
```
I have another module to test. Let's run Pass 1 only to see if
patterns hold across different content types.
```

---

## SYSTEM REMINDERS

**Core Architecture:**
- 4-pass independent review (we tested passes 1-2 only)
- 10 authoring + 10 style per pass in production (we used 5+5 for POC)
- Strict separation: authoring reviewers see ONLY pedagogical guidelines
- Student-success framing: "The module demonstrates..." not "You did..."

**Proper Workflow (Not Tested Yet):**
```
Pass 1 Review → Author Revises → Pass 2 Review (on revised version) → Human Checkpoint
```

**POC Workflow (What We Actually Tested):**
```
Pass 1 Review → [SKIPPED REVISION] → Pass 2 Review (on same version)
```

**Key Files:**
- System docs: `/Users/michaeljoyce/Desktop/LEARNVIA/README.md`
- Authoring guidelines: `/Users/michaeljoyce/Desktop/LEARNVIA/authoring_prompt_rules.txt`
- Style guidelines: `/Users/michaeljoyce/Desktop/LEARNVIA/style_prompt_rules.txt`
- Product vision: `/Users/michaeljoyce/Desktop/LEARNVIA/product_vision_context.txt`

---

## WHAT TO TELL THE NEW CLAUDE SESSION

**Copy and paste this:**

```
I'm continuing work on the LEARNVIA AI-Powered Content Revision System.

Phase 1 POC is complete. Please read:
- /Users/michaeljoyce/Desktop/LEARNVIA/POC_PHASE1_REPORT.md
- /Users/michaeljoyce/Desktop/LEARNVIA/PHASE2_HANDOFF_PROMPT.md (this file)

Then help me with [choose option A, B, C, or D from above].
```

---

## IMPORTANT NOTES

**Token Budget:**
- Phase 1 used ~10% of weekly Claude Max allowance
- Full 4-pass on 1 module ≈ 15-20% of allowance
- Plan accordingly for Phase 2 work

**Workflow Deviation:**
- Phase 1 skipped author revision between passes
- This creates appearance of inconsistency (same errors in both passes)
- Next phase MUST include proper workflow with revisions

**Success Criteria for Phase 2:**
- Precision ≥ 80% (validated by expert)
- Recall ≥ 85% (estimated from expert review)
- Critical miss rate < 10%
- Authors report supportive experience

---

## QUICK REFERENCE: ISSUES FOUND

**Critical (All Validated):**
1. Unclosed LaTeX tags (12+ instances)
2. LaTeX syntax error Line 105
3. Incomplete limit Line 171

**High Severity (Validated):**
4. Contraction "we'll"
5. Dfrac usage
6. Missing concrete examples
7. Lesson too long

**High Severity (Pass 2 Only):**
8. Cognitive overload
9. Difficulty jump

**Medium/Low:** 10-21 additional issues

---

**Last Updated:** October 30, 2025
**Next Action:** Choose Option A, B, C, or D above
