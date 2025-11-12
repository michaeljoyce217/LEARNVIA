#!/usr/bin/env python3
"""
Test the feedback loop system with example disputes.
Demonstrates how the system prevents prompt bloat through pattern recognition.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.feedback_loop import FeedbackLoop
from src.models import ConsensusResult


def simulate_common_disputes():
    """Simulate common dispute patterns to test the system."""

    feedback_loop = FeedbackLoop()

    print("="*70)
    print("FEEDBACK LOOP SYSTEM DEMONSTRATION")
    print("="*70)

    # Example disputes that show common patterns
    test_disputes = [
        # Mathematical context issues
        {
            "module": "algebra_001",
            "issue": "Uses contraction 'let's' in instruction",
            "location": "Example 3, line 45",
            "reason": "This is mathematical notation 'let x = 5', not the contraction 'let us'",
            "category": "mathematical_context"
        },
        {
            "module": "geometry_002",
            "issue": "Improper imperative 'Let' at start of sentence",
            "location": "Problem 2",
            "reason": "Mathematical convention 'Let ABC be a triangle' is standard notation",
            "category": "mathematical_context"
        },
        {
            "module": "calculus_003",
            "issue": "Uses contraction 'it's'",
            "location": "Definition section",
            "reason": "This is possessive 'its derivative' not contraction 'it is'",
            "category": "possessive_vs_contraction"
        },

        # Quoted text issues
        {
            "module": "history_math_001",
            "issue": "Contraction 'didn't' found",
            "location": "Quote from Euler",
            "reason": "This is a historical quote and must preserve original language",
            "category": "quoted_text"
        },
        {
            "module": "word_problem_002",
            "issue": "Informal language in dialogue",
            "location": "Example problem",
            "reason": "The problem quotes a student's question verbatim for authenticity",
            "category": "quoted_text"
        },

        # Procedural imperatives
        {
            "module": "algorithm_001",
            "issue": "Multiple imperatives in instructions",
            "location": "Step-by-step solution",
            "reason": "Algorithm steps require imperative voice for clarity",
            "category": "procedural_imperative"
        },
        # Add more to trigger pattern detection
        {
            "module": "proof_001",
            "issue": "Uses 'let' at sentence start",
            "location": "Proof section",
            "reason": "Standard mathematical proof language",
            "category": "mathematical_context"
        },
    ]

    print("\n📝 Simulating author disputes...")
    dispute_ids = []

    for i, dispute_data in enumerate(test_disputes, 1):
        # Create mock consensus result
        result = ConsensusResult(
            issue=dispute_data["issue"],
            severity=2,
            confidence=0.7,
            agreeing_reviewers=7,
            total_reviewers=10,
            location=dispute_data["location"],
            suggestions=["Follow style guide"],
            issue_type="style_violation"
        )

        # Log dispute
        feedback_id = feedback_loop.log_dispute(
            dispute_data["module"],
            result,
            dispute_data["reason"]
        )
        dispute_ids.append(feedback_id)

        print(f"  {i}. {dispute_data['category']}: {dispute_data['issue'][:40]}...")

    print(f"\n✅ Logged {len(dispute_ids)} disputes")

    # Simulate reviewer validation
    print("\n👤 Simulating reviewer validation...")
    for feedback_id in dispute_ids:
        # Mark all as valid for demonstration
        feedback_loop.validate_dispute(
            feedback_id,
            "valid",
            "Author correctly identified context-specific exception"
        )
        print(f"  ✓ Validated: {feedback_id}")

    # Show statistics
    print("\n📊 Current Statistics:")
    stats = feedback_loop.get_dispute_stats()
    print(f"  Total Disputes: {stats['total_disputes']}")
    print(f"  Valid Disputes: {stats['valid_disputes']}")
    print(f"  Categories: {stats['categories']}")

    # Generate refinement (lower threshold for demo)
    print("\n🔧 Generating Smart Refinement...")
    refinement = feedback_loop.generate_refinement(review_type="style", confidence_threshold=0.0)

    if refinement:
        print("\n" + "="*70)
        print("REFINEMENT PREVENTS PROMPT BLOAT")
        print("="*70)

        print("\n❌ WITHOUT FEEDBACK LOOP (Prompt Bloat):")
        print("  'Don't flag let in math. Don't flag contractions in quotes.'")
        print("  'Don't flag imperatives in procedures. Don't flag possessives.'")
        print("  'Don't flag... [50 more exceptions]'")
        print("  Result: 1000+ word prompt full of exceptions")

        print("\n✅ WITH FEEDBACK LOOP (Smart Refinement):")
        print(refinement.generate_refinement_text())
        print("\n  Result: Clean, principle-based prompt that stays maintainable")

    print("\n" + "="*70)
    print("KEY BENEFITS:")
    print("="*70)
    print("1. Prompts stay clean and principle-based")
    print("2. System learns from real usage patterns")
    print("3. Authors feel heard and contribute to improvements")
    print("4. No manual prompt maintenance needed")
    print("5. Reduces false positives systematically")


if __name__ == "__main__":
    simulate_common_disputes()