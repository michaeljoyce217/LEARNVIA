#!/usr/bin/env python3
"""
Tool for human reviewers to validate author disputes.
Usage: python validate_disputes.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.feedback_loop import FeedbackLoop
import json


def display_dispute(dispute):
    """Display a dispute for review."""
    print("\n" + "="*60)
    print(f"DISPUTE ID: {dispute.feedback_id}")
    print(f"Module: {dispute.module_id}")
    print(f"Category: {dispute.pattern_category}")
    print("-"*60)
    print(f"\nORIGINAL ISSUE:")
    print(f"  Issue: {dispute.original_issue['issue']}")
    print(f"  Location: {dispute.original_issue['location']}")
    print(f"  Severity: {dispute.original_issue['severity']}")
    print(f"  Confidence: {dispute.original_issue['confidence_level']}")

    print(f"\nAUTHOR'S DISPUTE:")
    print(f"  {dispute.author_dispute}")
    print("-"*60)


def main():
    # Initialize feedback loop
    feedback_loop = FeedbackLoop()

    # Get pending disputes
    pending = [d for d in feedback_loop.disputes.values()
              if d.reviewer_judgment is None]

    if not pending:
        print("✅ No pending disputes to review!")
        return

    print(f"\n📋 {len(pending)} disputes pending review\n")

    for dispute in pending:
        display_dispute(dispute)

        while True:
            print("\nJUDGMENT OPTIONS:")
            print("  1. Valid - Author is correct")
            print("  2. Invalid - AI was correct")
            print("  3. Partial - Both have merit")
            print("  4. Skip - Review later")
            print("  5. Quit")

            choice = input("\nYour judgment (1-5): ").strip()

            if choice == '5':
                print("Exiting...")
                return

            if choice == '4':
                print("Skipping...")
                break

            if choice in ['1', '2', '3']:
                judgment_map = {
                    '1': 'valid',
                    '2': 'invalid',
                    '3': 'partial'
                }
                judgment = judgment_map[choice]

                notes = input("Additional notes (optional): ").strip()

                feedback_loop.validate_dispute(
                    dispute.feedback_id,
                    judgment,
                    notes
                )

                print(f"\n✅ Dispute marked as: {judgment}")
                break

    # Show stats
    print("\n" + "="*60)
    print("VALIDATION SESSION COMPLETE")
    print("="*60)

    stats = feedback_loop.get_dispute_stats()
    print(f"\nCurrent Statistics:")
    print(f"  Total Disputes: {stats['total_disputes']}")
    print(f"  Validated: {stats['validated']}")
    print(f"  Pending: {stats['pending_validation']}")
    print(f"  Valid: {stats['valid_disputes']}")
    print(f"  Invalid: {stats['invalid_disputes']}")

    if stats['validated'] > 0:
        print(f"  Validity Rate: {stats['validity_rate']:.0%}")

    # Check if we can generate refinements
    if stats['valid_disputes'] >= 3:
        print("\n💡 Enough valid disputes for pattern analysis!")
        generate = input("Generate refinement suggestions? (y/n): ").strip().lower()

        if generate == 'y':
            refinement = feedback_loop.generate_refinement()
            if refinement:
                print("\n✨ Refinement generated successfully!")
                print("Review the refinement in the feedback/refinements directory")


if __name__ == "__main__":
    main()