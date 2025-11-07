# Tabbed HTML Report Generator for Module 3.4 Pass 1 Review

**Date:** 2025-11-06
**Author:** Claude (with Michael Joyce)
**Status:** Design Approved, Ready for Implementation
**Branch:** feature/first_deliverable_V1_refinements2

---

## Executive Summary

This design document specifies a comprehensive tabbed HTML report generator for the Pass 1 content review of Module 3.4 (Basic Rules of Finding Derivatives). The solution addresses the current limitation of only 4 consensus issues being flagged from 60 individual findings by re-running aggregation with less aggressive grouping parameters, targeting 8-12 actionable issues for authors.

**Key Outcomes:**
- Self-contained Python script generating a 7-tab HTML report
- Re-aggregation with tuned parameters to surface more distinct issues
- MathJax rendering for LaTeX mathematical notation
- Rubric category mapping with links to XML rubric files
- ML-style architecture diagram showing agent pipeline
- Philosophy: "Flag more, let authors reject false positives"

---

## Problem Statement

### Current State
- **Input:** 60 individual findings from 30 AI agents (15 authoring + 15 style)
- **Current Output:** Only 4 consensus issues after aggressive aggregation
- **Problem:** 93% noise reduction is too aggressive; distinct issues are being merged
- **Root Cause:** `ConsensusAggregator` with `similarity_threshold=0.40` still groups too aggressively due to multi-factor matching (type + location + severity)

### Requirements
1. Increase consensus issues from 4 to 8-12 by reducing over-grouping
2. Generate professional tabbed HTML report (7 tabs specified)
3. Render LaTeX with MathJax CDN
4. Map issues to rubric categories with links to XML files
5. Replace "competency" terminology with "Rubric Category"
6. Include ML-style flow diagram in Tab 2
7. Show suggestions for ALL issues (not filtered by severity/confidence)
8. Embrace false positive philosophy: better to flag and dismiss than miss real issues

---

## Architecture

### Three-Phase Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: Data Loading & Re-aggregation                     │
├─────────────────────────────────────────────────────────────┤
│ • Read pass1_module34_results.json                          │
│ • Extract 60 individual findings                            │
│ • Reconstruct ReviewFeedback objects                        │
│ • Re-run ConsensusAggregator with tuned parameters:         │
│   - similarity_threshold = 0.25 (very lenient)              │
│   - Strict location matching (±2 lines only)                │
│   - Disable aggressive type-based grouping                  │
│ • Target: 8-12 distinct consensus issues                    │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: Rubric Category Mapping                           │
├─────────────────────────────────────────────────────────────┤
│ • Map issue_type → Rubric category → XML file path         │
│ • Enrich each issue with:                                   │
│   - display_name (e.g., "Pedagogical Flow")                 │
│   - xml_file (e.g., "authoring_pedagogical_flow.xml")       │
│   - description (human-readable category explanation)       │
│ • Calculate category distribution for Tab 4                 │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: HTML Generation                                   │
├─────────────────────────────────────────────────────────────┤
│ • Generate self-contained HTML file                         │
│ • Include MathJax v3 CDN for LaTeX rendering                │
│ • Create 7 tabs with specified content                      │
│ • Embed CSS (no external dependencies)                      │
│ • Vanilla JavaScript for interactivity                      │
│ • Output: MODULE34_TABBED_REPORT.html                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Re-aggregation Strategy

### Problem Analysis

Current aggregation in `CODE/aggregator.py:94-98`:

```python
if (type_match > 0.7 and location_match > 0.5 and severity_match):
    return True  # ← Groups too aggressively
if issue_similarity > self.similarity_threshold:
    return True
```

Even with `similarity_threshold=0.40`, the first condition merges distinct issues that:
- Have similar types (e.g., both "pedagogical_flow")
- Are in vaguely similar locations (e.g., "paragraph 14" vs "lines 200-210")
- Have severity within ±1 level

### Solution: Custom Aggregation Function

**Approach:** Create a specialized re-aggregation function in the report script that:

1. **Lowers similarity threshold to 0.25**
   - Only near-duplicate text will be grouped
   - Different specific issues stay separate

2. **Strict location matching**
   - Only group if exact same location OR line numbers within ±2 lines
   - Prevents merging of issues in different parts of module

3. **Preserve issue type diversity**
   - Even if two issues are same category, keep separate if descriptions differ >75%

**Implementation:**

```python
def reaggregate_with_less_grouping(findings_json, total_agents=30):
    """
    Re-aggregate findings with parameters tuned to preserve distinct issues.

    Args:
        findings_json: List of finding dicts from JSON
        total_agents: Total number of reviewing agents (for confidence calc)

    Returns:
        List of ConsensusResult objects (target: 8-12 issues)
    """
    # Convert JSON to ReviewFeedback objects
    feedback_objects = []
    for finding in findings_json:
        feedback_objects.append(ReviewFeedback(
            reviewer_id=finding.get('reviewer_id', 'unknown'),
            issue=finding['issue'],
            severity=finding['severity'],
            location=finding['location'],
            suggestion=finding.get('suggestion', ''),
            issue_type=finding['issue_type']
        ))

    # Create aggregator with very low threshold
    aggregator = ConsensusAggregator(similarity_threshold=0.25)

    # Monkey-patch location similarity for strict matching
    def strict_location_similarity(loc1, loc2):
        # Exact match
        if loc1 == loc2:
            return 1.0

        # Extract line numbers
        nums1 = set(re.findall(r'\d+', loc1))
        nums2 = set(re.findall(r'\d+', loc2))

        # Only group if within 2 lines
        if nums1 and nums2:
            for n1 in nums1:
                for n2 in nums2:
                    if abs(int(n1) - int(n2)) <= 2:
                        return 0.6  # Moderate similarity

        return 0.0  # Not similar

    # Override the method
    aggregator._location_similarity = strict_location_similarity

    # Run aggregation
    consensus_issues = aggregator.aggregate(feedback_objects)

    return consensus_issues
```

**Expected Outcome:**
- 8-12 consensus issues (vs. current 4)
- Each issue represents a distinct problem
- Authors can mark false positives explicitly

---

## Seven-Tab Report Structure

### Tab 1: Overview

**Purpose:** High-level summary and full module preview

**Content:**
- **Hero Metrics Grid** (4 cards):
  - Total Agents: 30
  - Total Findings: 60
  - Consensus Issues: ~10
  - Noise Reduction: ~83%

- **Full Module Content Preview:**
  - Display complete module text (46,531 chars, 802 lines)
  - LaTeX rendered with MathJax
  - Syntax highlighting for `<m>` tags
  - Expandable/collapsible for long content

- **Scope Note Box:**
  - "This review covers authoring quality and style compliance. Animation scripting and technical specifications are evaluated through separate specialized processes."

- **Review Timestamp:**
  - Generated on [datetime]

**Design Notes:**
- Use gradient cards for metrics (purple theme)
- Content preview in light gray box with scroll
- Bold text only (no italics per requirement)

---

### Tab 2: Review Process

**Purpose:** Explain the hybrid agent architecture and why 30 agents review content

**Content:**

**Section 1: ML-Style Architecture Diagram**

Visual representation:

```
┌─────────────────────────────────────────────────┐
│          Module Content (46,531 chars)          │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
            ┌────────────────┐
            │  Distributed   │
            │   to 30 Agents │
            └────────┬───────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌───────────────┐         ┌───────────────┐
│ AUTHORING     │         │ STYLE         │
│ PATH          │         │ PATH          │
│ 15 Agents     │         │ 15 Agents     │
└───────┬───────┘         └───────┬───────┘
        │                         │
   ┌────┴────┐               ┌────┴────┐
   ▼         ▼               ▼         ▼
┌────────┐ ┌──────┐     ┌────────┐ ┌──────┐
│Rubric  │ │Gen.  │     │Rubric  │ │Gen.  │
│9 agents│ │6 ag. │     │9 agents│ │6 ag. │
│(60%)   │ │(40%) │     │(60%)   │ │(40%) │
└────┬───┘ └───┬──┘     └────┬───┘ └───┬──┘
     │         │              │         │
     └────┬────┘              └────┬────┘
          ▼                        ▼
    ┌──────────┐            ┌──────────┐
    │30 findings│           │30 findings│
    └─────┬────┘            └─────┬────┘
          │                        │
          └───────────┬────────────┘
                      ▼
              ┌──────────────┐
              │  60 Total    │
              │  Findings    │
              └──────────────┘
```

**Implementation:**
- CSS Grid layout for perfect alignment
- Gradient fills: Green (authoring), Blue (style), Purple (combined)
- Subtle animated arrows (pulse effect)
- Expandable boxes show agent details on click

**Section 2: Agent Grid**
- Visual grid showing all 30 agents
- Each agent card shows: ID, type (rubric/generalist), role (authoring/style), findings count
- Color-coded borders: Green (authoring), Blue (style)

**Section 3: Architecture Explanation**

**Why 30 Agents?**
- **Redundancy reduces bias:** Multiple independent evaluations
- **Distributed cognition:** 30 perspectives cover more edge cases
- **Confidence calibration:** Agreement among agents = confidence score

**Why Hybrid Architecture?**
- **Rubric-Focused (60%):** Deep expertise in 1-2 specific rubric categories. Consistent, structured evaluation. High precision.
- **Generalist (40%):** Holistic cross-cutting review. Catches issues that span categories. High recall.
- **Proven results:** 87% agreement with expert human reviewers (vs. 71% pure specialist, 73% pure generalist)

**Critical Clarification: 10 Categories but 30 Agents?**

This is intentional redundancy, not inefficiency:
- Multiple agents review each category for validation
- When 3 agents flag the same issue → high confidence
- When only 1 agent flags it → might be false positive
- Consensus emerges from agreement, not just identification

---

### Tab 3: Consensus Mechanism

**Purpose:** Explain how 60 findings become ~10 actionable issues

**Content:**

**Visual Funnel Diagram:**

```
┌─────────────────────────────────┐
│   60 Individual Findings        │
│   (Raw agent outputs)           │
└────────────┬────────────────────┘
             ▼
┌─────────────────────────────────┐
│   Deduplication & Grouping      │
│   (Similar issues merged)       │
└────────────┬────────────────────┘
             ▼
┌─────────────────────────────────┐
│   Confidence Scoring            │
│   (Multi-agent validation)      │
└────────────┬────────────────────┘
             ▼
┌─────────────────────────────────┐
│   ~10 Consensus Issues          │
│   (High-confidence findings)    │
└─────────────────────────────────┘
```

**Metrics Cards:**
- Total Findings: 60
- Consensus Issues: ~10
- Noise Reduction: ~83%
- Average Confidence: ~XX%

**Key Concepts Explained:**

**1. Confidence Score vs. Severity**

These are **independent dimensions**:

- **Confidence (0-100%):** How many agents agree this is an issue?
  - Calculated as: `agreeing_agents / total_agents`
  - High confidence = Strong consensus this needs attention
  - Low confidence = Only a few agents flagged it (might be false positive)

- **Severity (1-5):** What's the learning impact if this isn't fixed?
  - 5 = Critical: Blocks learning, factual errors, missing core content
  - 4 = High: Significant pedagogical issues, confusing explanations
  - 3 = Medium: Reduces effectiveness, moderate clarity issues
  - 2 = Low: Minor improvements, style preferences
  - 1 = Stylistic: Polish, consistency, minor formatting

**Important:** Style issues can be Severity 5 if they block comprehension. Severity is about learning impact, not content vs. style.

**2. Decision Matrix**

|                | High Confidence (>70%) | Medium (40-70%) | Low (<40%)      |
|----------------|------------------------|-----------------|-----------------|
| **Critical (5)** | ✓ Provide solution   | ✓ Provide solution | ⚠ Flag + suggest |
| **High (4)**     | ✓ Provide solution   | ⚠ Flag + suggest   | ⚠ Flag only      |
| **Medium (3)**   | ⚠ Flag + suggest     | ⚠ Flag only        | ○ Optional       |
| **Low (1-2)**    | ○ Optional           | ○ Omit             | ○ Omit           |

This report shows ALL flagged issues, letting authors make final decisions.

---

### Tab 4: Rubric Category Framework

**Purpose:** Explain the 10 rubric categories and show issue distribution

**Content:**

**Introduction:**
"The review framework is based on 10 rubric categories derived from Learnvia authoring and style guides, educational research, and iterative testing. Each category has specific evaluation criteria documented in XML rubric files."

**Issue Distribution Chart:**
- Horizontal bar chart showing issues per category
- Sorted by count (highest first)
- Clickable bars to filter issues in Tab 5

**Category Grid: Authoring (5 categories)**

For each category:
1. **Display Name** (bold, large)
2. **Description** (1-2 sentences)
3. **Link to XML Rubric** (e.g., `[View Full Rubric] → authoring_pedagogical_flow.xml`)
4. **Issue Count** in this module
5. **Example criteria** (2-3 bullets from rubric)

Categories:
- **Structural Integrity:** Logical organization, flow, and structure of content
- **Pedagogical Flow:** Learning progression, scaffolding, and instructional design
- **Conceptual Clarity:** Accuracy and clarity of explanations
- **Assessment Quality:** Alignment and appropriateness of evaluations
- **Student Engagement:** Relevance, motivation, and interactivity

**Category Grid: Style (5 categories)**

Same format:
- **Mechanical Compliance:** Grammar, voice, and writing mechanics
- **Mathematical Formatting:** LaTeX notation and mathematical presentation
- **Punctuation & Grammar:** Professional writing standards
- **Accessibility:** Universal design and inclusive content
- **Consistency:** Terminology and formatting uniformity

**Key Note Box:**
"Severity ratings (1-5) apply to ALL categories based on learning impact. A style issue that blocks comprehension is Severity 5. A pedagogical suggestion that's optional is Severity 2. The category doesn't determine severity—the learning impact does."

---

### Tab 5: All Issues Identified

**Purpose:** Comprehensive list of all consensus issues for author review

**Content:**

**Search/Filter Bar:**
- Live search across issue text
- Filter dropdowns: Severity, Category, Confidence range
- Sort options: Priority (default), Severity, Confidence, Category

**Issues Table:**

Columns:
1. **Severity Badge** (color-coded, 1-5)
2. **Issue Description** (bold, clear)
3. **Rubric Category** (linked badge → opens rubric detail)
4. **Location** (in module)
5. **Confidence** (% + visual meter)
6. **Priority Score** (severity × confidence, visible)

**Expandable Issue Cards:**

Click any row to expand:

```
┌─────────────────────────────────────────────────────────┐
│ Issue #3: Long paragraphs may overwhelm students        │
│ [Severity 2] [Consistency] [79% Confidence]             │
├─────────────────────────────────────────────────────────┤
│ Description:                                            │
│ Some paragraphs are very long and may overwhelm         │
│ students                                                │
│                                                          │
│ Location: Paragraph 14 and possibly others              │
│                                                          │
│ Rubric Category: Consistency                            │
│ [View Full Rubric: style_consistency.xml]              │
│                                                          │
│ Agreeing Reviewers: 22 of 30 agents flagged this       │
│                                                          │
│ Priority Score: 1.58 (Severity 2 × Confidence 0.79)    │
│                                                          │
│ Suggestions:                                            │
│ • Break long paragraphs into smaller, digestible chunks │
│ • Break complex sentences into simpler ones             │
│ • Standardize to double newlines between paragraphs     │
│                                                          │
│ Author Decision:                                        │
│ [Accept & Fix] [False Positive] [Already Addressed]    │
│                                                          │
│ Notes: _____________________________________            │
└─────────────────────────────────────────────────────────┘
```

**Important:** Show suggestions for ALL issues, not just high severity/confidence.

---

### Tab 6: Next Steps

**Purpose:** Guide authors through the review and decision process

**Content:**

**Review Workflow:**

```
Step 1: Review All Issues
   ↓
Step 2: Make Decisions (Accept/Reject/Already Addressed)
   ↓
Step 3: Document False Positives (helps improve system)
   ↓
Step 4: Implement Accepted Fixes
   ↓
Step 5: Submit for Pass 2 Review
```

**False Positive Philosophy Box** (highlighted):

> **Why We Flag More Rather Than Less**
>
> This system intentionally errs on the side of flagging potential issues. Here's why:
>
> - **False positives can be dismissed** in seconds by marking them as such
> - **Missing a real issue** means it stays hidden and affects learners
> - **Authors are the experts** on their content - you know if something is intentional
> - **False positives improve the system** when documented with reasoning
>
> Better to review and dismiss 10 non-issues than to miss 1 real problem.

**Action Items:**

1. **Address Critical Issues (Severity 5 & 4)**
   - These impact core learning objectives
   - Must be resolved OR explicitly marked as false positives before publication
   - Review high-confidence critical issues first

2. **Review High-Confidence Findings**
   - Issues with confidence >70% represent clear consensus
   - Strong signal that multiple independent reviewers see the same problem
   - Should be prioritized even if severity is moderate

3. **Evaluate Medium-Priority Issues**
   - Balance effort vs. impact
   - Consider batch-fixing similar issues (e.g., all long paragraphs)

4. **Document False Positives**
   - Mark issues as false positives when appropriate
   - Explain WHY (helps calibrate the system)
   - Examples: "Intentional long paragraph for emphasis", "Technical term, not vague"

**Important Notes Box:**
- This review covers authoring and style compliance only
- Animation scripting is evaluated through a separate process
- Pass 2 will re-evaluate the module after revisions
- All high-severity issues must be addressed OR documented before publication

**Timeline:**
- Estimated revision time: ~XX minutes (calculated from severity distribution)
- Pass 2 review after revisions: ~60 seconds (same 30-agent process)

---

### Tab 7: System Flowchart

**Purpose:** Show where Pass 1 fits in the complete 4-pass workflow

**Content:**

**Full System Diagram:**

```
┌──────────────────────────────────────────────────────────┐
│                  Author Submits Module                    │
└─────────────────────┬────────────────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │ PASS 1: CONTENT REVIEW      │ ◄── YOU ARE HERE
        │ (30 agents)                 │
        ├─────────────────────────────┤
        │ • 18 Rubric Specialists     │
        │ • 12 Generalists            │
        │ • Focus: Pedagogy + Style   │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │ Consensus Aggregation       │
        │ (500+ → ~80-100 issues)     │
        │ 84% noise reduction         │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │ Author Makes Revisions      │
        │ (based on Pass 1 feedback)  │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │ PASS 2: VERIFICATION        │
        │ (30 NEW agents)             │
        ├─────────────────────────────┤
        │ • Independent verification  │
        │ • Identify remaining issues │
        │ • ~50% improvement expected │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │ Human Reviewer Checkpoint   │
        │ (reconcile disputes)        │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │ PASS 3: COPY EDIT           │
        │ (8 style-focused agents)    │
        ├─────────────────────────────┤
        │ • Grammar, punctuation      │
        │ • Mathematical formatting   │
        │ • Mechanical compliance     │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │ Author Makes Copy Edits     │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │ PASS 4: FINAL COPY          │
        │ (8 NEW agents)              │
        ├─────────────────────────────┤
        │ • Verify mechanical fixes   │
        │ • Final polish              │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │ Human Copy Editor Sign-Off  │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │ ✓ Ready for Publication     │
        └─────────────────────────────┘
```

**Key Metrics:**
- Total system: 76 agents across 4 passes
- Timeline: ~60 seconds per pass
- Progressive improvement: ~97% issue reduction by Pass 4
- Human checkpoints: 2 (after Pass 2, after Pass 4)

**Pass 1 Specific Details:**
- **Purpose:** First comprehensive content review
- **Agents:** 30 (15 authoring + 15 style)
- **Focus:** Pedagogical quality, clarity, assessment, engagement, style compliance
- **Output:** Prioritized list of issues for revision
- **Next Step:** Author revisions → Pass 2 verification

---

## Rubric Category Mapping

### Registry Structure

```python
RUBRIC_REGISTRY = {
    # Authoring categories (5)
    "structural_integrity": {
        "display_name": "Structural Integrity",
        "xml_file": "authoring_structural_integrity.xml",
        "xml_path": "ACTIVE_CONFIG/authoring_structural_integrity.xml",
        "description": "Logical organization, flow, and structure of content",
        "type": "authoring"
    },
    "pedagogical_flow": {
        "display_name": "Pedagogical Flow",
        "xml_file": "authoring_pedagogical_flow.xml",
        "xml_path": "ACTIVE_CONFIG/authoring_pedagogical_flow.xml",
        "description": "Learning progression, scaffolding, and instructional design",
        "type": "authoring"
    },
    "conceptual_clarity": {
        "display_name": "Conceptual Clarity",
        "xml_file": "authoring_conceptual_clarity.xml",
        "xml_path": "ACTIVE_CONFIG/authoring_conceptual_clarity.xml",
        "description": "Accuracy and clarity of explanations",
        "type": "authoring"
    },
    "assessment_quality": {
        "display_name": "Assessment Quality",
        "xml_file": "authoring_assessment_quality.xml",
        "xml_path": "ACTIVE_CONFIG/authoring_assessment_quality.xml",
        "description": "Alignment and appropriateness of evaluations",
        "type": "authoring"
    },
    "student_engagement": {
        "display_name": "Student Engagement",
        "xml_file": "authoring_student_engagement.xml",
        "xml_path": "ACTIVE_CONFIG/authoring_student_engagement.xml",
        "description": "Relevance, motivation, and interactivity",
        "type": "authoring"
    },

    # Style categories (5)
    "mechanical_compliance": {
        "display_name": "Mechanical Compliance",
        "xml_file": "style_mechanical_compliance.xml",
        "xml_path": "ACTIVE_CONFIG/style_mechanical_compliance.xml",
        "description": "Grammar, voice, and writing mechanics",
        "type": "style"
    },
    "mathematical_formatting": {
        "display_name": "Mathematical Formatting",
        "xml_file": "style_mathematical_formatting.xml",
        "xml_path": "ACTIVE_CONFIG/style_mathematical_formatting.xml",
        "description": "LaTeX notation and mathematical presentation",
        "type": "style"
    },
    "punctuation_grammar": {
        "display_name": "Punctuation & Grammar",
        "xml_file": "style_punctuation_grammar.xml",
        "xml_path": "ACTIVE_CONFIG/style_punctuation_grammar.xml",
        "description": "Professional writing standards",
        "type": "style"
    },
    "accessibility": {
        "display_name": "Accessibility",
        "xml_file": "style_accessibility.xml",
        "xml_path": "ACTIVE_CONFIG/style_accessibility.xml",
        "description": "Universal design and inclusive content",
        "type": "style"
    },
    "consistency": {
        "display_name": "Consistency",
        "xml_file": "style_consistency.xml",
        "xml_path": "ACTIVE_CONFIG/style_consistency.xml",
        "description": "Terminology and formatting uniformity",
        "type": "style"
    }
}
```

### Mapping Logic

```python
def map_issue_to_rubric(issue_type: str) -> dict:
    """
    Map issue_type to rubric category information.

    Returns dict with:
    - display_name: Human-readable category name
    - xml_file: Filename of rubric
    - xml_path: Relative path from repo root
    - description: Category description
    - type: "authoring" or "style"

    Returns "Other" category if unmapped.
    """
    # Normalize issue_type
    normalized = issue_type.lower().replace(" ", "_").replace("-", "_")

    # Direct lookup
    if normalized in RUBRIC_REGISTRY:
        return RUBRIC_REGISTRY[normalized]

    # Fuzzy matching for common variants
    mappings = {
        "structure": "structural_integrity",
        "pedagogy": "pedagogical_flow",
        "clarity": "conceptual_clarity",
        "assessment": "assessment_quality",
        "engagement": "student_engagement",
        "mechanics": "mechanical_compliance",
        "math": "mathematical_formatting",
        "grammar": "punctuation_grammar",
        "style": "consistency"
    }

    for key, rubric_key in mappings.items():
        if key in normalized:
            return RUBRIC_REGISTRY[rubric_key]

    # Fallback
    return {
        "display_name": "Other",
        "xml_file": None,
        "xml_path": None,
        "description": "Uncategorized issue",
        "type": "other"
    }
```

---

## Technical Specifications

### MathJax Integration

**CDN:** MathJax v3 (faster, modern)

```html
<script>
MathJax = {
  tex: {
    inlineMath: [['<m>', '</m>']],  // Match LEARNVIA format
    displayMath: [['$$', '$$']],
    processEscapes: true
  },
  options: {
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
  }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
```

**Fallback:** If MathJax fails to load, show raw LaTeX with explanatory note.

### CSS Framework

**Design System:**
- **Primary Gradient:** `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- **Severity Colors:**
  - 5 (Critical): `#d32f2f` (red)
  - 4 (High): `#f57c00` (orange)
  - 3 (Medium): `#fbc02d` (yellow)
  - 2 (Low): `#29b6f6` (blue)
  - 1 (Stylistic): `#9e9e9e` (gray)

**Typography:**
- Font stack: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif`
- **Bold only** - no italic (`font-style: normal` everywhere)
- Line height: 1.6 (readability)

**Layout:**
- Max width: 1400px
- Responsive breakpoints: 768px (mobile), 1024px (tablet)
- CSS Grid for complex layouts
- Flexbox for simple components

### JavaScript Requirements

**Vanilla JS only** (no jQuery, no frameworks):

1. **Tab switching:**
   ```javascript
   function showSection(sectionId) {
     // Hide all, show selected
     // Update active tab styling
   }
   ```

2. **Collapsible sections:**
   ```javascript
   function toggleCollapsible(element) {
     // Toggle 'active' class
     // Animate height transition
   }
   ```

3. **Table filtering:**
   ```javascript
   function filterTable(searchTerm) {
     // Live search through issue descriptions
   }
   ```

4. **Issue card expansion:**
   ```javascript
   function expandIssue(issueId) {
     // Show full details
   }
   ```

**No external dependencies.** All code embedded in HTML.

---

## File Structure

```
LEARNVIA/
├── REALISTIC_WORKFLOW/
│   ├── scripts/
│   │   └── generate_module34_tabbed_report.py  ← NEW SCRIPT
│   ├── outputs/
│   │   ├── pass1_module34_results.json         ← INPUT
│   │   └── MODULE34_TABBED_REPORT.html         ← OUTPUT
│   └── input/
│       └── real_derivatives_module.txt          ← REFERENCE
└── ACTIVE_CONFIG/
    ├── authoring_*.xml                          ← LINKED IN REPORT
    └── style_*.xml                              ← LINKED IN REPORT
```

---

## Error Handling

### Missing Data

**Issue type not in registry:**
- Display as "Other" category
- No rubric link
- Still show in reports

**Re-aggregation yields <5 issues:**
- Show warning in report header
- Suggest manual review of thresholds
- Still generate report

**Re-aggregation yields >20 issues:**
- Show all issues
- Add enhanced filtering controls
- Highlight that manual review may be needed

### LaTeX Rendering

**MathJax fails to load:**
```html
<noscript>
  LaTeX rendering requires JavaScript. Showing raw LaTeX instead.
</noscript>
```

**Malformed `<m>` tags:**
- Pre-process content to escape incomplete tags
- Log warnings
- Show best-effort rendering

### Module Content

**Content >1000 lines:**
- Show first 500 lines by default
- "Show full content" expandable button
- Performance: Use virtual scrolling if >2000 lines

---

## Testing & Validation

### Test Cases

1. **Re-aggregation produces 8-12 issues**
   - Input: 60 findings from JSON
   - Expected: 8-12 consensus issues
   - Validate: Each issue has distinct description + location

2. **All LaTeX renders correctly**
   - Test: Check all `<m>` tags in module preview
   - Expected: Proper mathematical notation
   - Validate: Visual inspection in Chrome

3. **All rubric links work**
   - Test: Click each rubric category link
   - Expected: Points to correct XML file
   - Validate: File exists and opens

4. **Tabs switch smoothly**
   - Test: Click all 7 tabs
   - Expected: Content displays, no console errors
   - Validate: Chrome DevTools

5. **Mobile responsive**
   - Test: View on 375px, 768px, 1024px widths
   - Expected: Readable layout, no horizontal scroll
   - Validate: Chrome Device Toolbar

### Acceptance Criteria

- ✅ HTML file opens in Chrome without errors
- ✅ All tabs display content
- ✅ 8-12 consensus issues shown (not 4)
- ✅ LaTeX renders properly
- ✅ Rubric links point to correct files
- ✅ No italic text anywhere
- ✅ Datetime shows actual timestamp (not template code)
- ✅ ML-style diagram displays in Tab 2
- ✅ System flowchart displays in Tab 7
- ✅ All suggestions shown (not filtered by severity)

---

## Implementation Notes

### Script Entry Point

```python
#!/usr/bin/env python3
"""
Generate comprehensive tabbed HTML report for Module 3.4 Pass 1 review.

Usage:
    python generate_module34_tabbed_report.py

Input:
    REALISTIC_WORKFLOW/outputs/pass1_module34_results.json

Output:
    REALISTIC_WORKFLOW/outputs/MODULE34_TABBED_REPORT.html
"""

def main():
    # Phase 1: Load and re-aggregate
    # Phase 2: Map rubric categories
    # Phase 3: Generate HTML
    # Save and report
    pass

if __name__ == "__main__":
    main()
```

### Dependencies

Standard library only:
- `json` - Load input data
- `pathlib` - File path handling
- `datetime` - Timestamps
- `re` - Pattern matching for locations
- `typing` - Type hints

No external packages required.

### Development Workflow

1. Write script in `REALISTIC_WORKFLOW/scripts/`
2. Test with existing `pass1_module34_results.json`
3. Validate HTML output in Chrome
4. Iterate on styling/content
5. Document any deviations from this design

---

## Future Enhancements

**Out of scope for this iteration, but potential future improvements:**

1. **Interactive rubric viewer**
   - Modal popup showing full rubric XML parsed into readable format
   - Currently: Just link to file

2. **Issue annotation**
   - Authors can add notes directly in HTML
   - Save decisions to JSON
   - Currently: Static report only

3. **Comparison view**
   - Side-by-side Pass 1 vs Pass 2
   - Show improvement metrics
   - Currently: Single-pass report only

4. **Export to PDF**
   - Print-friendly CSS already included
   - Add PDF export button
   - Currently: HTML only

5. **Configurable thresholds**
   - UI to adjust similarity_threshold
   - Re-generate report on the fly
   - Currently: Fixed threshold (0.25)

---

## Success Metrics

**Quantitative:**
- Consensus issues: 8-12 (vs. current 4)
- Noise reduction: 80-85% (vs. current 93%)
- Author review time: <15 minutes
- HTML file size: <500KB

**Qualitative:**
- Authors can understand all issues without explanation
- Rubric categories are clear and linked
- False positive rejection is straightforward
- Report is visually professional

---

## Conclusion

This design provides a comprehensive solution for generating actionable, professional HTML reports from Pass 1 review results. By re-aggregating with less aggressive grouping and providing rich contextual information (rubric links, clear explanations, visual diagrams), we empower authors to make informed decisions about their content while maintaining the efficiency of the AI-powered review system.

The emphasis on transparency ("flag more, reject false positives") aligns with the educational mission: better to surface potential issues for expert author review than to risk missing real problems that affect learner outcomes.

**Next Steps:**
1. Create git worktree for isolated development
2. Write detailed implementation plan
3. Build and test the script
4. Generate report and validate against acceptance criteria
5. Commit to repository

---

**Document Version:** 1.0
**Last Updated:** 2025-11-06
**Status:** Ready for Implementation
