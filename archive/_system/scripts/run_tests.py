#!/usr/bin/env python3
"""
Simple test runner for the Learnvia AI Revision System.
Runs basic validation tests without requiring external test frameworks.
"""

import sys
import os
# Add parent directory (project root) to path so we can import src module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import (
    ReviewerRole, ReviewPass, SeverityLevel, ConfidenceLevel,
    ReviewFeedback, ConsensusResult, ModuleContent, ReviewSession,
    ReviewReport
)
from src.aggregator import ConsensusAggregator
from src.report_generator import ReportGenerator
from datetime import datetime


def test_models():
    """Test basic model functionality."""
    print("Testing Models...")

    # Test ReviewerRole enum
    assert ReviewerRole.AUTHORING.value == "authoring"
    assert ReviewerRole.STYLE.value == "style"

    # Test SeverityLevel
    assert SeverityLevel.CRITICAL == 5
    assert SeverityLevel.HIGH == 4

    # Test ReviewFeedback creation
    feedback = ReviewFeedback(
        reviewer_id="test_01",
        issue_type="test_type",
        severity=4,
        location="test location",
        issue="Test issue",
        suggestion="Test suggestion"
    )
    assert feedback.reviewer_id == "test_01"
    assert feedback.severity == 4

    # Test ModuleContent
    module = ModuleContent(
        content="Test content",
        module_id="test_module"
    )
    assert module.module_id == "test_module"
    assert module.word_count > 0

    print("✓ Models tests passed")


def test_aggregator():
    """Test consensus aggregation."""
    print("Testing Aggregator...")

    aggregator = ConsensusAggregator()

    # Create test feedback
    feedback_list = [
        ReviewFeedback(
            reviewer_id=f"reviewer_{i}",
            issue_type="same_issue",
            severity=4,
            location="same location",
            issue="Same issue description",
            suggestion=f"Suggestion {i}"
        ) for i in range(5)
    ]

    # Test aggregation
    results = aggregator.aggregate(feedback_list)
    assert len(results) == 1  # Should group into one consensus
    assert results[0].agreeing_reviewers == 5
    assert results[0].confidence == 1.0

    # Test confidence calculation
    conf = aggregator.calculate_confidence(7, 10)
    assert conf == 0.7

    print("✓ Aggregator tests passed")


def test_report_generator():
    """Test report generation."""
    print("Testing Report Generator...")

    generator = ReportGenerator()

    # Create test report
    consensus_results = [
        ConsensusResult(
            issue="Test issue",
            severity=4,
            confidence=0.8,
            agreeing_reviewers=8,
            total_reviewers=10,
            location="Test location",
            suggestions=["Fix it"]
        )
    ]

    report = ReviewReport(
        module_id="test_module",
        review_pass=ReviewPass.CONTENT_PASS_1,
        timestamp=datetime.now(),
        consensus_results=consensus_results,
        strengths=["Good structure"],
        estimated_revision_time=30
    )

    # Test text report generation
    text_report = generator.generate_text_report(report)
    assert "test_module" in text_report
    assert "Good structure" in text_report

    # Test priority matrix
    matrix = report.get_priority_matrix()
    assert "immediate" in matrix
    assert len(matrix["immediate"]) == 1  # High severity + high confidence

    print("✓ Report Generator tests passed")


def test_confidence_levels():
    """Test confidence level calculations."""
    print("Testing Confidence Levels...")

    assert ConfidenceLevel.get_level(10, 10) == "very_high"
    assert ConfidenceLevel.get_level(8, 10) == "high"
    assert ConfidenceLevel.get_level(5, 10) == "moderate"
    assert ConfidenceLevel.get_level(2, 10) == "low"
    assert ConfidenceLevel.get_level(1, 10) == "very_low"

    print("✓ Confidence Level tests passed")


def test_student_success_framing():
    """Test that feedback is properly reframed."""
    print("Testing Student-Success Framing...")

    feedback = ReviewFeedback(
        reviewer_id="test",
        issue_type="error",
        severity=4,
        location="para 1",
        issue="Missing concrete examples",
        suggestion="Add examples"
    )

    framed = feedback.to_student_success_framing()
    assert "ERROR" not in framed
    assert "Learning Opportunity" in framed or "Improvement" in framed

    print("✓ Student-Success Framing tests passed")


def test_session_management():
    """Test review session management."""
    print("Testing Session Management...")

    module = ModuleContent(content="Test", module_id="test_001")
    session = ReviewSession(module=module)

    # Add feedback
    feedback = ReviewFeedback(
        reviewer_id="r1",
        issue_type="test",
        severity=3,
        location="test",
        issue="test",
        suggestion="test"
    )
    session.add_feedback(feedback)

    assert len(session.all_feedback) == 1
    assert session.session_id.startswith("session_")

    # Complete session
    session.complete_session()
    assert session.end_time is not None

    print("✓ Session Management tests passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*50)
    print("RUNNING LEARNVIA AI REVISION SYSTEM TESTS")
    print("="*50 + "\n")

    try:
        test_models()
        test_aggregator()
        test_report_generator()
        test_confidence_levels()
        test_student_success_framing()
        test_session_management()

        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED SUCCESSFULLY!")
        print("="*50)
        return True

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()

    if success:
        print("\n📊 Test Summary:")
        print("  • Models: ✓")
        print("  • Aggregator: ✓")
        print("  • Report Generator: ✓")
        print("  • Confidence Levels: ✓")
        print("  • Student-Success Framing: ✓")
        print("  • Session Management: ✓")
        print("\nThe system is ready for use!")
    else:
        print("\nPlease fix the failing tests before using the system.")
        sys.exit(1)