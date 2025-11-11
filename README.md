# LEARNVIA - AI-Powered Calculus Content Review System

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

### Why This Architecture

**4-Pass Structure**: Mirrors the natural revision cycle (rough draft → pedagogical refinement → mechanical polish)

**30-Agent Consensus**: 
- Simulates having 30 expert reviewers independently flag issues
- Issues found by 2+ agents = high confidence (likely real problems)
- Single-agent findings = flagged but may be false positives
- Reduces false positives while maintaining liberal flagging

**Author Self-Review First**:
- Authors fix obvious issues independently before meeting reviewers
- Reduces reviewer workload by 50-70% (estimate)
- Authors learn faster through immediate feedback
- Reviewers focus on complex pedagogical decisions, not mechanical fixes

**Specialized + Generalist Agents**:
- 60% specialists (deep expertise in one competency)
- 40% generalists (holistic view, catch interactions)
- Mimics having both subject experts and experienced editors

### Goals & Benefits

**Primary Goals**:
1. **Reduce reviewer time** from 2-3 hours to 30-45 minutes per module
2. **Reduce copy editor time** from 1-2 hours to 15-30 minutes per module
3. **Accelerate author iteration** from days to hours
4. **Scale content production** without proportionally scaling human reviewers
5. **Maintain quality standards** through consensus mechanism

**Secondary Benefits**:
- Consistent feedback across all modules (same rubrics, every time)
- New authors learn guidelines faster through immediate, detailed feedback
- Reviewers focus on high-value pedagogical decisions, not mechanical issues
- Reduced author frustration through faster feedback cycles
- Better work-life balance for reviewers (less tedious mechanical checking)

### Expected KPIs

> **Note**: The following estimates are based on initial testing with 1-2 example modules and expert review of the system architecture. Actual performance will be validated through broader testing and real-world deployment. These represent our best current projections, not guaranteed outcomes.

**Efficiency Metrics**:
- **Reviewer time per module**: 2-3 hours → 30-45 minutes (estimated 75% reduction)
- **Copy editor time per module**: 1-2 hours → 15-30 minutes (estimated 75% reduction)
- **Author iteration cycle**: 3-7 days → same day (estimated 10x faster)
- **Modules per week capacity**: 2-3 → 10-15 (estimated 3-5x increase)

**Quality Metrics**:
- **Issues caught before human review**: 50-70% of mechanical/obvious issues (based on current simulation)
- **Consistency**: 100% of modules checked against all 10 competencies (architectural guarantee)
- **False positive rate**: <30% target (acceptable with priority ranking)
- **Missed critical issues**: <5% target (consensus mechanism designed to catch most)

**Author Experience**:
- **Time to first feedback**: 3-7 days → <1 hour (system capability)
- **Revision cycles to publication**: 3-4 → 2-3 (projected based on earlier issue detection)
- **Author satisfaction**: Expected improvements in waiting time, feedback clarity, and iteration speed

**Business Impact**:
- **Content production rate**: Projected 3-5x increase without proportional reviewer hiring
- **Reviewer hiring needs**: Flat scaling instead of linear growth with content volume
- **Quality maintenance**: Consistent application of guidelines across all modules
- **Scalability**: System cost per module decreases as volume increases

## Quick Navigation

### 📊 **Demo Output** - See the System in Action
**Download and open in browser**: [test_review/output/test_module_review_report.html](test_review/output/test_module_review_report.html)
- Download the HTML file and open it in your browser to see the 8-tab review report
- GitHub will show raw HTML; you need to download and open locally

### 🔬 **[test_review/](test_review/)** - Active Review System
Complete simulation system for testing and running reviews:
- **simulate_30_agent_review.py** - 30-agent review engine with consensus mechanism
- **QUICKSTART.md** - How to run reviews
- **IMPLEMENTATION_SUMMARY.md** - Technical architecture details

### 📚 **[guides/](guides/)** - Educational Content Guidelines
Human-readable guides that define what makes good calculus content:
- **authoring_guide_full.txt** - How to create effective calculus lessons (35KB)
- **style_guide_full.txt** - Writing standards for clarity and consistency (56KB)

### 🎓 **[modules/](modules/)** - Sample Calculus Content
Example calculus modules including:
- **module_5_6_exemplary.xml** and **module_5_7_exemplary.xml** - Exemplar modules demonstrating quality standards
- Review logs and helper scripts for module processing

### ⚙️ **[config/](config/)** - System Configuration
Prompts and rubrics used by the AI review system:
- `prompts/` - Master review context, authoring rules, style rules
- `rubrics/` - XML-formatted rubric definitions (5 authoring + 5 style)
- `agent_configuration.xml` - 30-agent setup specification

## How the Review System Works

The system uses a **4-pass review architecture** designed to reduce the workload on human reviewers and copy editors:

### Pass 1: Initial AI Review

- **30 AI agents** (15 authoring + 15 style) review content against both guides
- **Consensus mechanism** aggregates findings:
  - Issues flagged by 2+ agents = high-confidence consensus issues
  - Single-agent findings = flagged for review (may include false positives)
  - **Priority ranking** = Severity × Consensus (0-5 scale)

**Author Self-Review**: Author addresses AI-flagged issues independently

### Pass 2: Second AI Review

- **30 AI agents** run again on revised content (both guides)
- Results sent to **both author and human reviewer**
- Ensures fixes are working, catches new issues

**Human Reviewer Meeting**: Reviewer and author discuss remaining issues together
- Reduced workload - most issues already fixed
- Focus on complex pedagogical decisions

### Pass 3: Third AI Review (Style Focus)

- **30 AI agents** focus on style guide only
- No pedagogical review in this pass
- Author revises based on findings

**Author Self-Review**: Author addresses AI-flagged style issues independently

### Pass 4: Fourth AI Review (Final Style Check)

- **30 AI agents** run again on revised content (style guide only)
- Results sent to **both author and copy editor**
- Final mechanical polish

**Copy Editor Meeting**: Copy editor and author discuss final polish
- Reduced workload - mechanical issues already fixed
- Focus on nuanced style decisions

**Output**: Publication-ready calculus content

## Key Principles for Calculus Content

The system checks for critical calculus pedagogy best practices:

- **Multiple Representations**: Graphical, numerical, and symbolic views of concepts
- **Addressing Misconceptions**: Common errors like "derivative = slope" vs. "instantaneous rate"
- **Conceptual Before Procedural**: Understanding "why" before "how"
- **Real-World Context**: Relatable examples (phone battery) vs. abstract ones (rockets)
- **Assessment Alignment**: Testing concepts, not just computation

## Technical Implementation

### Running Reviews

See **[test_review/QUICKSTART.md](test_review/QUICKSTART.md)** for how to run the review system.

**Key file**: `test_review/simulate_30_agent_review.py` (957 lines)
- Currently generates realistic simulated findings for testing
- In production: Replace with actual Anthropic API calls
- Outputs 8-tab HTML report + JSON data

**Note on Performance**: The current simulation demonstrates the consensus mechanism and priority ranking system working effectively. Real Anthropic API calls (Claude Opus/Sonnet) would provide significantly more nuanced issue detection, deeper pedagogical analysis, and more contextual suggestions than the simulated findings.

### Repository Structure

- **test_review/** - Active simulation system
- **config/** - Prompts and rubrics
- **guides/** - Human-readable authoring and style guides
- **modules/** - Sample calculus content
- **docs/** - Architecture documentation and expert reviews
- **scripts/** - Analysis and testing utilities
- **archive/** - Historical implementation artifacts

---

## Success Metrics

- **Consensus-based confidence** - 2+ agents = high-confidence issues
- **Priority-driven workflow** - Severity × Consensus ranking
- **Calculus-specific** pedagogical feedback (not generic or CS-focused)
- **Educational approach** - every issue explains why it matters
- **Author empowerment** - humans make final decisions
- **Liberal flagging** - Better to flag and dismiss than to miss real issues

## Questions?

1. **See the latest output**: Download and open `test_review/output/test_module_review_report.html` in your browser
2. **Run a review**: Follow [test_review/QUICKSTART.md](test_review/QUICKSTART.md)
3. **Understand the standards**: 
   - [guides/authoring_guide_full.txt](guides/authoring_guide_full.txt) - Pedagogy (Passes 1-2)
   - [guides/style_guide_full.txt](guides/style_guide_full.txt) - Writing quality (Passes 1-4)
4. **Review the rubrics**: Browse [config/rubrics/](config/rubrics/)

---

**Built for educators who care about helping non-traditional learners succeed in calculus.**
