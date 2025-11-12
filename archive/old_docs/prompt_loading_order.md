# Prompt Loading Order

AI agents must load prompts in this specific order to ensure proper layering:

## Layer 1: Master Context (ALWAYS FIRST)

**File:** `config/prompts/master_review_context.txt`

**Purpose:** Establishes guardrails for ALL reviews

**Key Sections:**
- Out of scope items (images/animations)
- Content structure facts
- Specificity requirements
- Chain-of-thought requirements
- Anti-pattern guards
- Confidence scoring

## Layer 2: Domain Guidelines (SECOND)

### Authoring Rules

**File:** `config/prompts/authoring_prompt_rules.txt`

**Purpose:** Pedagogical and structural guidelines

**Key Sections:**
- Six core principles (ORGANIZED, CONCISE, PRECISE, INTUITIVE, CONCRETE, INTERACTIVE)
- Module structure requirements
- Critical writing rules
- Animated figures requirements
- Learning questions requirements

### Style Rules

**File:** `config/prompts/style_prompt_rules.txt`

**Purpose:** Writing mechanics and formatting

**Key Sections:**
- Mechanical rules (contractions, imperative voice, pronouns)
- Mathematical style rules
- LaTeX coding requirements
- Accessible style rules

## Layer 3: Competency Rubric (THIRD)

**Files:** `config/rubrics/*.xml`

**Purpose:** Specific evaluation criteria for assigned competency

**Available Rubrics:**
- `authoring_pedagogical_flow.xml`
- `authoring_structural_integrity.xml`
- `authoring_student_engagement.xml`
- (etc. - 15 total)

## Implementation in Agent System

### For Single Agent Review

```python
# Load prompts in order
master_context = load_file('config/prompts/master_review_context.txt')
authoring_rules = load_file('config/prompts/authoring_prompt_rules.txt')
style_rules = load_file('config/prompts/style_prompt_rules.txt')
rubric = load_file(f'config/rubrics/{competency}.xml')

# Construct full prompt
full_prompt = f"""
{master_context}

---

{authoring_rules}

---

{style_rules}

---

{rubric}

---

[MODULE CONTENT]

---

Your task: Review the module above following ALL layers of guidance.
"""
```

### For Multi-Agent System

Each agent gets:
1. Master context (same for all)
2. Domain prompts (same for all)
3. Specific rubric (based on assignment)

**Critical:** Master context MUST be first to establish guardrails before domain knowledge.

## Testing Prompt Order

To verify prompts are loaded correctly:

```bash
# Test single agent
python scripts/test_sonnet_review.py --module modules/module_5.6_exemplary.xml

# Check output includes specificity requirements
grep -i "line number" outputs/test_review_5.6_sonnet.json
```

Expected: All issues have line numbers, quotes, impacts, suggestions
