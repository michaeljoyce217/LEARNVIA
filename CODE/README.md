# CODE - Python Implementation

This folder contains the actual review system implementation. The production code.

## Key Files

- `reviewers.py` - Agent classes and review logic
  - `BaseReviewer`, `RubricFocusedReviewer`, `GeneralistReviewer`
  - How individual agents conduct reviews

- `aggregator.py` - Consensus and voting
  - Groups similar feedback, calculates confidence, filters by thresholds
  - Ranks issues by severity × confidence

- `orchestrator.py` - Multi-pass workflow coordination
  - Manages 4-pass review sequence (2 content + 2 copy editing)
  - Handles feedback collection and aggregation

- `report_generator.py` - Report creation and formatting
  - Generates final review reports and metrics

- `models.py` - Data structures
  - ReviewFeedback, ConsensusResult, ReviewReport, etc.

- `claude_api.py` - API client for Claude
  - Handles authentication and requests

- `feedback_loop.py` - Iterative refinement
  - Manages feedback cycles with authors

## Entry Points

- **Run a review**: `python orchestrator.py --module path/to/module.md`
- **Run tests**: `pytest ../tests/`
- **Run demo**: `cd ../DEMO/scripts && python run_demo.py`

## Key Concepts

- **Hybrid approach**: 60% rubric specialists + 40% holistic generalists
- **Consensus**: Aggregates multiple agents to find high-confidence issues
- **Multi-pass**: Content review, then copy editing with fresh agents
- **Severity + Confidence**: Only prescriptive solutions for high severity × high confidence

---

**See [NAVIGATION.md](../NAVIGATION.md) for the complete project map.**
