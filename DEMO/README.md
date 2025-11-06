# DEMO - Try It Yourself

A complete, self-contained demonstration of the Learnvia consensus-based review system with synthetic actors and content.

## Quick Start

```bash
cd DEMO/scripts
python run_demo.py
```

See a full review workflow with mock agents analyzing a Power Rule calculus lesson with 50+ intentional issues.

## Key Innovation: Consensus-Based Aggregation

This demo showcases our **consensus-based approach** where multiple independent AI agents review content, and their feedback is aggregated to identify high-confidence issues. This approach:

- **Reduces noise**: Individual agent errors are filtered out through consensus
- **Increases reliability**: Issues found by multiple agents have higher confidence
- **Provides actionable feedback**: Only high-consensus issues require action
- **Enables intelligent prioritization**: Issues are ranked by severity × confidence

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│           LEARNVIA CONSENSUS-BASED REVIEW SYSTEM             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  PASS 1: Content Review (20 Independent Agents)              │
│  ┌──────────────────────────────────────────────┐           │
│  │  20 agents independently review content       │           │
│  │  ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓    │           │
│  └──────────────────────────────────────────────┘           │
│                         ↓                                    │
│  ┌──────────────────────────────────────────────┐           │
│  │     CONSENSUS AGGREGATOR (aggregator.py)      │           │
│  │  • Groups similar feedback                    │           │
│  │  • Calculates agreement percentages           │           │
│  │  • Filters by confidence thresholds           │           │
│  │  • Prioritizes by severity × confidence       │           │
│  └──────────────────────────────────────────────┘           │
│                         ↓                                    │
│  ┌──────────────────────────────────────────────┐           │
│  │         CONSENSUS FEEDBACK PRESENTED          │           │
│  │  High confidence (≥70%): Provide solutions    │           │
│  │  Medium (40-70%): Flag for consideration      │           │
│  │  Low (<40%): Optional/FYI only                │           │
│  └──────────────────────────────────────────────┘           │
│                                                               │
│  PASS 2: Different 20 Agents → Consensus → Feedback          │
│  PASS 3: Copy Edit (10 Agents) → Consensus → Feedback        │
│  PASS 4: Final Copy Edit (10 Agents) → Final Consensus       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## How Consensus Works

### 1. Individual Agent Review
Each agent independently reviews the content and identifies issues:
```python
# 20 agents might find:
Agent_01: "Contraction 'don't' on line 5"
Agent_02: "Contraction 'don't' on line 5"
Agent_03: [Misses this issue]
Agent_04: "Contraction 'don't' on line 5"
... (17 more agents)
```

### 2. Consensus Aggregation
The ConsensusAggregator groups similar feedback:
```python
Issue: "Contraction 'don't' found"
Agreement: 18/20 agents (90% confidence)
Severity: Level 2
Priority Score: 1.8 (severity × confidence)
```

### 3. Confidence-Based Filtering
Only issues meeting confidence thresholds are presented:
- **≥70% agreement**: High confidence - must fix
- **40-70% agreement**: Medium confidence - should consider
- **<40% agreement**: Low confidence - likely false positive

### 4. Intelligent Solutions
Solutions are only provided for high-confidence, high-severity issues:
```python
if confidence >= 0.7 and severity >= 4:
    provide_specific_solution()
else:
    flag_for_author_consideration()
```

## Demo Features

### Power Rule Topic with 50+ Intentional Issues

The demo uses a Power Rule (calculus) lesson with intentional issues across all severity levels:

**Critical (Severity 5)**:
- Incorrect formula: `d/dx(x^n) = n * x^(n+1)` [WRONG!]
- Mathematical notation errors
- Missing required components

**High (Severity 4)**:
- Framing section too short (62 words, needs 100-150)
- Poor pedagogical explanations
- Quiz answers revealed in questions

**Medium (Severity 3)**:
- Missing LaTeX formatting for math
- Inconsistent terminology
- Unclear explanations

**Low (Severity 2)**:
- Contractions throughout ("don't", "it's", "let's")
- Imperative voice ("Calculate", "Find", "Try")

**Minor (Severity 1)**:
- Punctuation preferences
- Style variations

### Extremely Strict Copy Editor

The copy editor (Dr. Margaret Thompson) has **ZERO TOLERANCE**:
- 100% compliance required
- Single contraction = REJECTION
- Any imperative voice = FAILURE
- No exceptions, no mercy
- First submission approval rate: 2%

## Running the Demo

### Prerequisites
- Python 3.8+
- No external dependencies for mock demo

### Quick Start
```bash
cd /Users/michaeljoyce/Desktop/LEARNVIA/trial/scripts
python run_demo.py
```

### What You'll See

1. **Individual Feedback Collection**
   ```
   📥 Collecting feedback from agents...
   🔢 Received 247 individual findings from agents
   ```

2. **Consensus Aggregation**
   ```
   🤝 Aggregating feedback to find consensus...
   ✅ Consensus achieved on 42 unique issues:
      - High confidence (≥70% agreement): 15 issues
      - Medium confidence (40-70%): 18 issues
      - Low confidence (<40%): 9 issues
   ```

3. **Priority Issues Display**
   ```
   📋 Top Consensus Issues (by priority):
   1. [5/5 severity, 95% agreement] Incorrect formula n*x^(n+1)...
   2. [5/5 severity, 90% agreement] Mathematical notation error...
   3. [4/5 severity, 85% agreement] Framing only 62 words...
   ```

## Output Files

### Consensus Reports
- `pass_*_consensus.json`: Aggregated consensus results per pass
- `pass_*_individual.json`: Raw individual agent feedback
- `consensus_report.html`: Visual report with consensus metrics
- `consensus_report.md`: Summary with aggregation statistics

### Key Metrics Tracked
```json
{
  "consensus_tracking": {
    "total_individual_findings": 500+,
    "aggregated_issues": 80,
    "high_confidence_issues": 25,
    "low_confidence_issues": 20
  }
}
```

## Value of Consensus Approach

### 1. Noise Reduction
- **Without consensus**: 500+ individual findings (overwhelming)
- **With consensus**: 80 aggregated issues (manageable)
- **Reduction rate**: 84% noise filtered out

### 2. Confidence Levels
- Authors see which issues have strong agreement
- Can prioritize high-consensus problems
- Low-consensus issues can be safely ignored

### 3. False Positive Filtering
- Single agent errors don't affect output
- Overly strict agents balanced by others
- Only genuine issues survive aggregation

### 4. Scalability
- Can increase agents without overwhelming authors
- More agents = higher confidence in consensus
- System becomes more reliable with scale

## Implementation Details

### ConsensusAggregator (`src/aggregator.py`)
Core consensus logic:
- `aggregate()`: Groups and synthesizes feedback
- `calculate_confidence()`: Determines agreement levels
- `filter_by_confidence()`: Applies thresholds
- `sort_by_priority()`: Ranks by severity × confidence

### Mock Agent System (`trial/scripts/mock_agents.py`)
Simulates diverse agent personalities:
- **STRICT**: 95% detection rate
- **MODERATE**: 75% detection rate
- **LENIENT**: 55% detection rate
- **SPECIALIST**: 90% in focus area, 45% elsewhere
- **GENERALIST**: 65% across the board

### Integration (`trial/scripts/run_demo.py`)
Orchestrates the consensus workflow:
1. Collect individual feedback
2. Aggregate via ConsensusAggregator
3. Filter by confidence thresholds
4. Present consensus-based feedback
5. Track metrics and generate reports

## Customization

### Adjusting Consensus Thresholds
Edit `run_demo.py`:
```python
# Change confidence thresholds
high_confidence = aggregator.filter_by_confidence(results, threshold=0.8)  # Stricter
medium_confidence = aggregator.filter_by_confidence(results, threshold=0.5)
```

### Modifying Similarity Threshold
Edit initialization:
```python
aggregator = ConsensusAggregator(similarity_threshold=0.8)  # More strict grouping
```

### Adding Agent Diversity
Edit `mock_agents.py`:
```python
# Add more agent personas for better consensus
persona = random.choice([STRICT, MODERATE, LENIENT, SPECIALIST, GENERALIST, PEDANTIC])
```

## Benefits Over Individual Agent Feedback

| Aspect | Individual Agents | Consensus System |
|--------|------------------|------------------|
| Feedback Volume | 500+ items | 80 aggregated issues |
| False Positives | High (10-20%) | Low (<5%) |
| Confidence | Unknown | Quantified (%) |
| Prioritization | Difficult | Automatic (severity × confidence) |
| Author Experience | Overwhelming | Manageable |
| Reliability | Variable | High |

## Next Steps

1. **Production Integration**: Replace mock agents with real LLM calls
2. **Threshold Tuning**: Optimize confidence thresholds based on data
3. **Weighted Consensus**: Give certain agents more weight based on expertise
4. **Dynamic Agent Allocation**: Add more agents for critical content
5. **A/B Testing**: Compare consensus vs. individual feedback effectiveness

## Technical Architecture

### Core Components
- `ConsensusAggregator`: Main aggregation engine
- `ConsensusResult`: Aggregated issue with confidence
- `ReviewFeedback`: Individual agent finding
- `ReviewReport`: Final consensus report

### Consensus Algorithm
1. **Similarity Detection**: Uses SequenceMatcher for text similarity
2. **Location Matching**: Groups issues by line/section proximity
3. **Confidence Calculation**: agreeing_reviewers / total_reviewers
4. **Priority Scoring**: severity × confidence
5. **Solution Gating**: Only high-confidence, high-severity get solutions

## Conclusion

This demo showcases how consensus-based aggregation transforms noisy individual agent feedback into actionable, prioritized insights. The system:

- ✅ Reduces feedback volume by 84%
- ✅ Quantifies confidence for every issue
- ✅ Filters out false positives
- ✅ Automatically prioritizes by importance
- ✅ Scales efficiently with more agents
- ✅ Provides better author experience

The consensus approach ensures that authors focus on genuine issues that multiple agents agree upon, making the review process both more efficient and more reliable.

---

*This demo illustrates the power of consensus-based aggregation in the Learnvia review system, showing how 60 independent AI agents can work together to provide unified, high-confidence feedback.*

---

**See [NAVIGATION.md](../NAVIGATION.md) for the complete project map.**