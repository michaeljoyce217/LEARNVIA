import pytest
from datetime import datetime
from src.models import (
    ReviewerRole, ReviewPass, SeverityLevel, ConfidenceLevel,
    ReviewFeedback, ConsensusResult, ModuleContent, ReviewSession
)

def test_reviewer_role_enum():
    assert ReviewerRole.AUTHORING.value == "authoring"
    assert ReviewerRole.STYLE.value == "style"

def test_severity_level_values():
    assert SeverityLevel.CRITICAL == 5
    assert SeverityLevel.HIGH == 4
    assert SeverityLevel.MEDIUM == 3
    assert SeverityLevel.LOW == 2
    assert SeverityLevel.MINOR == 1

def test_review_feedback_creation():
    feedback = ReviewFeedback(
        reviewer_id="authoring_01",
        issue_type="pedagogical_flow",
        severity=4,
        location="lines 10-15",
        issue="Concept jump too large between examples",
        suggestion="Consider adding intermediate step",
        confidence_contribution=1.0
    )
    assert feedback.reviewer_id == "authoring_01"
    assert feedback.severity == 4
    assert feedback.to_dict()["issue_type"] == "pedagogical_flow"

def test_consensus_result_aggregation():
    result = ConsensusResult(
        issue="Missing concrete examples",
        severity=4,
        confidence=0.8,
        agreeing_reviewers=8,
        total_reviewers=10,
        location="paragraph 3",
        suggestions=["Add student-relevant example", "Use everyday objects"]
    )
    assert result.confidence_level == "high"
    assert result.should_provide_solution == True
