# LEARNVIA Navigation Guide

**START HERE** - This is your map to understanding and working with the Learnvia content review system.

Last Updated: 2025-11-05

---

## 🚀 Quick Start

**New to Learnvia?** Read in this order:
1. This file (you're here!)
2. `README.md` (project overview)
3. `FOUNDATION/README.md` (understand the core principles)
4. `DOCUMENTATION/architecture.md` (see how the system works)
5. `DEMO/README.md` (run the demo to see it in action)

**Looking for something specific?** Use the directory guide below.

---

## 📁 Directory Guide

### `FOUNDATION/` ← **Source of Truth**
The original, authoritative documents that define what Learnvia is and how content should be created.

**What's in it:**
- `authoring_guide_full.txt` - Complete authoring guidelines
- `style_guide_full.txt` - Complete style guidelines
- `product_vision.txt` - Product vision and target audience
- `README.md` - Explains these documents

**When to use it:**
- Understanding the "why" behind the rules
- Deciding if a rule should be changed
- Creating new condensed versions or rubrics
- Onboarding new team members

**DO NOT modify these without team discussion!**

---

### `ACTIVE_CONFIG/` ← **What the System Uses RIGHT NOW**
The current configuration that AI agents are actually using. These are derived from FOUNDATION/ but condensed and structured for agent consumption.

**What's in it:**
- `prompts/` - Current condensed prompts for agents
  - `authoring_prompt_rules.txt`
  - `style_prompt_rules.txt`
  - `product_vision_context.txt`
- `rubrics/` - XML rubric files (10 competencies)
- `templates/` - XML prompt templates
- `agent_configuration.xml` - Master agent setup

**When to use it:**
- Modifying what agents see
- Adjusting rubrics or competencies
- Changing agent distribution or behavior
- Debugging agent responses

**Changes here affect production!**

---

### `DOCUMENTATION/` ← **How It Works**
Technical documentation, architecture explanations, and research.

**What's in it:**
- `architecture.md` - Hybrid rubric-generalist system explained
- `rubrics/` - Markdown documentation of all 10 rubrics
- `analysis/` - Research, comparisons, recommendations

**When to use it:**
- Understanding system architecture
- Learning about the hybrid approach
- Researching design decisions
- Writing technical documentation

**For reading, not execution.**

---

### `CODE/` ← **Python Source Code**
The actual implementation of the review system.

**Key files:**
- `reviewers.py` - Agent classes (BaseReviewer, RubricFocusedReviewer, GeneralistReviewer)
- `aggregator.py` - Consensus and voting system
- `orchestrator.py` - Multi-pass workflow coordination
- `models.py` - Data structures
- `claude_api.py` - API client
- `report_generator.py` - Creates review reports

**When to use it:**
- Implementing new features
- Fixing bugs
- Understanding how agents work
- Running the actual review system

**This is the production code.**

---

### `DEMO/` ← **Trial & Demonstration**
A complete, self-contained demo showing the entire review workflow with synthetic actors and content.

**What's in it:**
- `sample_content/` - Educational module drafts (Power Rule example)
- `synthetic_actors/` - Personas (author, reviewer, copy editor)
- `scripts/` - Demo orchestration code
- `outputs/` - Generated reports and feedback
- `README.md` - How to run the demo

**When to use it:**
- Demonstrating Learnvia to stakeholders
- Testing changes before production
- Understanding the end-to-end workflow
- Training new team members

**Run with:** `cd DEMO/scripts && python run_demo.py`

---

### `tests/` ← **Test Suite**
Unit and integration tests for the codebase.

**When to use it:**
- Running tests before commits
- Adding tests for new features
- Debugging failures

**Run with:** `pytest tests/`

---

### `ARCHIVE/` ← **Historical Materials**
Old plans, session notes, and deprecated files. Rarely accessed.

**What's in it:**
- `session_notes/` - Old session wrapups and notes
- `old_plans/` - Completed plans, setup guides

**When to use it:**
- Historical reference
- Understanding past decisions
- Archeology

**Ignore unless you need history.**

---

## 🔄 Common Workflows

### I want to change what agents see
1. Go to `ACTIVE_CONFIG/prompts/` or `ACTIVE_CONFIG/rubrics/`
2. Make your edits
3. Test with `DEMO/` or `tests/`
4. Commit changes

### I want to understand why a rule exists
1. Go to `FOUNDATION/`
2. Read the full guidelines
3. See context and reasoning

### I want to add a new competency
1. Create new rubric in `ACTIVE_CONFIG/rubrics/`
2. Document it in `DOCUMENTATION/rubrics/`
3. Update `CODE/reviewers.py` to use it
4. Update `ACTIVE_CONFIG/agent_configuration.xml`
5. Test with `DEMO/`

### I want to run a demo
```bash
cd DEMO/scripts
python run_demo.py
```

### I want to run the actual review system
```bash
cd CODE
python orchestrator.py --module path/to/module.md
```

---

## 🎯 Key Principles

1. **FOUNDATION/ is sacred** - Only change with team consensus
2. **ACTIVE_CONFIG/ is what runs** - Changes affect production
3. **DOCUMENTATION/ explains** - Keep it updated when system changes
4. **CODE/ implements** - This is the source of truth for behavior
5. **DEMO/ demonstrates** - Use it to test and show off
6. **ARCHIVE/ is historical** - Move completed work here

---

## 📊 System Architecture Quick Reference

**Hybrid Rubric-Generalist System**
- 10 competencies (5 authoring + 5 style)
- 60/40 split: rubric-focused specialists + holistic generalists
- 4-pass review: 2 content passes + 2 copy editing passes
- Consensus-based aggregation
- High severity + high confidence = prescriptive solutions

See `DOCUMENTATION/architecture.md` for details.

---

## 🆘 Lost? Start Here

**"I'm new and confused"**
→ Start with `README.md`, then `FOUNDATION/README.md`

**"I want to see it work"**
→ `cd DEMO/scripts && python run_demo.py`

**"I need to change agent behavior"**
→ `ACTIVE_CONFIG/`

**"I want to understand the system"**
→ `DOCUMENTATION/architecture.md`

**"I need to code something"**
→ `CODE/`

**"Where did that old plan go?"**
→ `ARCHIVE/`

---

## 📝 Maintenance

This NAVIGATION.md file should be updated when:
- Major folder structure changes
- New key files are added
- Workflows change significantly
- Common questions arise repeatedly

Keep it simple, scannable, and helpful.

---

**Questions?** Update this file or create an issue.
