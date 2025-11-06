"""
Consensus aggregation module for the Learnvia content revision system.
Combines feedback from multiple reviewers to identify high-confidence issues.
"""

from typing import List, Dict, Tuple, Set
from collections import defaultdict
from datetime import datetime
import re
from difflib import SequenceMatcher

from .models import (
    ReviewFeedback, ConsensusResult, ReviewReport,
    ReviewPass, ConfidenceLevel
)


class ConsensusAggregator:
    """Aggregates feedback from multiple reviewers into consensus results."""

    def __init__(self, similarity_threshold: float = 0.75):
        """Initialize aggregator with similarity threshold for grouping."""
        self.similarity_threshold = similarity_threshold

    def aggregate(self, feedback_list: List[ReviewFeedback]) -> List[ConsensusResult]:
        """Aggregate all feedback into consensus results."""
        if not feedback_list:
            return []

        # Calculate total number of unique reviewers
        total_reviewers = len(set(f.reviewer_id for f in feedback_list))

        # Group similar feedback
        grouped_feedback = self.group_similar_feedback(feedback_list)

        # Create consensus results for each group
        consensus_results = []
        for group in grouped_feedback:
            if group:  # Skip empty groups
                result = self._create_consensus_result(group, total_reviewers)
                consensus_results.append(result)

        # Sort by priority
        return self.sort_by_priority(consensus_results)

    def group_similar_feedback(self, feedback_list: List[ReviewFeedback]) -> List[List[ReviewFeedback]]:
        """Group similar feedback items together."""
        if not feedback_list:
            return []

        groups = []
        used = set()

        for i, feedback1 in enumerate(feedback_list):
            if i in used:
                continue

            group = [feedback1]
            used.add(i)

            for j, feedback2 in enumerate(feedback_list[i + 1:], start=i + 1):
                if j in used:
                    continue

                if self._are_similar(feedback1, feedback2):
                    group.append(feedback2)
                    used.add(j)

            groups.append(group)

        return groups

    def _are_similar(self, feedback1: ReviewFeedback, feedback2: ReviewFeedback) -> bool:
        """Determine if two feedback items are similar enough to group."""
        # Check issue type similarity
        if feedback1.issue_type == feedback2.issue_type:
            type_match = 1.0
        else:
            type_match = self._string_similarity(feedback1.issue_type, feedback2.issue_type)

        # Check issue description similarity
        issue_similarity = self._string_similarity(feedback1.issue, feedback2.issue)

        # Check location similarity
        location_match = self._location_similarity(feedback1.location, feedback2.location)

        # Check severity match (within 1 level)
        severity_match = abs(feedback1.severity - feedback2.severity) <= 1

        # Combine factors
        # Issues are similar if:
        # - Same type/similar description AND similar location
        # - OR very similar description regardless of location
        if (type_match > 0.7 and location_match > 0.5 and severity_match):
            return True

        if issue_similarity > self.similarity_threshold:
            return True

        return False

    def _string_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings."""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

    def _location_similarity(self, loc1: str, loc2: str) -> float:
        """Calculate similarity between two location descriptions."""
        # Extract numbers from locations
        nums1 = set(re.findall(r'\d+', loc1))
        nums2 = set(re.findall(r'\d+', loc2))

        if nums1 and nums2:
            # Check if line numbers are close
            for n1 in nums1:
                for n2 in nums2:
                    if abs(int(n1) - int(n2)) <= 5:
                        return 0.8

        # Check string similarity
        return self._string_similarity(loc1, loc2)

    def _create_consensus_result(self, feedback_group: List[ReviewFeedback],
                                total_reviewers: int) -> ConsensusResult:
        """Create a consensus result from a group of similar feedback."""
        # Get the most common severity (mode)
        severities = [f.severity for f in feedback_group]
        severity = max(set(severities), key=severities.count)

        # Get the most detailed issue description
        longest_issue = max(feedback_group, key=lambda f: len(f.issue)).issue

        # Collect all unique suggestions
        suggestions = list(set(f.suggestion for f in feedback_group if f.suggestion))

        # Get the most specific location
        locations = [f.location for f in feedback_group]
        location = self._get_most_specific_location(locations)

        # Get the most common issue type
        issue_types = [f.issue_type for f in feedback_group]
        issue_type = max(set(issue_types), key=issue_types.count)

        # Calculate confidence based on reviewer agreement
        # Count unique reviewers in this group (in case same reviewer flagged issue multiple times)
        agreeing_reviewers = len(set(f.reviewer_id for f in feedback_group))

        confidence = self.calculate_confidence(agreeing_reviewers, total_reviewers)

        return ConsensusResult(
            issue=longest_issue,
            severity=severity,
            confidence=confidence,
            agreeing_reviewers=agreeing_reviewers,
            total_reviewers=total_reviewers,
            location=location,
            suggestions=suggestions,
            issue_type=issue_type
        )

    def _get_most_specific_location(self, locations: List[str]) -> str:
        """Get the most specific location from a list."""
        # Prefer locations with line numbers
        for loc in locations:
            if re.search(r'line \d+', loc, re.IGNORECASE):
                return loc

        # Then prefer locations with any numbers
        for loc in locations:
            if re.search(r'\d+', loc):
                return loc

        # Otherwise return the longest (likely most specific)
        return max(locations, key=len) if locations else "unspecified"

    def calculate_confidence(self, agreeing: int, total: int) -> float:
        """Calculate confidence score based on reviewer agreement."""
        if total == 0:
            return 0.0
        return agreeing / total

    def group_by_location(self, feedback_list: List[ReviewFeedback]) -> Dict[str, List[ReviewFeedback]]:
        """Group feedback by location, merging overlapping ranges."""
        location_groups = {}
        location_ranges = {}  # Track the range for each group key

        for feedback in feedback_list:
            # Extract line range from location
            location_range = self._extract_line_range(feedback.location)

            # Find if this location overlaps with any existing group
            merged = False
            for existing_key, existing_group in list(location_groups.items()):
                existing_range = location_ranges.get(existing_key)

                # Check if ranges overlap
                if existing_range and self._ranges_overlap(location_range, existing_range):
                    existing_group.append(feedback)
                    merged = True
                    break

            # If no overlap found, create new group
            if not merged:
                normalized = self._normalize_location(feedback.location)
                if normalized not in location_groups:
                    location_groups[normalized] = []
                    location_ranges[normalized] = location_range
                location_groups[normalized].append(feedback)

        return location_groups

    def _extract_line_range(self, location: str) -> Tuple[int, int]:
        """Extract line range from location string. Returns (start, end) or (None, None)."""
        if match := re.search(r'line[s]?\s*(\d+)(?:\s*-\s*(\d+))?', location, re.IGNORECASE):
            start = int(match.group(1))
            end = int(match.group(2)) if match.group(2) else start
            return (start, end)
        return (None, None)

    def _ranges_overlap(self, range1: Tuple[int, int], range2: Tuple[int, int]) -> bool:
        """Check if two line ranges overlap or if one contains the other."""
        start1, end1 = range1
        start2, end2 = range2

        # If either range is invalid (None), they don't overlap
        if start1 is None or start2 is None:
            return False

        # Check for overlap: range1 contains range2, range2 contains range1, or they intersect
        return not (end1 < start2 or end2 < start1)

    def _normalize_location(self, location: str) -> str:
        """Normalize location string for grouping."""
        # Extract key location indicators
        if match := re.search(r'line[s]?\s*(\d+)(?:\s*-\s*(\d+))?', location, re.IGNORECASE):
            start = int(match.group(1))
            end = int(match.group(2)) if match.group(2) else start
            return f"lines_{start}_{end}"

        if match := re.search(r'paragraph\s*(\d+)', location, re.IGNORECASE):
            return f"paragraph_{match.group(1)}"

        if match := re.search(r'section\s*(\d+)', location, re.IGNORECASE):
            return f"section_{match.group(1)}"

        if match := re.search(r'example\s*(\d+)', location, re.IGNORECASE):
            return f"example_{match.group(1)}"

        return location.lower().strip()

    def filter_by_confidence(self, results: List[ConsensusResult],
                            threshold: float = 0.7) -> List[ConsensusResult]:
        """Filter results to only include those above confidence threshold."""
        return [r for r in results if r.confidence >= threshold]

    def sort_by_priority(self, results: List[ConsensusResult]) -> List[ConsensusResult]:
        """Sort results by priority (severity * confidence)."""
        return sorted(results, key=lambda r: r.get_priority_score(), reverse=True)

    def generate_report(self, consensus_results: List[ConsensusResult],
                       module_id: str, review_pass: ReviewPass,
                       strengths: List[str] = None) -> ReviewReport:
        """Generate a review report from consensus results."""
        # Estimate revision time based on issues
        revision_time = self._estimate_revision_time(consensus_results)

        # Extract strengths if not provided
        if not strengths:
            strengths = self._extract_strengths(consensus_results)

        return ReviewReport(
            module_id=module_id,
            review_pass=review_pass,
            timestamp=datetime.now(),
            consensus_results=consensus_results,
            strengths=strengths,
            estimated_revision_time=revision_time
        )

    def _estimate_revision_time(self, results: List[ConsensusResult]) -> int:
        """Estimate revision time in minutes based on issues."""
        time_estimate = 0

        for result in results:
            # Base time on severity
            if result.severity >= 5:
                time_estimate += 15  # Critical issues take longer
            elif result.severity >= 4:
                time_estimate += 10
            elif result.severity >= 3:
                time_estimate += 5
            else:
                time_estimate += 2

            # Adjust based on confidence
            if result.confidence < 0.5:
                time_estimate *= 0.5  # Low confidence issues may not need fixing

        return int(time_estimate)

    def _extract_strengths(self, results: List[ConsensusResult]) -> List[str]:
        """Extract content strengths based on what's NOT mentioned in issues.
        Focus on the MODULE'S strengths, not the author's abilities."""
        strengths = []

        # Check issue types to determine content strengths
        issue_types = set(r.issue_type for r in results)

        if "pedagogical_flow" not in issue_types:
            strengths.append("The content flows well with good scaffolding")

        if "missing_examples" not in issue_types and "example" not in str(issue_types):
            strengths.append("Examples are relevant and well-constructed")

        if "quiz" not in str(issue_types):
            strengths.append("Quiz questions effectively assess understanding")

        if not any(r.severity >= 4 for r in results):
            strengths.append("The module has no critical issues")

        if not any("chunk" in r.issue.lower() for r in results):
            strengths.append("Content is well-chunked for learning")

        if not any("concrete" in r.issue.lower() for r in results):
            strengths.append("Concepts are presented concretely")

        if not strengths:
            strengths.append("The module provides a foundation to build upon")

        return strengths

    def merge_passes(self, pass1_results: List[ConsensusResult],
                    pass2_results: List[ConsensusResult]) -> List[ConsensusResult]:
        """Merge results from multiple passes, avoiding duplicates."""
        merged = pass1_results.copy()

        for result2 in pass2_results:
            # Check if this issue already exists
            duplicate = False
            for result1 in pass1_results:
                if self._are_results_similar(result1, result2):
                    duplicate = True
                    # Update with new information if confidence is higher
                    if result2.confidence > result1.confidence:
                        idx = merged.index(result1)
                        merged[idx] = result2
                    break

            if not duplicate:
                merged.append(result2)

        return self.sort_by_priority(merged)

    def _are_results_similar(self, result1: ConsensusResult,
                            result2: ConsensusResult) -> bool:
        """Check if two consensus results refer to the same issue."""
        issue_similarity = self._string_similarity(result1.issue, result2.issue)
        location_similarity = self._location_similarity(result1.location, result2.location)

        return issue_similarity > 0.8 and location_similarity > 0.5

    def get_improvement_rate(self, before: List[ConsensusResult],
                            after: List[ConsensusResult]) -> float:
        """Calculate the improvement rate between two review passes."""
        if not before:
            return 1.0  # 100% improvement if no issues before

        fixed_count = 0
        for old_result in before:
            # Check if issue still exists in after
            still_exists = False
            for new_result in after:
                if self._are_results_similar(old_result, new_result):
                    still_exists = True
                    break

            if not still_exists:
                fixed_count += 1

        return fixed_count / len(before) if before else 0.0