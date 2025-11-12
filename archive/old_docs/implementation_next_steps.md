# Implementation Next Steps

## Completed Tasks

- ✅ Created master review context prompt with guardrails
- ✅ Documented out-of-scope items (images/animations)
- ✅ Created review log analysis script
- ✅ Generated initial pattern analysis report
- ✅ Documented prompt loading order
- ✅ Created iteration testing workflow
- ⚠️  Augmented pedagogical flow rubric (pending: need real severity examples from logs)

## Remaining Manual Tasks

### 1. Extract Real Severity Examples from Review Logs

**Why Manual:** CSV logs don't include severity ratings; requires human judgment to assess impact

**Status:** Review log analysis complete, but severity levels need manual assignment

**Steps:**
1. Read `docs/review_log_analysis.md`
2. For each good catch, assess its severity (1-5) based on student impact
3. Group examples by severity level
4. Select 2-3 representative examples at each level

**Time Estimate:** 1-2 hours

---

### 2. Augment All Rubrics with Real Examples

**Why Manual:** Requires human judgment to match issues with competencies

**Currently Done:**
- ⚠️ Pedagogical Flow rubric (awaiting severity assignments)

**Remaining Rubrics (14 total):**
- Structural Integrity
- Student Engagement
- Conceptual Clarity
- Assessment Quality
- Mathematical Accuracy
- Language Accessibility
- Practice Opportunities
- Feedback Mechanisms
- Real-World Relevance
- Error Prevention
- Technical Precision
- Progressive Complexity
- Motivational Elements
- Cognitive Load Management

**Steps for Each Rubric:**
1. Read `docs/review_log_analysis.md`
2. Find 2-3 real examples matching this competency at severity 5, 3, and 1
3. Edit rubric XML to add examples
4. Validate XML syntax
5. Commit

**Time Estimate:** 2-3 hours total (~10 min per rubric)

---

### 3. Create Test Review Scripts

**Why Manual:** Need to implement API calls with actual authentication and error handling

**Current Status:** Script referenced in workflow but not yet created

**Required Scripts:**
- `scripts/test_sonnet_review.py` - Single module AI review with Claude Sonnet
- `scripts/compare_reviews.py` - Compare AI vs human reviews

**Steps:**
1. Create `scripts/test_sonnet_review.py` with:
   - Prompt loading (3 layers)
   - Module loading
   - Anthropic API call
   - JSON output formatting
2. Create `scripts/compare_reviews.py` with:
   - AI review JSON loading
   - Human review CSV loading
   - Text similarity matching
   - Markdown report generation
3. Test with module 5.6
4. Verify output has required fields (line numbers, quotes, etc.)

**Dependencies:**
- `ANTHROPIC_API_KEY` environment variable
- `anthropic` Python package installed

**Time Estimate:** 2-4 hours

---

### 4. Add More Text Issues to Analysis

**Why Manual:** Current analysis only captures 4 text issues; CSV likely has more

**Observation:** Most issues in the CSVs are marked "Open" and many are legitimate text issues

**Steps:**
1. Review the raw CSV files more carefully
2. Identify patterns in what's being filtered as "visual"
3. Refine the visual detection logic in `analyze_review_logs.py`
4. Re-run analysis
5. Verify text issues count increases appropriately

**Time Estimate:** 30 minutes - 1 hour

---

### 5. Extract False Positive Patterns

**Why Manual:** Requires human judgment to identify patterns vs one-off issues

**Current Status:** No rejected issues found in logs (all are either Open or Resolved)

**Alternative Approach:**
Since we don't have explicit false positives from these logs, we can:
1. Run initial AI review on module 5.6
2. Compare AI findings with human review log
3. Identify what AI flagged that humans didn't
4. Add those patterns to anti-pattern guards

**Time Estimate:** 1-2 hours (after test scripts are built)

---

### 6. Run AI Review on New, Unreviewed Module

**Why Manual:** Need actual feedback quality assessment from human expert

**Prerequisites:**
- Task 3 completed (test scripts working)
- API key configured
- At least 1 new, unreviewed module available

**Important:** Modules 5.6 and 5.7 are **exemplars** used to ground the prompts (extract patterns, populate rubrics). They should NOT be used for iteration testing.

**Steps:**
1. Run AI review on a NEW module: `python scripts/test_sonnet_review.py --module modules/new_module.xml --output outputs/review_new.json`
2. Human expert reviews AI feedback for quality:
   - Are issues specific (line numbers, quotes, student impact, suggestions)?
   - Are flagged issues legitimate?
   - What real issues did AI miss?
   - Any false positives?
3. Identify false positive patterns
4. Add patterns to master prompt anti-pattern guards
5. Re-run AI review on same module
6. Compare results (should see improvement)

**Time Estimate:** 2-3 hours (including human expert review)

---

### 7. Validate with Additional New Modules

**Why Manual:** Confirm improvements generalize

**Steps:**
1. Run AI review on 2-3 more NEW modules
2. Human expert reviews each
3. Track metrics:
   - False positive rate
   - Specificity compliance (4 components present)
   - Coverage (what % of real issues caught)
4. Refine prompts based on patterns
5. Document improvement metrics

**Time Estimate:** 2-4 hours

---

### 8. Test with Rough (Unreviewed) Modules

**Why Manual:** Real-world validation

**Prerequisites:**
- 2-3 rough modules available (not yet human-reviewed)
- Iteration tests 6 and 7 show good results

**Steps:**
1. Run AI review on rough module 1
2. Human expert reviews AI feedback for quality
3. Identify any new false positives or missed patterns
4. Refine prompts
5. Repeat for modules 2 and 3
6. Document final metrics and readiness

**Time Estimate:** 4-6 hours total

---

## Success Criteria

System is ready for production when:

1. ✅ Master review context created with all guardrails
2. ✅ Review log analysis completed
3. ✅ Prompt loading order documented
4. ✅ Iteration testing workflow automated
5. ⚠️ Test scripts implemented and working
6. ⚠️ False positive rate < 20% on exemplar modules
7. ⚠️ 95%+ of AI issues include all 4 required components (line, quote, impact, suggestion)
8. ⚠️ Severity alignment within ±1 level of human judgment 70%+ of time
9. ✅ No visual/animation issues flagged (verified by anti-pattern guards)
10. ⚠️ Author feedback on rough modules is positive ("actionable", "specific", "helpful")

## Estimated Total Time

- **Core functionality (scripts + first iteration):** 6-10 hours
- **Full rubric augmentation (all 15 rubrics):** +2-3 hours
- **Multiple iterations and refinement:** +4-6 hours
- **Total:** 12-19 hours

## Next Immediate Action

**Start with Task 3:** Create test review scripts (`test_sonnet_review.py` and `compare_reviews.py`)

This unblocks iteration testing and provides concrete feedback for prompt refinement.

## Notes

**What's Working:**
- Master prompt clearly defines scope (excludes visual elements)
- Analysis script successfully separates visual from text issues
- Workflow infrastructure is in place

**What Needs Work:**
- Review logs lack severity ratings (will need to assign during testing)
- Need actual AI reviews to identify false positive patterns
- Test scripts are critical path - everything else depends on them
