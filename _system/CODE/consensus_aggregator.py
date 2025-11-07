"""
Consensus aggregator for combining feedback from multiple reviewers
Implements deduplication, confidence scoring, and issue prioritization
"""

from typing import List, Dict, Any
from collections import defaultdict
from dataclasses import dataclass
import difflib

from CODE.models import ReviewFeedback, ConsensusResult, SeverityLevel


class ConsensusAggregator:
    """Aggregates feedback from multiple reviewers into consensus results"""

    def __init__(self, similarity_threshold: float = 0.7):
        """
        Initialize the consensus aggregator

        Args:
            similarity_threshold: Minimum similarity score to consider issues as duplicates
        """
        self.similarity_threshold = similarity_threshold

    def aggregate_feedback(self, feedback_list: List[ReviewFeedback]) -> List[ConsensusResult]:
        """
        Aggregate feedback from multiple reviewers into consensus results

        Args:
            feedback_list: List of feedback items from all reviewers

        Returns:
            List of consensus results with confidence scores
        """
        if not feedback_list:
            return []

        # Group similar issues
        issue_groups = self._group_similar_issues(feedback_list)

        # Create consensus results
        consensus_results = []
        for group in issue_groups:
            if len(group) >= 2:  # Require at least 2 agents to agree
                consensus = self._create_consensus_result(group)
                consensus_results.append(consensus)

        # Sort by priority (severity * confidence)
        consensus_results.sort(key=lambda x: x.get_priority_score(), reverse=True)

        return consensus_results

    def _group_similar_issues(self, feedback_list: List[ReviewFeedback]) -> List[List[ReviewFeedback]]:
        """
        Group similar issues based on text similarity

        Args:
            feedback_list: List of all feedback items

        Returns:
            List of grouped feedback items
        """
        groups = []
        processed = set()

        for i, feedback in enumerate(feedback_list):
            if i in processed:
                continue

            # Start a new group with this feedback
            group = [feedback]
            processed.add(i)

            # Find similar issues
            for j, other in enumerate(feedback_list[i+1:], start=i+1):
                if j in processed:
                    continue

                # Calculate similarity
                similarity = self._calculate_similarity(feedback.issue, other.issue)

                # Also check if location is similar
                location_similarity = self._calculate_similarity(
                    str(feedback.location),
                    str(other.location)
                )

                # Consider as duplicate if issue is similar and location is somewhat similar
                if similarity >= self.similarity_threshold and location_similarity >= 0.3:
                    group.append(other)
                    processed.add(j)
                # Also group if exact same issue text
                elif feedback.issue == other.issue:
                    group.append(other)
                    processed.add(j)

            groups.append(group)

        return groups

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two text strings

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score between 0 and 1
        """
        # Use sequence matcher for similarity
        return difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def _create_consensus_result(self, feedback_group: List[ReviewFeedback]) -> ConsensusResult:
        """
        Create a consensus result from a group of similar feedback

        Args:
            feedback_group: Group of similar feedback items

        Returns:
            ConsensusResult object
        """
        # Use the most detailed issue description
        issue_descriptions = [f.issue for f in feedback_group]
        issue = max(issue_descriptions, key=len)

        # Use highest severity
        severity = max(f.severity for f in feedback_group)

        # Most common location
        locations = [f.location for f in feedback_group]
        location = max(set(locations), key=locations.count)

        # Best suggestion (longest, most detailed)
        suggestions = [f.suggestion for f in feedback_group if f.suggestion]
        suggestion = max(suggestions, key=len) if suggestions else ""

        # Calculate confidence based on agreement
        agreeing_reviewers = len(feedback_group)
        total_reviewers = 30  # Fixed for our Pass 1 scenario
        confidence = min(0.95, (agreeing_reviewers / total_reviewers) * 1.5)

        # Determine if solution should be provided
        should_provide_solution = severity >= 4 and confidence >= 0.7

        # Determine issue type from feedback
        issue_types = [f.issue_type for f in feedback_group if f.issue_type]
        issue_type = max(set(issue_types), key=issue_types.count) if issue_types else "general"

        # Prepare suggestions list
        suggestions_list = [suggestion] if suggestion and should_provide_solution else []

        return ConsensusResult(
            issue=issue,
            severity=severity,
            location=location,
            suggestions=suggestions_list,
            confidence=confidence,
            agreeing_reviewers=agreeing_reviewers,
            total_reviewers=total_reviewers,
            issue_type=issue_type
        )

    def calculate_metrics(self, feedback_list: List[ReviewFeedback],
                         consensus_results: List[ConsensusResult]) -> Dict[str, Any]:
        """
        Calculate aggregation metrics

        Args:
            feedback_list: Original feedback list
            consensus_results: Aggregated consensus results

        Returns:
            Dictionary of metrics
        """
        if not feedback_list:
            return {
                "total_feedback": 0,
                "consensus_issues": 0,
                "noise_reduction": 0,
                "average_confidence": 0,
                "high_priority_issues": 0
            }

        noise_reduction = ((len(feedback_list) - len(consensus_results)) / len(feedback_list)) * 100
        avg_confidence = sum(r.confidence for r in consensus_results) / len(consensus_results) if consensus_results else 0
        high_priority = sum(1 for r in consensus_results if r.severity >= 4 and r.confidence >= 0.7)

        return {
            "total_feedback": len(feedback_list),
            "consensus_issues": len(consensus_results),
            "noise_reduction": round(noise_reduction, 1),
            "average_confidence": round(avg_confidence * 100, 1),
            "high_priority_issues": high_priority
        }