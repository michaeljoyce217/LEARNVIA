# LEARNVIA - AI-Powered Calculus Content Review System

## What This Is

An intelligent review system that helps calculus content authors improve their work through educational AI feedback. The system reviews Calculus I-IV educational content using 30 AI agents focused on calculus pedagogy and teaching quality.

### Core Philosophy

**Empower authors through educational feedback aligned with pedagogical best practices, rather than gatekeeping through pass/fail judgments.**

This system is designed to support non-traditional learners who struggle with traditional math education, particularly students from underserved communities.

## Quick Navigation

### 📊 **[demo/](demo/)** - See the System in Action
View a complete example of the system reviewing actual calculus content:
- **[MODULE34_TABBED_REPORT.html](demo/MODULE34_TABBED_REPORT.html)** - Open this in your browser to see the review system's output

### 📚 **[guides/](guides/)** - Educational Content Guidelines
Human-readable guides that define what makes good calculus content:
- **authoring_guide_full.txt** - How to create effective calculus lessons
- **style_guide_full.txt** - Writing standards for clarity and consistency

### 📖 **[rubrics/](rubrics/)** - Review Standards (Human-Readable)
Markdown files explaining how content is evaluated:
- Pedagogical Flow
- Conceptual Clarity
- Assessment Quality
- Student Engagement
- Accessibility and more...

### 🎓 **[modules/](modules/)** - Sample Calculus Content
Example calculus modules that have been reviewed by the system.

### ⚙️ **[config/](config/)** - System Configuration
XML-formatted rubrics and prompts used by the AI review system:
- `rubrics/` - Machine-readable rubric definitions
- `prompts/` - Specialized reviewer instructions
- `agent_configuration.xml` - AI agent setup

## How the Review System Works

The system uses a **4-pass review process**:

1. **Pass 1: Content Review** (30 agents)
   - 15 authoring agents check pedagogy, clarity, and teaching quality
   - 15 style agents check writing, formatting, and consistency
   - Agents identify potential issues independently

2. **Consensus Aggregation**
   - Multiple agents finding the same issue = high confidence
   - Single agent findings = flagged for human review
   - Result: ~90% reduction in false positives

3. **Author Review**
   - Author receives educational feedback explaining WHY something matters
   - Author decides which issues to address
   - Human stays in control

4. **Passes 2-4**
   - Follow-up reviews ensure improvements are working
   - Progressive refinement toward publication quality

## Key Principles for Calculus Content

The system checks for critical calculus pedagogy best practices:

- **Multiple Representations**: Graphical, numerical, and symbolic views of concepts
- **Addressing Misconceptions**: Common errors like "derivative = slope" vs. "instantaneous rate"
- **Conceptual Before Procedural**: Understanding "why" before "how"
- **Real-World Context**: Relatable examples (phone battery) vs. abstract ones (rockets)
- **Assessment Alignment**: Testing concepts, not just computation

## Technical Implementation

All technical code, scripts, and implementation details are in **[_system/](_system/)**.

This includes:
- Python source code
- Test suites
- Implementation scripts
- Technical documentation
- Development history

---

## Success Metrics

- **90% reduction** in false positive issues through consensus
- **Calculus-specific** pedagogical feedback (not generic or CS-focused)
- **Educational approach** - every issue explains why it matters
- **Author empowerment** - humans make final decisions

## Questions?

1. **See it in action**: Open [demo/MODULE34_TABBED_REPORT.html](demo/MODULE34_TABBED_REPORT.html)
2. **Understand the standards**: Read [guides/authoring_guide_full.txt](guides/authoring_guide_full.txt)
3. **Review the rubrics**: Browse [rubrics/](rubrics/)
4. **Technical details**: Explore [_system/](_system/)

---

**Built for educators who care about helping non-traditional learners succeed in calculus.**
