# Generic Rule-Based Content Review System

## Overview
Successfully converted the 30-agent content review system from hardcoded module-specific findings to a generic rule-based detection system that works on ANY educational module.

## What Was Fixed

### Original Problems (run_review.py)
1. **Hardcoded Findings**: Lines 250-515 contained hardcoded issues specific to the Power Series module
   - Hardcoded line numbers (e.g., "Line 3: Title is 'Todo'")
   - Hardcoded content quotes specific to Power Series
   - Would fail or give wrong results on any other module

2. **Data Leakage**: The simulation "knew" what issues to find beforehand
3. **Overfitting**: System only worked for one specific test module

### New Solution (run_review_generic.py)

#### Generic Rule-Based Detection System
Implemented a `RuleBasedDetector` class that uses pattern matching to detect issues:

1. **Todo Placeholders** (Severity 3)
   - Regex: `\btodo\b` (case-insensitive)
   - Detects unfinished content markers
   - Works on any field: Title, Description, KSAs, LearningOutcomes

2. **Contractions** (Severity 2)
   - Detects: what's, let's, don't, doesn't, won't, can't, isn't, etc.
   - Provides proper expansions (e.g., "don't" → "do not")
   - Distinguishes contractions from possessives

3. **Vague Pronouns** (Severity 2)
   - Detects: it, this, they without clear antecedents
   - Flags sentences starting with "It" or "This"
   - Improves clarity for struggling readers

4. **Missing LaTeX Tags** (Severity 2)
   - Detects mathematical symbols: ∑, ∏, ∫, ∞, ≈, ≤, ≥
   - Finds functions without LaTeX: sin(), cos(), log()
   - Identifies subscripts/superscripts: x_n, x^2

5. **Lazy Sentence Starts** (Severity 1)
   - Pattern: "There is/are/was/were"
   - Encourages active voice

6. **Complex Sentences** (Severity 1)
   - Detects sentences with 3+ commas
   - Flags semicolon usage
   - Promotes simpler structure for target learners

7. **Missing Definitions** (Severity 3)
   - Tracks technical terms: derivative, integral, convergence, etc.
   - Checks if terms are defined with `<definition>` tags
   - Critical for self-study students

8. **Pedagogical Issues** (Authoring agents)
   - Abstract before concrete detection
   - Missing scaffolding (jumping to complex topics)
   - Checks for explanation before application

## Agent Variability System

### Probability-Based Detection
Each agent has a probability of detecting issues based on severity:
- Severity 5: 90% of agents catch it (~27 agents)
- Severity 4: 80% of agents catch it (~24 agents)
- Severity 3: 60% of agents catch it (~18 agents)
- Severity 2: 40% of agents catch it (~12 agents)
- Severity 1: 20% of agents catch it (~6 agents)

### Agent Specialization
- **Authoring Specialists**: Focus on pedagogical flow, structure, clarity
- **Style Specialists**: Focus on mechanics, formatting, grammar
- **Generalists**: Broader coverage but lower detection rates
- Each agent has a deterministic seed for consistent but varied behavior

## Test Results

### Power Series Module
- **Total Findings**: 409
- **Consensus Issues**: 46 (flagged by 4+ agents)
- **Other Flagged**: 13 (flagged by 1-3 agents)
- Top issues: Todo placeholders, undefined technical terms

### Fund_Thm_of_Calculus Module
- **Total Findings**: 2,667
- **Consensus Issues**: 338
- **Other Flagged**: 58
- Much larger module with more content to review

## Key Improvements

1. **Truly Generic**: Works on ANY module without modification
2. **Rule-Based**: Uses regex patterns and heuristics, not hardcoded content
3. **Configurable**: Easy to add new rules or adjust severity/probability
4. **Maintainable**: Clear separation of detection rules from agent logic
5. **Realistic Variability**: Different agents catch different issues based on specialization and probability

## Files

- `run_review.py`: Original hardcoded version (1,378 lines)
- `run_review_generic.py`: New generic version (1,120 lines)
- Pattern matching rules in `RuleBasedDetector` class (lines 200-575)

## Usage

```bash
python run_review_generic.py <module_folder> <xml_file> <readable_file>

# Examples:
python run_review_generic.py Power_Series power_series_test.xml power_series_readable.txt
python run_review_generic.py Fund_Thm_of_Calculus module_5_6.xml module_5_6_readable.txt
```

## Limitations & Future Work

1. **Current Limitations**:
   - Some rules may generate false positives
   - Regex patterns may miss complex cases
   - No machine learning or context understanding

2. **Potential Improvements**:
   - Add more sophisticated NLP for pronoun resolution
   - Implement edit distance for near-miss detection
   - Add configuration file for rule customization
   - Integrate with actual LLM APIs for production use

## Conclusion

Successfully eliminated hardcoded module-specific content and created a generic, rule-based system that can analyze any educational module for style and authoring violations. The system maintains the multi-agent architecture with realistic variability while being completely content-agnostic.