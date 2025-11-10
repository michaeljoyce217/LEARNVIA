# Quick Start: Test Review System

## Run the Simulation (2 minutes)

```bash
cd /Users/michaeljoyce/Desktop/LEARNVIA/test_review
python3 simulate_30_agent_review.py
```

Expected output:
```
================================================================================
LEARNVIA 30-Agent Content Review Simulation
================================================================================

Loading layered prompt system...
✓ Master context: 8267 chars
✓ Authoring rules: 9830 chars
✓ Style rules: 15669 chars

Loading test module...
✓ Module loaded: 5897 chars

Simulating 30 agent reviews...

AUTHORING AGENTS (15 total):
  ✓ Authoring-Specialist-PedagogicalFlow-1: 1 findings
  [... 15 agents total ...]

STYLE AGENTS (15 total):
  ✓ Style-Specialist-MathematicalFormatting-2: 1 findings
  [... 15 agents total ...]

================================================================================
TOTAL FINDINGS: 34

Aggregating consensus issues...
✓ Consensus issues identified: 6

Generating HTML report...
✓ Report saved: output/test_module_review_report.html
✓ JSON data saved: output/test_module_review_data.json

================================================================================
SIMULATION COMPLETE
================================================================================
```

## View the Results

### HTML Report (Recommended)
```bash
open output/test_module_review_report.html
```

The report shows:
- **Overview Tab**: Metrics and architecture explanation
- **Consensus Issues Tab**: Ranked problems with line numbers, quotes, impacts, fixes
- **Category Distribution Tab**: Visual breakdown by rubric category

### JSON Data (For Analysis)
```bash
python3 -m json.tool output/test_module_review_data.json | less
```

Contains:
- All 34 individual findings from agents
- 6 consensus issues with importance scores
- Metadata: timestamps, agent counts, percentages

## What the Simulation Tests

### Input
- Your power series test module (XML)
- Layered prompt system (master + domain + rubrics)
- 30-agent architecture (60% specialists, 40% generalists)

### Processing
- Each agent reviews using 3-layer prompt
- Findings aggregated by similarity
- Consensus scoring and importance ranking
- Noise filtering (34 → 6 issues)

### Output
- HTML report matching MODULE34_TABBED_REPORT.html format
- Boss feedback implemented: "Importance" column, no Severity/Confidence, specific line numbers
- JSON data for programmatic analysis

## Files Created

```
test_review/
├── README.md                          ← How to use (detailed)
├── QUICKSTART.md                      ← This file
├── IMPLEMENTATION_SUMMARY.md          ← What we built (comprehensive)
├── simulate_30_agent_review.py        ← Main script (957 lines)
│
├── module_files/
│   ├── test_module_raw.xml           ← Your test module
│   └── test_module_readable.txt      ← Human-readable version
│
└── output/
    ├── test_module_review_report.html ← Beautiful HTML report
    └── test_module_review_data.json   ← Raw JSON data
```

## Key Features Demonstrated

✅ **Layered Prompt System**
- Layer 1: Master review context (universal guardrails)
- Layer 2: Domain guidelines (authoring vs. style)
- Layer 3: Rubric focus (specialist competencies)

✅ **Hybrid Agent Architecture**
- 60% rubric-focused specialists (deep expertise)
- 40% generalists (cross-cutting patterns)
- 30 total agents (15 authoring + 15 style)

✅ **Consensus Aggregation**
- Groups similar findings
- Calculates importance = severity × consensus
- Ranks by importance for authors

✅ **Boss Feedback Compliance**
- "Importance" not "Priority"
- No Severity/Confidence columns
- Specific line numbers and quotes
- Student impact + concrete fixes

## What's Missing (By Design)

This is a **simulation** using hardcoded findings, not real LLM calls.

**To make it production-ready:**

1. Replace `simulate_agent_review()` with actual Anthropic API calls
2. Add parallel execution with asyncio for speed
3. Implement error handling and retries
4. Add cost tracking and optimization

See `IMPLEMENTATION_SUMMARY.md` for production upgrade path.

## Validation

Expected consensus issues detected:

1. **Title is "Todo" placeholder** (Severity 5, Structural Integrity)
2. **Misleading x=-1 explanation** (Severity 4, Conceptual Clarity)  
3. **Mathematical notation without LaTeX** (Severity 2, Math Formatting)
4. **Inconsistent series notation** (Severity 2, Consistency)
5. **Missing screen reader description** (Severity 3, Accessibility)
6. **Dense abstraction before examples** (Severity 3, Pedagogical Flow)

All issues have:
- Exact line numbers (e.g., "Line 3" or "Lines 42-43")
- Quoted problematic text
- Student impact explanation
- Concrete suggested fix

## Next Steps

1. **Open the HTML report** - Verify it matches MODULE34_TABBED_REPORT.html format
2. **Check the JSON data** - Examine consensus issues structure
3. **Review the code** - Understand the architecture in `simulate_30_agent_review.py`
4. **Test on real modules** - Apply to modules 5.6 or 5.7
5. **Integrate real LLM** - Replace simulation with API calls

## Questions?

See comprehensive docs:
- `README.md` - Architecture and usage details
- `IMPLEMENTATION_SUMMARY.md` - Complete build documentation
- `../docs/layered_prompt_architecture.md` - System design
- `../docs/OPUS_REVIEW_2_SUMMARY.md` - Expert validation

---

**Ready?** Run `python3 simulate_30_agent_review.py` and open the HTML report!
