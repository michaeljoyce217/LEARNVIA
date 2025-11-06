# ACTIVE_CONFIG - Production Configuration

This folder contains **what the system currently uses in production**. Every file here affects live agent behavior.

## What's Here

- `prompts/` - Condensed prompt rules agents receive
  - `authoring_prompt_rules.txt` - Authoring competencies
  - `style_prompt_rules.txt` - Style competencies
  - `product_vision_context.txt` - Context and constraints

- `rubrics/` - 10 XML rubrics (5 authoring + 5 style)
  - Assessment Quality, Conceptual Clarity, Pedagogical Flow, Structural Integrity, Student Engagement
  - Accessibility, Consistency, Math Formatting, Mechanical Compliance, Punctuation/Grammar

- `templates/` - XML prompt templates for agents

- `agent_configuration.xml` - Master agent distribution and behavior setup

## Key Principle

**Changes here affect production immediately.** Test thoroughly before modifying.

## When to Use This

- Adjusting what agents see or evaluate
- Tuning rubric criteria or severity levels
- Changing agent distribution or review passes
- Debugging agent behavior
- Improving prompt clarity for agents

---

**See [NAVIGATION.md](../NAVIGATION.md) for the complete project map.**
