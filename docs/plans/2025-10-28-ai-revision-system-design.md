# Learnvia AI-Powered Content Revision System Design
## Date: 2025-10-28
## Version: 1.0

## Executive Summary

This document outlines the design for an AI-powered revision system for Learnvia educational modules. The system uses 60 AI reviewers in a structured consensus approach to reduce human reviewer workload by 70-80% while maintaining quality and empowering authors to improve their skills.

**Core Philosophy:** Empower authors through educational feedback aligned with product vision, rather than gatekeeping through pass/fail judgments.

## System Overview

### Key Metrics
- **Total AI Reviewers:** 60 (30 for authoring guidelines, 30 for style guide)
- **Review Passes:** 4 (2 authoring, 2 style)
- **Author Revision Points:** 3 (after each AI pass except the last)
- **Target Efficiency:** 70-80% reduction in human reviewer time
- **Module Size:** ~5,000 words (stripped-down format for non-traditional learners)

### Guiding Documents
1. **Product Vision** (Learnvia_Product_Vision_2025.txt) - Overriding theme for all reviews
2. **Authoring Guidelines** (Learnvia_authoring_guidelines_2025.txt) - Pedagogical requirements
3. **Style Guide** (Learnvia_style_guide_091625.txt) - Mechanical requirements

## Architecture: Four-Pass Consensus System

### AUTHORING GUIDELINES REVIEW (30 Reviewers)

#### Pass 1: Initial Authoring Review (20 reviewers)
**Stage 1 - Pedagogical Flow (10 reviewers)**
- 5 reviewers examine teaching flow: framing→lesson→examples→quiz coherence
- 5 reviewers check component alignment with product vision
- Focus: Does this module serve the "studying alone, low confidence" learner?

**Stage 2 - Component Deep Dive (10 reviewers)**
- 3 reviewers: Examples (mathematical correctness, progression)
- 3 reviewers: Quiz questions & feedback quality
- 2 reviewers: Framing effectiveness
- 2 reviewers: Homework appropriateness

**Output:** Comprehensive pedagogical feedback with confidence scores

#### Author Revision Period 1
- Authors receive educationally-framed feedback
- Issues ranked by confidence (1-10/10) and severity (1-5)
- Estimated revision time provided

#### Pass 2: Authoring Progress Review (10 reviewers)
**Stage 3 - Adaptive Progress Check (5 reviewers)**
- Fresh perspective on revised module
- Adaptive focus based on completion rate:
  - 80%+ fixed: Polish and refinement
  - 50-80% fixed: Reinforce critical issues
  - <50% fixed: Focus on highest severity only

**Stage 4 - Authoring Readiness Assessment (5 reviewers)**
- Evaluate alignment with authoring guidelines
- Provide recommendation to next phase:
  - Green: Ready for style review
  - Yellow: Proceed with noted guidance areas
  - Orange: Significant pedagogy gaps remain

### STYLE GUIDE REVIEW (30 Reviewers)

#### Pass 3: Initial Style Review (20 reviewers)
**Stage 1 - Writing Mechanics (10 reviewers)**
- 5 reviewers: Style guide compliance (contractions, imperatives, formatting)
- 5 reviewers: Mathematical notation and consistency
- All maintaining product vision alignment

**Stage 2 - Component Style Specifics (10 reviewers)**
- 3 reviewers: Question wording and clarity
- 3 reviewers: Example presentation and formatting
- 2 reviewers: Framing text style
- 2 reviewers: Overall consistency

**Output:** Style and mechanical feedback

#### Author Revision Period 2
- Focus on mechanical improvements
- Clear examples of style violations
- Resource links to style guide sections

#### Pass 4: Final Style Progress Review (10 reviewers)
**Stage 3 - Style Progress Check (5 reviewers)**
- Verify style improvements
- Catch any regression in pedagogical quality
- Final polish suggestions

**Stage 4 - Final Readiness Assessment (5 reviewers)**
- Overall guide compliance check
- Recommendation for human reviewer:
  - Green: Standard review recommended
  - Yellow: Review with mentoring focus
  - Orange: Substantial support needed

### HUMAN REVIEW (Final Step)
- Receives AI preprocessing from all 60 reviewers
- Clear focus areas based on AI assessment
- Handles disputes and edge cases
- Makes final approval decision

## Severity Framework

### Level 5 - Critical (Must Fix)
- Incorrect mathematical content
- Missing core module components
- Major product vision misalignment
- Accessibility violations

### Level 4 - High (Core Pedagogy)
- Poor chunking/scaffolding
- Missing concrete examples
- Lack of interactivity
- Target learner misalignment

### Level 3 - Medium (Writing Quality)
- Synonym/homonym violations
- Complex sentence structures
- Vague references
- Missing definitions

### Level 2 - Low (Style Compliance)
- Improper imperative usage
- Contractions in instruction
- Formatting inconsistencies
- Minor punctuation issues

### Level 1 - Minor (Polish)
- Word choice improvements
- Verbose passages
- Optional enhancements

## Consensus Scoring System

### Confidence Levels
- **10/10 reviewers agree:** Very high confidence - critical issue
- **7-9/10 agree:** High confidence - important issue
- **4-6/10 agree:** Moderate confidence - should consider
- **2-3/10 agree:** Low confidence - optional consideration
- **1/10 flags:** Very low confidence - FYI only

### Feedback Presentation
All issues reported, but with confidence-based framing:
- High confidence + high severity → Specific solution provided
- All others → Issue identified, author develops solution
- Single reviewer flags marked as "low confidence - may be fine"

## Feedback Philosophy

### Student-Success Framing
Instead of: "ERROR: Concept jump too large"
Present as: "Learning Opportunity: Students might struggle with this concept jump. Consider adding an intermediate step."

### Author Empowerment Features
1. **Strengths Callout** - What the module does well
2. **Priority Matrix** - What to tackle first
3. **Time Estimates** - Expected revision duration
4. **Learning Resources** - Links to guidelines
5. **Dispute Mechanism** - Author can explain reasoning

### Experience-Based Adaptation
**New Authors:**
- See only 7+ confidence issues initially
- Extra educational context
- Encouragement on strengths
- Access to first-module guidance

**Experienced Authors:**
- All feedback visible
- Streamlined presentation
- Bulk dismiss options
- Advanced insights

## Implementation Considerations

### Prompt Engineering
Each reviewer gets:
1. Base prompt with role and product vision context
2. Specific guideline injection (authoring OR style)
3. Variation for perspective (student focus, precision focus, etc.)
4. Structured output format requirements

### API Architecture
- Parallel execution within each stage (all 10 reviewers concurrent)
- Sequential execution between stages
- Estimated 60 API calls per complete module review
- No budget constraints for POC

### Feedback Loop
- Track human reviewer accept/reject patterns
- If rejection rate >30% for category, flag for prompt refinement
- Monthly prompt adjustment based on patterns
- Continuous improvement focus

## Success Metrics

### Primary Goals
- 70-80% reduction in human reviewer time
- Quality maintenance vs. current human review
- Author skill improvement over time
- Reduced author turnover through support

### Tracking Metrics
- Issues found vs. human baseline
- Author revision completion rates
- Time to acceptable module
- Dispute rates and resolutions
- Author retention/success rates

## Risk Mitigation

### Overwhelming Authors
- Adaptive feedback volume based on experience
- Clear prioritization
- Supportive framing
- Time estimates to set expectations

### Inconsistent AI Feedback
- Consensus mechanism reduces noise
- Confidence scoring sets expectations
- Human reviewer as final arbiter
- Continuous prompt refinement

### Guide Misalignment
- Regular prompt updates as guides evolve
- Human reviewer catches systematic issues
- Feedback loop for prompt adjustment

## Next Steps

1. **Prompt Development** - Create base prompts and variations
2. **Test Corpus Preparation** - Gather human-reviewed examples
3. **POC Implementation** - Build orchestration system
4. **Validation Testing** - Compare against human reviews
5. **Author Trial** - Test with volunteer authors
6. **Refinement** - Adjust based on results
7. **Full Deployment** - Roll out to all authors

## Conclusion

This system balances thoroughness with empowerment, using 60 AI reviewers to provide comprehensive, educational feedback while reducing human reviewer workload. The key innovation is the consensus-based confidence scoring combined with student-success framing, ensuring authors receive supportive guidance aligned with Learnvia's product vision of serving non-traditional learners.

By treating revision as an educational opportunity rather than a gatekeeping exercise, the system aims to develop author capabilities while maintaining content quality, ultimately serving students who struggle with traditional math education.