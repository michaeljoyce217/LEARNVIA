# LEARNVIA - AI-Powered Calculus Content Review System

**A sample review can be seen at https://michaeljoyce217.github.io/LEARNVIA/**

## What This Is

A 30-agent AI review system that helps calculus content authors improve their work through educational feedback. The system reviews Calculus I-IV educational content using specialized AI agents focused on calculus pedagogy and writing quality.

### Core Philosophy

**Empower authors through educational feedback aligned with pedagogical best practices, rather than gatekeeping through pass/fail judgments.**

This system is designed to support non-traditional learners who struggle with traditional math education, particularly students from underserved communities.

## The Problem We're Solving

### Current Manual Review Process

Learnvia's calculus content currently goes through a manual review workflow:
1. **Author creates content** - Often new authors unfamiliar with all guidelines
2. **Human reviewer examines content** - Time-intensive, ~2-3 hours per module
3. **Author revises** - Based on reviewer feedback
4. **Second review** - Ensures fixes are working
5. **Copy editor polish** - Final mechanical cleanup
6. **Final approval** - Publication readiness

### Key Challenges

- **Reviewer bottleneck**: 2-3 hours per module, limited reviewer availability
- **Copy editor bottleneck**: Additional 1-2 hours for mechanical issues
- **Inconsistent feedback**: Different reviewers emphasize different issues
- **Author frustration**: Waiting days/weeks for feedback on fixable issues
- **Scaling limitations**: Can't add content faster than reviewers can review
- **High cognitive load**: Reviewers must juggle 10 competencies simultaneously

## Our Solution: AI-Augmented Review

### The Architecture: Why 30 Separate API Calls Matter

**Critical Design Decision**: When deploying this system, we make 30 separate API calls to Claude - one for each agent - rather than asking a single LLM to simulate 30 agents.

**Why this matters**:
- **True independence**: Each API call gets a fresh context, eliminating cross-contamination between agent perspectives
- **Authentic disagreement**: Agents can genuinely disagree without being influenced by other agents' findings
- **Statistical validity**: The consensus mechanism (4+ agents flagging = high confidence) only works with truly independent observations
- **Reduced hallucination**: Single LLM pretending to be 30 agents tends to create artificial agreement patterns

This architectural choice is fundamental to the system's reliability. A single LLM roleplaying multiple agents would defeat the entire purpose of the consensus mechanism.

**Current implementation note**: The demonstration currently simulates the 30 agents in a single run. Once deployed with truly independent API calls for each agent, we expect significant improvements in accuracy and reliability, as each agent will provide genuinely independent perspectives without any possibility of cross-influence.

### 4-Pass Structure with Deliberate Boundaries

The system uses exactly 4 passes - not 3, not 5, but precisely 4. Here's why:

**Pass 1**: 30 agents (15 authoring + 15 style) → Author self-review
**Pass 2**: 30 agents on revised content → Human reviewer meeting
**Pass 3**: 30 agents (style focus) → Author polish
**Pass 4**: 30 agents (final check) → Copy editor meeting

**Why exactly 4 passes?**
- **Diminishing returns**: Beyond 2 passes, additional reviews yield fewer actionable insights
- **Contradiction risk**: More passes increase the likelihood of agents contradicting each other on subjective matters
- **Trust erosion**: When passes start contradicting, authors lose faith in the system's reliability
- **Optimal balance**: 4 passes provide thorough coverage without overwhelming authors or creating confusion

### The Human-in-the-Loop Imperative

**Fundamental truth**: It's always the last 5% that betrays you.

The AI system excels at catching the vast majority of issues:
- Undefined technical terms
- Missing conceptual explanations
- Grammatical errors
- Structural problems
- Assessment misalignment

But those final, subtle issues require human judgment:
- **Pedagogical nuance**: Is this explanation truly helpful for a struggling student?
- **Cultural sensitivity**: Does this example resonate with diverse learners?
- **Edge cases**: Unusual module structures that break expected patterns
- **False positives**: The AI flags something technically correct but unconventional
- **Context awareness**: Understanding when to break rules for good reasons

This is why the system is designed as human-AI collaboration, not replacement. The AI handles the mechanical and pattern-based review, freeing humans to focus on nuanced pedagogical decisions that require experience, empathy, and judgment.

### Two-Shot Prompting: Learning from Exemplars

The system uses two exemplary modules as learning anchors:
- **Module 5.6**: The Definite Integral (by Chris Chan)
- **Module 5.7**: The Net Change Theorem (by Katie Stewart)

These modules serve as pattern examples for the AI agents, demonstrating:
- High-quality pedagogical flow (concrete → abstract progression)
- Accessible writing style (clear definitions, short sentences)
- Effective assessment design (aligned with learning outcomes)
- Proper mathematical formatting and notation

**Important**: The exemplars teach patterns, not content. The system extracts generalizable principles that apply to any Calculus module, whether it covers Power Series, Taylor polynomials, or integration techniques.

## Real-World Application: Power Series Module Review

### What We Found

When we ran the 30-agent system on the Power Series module:

**Consensus Issues (4+ agents agreed)**: 18 high-confidence problems
- Undefined technical terms used repeatedly ("radius of convergence" used 15 times without definition)
- Missing conceptual explanations before mathematical formulas
- Vague pronoun usage making explanations unclear
- Assessment questions testing concepts not covered in lessons

**Total Findings**: 177 individual observations across all agents
- Shows the system's thoroughness in examination
- Most are minor issues, but patterns emerge through consensus
- Demonstrates the value of multiple perspectives

### The Consensus Mechanism

**How it works**:
- Each finding gets a priority score based on both issue severity and agent agreement
- **Priority 1-2**: High severity issues flagged by 4+ agents (Consensus Issues)
- **Priority 3-4**: Moderate severity issues or those flagged by 2-3 agents (Notable Patterns)
- **Priority 5**: Lower severity issues or those flagged by single agents (Potential Issues)

The priority score combines both the inherent severity of the issue (how much it impacts learning) and the confidence level (how many agents independently identified it). This dual mechanism naturally filters signal from noise, ensuring authors focus on the most impactful improvements first.

## System Components

### Core Review Engine
**File**: `Testing/run_review.py` (2200+ lines)

**Key capabilities**:
- LaTeX preservation through custom XML processing
- Line-by-line text extraction with numbering
- 30-agent simulation with consensus scoring
- HTML report generation with 9 detailed tabs
- Pattern-based detection (never hardcoded to specific content)

### Prompt System
**Location**: `ACTIVE_CONFIG/v2_master_prompts/`

The prompts encode pedagogical best practices from the authoring and style guides, enabling agents to detect:
- Abstract concepts introduced before concrete examples
- Undefined technical terminology
- Missing or inadequate problem hints
- Inconsistent notation and formatting
- Accessibility issues for struggling students

### Expected Outcomes

**For Authors**:
- Receive comprehensive feedback orders of magnitude faster
- See exactly where issues occur (line numbers + quotes)
- Understand student impact of each issue
- Get specific, actionable fixes

**For Reviewers**:
- Dramatically reduce time spent on mechanical review
- Focus on pedagogical decisions, not routine issues
- See pre-filtered, prioritized issue lists
- Maintain consistency across all reviews

**For the Organization**:
- Scale content production significantly without proportional reviewer hiring
- Maintain quality standards consistently
- Reduce time-to-publication substantially
- Build author expertise through immediate feedback

## Current Status

- **Implemented**: Pass 1 of the 4-pass system
- **Tested**: Power Series module with 177 findings, 18 consensus issues
- **Architecture**: Fully generic, works with any Calculus module
- **Next Steps**: Deploy remaining passes, integrate with production workflow

## Technical Implementation Notes

### Why Generic Matters

The system is designed to work with ANY calculus module without modification:
- No hardcoded content checks
- Pattern-based detection only
- Dynamic topic identification
- Universal pedagogical principles

This ensures the system remains valuable as new modules are created, without requiring constant updates to detection logic.

### The Critical Balance

**60% Specialist Agents**: Deep expertise in specific competencies
**40% Generalist Agents**: Holistic view, catching interaction effects

This mimics having both subject matter experts and experienced editors reviewing content, ensuring both detailed and big-picture issues are caught.

## Conclusion

LEARNVIA represents a new paradigm in educational content review: AI agents handle the mechanical and pattern-based review, while humans focus on nuanced pedagogical decisions. The system's strength lies not in replacing human reviewers, but in amplifying their effectiveness by handling the routine work that consumes most of their time.

The key insights from our implementation:
1. **Human oversight remains essential** - Critical nuances require judgment AI cannot provide
2. **Multiple passes need boundaries** - More than 4 passes leads to contradictions and confusion
3. **True agent independence matters** - 30 separate API calls, not one LLM pretending
4. **Pattern learning beats content matching** - Exemplars teach principles, not specific topics

This system enables Learnvia to scale quality content creation while maintaining pedagogical excellence, ultimately serving more students who need accessible, well-crafted calculus education.