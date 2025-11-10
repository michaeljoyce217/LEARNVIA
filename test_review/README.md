# Test Review: 30-Agent Simulation

This folder contains everything needed to test the layered AI content review system on a sample module.

## What's Here

### Module Files (`module_files/`)
- **`test_module_raw.xml`** - Raw XML module about power series convergence (provided by user)
- **`test_module_readable.txt`** - Human-readable formatted version for easy review

### Simulation Script
- **`simulate_30_agent_review.py`** - Python script that simulates the 30-agent review process

### Output (`output/`)
- **`test_module_review_report.html`** - Generated HTML report matching MODULE34_TABBED_REPORT.html format
- **`test_module_review_data.json`** - Raw JSON data with all findings and consensus issues

## How to Run

```bash
cd /Users/michaeljoyce/Desktop/LEARNVIA/test_review
python3 simulate_30_agent_review.py
```

The script will:
1. Load the layered prompt system (master, authoring, style, rubrics)
2. Simulate 30 agents reviewing the test module (15 authoring + 15 style)
3. Aggregate findings into consensus issues
4. Generate HTML report with boss feedback implemented
5. Save JSON data for analysis

## Architecture Details

### Agent Configuration (from agent_configuration.xml)
- **30 Total Agents**: 15 authoring + 15 style
- **60% Rubric-Focused**: 9 agents per domain focus on specific competencies
- **40% Generalists**: 6 agents per domain review cross-cutting issues

### Layered Prompt System
Each agent receives:
1. **Layer 1: Master Review Context** - Universal guardrails (master_review_context.txt)
2. **Layer 2: Domain Guidelines** - Authoring or style rules
3. **Layer 3: Rubric Focus** - Specific competency rubric (if rubric-focused agent)

### Consensus Aggregation
- Issues flagged by multiple agents get higher confidence
- Importance score = severity × consensus strength
- Similar issues grouped together
- Ranked by importance for author review

## Boss Feedback Implemented

✅ **Column is "Importance" not "Priority"**  
✅ **NO Severity column in final output**  
✅ **NO Confidence column in final output**  
✅ **All issues have specific line numbers and quotes**  
✅ **Issues are specific, not vague** (e.g., "Line 42: 'some students' → specify which students")

## Important Notes

### This is a SIMULATION
The `simulate_agent_review()` function generates realistic findings based on known patterns in the test module. In production, this function would:

```python
def simulate_agent_review(agent_id: str, prompt: str) -> List[Dict[str, Any]]:
    # Production: Call Claude/GPT API
    response = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": prompt}]
    )
    return parse_json_findings(response.content)
```

### Sub-Agent vs. Independent API Calls
This simulation uses **sub-agents** (shared LLM context) NOT independent API calls.

**What proper independent calls would provide:**
- ✅ **True diversity**: Each agent gets independent reasoning without context contamination
- ✅ **Parallel execution**: All 30 agents run simultaneously for faster results  
- ✅ **Independent judgment**: Genuine multi-perspective analysis vs. simulated variation

**Current simulation provides:**
- ✅ Demonstrates architecture and prompt layering
- ✅ Shows consensus aggregation logic
- ✅ Generates proper HTML output format
- ❌ Lacks true agent diversity
- ❌ Runs sequentially not in parallel

## Test Module Content

The test module covers **Power Series: Radius and Interval of Convergence** with:
- Abstract definitions and formulas
- Two animated figure specifications  
- Two multiple choice questions
- Two short answer questions
- Examples using ratio test

**Known Issues in Test Module:**
- Title/Description/KSAs/LearningOutcomes are "Todo" placeholders
- Mathematical notation uses Unicode subscripts instead of LaTeX `<m>` tags
- Dense abstract text before concrete examples
- Missing screen reader descriptions for figures
- Some conceptual explanations could be clearer

The simulation should detect these issues across different agent perspectives.

## Output Format

The HTML report matches `demo/MODULE34_TABBED_REPORT.html` with:
- **Overview Tab**: Metrics, architecture explanation, timestamp
- **Consensus Issues Tab**: Ranked issues with importance scores, line numbers, quotes, student impact, fixes
- **Category Distribution Tab**: Visual breakdown of issues by rubric category

Each issue includes:
- **Importance Score**: Calculated from severity × consensus strength
- **Issue Description**: Specific problem with line numbers
- **Location**: Exact line references
- **Quoted Text**: The problematic content from module
- **Student Impact**: How this affects learning
- **Suggested Fix**: Concrete actionable remedy
- **Agent Count**: How many of 30 agents flagged this

## Next Steps

1. **Run the simulation** to generate initial report
2. **Review output** - Does it match MODULE34_TABBED_REPORT.html format?
3. **Validate findings** - Are issues specific with line numbers?
4. **Check boss feedback** - Is "Importance" used, are Severity/Confidence columns removed?
5. **Test on real modules** - Replace `simulate_agent_review()` with actual LLM API calls
6. **Parallel execution** - Implement async API calls for true independent agents

## Files Referenced

The simulation loads from the main LEARNVIA config:
- `config/prompts/master_review_context.txt`
- `config/prompts/authoring_prompt_rules.txt`  
- `config/prompts/style_prompt_rules.txt`
- `config/rubrics/authoring_*.xml` (5 rubrics)
- `config/rubrics/style_*.xml` (5 rubrics)

These were created and validated through the Opus review process documented in:
- `docs/OPUS_REVIEW_1_SUMMARY.md`
- `docs/OPUS_REVIEW_2_SUMMARY.md`
