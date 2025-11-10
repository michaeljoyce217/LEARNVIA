# LEARNVIA - AI-Powered Calculus Content Review System

## What This Is

A 30-agent AI review system that helps calculus content authors improve their work through educational feedback. The system reviews Calculus I-IV educational content using specialized AI agents focused on calculus pedagogy and writing quality.

### Core Philosophy

**Empower authors through educational feedback aligned with pedagogical best practices, rather than gatekeeping through pass/fail judgments.**

This system is designed to support non-traditional learners who struggle with traditional math education, particularly students from underserved communities.

## Quick Navigation

### 📊 **[test_review/](test_review/)** - Active Review System
Complete simulation system for testing and running reviews:
- **simulate_30_agent_review.py** - 30-agent review engine with consensus mechanism
- **output/** - Generated HTML reports and JSON data
- **QUICKSTART.md** - How to run reviews
- **IMPLEMENTATION_SUMMARY.md** - Technical architecture details

### 📚 **[guides/](guides/)** - Educational Content Guidelines
Human-readable guides that define what makes good calculus content:
- **authoring_guide_full.txt** - How to create effective calculus lessons (35KB)
- **style_guide_full.txt** - Writing standards for clarity and consistency (56KB)

### 🎓 **[modules/](modules/)** - Sample Calculus Content
Example calculus modules including:
- **5.6/** and **5.7/** - Exemplar modules demonstrating quality standards
- Test modules used for system development

### ⚙️ **[config/](config/)** - System Configuration
Prompts and rubrics used by the AI review system:
- `prompts/` - Master review context, authoring rules, style rules
- `rubrics/` - XML-formatted rubric definitions (5 authoring + 5 style)
- `agent_configuration.xml` - 30-agent setup specification

## How the Review System Works

The system uses a **4-pass review architecture**:

### Pass 1: Initial 30-Agent Content Review (CURRENT FOCUS)

- **15 authoring agents** check pedagogy, clarity, and teaching quality
- **15 style agents** check writing, formatting, and consistency
- Each agent independently identifies issues
- **Consensus mechanism** aggregates findings:
  - Issues flagged by 2+ agents = high-confidence consensus issues
  - Single-agent findings = flagged for review (may include false positives)
- **Priority ranking** = Severity × Consensus (0-5 scale)

**Human Review Checkpoint**: Author reviews flagged issues and makes fixes

### Pass 2: Refinement Review

- Same 30-agent review on revised content
- Ensures initial fixes are working
- Identifies any new issues introduced

**Human Review Checkpoint**: Author addresses remaining issues

### Passes 3-4: Copy Editor Focus

- **Style guide only** - mimics professional copy editor
- Focus on writing mechanics, formatting, and consistency
- Final polish before publication

**Human Review Checkpoint**: Final approval

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

1. **See the latest output**: Open `test_review/output/test_module_review_report.html`
2. **Run a review**: Follow [test_review/QUICKSTART.md](test_review/QUICKSTART.md)
3. **Understand the standards**: Read [guides/authoring_guide_full.txt](guides/authoring_guide_full.txt)
4. **Review the rubrics**: Browse [config/rubrics/](config/rubrics/)

---

**Built for educators who care about helping non-traditional learners succeed in calculus.**
