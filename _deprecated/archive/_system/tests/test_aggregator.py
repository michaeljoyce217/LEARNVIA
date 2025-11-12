"""
Test suite for the consensus aggregation logic.
Tests how feedback from multiple reviewers is combined and scored.
"""

import pytest
from datetime import datetime
from typing import List

from src.aggregator import ConsensusAggregator
from src.models import (
    ReviewFeedback, ConsensusResult, SeverityLevel,
    ReviewPass, ReviewReport
)


class TestConsensusAggregator:
    """Tests for the ConsensusAggregator class."""

    # Class-level counter to ensure globally unique disagreeing issues
    _disagreeing_issue_counter = 0

    def create_test_feedback(self, num_reviewers: int, issue: str, severity: int,
                            agreement_rate: float = 1.0) -> List[ReviewFeedback]:
        """Helper to create test feedback with specified agreement rate."""
        feedback_list = []
        num_agreeing = int(num_reviewers * agreement_rate)

        # Create agreeing feedback
        for i in range(num_agreeing):
            feedback_list.append(ReviewFeedback(
                reviewer_id=f"reviewer_{i:02d}",
                issue_type="test_type",
                severity=severity,
                location="test_location",
                issue=issue,
                suggestion=f"Suggestion {i}"
            ))

        # Create disagreeing feedback (each with completely different text)
        # Need <25% text similarity to avoid grouping by fuzzy matching (threshold=0.75)
        unique_issues_text = [
            "Missing scaffolding in the introduction section",
            "Quiz question two has ambiguous wording that confuses students",
            "Example three contains a mathematical error in step four",
            "LaTeX formatting is incorrect for the equation on line 42",
            "The explanation jumps concepts without bridging between them",
            "Homework problem five is too difficult for the target audience",
            "Contraction 'don't' found in paragraph seven violates style guide",
            "Definition of derivative needs more concrete examples",
            "Graph labels are unclear and need better formatting",
            "Summary section omits key learning objectives from framing"
        ]
        for idx, i in enumerate(range(num_agreeing, num_reviewers)):
            TestConsensusAggregator._disagreeing_issue_counter += 1
            unique_id = TestConsensusAggregator._disagreeing_issue_counter
            # Use completely different text for each issue to prevent fuzzy matching
            issue_text = unique_issues_text[unique_id % len(unique_issues_text)]
            feedback_list.append(ReviewFeedback(
                reviewer_id=f"reviewer_{i:02d}",
                issue_type=f"unique_type_{unique_id}",
                severity=2,
                location=f"location_{unique_id}",
                issue=issue_text + f" [ID:{unique_id}]",
                suggestion=f"Fix for issue {unique_id}"
            ))

        return feedback_list

    def test_aggregator_initialization(self):
        """Test creating an aggregator instance."""
        aggregator = ConsensusAggregator()
        assert aggregator is not None

    def test_group_similar_feedback(self):
        """Test grouping of similar feedback items."""
        feedback_list = [
            ReviewFeedback(
                reviewer_id="r1",
                issue_type="concept_jump",
                severity=4,
                location="paragraph 3",
                issue="Large concept jump",
                suggestion="Add step"
            ),
            ReviewFeedback(
                reviewer_id="r2",
                issue_type="concept_jump",
                severity=4,
                location="paragraph 3",
                issue="Concept jump too large",
                suggestion="Add intermediate example"
            ),
            ReviewFeedback(
                reviewer_id="r3",
                issue_type="missing_example",
                severity=3,
                location="section 2",
                issue="No examples",
                suggestion="Add examples"
            )
        ]

        aggregator = ConsensusAggregator()
        grouped = aggregator.group_similar_feedback(feedback_list)

        # Should have 2 groups (concept jump and missing example)
        assert len(grouped) == 2

        # Check that similar issues are grouped together
        concept_jump_group = next(g for g in grouped if "concept_jump" in str(g))
        assert len(concept_jump_group) == 2

    def test_calculate_consensus_high_agreement(self):
        """Test consensus calculation with high agreement."""
        feedback_list = self.create_test_feedback(
            num_reviewers=10,
            issue="Missing concrete examples",
            severity=4,
            agreement_rate=0.9  # 9 out of 10 agree
        )

        aggregator = ConsensusAggregator()
        consensus_results = aggregator.aggregate(feedback_list)

        # Find the high-consensus result
        high_consensus = next(r for r in consensus_results if r.issue == "Missing concrete examples")

        assert high_consensus.agreeing_reviewers == 9
        assert high_consensus.total_reviewers == 10
        assert high_consensus.confidence == 0.9
        assert high_consensus.confidence_level == "high"
        assert high_consensus.severity == 4

    def test_calculate_consensus_low_agreement(self):
        """Test consensus calculation with low agreement."""
        feedback_list = self.create_test_feedback(
            num_reviewers=10,
            issue="Minor style issue",
            severity=2,
            agreement_rate=0.2  # Only 2 out of 10 agree
        )

        aggregator = ConsensusAggregator()
        consensus_results = aggregator.aggregate(feedback_list)

        low_consensus = next(r for r in consensus_results if r.issue == "Minor style issue")

        assert low_consensus.agreeing_reviewers == 2
        assert low_consensus.confidence == 0.2
        assert low_consensus.confidence_level == "low"

    def test_aggregate_suggestions(self):
        """Test that suggestions from multiple reviewers are aggregated."""
        feedback_list = [
            ReviewFeedback(
                reviewer_id=f"r{i}",
                issue_type="same_issue",
                severity=4,
                location="same_location",
                issue="Same issue",
                suggestion=f"Suggestion {i}"
            ) for i in range(5)
        ]

        aggregator = ConsensusAggregator()
        consensus_results = aggregator.aggregate(feedback_list)

        assert len(consensus_results) == 1
        result = consensus_results[0]

        # Should have all 5 unique suggestions
        assert len(result.suggestions) == 5
        assert all(f"Suggestion {i}" in result.suggestions for i in range(5))

    def test_severity_preservation(self):
        """Test that severity levels are correctly preserved in consensus."""
        feedback_list = [
            ReviewFeedback(
                reviewer_id=f"r{i}",
                issue_type="critical_issue",
                severity=SeverityLevel.CRITICAL,
                location="location",
                issue="Critical math error",
                suggestion="Fix calculation"
            ) for i in range(3)
        ]

        aggregator = ConsensusAggregator()
        consensus_results = aggregator.aggregate(feedback_list)

        assert consensus_results[0].severity == SeverityLevel.CRITICAL

    def test_location_similarity(self):
        """Test that issues at similar locations are grouped."""
        feedback_list = [
            ReviewFeedback(
                reviewer_id="r1",
                issue_type="issue",
                severity=3,
                location="lines 10-15",
                issue="Problem A",
                suggestion="Fix A"
            ),
            ReviewFeedback(
                reviewer_id="r2",
                issue_type="issue",
                severity=3,
                location="line 12",
                issue="Problem A",
                suggestion="Fix A"
            ),
            ReviewFeedback(
                reviewer_id="r3",
                issue_type="issue",
                severity=3,
                location="paragraph 20",
                issue="Problem B",
                suggestion="Fix B"
            )
        ]

        aggregator = ConsensusAggregator()
        groups = aggregator.group_by_location(feedback_list)

        # Should group lines 10-15 and line 12 together
        assert len(groups) == 2

    def test_confidence_score_calculation(self):
        """Test the confidence score calculation formula."""
        aggregator = ConsensusAggregator()

        # Test various agreement levels
        assert aggregator.calculate_confidence(10, 10) == 1.0
        assert aggregator.calculate_confidence(7, 10) == 0.7
        assert aggregator.calculate_confidence(5, 10) == 0.5
        assert aggregator.calculate_confidence(0, 10) == 0.0

    def test_filter_by_confidence_threshold(self):
        """Test filtering consensus results by confidence threshold."""
        # Create three completely distinct issues with different agreement levels
        feedback_list = []

        # Issue 1: High confidence (9 out of 10 reviewers) - should pass threshold
        for i in range(9):
            feedback_list.append(ReviewFeedback(
                reviewer_id=f"reviewer_{i:02d}",
                issue_type="pedagogical_flow",
                severity=5,
                location="paragraph 3 lines 45-67",
                issue="Missing scaffolding between derivative definition and first example causes concept jump",
                suggestion=f"Add bridging explanation {i}"
            ))

        # Issue 2: Moderate confidence (5 out of 10 reviewers) - should NOT pass threshold
        for i in range(5):
            feedback_list.append(ReviewFeedback(
                reviewer_id=f"reviewer_{i:02d}",
                issue_type="latex_formatting",
                severity=2,
                location="equation 7",
                issue="LaTeX fraction notation should use \\frac instead of / symbol",
                suggestion=f"Update LaTeX {i}"
            ))

        # Issue 3: Low confidence (2 out of 10 reviewers) - should NOT pass threshold
        for i in range(2):
            feedback_list.append(ReviewFeedback(
                reviewer_id=f"reviewer_{i:02d}",
                issue_type="quiz_wording",
                severity=3,
                location="quiz question 4",
                issue="Question wording might be ambiguous for students with limited background",
                suggestion=f"Clarify wording {i}"
            ))

        aggregator = ConsensusAggregator()
        all_results = aggregator.aggregate(feedback_list)

        # Should have 3 distinct issues
        assert len(all_results) == 3

        # Filter for high confidence only (>= 0.7)
        high_confidence = aggregator.filter_by_confidence(all_results, threshold=0.7)

        assert len(high_confidence) == 1
        assert high_confidence[0].confidence >= 0.7
        assert "scaffolding" in high_confidence[0].issue.lower()

    def test_merge_duplicate_issues(self):
        """Test that duplicate issues are properly merged."""
        feedback_list = [
            ReviewFeedback(
                reviewer_id=f"r{i}",
                issue_type="contraction",
                severity=2,
                location=f"line {10 + i % 3}",  # Slightly different locations
                issue="Uses contraction 'don't'",
                suggestion="Replace with 'do not'"
            ) for i in range(6)
        ]

        aggregator = ConsensusAggregator()
        consensus_results = aggregator.aggregate(feedback_list)

        # Should merge into fewer groups based on issue similarity
        assert len(consensus_results) < 6

    def test_priority_scoring(self):
        """Test the priority scoring system."""
        results = [
            ConsensusResult(
                issue="Critical issue",
                severity=5,
                confidence=0.9,
                agreeing_reviewers=9,
                total_reviewers=10,
                location="test"
            ),
            ConsensusResult(
                issue="Minor issue",
                severity=1,
                confidence=0.3,
                agreeing_reviewers=3,
                total_reviewers=10,
                location="test"
            ),
            ConsensusResult(
                issue="Medium issue",
                severity=3,
                confidence=0.7,
                agreeing_reviewers=7,
                total_reviewers=10,
                location="test"
            )
        ]

        aggregator = ConsensusAggregator()
        sorted_results = aggregator.sort_by_priority(results)

        # Critical issue should be first (5 * 0.9 = 4.5)
        assert sorted_results[0].issue == "Critical issue"
        # Medium issue should be second (3 * 0.7 = 2.1)
        assert sorted_results[1].issue == "Medium issue"
        # Minor issue should be last (1 * 0.3 = 0.3)
        assert sorted_results[2].issue == "Minor issue"

    def test_empty_feedback_handling(self):
        """Test that aggregator handles empty feedback list gracefully."""
        aggregator = ConsensusAggregator()
        results = aggregator.aggregate([])

        assert results == []

    def test_single_reviewer_handling(self):
        """Test handling of feedback from a single reviewer."""
        feedback_list = [
            ReviewFeedback(
                reviewer_id="solo",
                issue_type="issue",
                severity=3,
                location="location",
                issue="Single reviewer issue",
                suggestion="Fix it"
            )
        ]

        aggregator = ConsensusAggregator()
        results = aggregator.aggregate(feedback_list)

        assert len(results) == 1
        assert results[0].confidence == 1.0  # Single reviewer = 100% of reviewers agree
        assert results[0].confidence_level == "very_high"

    def test_fuzzy_matching(self):
        """Test fuzzy matching of similar issues."""
        feedback_list = [
            ReviewFeedback(
                reviewer_id="r1",
                issue_type="concept",
                severity=4,
                location="para 3",
                issue="Concept jump is too large",
                suggestion="Add step"
            ),
            ReviewFeedback(
                reviewer_id="r2",
                issue_type="concept",
                severity=4,
                location="para 3",
                issue="Large conceptual leap",
                suggestion="Add intermediate"
            ),
            ReviewFeedback(
                reviewer_id="r3",
                issue_type="concept",
                severity=4,
                location="para 3",
                issue="Big jump in concepts",
                suggestion="Break down"
            )
        ]

        aggregator = ConsensusAggregator(similarity_threshold=0.7)
        results = aggregator.aggregate(feedback_list)

        # Similar issues should be grouped into one consensus
        assert len(results) == 1
        assert results[0].agreeing_reviewers == 3

    def test_generate_report(self):
        """Test generation of a review report from consensus results."""
        consensus_results = [
            ConsensusResult(
                issue="Missing examples",
                severity=4,
                confidence=0.8,
                agreeing_reviewers=8,
                total_reviewers=10,
                location="section 2",
                suggestions=["Add concrete examples"]
            ),
            ConsensusResult(
                issue="Contraction used",
                severity=2,
                confidence=0.6,
                agreeing_reviewers=6,
                total_reviewers=10,
                location="line 5",
                suggestions=["Replace don't with do not"]
            )
        ]

        aggregator = ConsensusAggregator()
        report = aggregator.generate_report(
            consensus_results=consensus_results,
            module_id="test_module",
            review_pass=ReviewPass.CONTENT_PASS_1
        )

        assert report.module_id == "test_module"
        assert report.review_pass == ReviewPass.CONTENT_PASS_1
        assert len(report.consensus_results) == 2

        # Check priority matrix
        matrix = report.get_priority_matrix()
        assert len(matrix["immediate"]) == 1  # High severity + high confidence
        assert len(matrix["consider"]) == 1   # Low severity + medium confidence