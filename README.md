# Learnvia AI-Powered Content Revision System

## Overview

An intelligent educational content revision system that uses 60 AI reviewers in a structured 4-pass consensus approach to reduce human reviewer workload by 70-80% while maintaining quality and empowering authors through educational feedback.

### Core Philosophy
**Empower authors through educational feedback aligned with product vision, rather than gatekeeping through pass/fail judgments.**

## Key Features

- **60 AI Reviewers**: Distributed across 4 review passes for comprehensive coverage
- **Consensus Scoring**: High-confidence issue identification through reviewer agreement
- **Student-Success Framing**: Supportive, educational feedback instead of error lists
- **Parallel Processing**: Efficient API usage with concurrent reviewer execution
- **Adaptive Focusing**: Progress-aware review adjustments based on improvement rates
- **Multi-Format Reports**: Text, HTML, Markdown, JSON, and CSV output formats
- **Author Experience Levels**: Tailored feedback based on author expertise

## System Architecture

### Four-Pass Review Structure

1. **Pass 1: Initial Authoring Review (20 reviewers)**
   - 10 reviewers: Pedagogical flow and alignment
   - 10 reviewers: Component deep dive (examples, quiz, framing)

2. **Pass 2: Authoring Progress Review (10 reviewers)**
   - 5 reviewers: Adaptive progress check
   - 5 reviewers: Authoring readiness assessment

3. **Pass 3: Initial Style Review (20 reviewers)**
   - 10 reviewers: Writing mechanics and style compliance
   - 10 reviewers: Component style specifics

4. **Pass 4: Final Style Progress Review (10 reviewers)**
   - 5 reviewers: Style progress verification
   - 5 reviewers: Final readiness assessment

### Severity Framework

- **Level 5 (Critical)**: Mathematical errors, missing components
- **Level 4 (High)**: Core pedagogy issues
- **Level 3 (Medium)**: Writing quality issues
- **Level 2 (Low)**: Style compliance
- **Level 1 (Minor)**: Polish suggestions

### Confidence Levels

- **10/10 reviewers agree**: Very high confidence
- **7-9/10 agree**: High confidence
- **4-6/10 agree**: Moderate confidence
- **2-3/10 agree**: Low confidence
- **1/10 flags**: Very low confidence

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd LEARNVIA

# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key
export OPENAI_API_KEY='your-api-key-here'
```

## Quick Start

```python
from src.models import ModuleContent
from src.orchestrator import RevisionOrchestrator

# Create module content
module = ModuleContent(
    content=open('your_module.txt').read(),
    module_id='module_001',
    title='Your Module Title'
)

# Initialize orchestrator
orchestrator = RevisionOrchestrator()

# Run complete 4-pass review
session = orchestrator.run_complete_review(
    module,
    author_experience="new"  # or "experienced"
)

# Or run a single pass
report = orchestrator.run_single_pass(
    module,
    ReviewPass.AUTHORING_PASS_1
)
```

## Usage Examples

### Basic Review
```python
# Run example script to see demonstrations
python example_usage.py
```

### Load Module from File
```python
from src.orchestrator import ModuleLoader

module = ModuleLoader.load_from_file('path/to/module.txt')
```

### Custom API Configuration
```python
orchestrator = RevisionOrchestrator(
    api_key="your-api-key",
    output_dir="custom/reports/directory"
)
```

## Project Structure

```
LEARNVIA/
├── src/                       # Core system code
│   ├── models.py              # Data models and structures
│   ├── reviewers.py           # AI reviewer implementation (60 reviewers)
│   ├── aggregator.py          # Consensus aggregation logic
│   ├── report_generator.py    # Multi-format report generation
│   ├── orchestrator.py        # 4-pass workflow orchestration
│   ├── feedback_loop.py       # Dual learning mechanisms
│   └── claude_api.py          # Claude API integration
├── tests/                     # Test suite (55 tests)
│   ├── test_models.py
│   ├── test_reviewers.py
│   ├── test_aggregator.py
│   └── test_report_generator.py
├── scripts/                   # Utility scripts
│   ├── run_tests.py           # Test runner
│   ├── test_claude_workflow.py # Workflow test
│   └── example_usage.py       # Usage examples
├── config/                    # Configuration & guidelines
│   ├── authoring_prompt_rules.txt
│   ├── style_prompt_rules.txt
│   └── product_vision_context.txt
├── docs/                      # Documentation
│   ├── summaries/             # Executive summaries
│   ├── reports/               # System reports
│   ├── handoffs/              # Session handoffs
│   └── team_review/           # Team review materials
├── reports/                   # Generated HTML reports
├── feedback/                  # Feedback loop storage
│   ├── disputes/
│   ├── validations/
│   ├── patterns/
│   └── metrics/
├── modules/                   # Test modules
├── requirements.txt           # Python dependencies
├── NEXT_SESSION_START_HERE.md # Session handoff (always current)
└── README.md                  # This file
```

## Testing

```bash
# Run all tests (simple test runner)
python scripts/run_tests.py

# Run complete 4-pass workflow test
python scripts/test_claude_workflow.py

# Or use pytest
pytest tests/ -v

# Run specific test file
pytest tests/test_models.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Report Formats

The system generates reports in multiple formats:

1. **Text Report**: Human-readable console/file output
2. **HTML Report**: Web-viewable with styling and color coding
3. **Markdown Report**: Documentation-friendly format
4. **JSON Report**: Machine-readable for API integration
5. **CSV Export**: Spreadsheet-compatible issue list

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `LEARNVIA_OUTPUT_DIR`: Custom output directory (optional)

### Customization Options
- Similarity threshold for issue grouping (default: 75%)
- Reviewer temperature settings (0.6-0.9)
- Maximum tokens per reviewer (default: 2000)
- Retry settings for API calls

## API Costs

With 60 API calls per complete review:
- Estimated tokens per call: ~2000-3000
- Total tokens per review: ~120,000-180,000
- Cost varies based on OpenAI pricing

## Success Metrics

- **70-80%** reduction in human reviewer time
- **Quality maintenance** vs. current human review
- **Author skill improvement** over time
- **Reduced author turnover** through support

## Contributing

1. Follow TDD practices - write tests first
2. Maintain the student-success framing philosophy
3. Ensure all feedback is educational, not punitive
4. Test with various module types and edge cases

## Support

For issues or questions:
- Review the design document: `docs/plans/2025-10-28-ai-revision-system-design.md`
- Check example usage: `python example_usage.py`
- Examine test files for implementation details

## License

[Your License Here]

## Acknowledgments

Built for Learnvia to support non-traditional learners who struggle with traditional math education, particularly students from underserved communities.

---

**Remember**: This system is designed to empower authors through educational feedback, not to gatekeep. Every piece of feedback should help authors grow and improve their skills while serving students who need the most support.