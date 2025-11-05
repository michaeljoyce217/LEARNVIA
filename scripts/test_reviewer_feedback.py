#!/usr/bin/env python3
"""
Demonstration of the reviewer feedback loop.
Shows how the system learns from what AI misses.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.reviewer_feedback_loop import ReviewerFeedbackLoop
from src.models import ReviewPass


def simulate_reviewer_feedback():
    """Simulate a human reviewer finding issues AI missed."""

    print("="*70)
    print("REVIEWER FEEDBACK LOOP DEMONSTRATION")
    print("="*70)
    print("\nGoal: Learn from what AI reviewers miss")
    print("Philosophy: Accept that nothing is perfect, improve systematically\n")

    feedback_loop = ReviewerFeedbackLoop()

    # Set acceptable miss rate (15% is realistic)
    feedback_loop.set_acceptable_miss_rate(0.15)

    print("\n📋 Simulating Human Review Session...")
    print("-"*40)

    # Simulate confirming some AI issues
    print("\n✅ Human confirms AI-found issues:")
    for i in range(7):
        feedback_loop.log_confirmed_issue(f"module_{i:03d}", f"ai_issue_{i}")
        print(f"   • Confirmed: AI correctly identified issue {i+1}")

    # Simulate finding missed issues (pattern emerges)
    print("\n❌ Human finds issues AI missed:")

    missed_issues = [
        # Pattern 1: Poor chunking (will trigger after 5 occurrences)
        {
            "module": "algebra_001",
            "issue": "Large conceptual jump between basic addition and algebraic expressions",
            "severity": 4,
            "location": "Section 2",
            "type": "pedagogical"
        },
        {
            "module": "geometry_002",
            "issue": "No intermediate step between 2D and 3D visualization",
            "severity": 4,
            "location": "Examples section",
            "type": "pedagogical"
        },
        {
            "module": "calculus_003",
            "issue": "Concept chunking too large - needs breakdown",
            "severity": 4,
            "location": "Lesson content",
            "type": "pedagogical"
        },
        {
            "module": "stats_004",
            "issue": "Missing scaffolding between mean and standard deviation",
            "severity": 4,
            "location": "Section 3",
            "type": "pedagogical"
        },
        {
            "module": "trig_005",
            "issue": "Chunking issue - jumps from angles to unit circle",
            "severity": 4,
            "location": "Lesson",
            "type": "pedagogical"
        },

        # Pattern 2: Missing concrete examples (will trigger)
        {
            "module": "algebra_001",
            "issue": "No concrete example for abstract concept",
            "severity": 3,
            "location": "Definition section",
            "type": "examples"
        },
        {
            "module": "geometry_002",
            "issue": "Missing student-relevant example",
            "severity": 3,
            "location": "Applications",
            "type": "examples"
        },
        {
            "module": "physics_003",
            "issue": "Abstract formula without concrete example",
            "severity": 3,
            "location": "Formula section",
            "type": "examples"
        },

        # Critical issue (triggers faster)
        {
            "module": "calculus_006",
            "issue": "Incorrect derivative formula",
            "severity": 5,
            "location": "Example 3",
            "type": "mathematical"
        },
        {
            "module": "algebra_007",
            "issue": "Mathematical error in solution",
            "severity": 5,
            "location": "Problem 5",
            "type": "mathematical"
        }
    ]

    for i, issue_data in enumerate(missed_issues, 1):
        missed_id = feedback_loop.log_missed_issue(
            module_id=issue_data["module"],
            review_pass=ReviewPass.CONTENT_PASS_1,
            issue_description=issue_data["issue"],
            severity=issue_data["severity"],
            location=issue_data["location"],
            issue_type=issue_data["type"]
        )
        print(f"   • Found: {issue_data['issue'][:50]}...")

    # Show metrics
    print("\n" + "="*70)
    print("ACCURACY METRICS")
    print("="*70)

    report = feedback_loop.get_accuracy_report()

    print(f"\n📊 Performance Metrics:")
    print(f"   Precision: {report['precision']} (% of AI flags that were correct)")
    print(f"   Recall: {report['recall']} (% of real issues AI caught)")
    print(f"   F1 Score: {report['f1_score']}")
    print(f"   Critical Miss Rate: {report['critical_miss_rate']}")

    print(f"\n📈 Issue Counts:")
    print(f"   AI Found & Confirmed: {report['true_positives']}")
    print(f"   AI Missed: {report['false_negatives']}")
    print(f"   Critical Issues Missed: {report['missed_critical']}")

    # Check what patterns triggered
    print("\n" + "="*70)
    print("PATTERN DETECTION")
    print("="*70)

    print("\n🔍 Analyzing patterns in missed issues...")
    feedback_loop._check_refinement_triggers()

    # Philosophy summary
    print("\n" + "="*70)
    print("KEY INSIGHTS")
    print("="*70)

    print("\n✅ REALISTIC EXPECTATIONS:")
    print("   • AI will never catch 100% of issues (nor do humans)")
    print("   • 85% recall is excellent, 70% is acceptable")
    print("   • Focus on catching critical issues (severity 4-5)")

    print("\n✅ SYSTEMATIC IMPROVEMENT:")
    print("   • Track patterns in what AI misses")
    print("   • Only refine prompts when pattern is clear (5+ occurrences)")
    print("   • Critical issues trigger refinement faster (2+ occurrences)")

    print("\n✅ BALANCED APPROACH:")
    print("   • Don't chase perfection (causes prompt bloat)")
    print("   • Accept some false negatives (AI misses)")
    print("   • Accept some false positives (author disputes)")
    print("   • Focus on the most impactful improvements")


if __name__ == "__main__":
    simulate_reviewer_feedback()