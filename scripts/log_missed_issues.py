#!/usr/bin/env python3
"""
Tool for human reviewers to log issues that AI reviewers missed.
This feeds back into the system to improve AI detection.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.reviewer_feedback_loop import ReviewerFeedbackLoop
from src.models import ReviewPass


def main():
    print("="*60)
    print("LOG ISSUES THAT AI REVIEWERS MISSED")
    print("="*60)
    print("\nThis tool tracks what human reviewers find that AI missed.")
    print("When patterns emerge, the system will suggest prompt refinements.\n")

    feedback_loop = ReviewerFeedbackLoop()

    # Set acceptable miss rate
    feedback_loop.set_acceptable_miss_rate(0.15)  # 15% is acceptable

    while True:
        print("\n" + "-"*40)
        print("OPTIONS:")
        print("1. Log a missed issue")
        print("2. Confirm an AI-flagged issue")
        print("3. View accuracy metrics")
        print("4. Check refinement triggers")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == '1':
            # Log missed issue
            print("\n📝 LOG MISSED ISSUE")

            module_id = input("Module ID: ").strip()
            if not module_id:
                module_id = "example_module"

            print("\nReview Pass:")
            print("1. Authoring Pass 1")
            print("2. Authoring Pass 2")
            print("3. Style Pass 1")
            print("4. Style Pass 2")
            pass_choice = input("Select (1-4): ").strip()

            pass_map = {
                '1': ReviewPass.CONTENT_PASS_1,
                '2': ReviewPass.CONTENT_PASS_2,
                '3': ReviewPass.COPY_PASS_1,
                '4': ReviewPass.COPY_PASS_2
            }
            review_pass = pass_map.get(pass_choice, ReviewPass.CONTENT_PASS_1)

            issue_desc = input("\nIssue description: ").strip()

            print("\nSeverity:")
            print("5 - Critical (math errors, missing components)")
            print("4 - High (pedagogy issues)")
            print("3 - Medium (writing quality)")
            print("2 - Low (style compliance)")
            print("1 - Minor (polish)")
            severity = int(input("Select (1-5): ").strip() or "3")

            location = input("\nLocation (e.g., 'Line 45', 'Example 2'): ").strip()

            print("\nIssue Type:")
            print("1. Pedagogical")
            print("2. Style")
            print("3. Mathematical")
            print("4. Examples")
            print("5. Quiz/Assessment")
            print("6. Other")
            type_choice = input("Select (1-6): ").strip()

            type_map = {
                '1': 'pedagogical',
                '2': 'style',
                '3': 'mathematical',
                '4': 'examples',
                '5': 'assessment',
                '6': 'other'
            }
            issue_type = type_map.get(type_choice, 'other')

            # Log the missed issue
            missed_id = feedback_loop.log_missed_issue(
                module_id=module_id,
                review_pass=review_pass,
                issue_description=issue_desc,
                severity=severity,
                location=location,
                issue_type=issue_type
            )

            print(f"\n✅ Missed issue logged: {missed_id}")

        elif choice == '2':
            # Confirm AI issue
            module_id = input("\nModule ID: ").strip() or "example_module"
            ai_issue_id = input("AI Issue ID (or description): ").strip()

            feedback_loop.log_confirmed_issue(module_id, ai_issue_id)
            print("✅ AI issue confirmed")

        elif choice == '3':
            # View metrics
            print("\n📊 ACCURACY METRICS")
            print("-"*40)

            report = feedback_loop.get_accuracy_report()

            print(f"Precision: {report['precision']} (% of AI flags that were correct)")
            print(f"Recall: {report['recall']} (% of real issues AI caught)")
            print(f"F1 Score: {report['f1_score']}")
            print(f"Critical Miss Rate: {report['critical_miss_rate']}")

            print(f"\nCounts:")
            print(f"  True Positives: {report['true_positives']}")
            print(f"  False Positives: {report['false_positives']}")
            print(f"  False Negatives: {report['false_negatives']}")
            print(f"  Missed Critical: {report['missed_critical']}")
            print(f"  Missed High: {report['missed_high']}")

        elif choice == '4':
            # Check triggers
            print("\n🔍 Checking for refinement triggers...")
            feedback_loop._check_refinement_triggers()

        elif choice == '5':
            break

    print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()