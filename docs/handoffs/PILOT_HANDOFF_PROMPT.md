# HANDOFF PROMPT FOR PILOT PHASE
**Use this to start your next Claude Code session**

---

## CONTEXT FOR NEW CLAUDE SESSION

I need you to help me run a controlled pilot of the Learnvia AI-Powered Content Revision System.

### IMPORTANT: Read the entire codebase first
Please start by reading all files in `/Users/michaeljoyce/Desktop/LEARNVIA` to understand:
- The 4-pass review architecture (Pass 1-2: content review, Pass 3-4: copy edit)
- How the 60 AI agents are configured (10 authoring + 10 style per content pass, 10 style per copy pass)
- The feedback loop mechanisms
- The current implementation state

### System Summary
This is a working AI content review system that:
- Uses 60 AI agents across 4 independent passes
- Provides consensus-based confidence scoring
- Only suggests solutions when high severity + high confidence
- Has dual feedback loops to prevent system degradation
- Currently uses mock API (needs real OpenAI validation)
- All tests passing (100% coverage)

### Current Status
✓ Core system complete and tested
✓ 4-pass workflow implemented
✓ Strict separation: 10 authoring agents (pedagogy only) + 10 style agents (mechanics only) in passes 1-2
✗ No real-world testing yet
✗ No OpenAI API cost validation
✗ No actual Learnvia module reviews

---

## PILOT OBJECTIVES

### Primary Goals
1. **Validate with Real OpenAI API**: Switch from mock to real API, measure costs
2. **Test with 5-10 Real Modules**: Run complete 4-pass reviews on actual Learnvia content
3. **Measure Accuracy**: Calculate precision (80%+ target), recall (85%+ target), critical miss rate (<10% target)
4. **Evaluate Coverage**: Identify any systematic gaps in issue detection
5. **Author Experience**: Gather feedback on supportiveness and clarity
6. **Reviewer Time Savings**: Measure actual workload reduction (target 50%+ conservative)

### Secondary Goals
7. **Evaluate Agent Diversity Need**: Determine if current focus-only approach covers all issue categories, or if persona-based diversity would help
8. **Cost Analysis**: Calculate actual per-review costs, identify optimization opportunities
9. **Prompt Refinement**: Adjust based on false positives/negatives
10. **Guideline Contradiction Tracking**: Manually tag each dispute/adjustment with which guideline it contradicts (authoring/style/both/neither) to inform future enhancement

---

## PILOT EXECUTION STEPS

### Phase 1: API Setup & Initial Test (Day 1)
1. Configure real OpenAI API key (replace mock)
2. Run 1 simple test module through Pass 1 only
3. Measure token usage and cost
4. Validate output quality
5. Fix any integration issues

### Phase 2: Full 4-Pass Test (Days 2-3)
1. Select 1 representative module
2. Run complete 4-pass workflow
3. Time each pass
4. Calculate total cost
5. Review all generated reports
6. Document any issues or gaps

### Phase 3: Pilot Batch (Days 4-10)
1. Select 5-10 diverse modules:
   - Mix of difficulty levels
   - Different mathematical topics
   - Various author experience levels
2. Run all through complete 4-pass workflow
3. Human reviewers validate each checkpoint
4. Track disputes and model failures
5. Feed data into feedback loops

### Phase 4: Analysis & Recommendations (Days 11-14)
1. Calculate accuracy metrics:
   - Precision: True positives / (True positives + False positives)
   - Recall: True positives / (True positives + False negatives)
   - Critical miss rate: Critical issues missed / Total critical issues
2. Analyze coverage gaps:
   - Are certain issue types systematically missed?
   - Would persona diversity help? (e.g., "mathematics education expert", "struggling learner advocate")
3. Cost analysis:
   - Average cost per review
   - Cost per issue found
   - ROI calculation
4. Author interviews:
   - Was feedback supportive?
   - Did confidence scores help prioritization?
   - Were suggestions actionable?
5. Generate recommendations report

---

## KEY FILES TO UNDERSTAND

**Core System:**
- `src/orchestrator.py` - 4-pass workflow orchestration
- `src/reviewers.py` - 60 AI agent configuration (10+10+10+10 structure)
- `src/models.py` - Data models, ReviewPass enum
- `src/aggregator.py` - Consensus scoring algorithm
- `src/report_generator.py` - Output generation (conditional suggestions)
- `src/feedback_loop.py` - False positive handling
- `src/reviewer_feedback_loop.py` - False negative handling

**Configuration:**
- `authoring_prompt_rules.txt` - Pedagogical guidelines (71 lines)
- `style_prompt_rules.txt` - Mechanical/style rules (99 lines)
- `product_vision_context.txt` - Target learner context (88 lines)

**Testing:**
- `run_tests.py` - Main test runner
- `tests/` - Comprehensive test suite

**Tools:**
- `dispute_issue.py` - Author dispute interface
- `validate_disputes.py` - Reviewer validation interface
- `log_missed_issues.py` - False negative logging

---

## CRITICAL DESIGN PRINCIPLES (DON'T VIOLATE)

1. **No Information Transfer Between Passes**: Each pass uses completely different agents with no knowledge of previous passes
2. **Conditional Suggestions Only**: Suggestions ONLY when high severity (4-5) AND high confidence (≥70%)
3. **Content-Focused Feedback**: "The module demonstrates..." NOT "You did..."
4. **Strict Separation in Passes 1-2**: 10 agents ONLY authoring, 10 agents ONLY style (no mixing)
5. **Human Final Authority**: Humans always have final say, AI is advisory only

---

## POST-PILOT ENHANCEMENT DECISIONS

### Enhancement 1: Persona Diversity

**Current Approach:**
- Focus-area only (e.g., "pedagogical_flow", "scaffolding")
- All agents have similar "voice"

**Potential Enhancement:**
Add light persona framing to authoring agents (NOT style agents):
- "You have expertise in mathematics education"
- "You specialize in supporting struggling learners"
- "You focus on cognitive load and chunking"
- "You prioritize conceptual understanding over procedures"

**Decision Criteria:**
- If pilot shows systematic gaps in issue categories → Implement personas
- If current approach achieves 85%+ recall → Keep focus-only approach
- Style agents remain focus-only (objective, no benefit from personas)

**Implementation Note:**
This is a simple prompt_variation change in `src/reviewers.py` lines 390-395 (authoring agents). Do NOT implement until pilot data supports it.

---

### Enhancement 2: Pre-Review Dispute & Automated Feedback Loop

**Current System:**
- Authors can dispute AI feedback AFTER they see it
- Human reviewers validate disputes during checkpoint
- Feedback loop collects patterns and suggests refinements
- System exists but could be enhanced

**Future Enhancement (Post-Pilot Implementation):**

**Phase 1: Pre-Review Dispute Interface**
- Add "Actually Correct" button to author interface
- Authors mark AI flags as incorrect BEFORE human review
- Author provides explanation for why it's actually correct
- Pre-disputes forwarded to human reviewer with context

**Phase 2: Revision Tracking for Reviewers**
- Human reviewer sees THREE things:
  1. AI suggestions (what AI flagged)
  2. Author revisions (what author changed)
  3. Author pre-disputes (what author marked as "actually correct")
- Reviewer can validate or override each

**Phase 3: Severity Adjustment**
- Reviewer can mark AI suggestions as:
  - "Not a misalignment" (false positive)
  - "Less severe than AI claimed" (e.g., severity 4 → severity 2)
- Each adjustment MUST be tagged: Which guideline does this contradict?
  - Authoring guideline
  - Style guideline
  - Both
  - Neither (guideline ambiguous or incomplete)

**Phase 4: Intelligent Feedback Loop Enhancement**
- System tracks patterns in:
  - Validated "actually correct" disputes
  - Severity adjustments
  - Guideline contradiction tags
- When pattern threshold reached (5+ similar cases, 2+ for critical):
  - System generates principle-based refinement suggestion
  - Refinement tagged by guideline source
  - Initially: Human reviews and approves all refinements
  - Future: Automated application with human oversight

**Phase 5: Prompt Creep Prevention (Critical)**
- Before applying any refinement:
  - Check for contradictions with existing guidelines
  - Flag contradictions for human resolution
  - Prefer updating existing principle over adding new rule
- Periodic prompt audits (monthly):
  - Consolidate redundant rules
  - Simplify complex rules into principles
  - Remove obsolete exceptions
- Hard limit: Maximum prompt length enforced
- Principle-based refinements replace individual exceptions

**Why This Matters:**
1. **Faster Feedback:** Authors dispute immediately, not after waiting for human review
2. **Better Data:** Reviewers see author intent, making validation more accurate
3. **Contradiction Prevention:** Guideline tagging catches conflicts before they corrupt prompts
4. **Scalable Learning:** Patterns across many reviews inform systematic improvements
5. **Maintains Simplicity:** Principle-based, not exception-based (prevents prompt bloat)

**Implementation Timeline:**
- Pilot Phase: Current system (dispute after viewing)
- Post-Pilot Phase 1: Pre-review dispute button (2 weeks dev)
- Post-Pilot Phase 2: Revision tracking interface (2 weeks dev)
- Post-Pilot Phase 3: Severity adjustment + guideline tagging (1 week dev)
- Post-Pilot Phase 4: Enhanced pattern tracking (2 weeks dev)
- Post-Pilot Phase 5: Contradiction detection + prompt audits (2 weeks dev)

**Pilot Action:**
During pilot, manually track which guideline (authoring/style/both) each dispute relates to. This data will inform Phase 3 implementation.

---

## SUCCESS CRITERIA

**Proceed to Production If:**
✓ Precision ≥ 80% (AI correctness)
✓ Recall ≥ 85% (AI completeness)
✓ Critical miss rate < 10%
✓ Authors report supportive experience (qualitative)
✓ Reviewers report 50%+ time savings
✓ Cost per review is acceptable (<$X, define based on budget)

**Run Second Pilot If:**
- Metrics close but not quite hitting targets (75-79% precision, 80-84% recall)
- Persona enhancement may close the gap
- Prompt refinement needed

**Back to Drawing Board If:**
- Precision < 75% (too many false positives)
- Recall < 75% (missing too many real issues)
- Critical miss rate > 15%
- Cost per review prohibitively expensive

---

## QUESTIONS TO ANSWER DURING PILOT

1. **Accuracy**: Do we hit 80% precision, 85% recall targets?
2. **Coverage**: Are there systematic blind spots? Would personas help?
3. **Cost**: What's the actual per-review cost? Is it sustainable?
4. **Experience**: Do authors find feedback supportive and actionable?
5. **Efficiency**: Do reviewers save 50%+ time?
6. **Feedback Loops**: Do they successfully identify patterns?
7. **Confidence Scoring**: Does consensus mechanism work as expected?
8. **Conditional Suggestions**: Are high severity + high confidence suggestions accurate?

---

## EXPECTED DELIVERABLES

At end of pilot, produce:

1. **Metrics Report**:
   - Precision, recall, critical miss rate
   - Per-pass accuracy breakdown
   - Coverage gap analysis
   - Cost analysis

2. **Recommendations Document**:
   - Go/No-Go decision for production
   - Persona diversity recommendation (implement or skip)
   - Prompt refinements needed
   - Agent count adjustments (if needed)
   - Cost optimization strategies

3. **Author Feedback Summary**:
   - Quotes from author interviews
   - Supportiveness ratings
   - Actionability ratings
   - Suggested improvements

4. **Technical Adjustments List**:
   - Any bugs found
   - Integration improvements needed
   - Performance optimizations

---

## GETTING STARTED

**BEST PRACTICE: Two-Message Approach**

**Message 1 (Understanding Phase):**
```
Read the entire /Users/michaeljoyce/Desktop/LEARNVIA folder and understand
the current system architecture, implementation status, and any gaps.

Focus on:
- The 4-pass review workflow (content review passes 1-2, copy edit passes 3-4)
- How the 60 AI agents are configured (10 authoring + 10 style per content pass, 10 style per copy pass)
- The feedback loop mechanisms (false positive and false negative handling)
- Current test status
- What's implemented vs. what needs validation

Once you've read everything, summarize your understanding of the system.
```

**Message 2 (Task Assignment):**
```
Now that you understand the system, help me execute the pilot plan detailed
in PILOT_HANDOFF_PROMPT.md. Confirm you understand the pilot objectives and
are ready to start with Phase 1: API Setup & Initial Test.
```

**Alternative (Single Message with Explore Agent):**
```
Use the Explore agent with 'very thorough' setting to analyze the codebase
at /Users/michaeljoyce/Desktop/LEARNVIA and report on:
- System architecture and 4-pass workflow
- Current implementation completeness
- What's ready for pilot vs. what needs work
- Any issues or gaps you identify

After exploration, help me execute the pilot plan in PILOT_HANDOFF_PROMPT.md.
```

**Why This Approach:**
- Claude reads ALL files before starting work (not discovering mid-task)
- Avoids assumptions based on outdated documentation
- Identifies any issues or gaps upfront
- Ensures full context for pilot execution

---

## NOTES & CONTEXT

- This is a revision system for educational math content
- Target learner: Home alone, low confidence, limited time, scared of failing
- Human reviewers and copy editors retain final authority
- System has never been tested with real content or real API
- Mock API currently provides plausible fake feedback
- All code is tested and working, just needs real-world validation

**Good luck with the pilot!**
