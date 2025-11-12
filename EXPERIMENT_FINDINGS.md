# Experiment Findings - Feature/Experiment Branch
**Date:** 2025-11-12
**Branch:** feature/experiment
**Test Module:** Power Series (power_series_original.xml)

## Summary
Ran the 30-agent review system on the Power Series test module to identify potential improvements. The system generated 177 findings with 18 consensus issues (4+ agents agreeing).

---

## Results Overview

### Positive Observations ✅

1. **Consensus Mechanism Working Well**
   - 177 total findings → 18 consensus issues (10% pass rate)
   - Good signal-to-noise filtering through agent agreement
   - High confidence (80%) on critical issues like "Todo" placeholders

2. **Placeholder Detection Excellent**
   - Successfully identified all "Todo" placeholders with 80% and 53% consensus
   - Clear student impact articulated
   - Actionable fix suggestions provided

3. **Vague Pronoun Detection**
   - System correctly identifies vague "it" references
   - Multiple agents independently flag same patterns

4. **All Issues Have Required Components**
   - Line numbers ✓
   - Quoted text ✓
   - Student impact ✓
   - Suggested fix ✓

---

## Identified Improvement Opportunities 🔧

### 1. **CRITICAL: False Positives on Informal Definitions**
**Problem:**
The system flags "Ratio Test", "radius of convergence", and "interval of convergence" as potentially undefined with severity 4, even though they ARE defined in the framing text (XML lines 14-15):

```xml
<p>The distance from the center to the edge of this interval is the
<b>radius of convergence</b>, <m>R</m>. The complete set of <m>x</m>-values
for which the series converges is the <b>interval of convergence</b>.</p>
```

**Why This Happens:**
The system is looking for formal `<definition>` tags but these terms are defined inline with `<b>` tags in regular paragraphs.

**Impact:**
- False positives waste author time
- Reduces trust in system accuracy
- 11-14 agents flagging these = high consensus on false positive

**Proposed Fix:**
- Enhance definition detection to recognize `<b>term</b> is/are` patterns outside `<definition>` tags
- Add heuristic: If a compound term appears with `<b>` tags near first usage + followed by "is/are", treat as definition
- Add to authoring prompt: "Definitions may appear in `<definition>` tags OR as bold terms followed by 'is/are' in framing text"

**Priority:** P1 - This is causing multiple high-severity false positives

---

### 2. **Context-Aware Pronoun Analysis**
**Problem:**
System flags "it" references even when context is clear:

```
Line 47: "...and it may include one, both, or neither..."
```

In context, "it" clearly refers to "interval of convergence" mentioned in the same sentence.

**Proposed Fix:**
- Add proximity check: If "it" appears within 2 sentences of clear antecedent, reduce severity
- Only flag "it" as severity 2+ if antecedent is >2 sentences away OR ambiguous
- Lower confidence for "it" detection when clear referent exists

**Priority:** P2 - Moderate impact on false positive rate

---

### 3. **Duplicate Issue Consolidation**
**Problem:**
Multiple agents flag the same vague pronouns at slightly different character positions:
- Line 46: "It is found..." (5 agents)
- Line 46: Same sentence, different excerpt (7 agents)

**Proposed Fix:**
- Add post-processing step to merge issues on same line with similar categories
- If >50% text overlap + same category + same line → consolidate into single issue
- Aggregate agent counts and take highest confidence

**Priority:** P2 - Improves report readability

---

### 4. **Enhanced Prerequisite Knowledge Detection**
**Problem:**
System flags "Ratio Test" as potentially undefined (14 agents, severity 4), but:
- This is a Calc 2 prerequisite topic
- Module title is about convergence, not defining the Ratio Test
- The test IS mentioned and explained in framing text

**Current Logic:**
System uses compound term frequency (8+ occurrences) → assume new → require definition

**Proposed Enhancement:**
```
IF compound_term appears 8+ times:
  1. Check if term has <b> tags on first usage
  2. Check if explanation follows (is/are + 10+ words)
  3. Check against Calc 2 prerequisite list
  4. If (has_bold_on_first_use AND has_explanation) OR is_prerequisite:
       → Don't flag or flag as severity 2 "verification needed"
     ELSE:
       → Flag as severity 4
```

**Priority:** P1 - Major source of false positives

---

### 5. **Agent Performance Dashboard**
**Problem:**
No visibility into which agents are most accurate vs. generating false positives.

**Proposed Enhancement:**
Add new HTML report tab: "Agent Performance Analysis"

Show for each agent:
- Total findings generated
- Consensus rate (% of findings that became consensus issues)
- Average confidence of findings
- Category breakdown
- False positive rate (if human validation data available)

**Benefits:**
- Identify agents that need prompt refinement
- Balance agent weights in consensus scoring
- Data-driven prompt optimization

**Priority:** P3 - Nice to have, improves long-term system quality

---

### 6. **Confidence Score Calibration**
**Problem:**
Confidence scores (0.65-1.0) don't reflect actual accuracy:
- High-confidence (0.8-1.0) issues include false positives on definitions
- Need empirical validation

**Proposed Fix:**
- Track human reviewer feedback: "Was this issue valid?"
- Adjust agent confidence weights based on historical accuracy
- Implement Bayesian updating: `new_confidence = base_confidence × historical_accuracy_rate`

**Priority:** P2 - Improves consensus mechanism reliability

---

### 7. **Better Visualization of Agent Agreement**
**Problem:**
HTML report shows consensus percentage but not WHICH agents agreed.

**Proposed Enhancement:**
For each consensus issue, show:
```
👥 Agent Agreement (14/30 agents):
  ✓ Authoring-Specialist-ConceptualClarity-4
  ✓ Authoring-Specialist-ConceptualClarity-9
  ✓ Authoring-Generalist-10
  ... (expandable list)
```

**Benefits:**
- Transparency in consensus mechanism
- Pattern detection: Do certain agent types consistently agree?
- Debugging: Why did certain agents disagree?

**Priority:** P3 - Enhances transparency

---

### 8. **Abstract-Before-Concrete Detection Refinement**
**Problem:**
System flags line 5 for "abstract before concrete" but the full framing text (lines 11-16) actually follows good pedagogical flow:
1. Presents three possibilities (concrete cases)
2. Defines terms
3. Explains methodology

**Issue:**
Line-by-line analysis loses document-level context.

**Proposed Fix:**
- Analyze framing text as a unit, not line-by-line
- Check if ANY concrete example exists in first 50% of framing text
- Only flag if abstract definitions appear before ANY concrete context

**Priority:** P2 - Reduces false positives on pedagogical flow

---

## Quick Wins (Implement First)

1. **Enhanced Definition Detection** (P1)
   - Add `<b>term</b> is/are` pattern recognition
   - 1-2 hours implementation in `run_review.py`
   - High impact on false positive rate

2. **Duplicate Issue Consolidation** (P2)
   - Post-processing step after agent aggregation
   - 2-3 hours implementation
   - Immediate report quality improvement

3. **Prerequisite Knowledge List Expansion** (P1)
   - Add comprehensive Calc 2 prerequisite term list to prompts
   - 1 hour to compile list
   - Major reduction in false positives

---

## Testing Recommendations

After implementing improvements:
1. Re-run on Power Series module → Compare false positive rate
2. Test on Fundamental Theorem module (different topic)
3. Compare against human review logs from exemplary modules
4. Calculate precision/recall metrics

---

## System Strengths to Preserve

✅ **Generic architecture** - Works on any Calc 2 module
✅ **Consensus mechanism** - Effective noise filtering
✅ **Specificity requirements** - All issues actionable
✅ **LaTeX preservation** - Math rendering works correctly
✅ **Clear reporting** - 9-tab HTML with good UX

---

## Next Steps

1. Prioritize P1 improvements (definition detection, prerequisite handling)
2. Implement quick wins first
3. Re-test on Power Series module
4. Validate improvements with human reviewer
5. Test on second module type
6. Deploy to production if accuracy improves significantly

---

## Conclusion

The system is fundamentally sound with a working consensus mechanism and good UI. Main improvement area: **reducing false positives through smarter definition detection and prerequisite knowledge handling**. With P1 fixes, estimated false positive rate reduction: 40-50%.
