#!/usr/bin/env python3
"""
Command-line tool for authors to dispute AI feedback issues.
Usage: python dispute_issue.py <module_id> <issue_description> '<dispute_reason>'
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.feedback_loop import FeedbackLoop
from src.models import ConsensusResult


def main():
    if len(sys.argv) < 4:
        print("Usage: python dispute_issue.py <module_id> <issue_description> '<dispute_reason>'")
        print("\nExample:")
        print("  python dispute_issue.py module_001 'Uses contraction' 'This is a possessive, not a contraction'")
        sys.exit(1)

    module_id = sys.argv[1]
    issue_desc = sys.argv[2]
    dispute_reason = sys.argv[3]

    # Initialize feedback loop
    feedback_loop = FeedbackLoop()

    # Create a mock consensus result for the dispute
    # In production, this would look up the actual issue from the report
    mock_result = ConsensusResult(
        issue=issue_desc,
        severity=2,  # Will be filled from actual data
        confidence=0.7,
        agreeing_reviewers=7,
        total_reviewers=10,
        location="specified location",
        suggestions=[]
    )

    # Log the dispute
    feedback_id = feedback_loop.log_dispute(module_id, mock_result, dispute_reason)

    print("\n✅ Dispute successfully logged!")
    print(f"   Feedback ID: {feedback_id}")
    print("\n📝 What happens next:")
    print("   1. A human reviewer will validate your dispute")
    print("   2. Valid disputes contribute to system improvements")
    print("   3. Patterns lead to prompt refinements, not just exceptions")
    print("\n💡 Thank you for helping improve the system!")


if __name__ == "__main__":
    main()