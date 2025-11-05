"""
Reviewer feedback loop system for tracking what AI reviewers miss.
This captures errors that human reviewers find but AI didn't flag.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict, Counter
from pathlib import Path

from .models import ReviewPass


@dataclass
class MissedIssue:
    """Tracks issues that human reviewers found but AI missed."""
    missed_issue_id: str
    module_id: str
    review_pass: ReviewPass

    # What the human found
    issue_description: str
    severity: int
    location: str
    issue_type: str  # "pedagogical", "style", "mathematical", etc.

    # Context
    was_flagged_by_ai: bool = False  # True if AI flagged something similar
    ai_confidence_if_flagged: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)

    # Analysis
    pattern_category: Optional[str] = None
    should_add_to_prompt: bool = False

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "missed_issue_id": self.missed_issue_id,
            "module_id": self.module_id,
            "review_pass": self.review_pass.value if hasattr(self.review_pass, 'value') else self.review_pass,
            "issue_description": self.issue_description,
            "severity": self.severity,
            "location": self.location,
            "issue_type": self.issue_type,
            "was_flagged_by_ai": self.was_flagged_by_ai,
            "ai_confidence_if_flagged": self.ai_confidence_if_flagged,
            "timestamp": self.timestamp.isoformat(),
            "pattern_category": self.pattern_category,
            "should_add_to_prompt": self.should_add_to_prompt
        }


@dataclass
class FalseNegativePattern:
    """Identifies patterns in what AI reviewers consistently miss."""
    pattern_id: str
    pattern_name: str
    issue_type: str
    frequency: int  # How many times this type was missed
    severity_average: float
    examples: List[str]

    # Thresholds
    refinement_threshold: int = 5  # Need 5+ occurrences to trigger refinement
    critical_threshold: int = 2    # Only 2 for critical issues

    def needs_refinement(self) -> bool:
        """Check if this pattern has occurred enough to warrant prompt refinement."""
        if self.severity_average >= 4:  # Critical/High severity
            return self.frequency >= self.critical_threshold
        else:
            return self.frequency >= self.refinement_threshold


@dataclass
class ReviewerAccuracyMetrics:
    """Tracks overall accuracy of AI reviewers vs human reviewers."""
    total_ai_issues: int = 0
    total_human_issues: int = 0

    # Categorized counts
    true_positives: int = 0   # AI found, human confirmed
    false_positives: int = 0  # AI found, human disputed (valid disputes)
    false_negatives: int = 0  # AI missed, human found

    # By severity
    missed_critical: int = 0  # Severity 5 issues AI missed
    missed_high: int = 0      # Severity 4 issues AI missed

    @property
    def precision(self) -> float:
        """What % of AI-flagged issues were real issues."""
        if self.true_positives + self.false_positives == 0:
            return 0.0
        return self.true_positives / (self.true_positives + self.false_positives)

    @property
    def recall(self) -> float:
        """What % of real issues did AI catch."""
        if self.true_positives + self.false_negatives == 0:
            return 0.0
        return self.true_positives / (self.true_positives + self.false_negatives)

    @property
    def f1_score(self) -> float:
        """Harmonic mean of precision and recall."""
        if self.precision + self.recall == 0:
            return 0.0
        return 2 * (self.precision * self.recall) / (self.precision + self.recall)

    @property
    def critical_miss_rate(self) -> float:
        """What % of critical issues did AI miss."""
        total_critical = self.missed_critical + self.missed_high
        if self.total_human_issues == 0:
            return 0.0
        return total_critical / self.total_human_issues


class ReviewerFeedbackLoop:
    """Manages feedback from human reviewers about what AI missed."""

    def __init__(self, storage_dir: str = "/Users/michaeljoyce/Desktop/LEARNVIA/feedback"):
        """Initialize reviewer feedback loop."""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)

        # Create subdirectories
        (self.storage_dir / "missed_issues").mkdir(exist_ok=True)
        (self.storage_dir / "patterns").mkdir(exist_ok=True)
        (self.storage_dir / "metrics").mkdir(exist_ok=True)

        # Load existing data
        self.missed_issues = self._load_missed_issues()
        self.patterns = self._load_patterns()
        self.metrics = self._load_metrics()

    def log_missed_issue(self, module_id: str, review_pass: ReviewPass,
                         issue_description: str, severity: int,
                         location: str, issue_type: str) -> str:
        """Log an issue that human reviewer found but AI missed."""
        missed_id = f"missed_{module_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        missed_issue = MissedIssue(
            missed_issue_id=missed_id,
            module_id=module_id,
            review_pass=review_pass,
            issue_description=issue_description,
            severity=severity,
            location=location,
            issue_type=issue_type
        )

        # Categorize the missed issue
        missed_issue.pattern_category = self._categorize_missed_issue(missed_issue)

        # Save to file
        filepath = self.storage_dir / "missed_issues" / f"{missed_id}.json"
        with open(filepath, 'w') as f:
            json.dump(missed_issue.to_dict(), f, indent=2)

        self.missed_issues[missed_id] = missed_issue

        # Update metrics
        self.metrics.false_negatives += 1
        self.metrics.total_human_issues += 1
        if severity >= 5:
            self.metrics.missed_critical += 1
        elif severity >= 4:
            self.metrics.missed_high += 1

        # Check if we need to trigger refinement
        self._check_refinement_triggers()

        print(f"📝 Missed issue logged: {missed_id}")
        print(f"   Type: {issue_type}, Severity: {severity}")

        return missed_id

    def log_confirmed_issue(self, module_id: str, ai_issue_id: str):
        """Log that a human reviewer confirmed an AI-flagged issue."""
        self.metrics.true_positives += 1
        self.metrics.total_ai_issues += 1
        self.metrics.total_human_issues += 1

        # Save metrics update
        self._save_metrics()

    def _categorize_missed_issue(self, issue: MissedIssue) -> str:
        """Categorize a missed issue for pattern recognition."""
        desc_lower = issue.issue_description.lower()

        # Common categories of missed issues
        if "chunk" in desc_lower or "scaffold" in desc_lower:
            return "pedagogical_structure"
        elif "example" in desc_lower:
            return "missing_examples"
        elif "quiz" in desc_lower or "question" in desc_lower:
            return "assessment_quality"
        elif "math" in desc_lower or "equation" in desc_lower or "formula" in desc_lower:
            return "mathematical_accuracy"
        elif "contraction" in desc_lower or "imperative" in desc_lower:
            return "style_mechanics"
        elif "vague" in desc_lower or "unclear" in desc_lower:
            return "clarity"
        elif "definition" in desc_lower:
            return "missing_definitions"
        else:
            return f"{issue.issue_type}_general"

    def _check_refinement_triggers(self):
        """Check if any patterns have hit their refinement thresholds."""
        # Group missed issues by pattern
        pattern_groups = defaultdict(list)
        for issue in self.missed_issues.values():
            key = f"{issue.issue_type}_{issue.pattern_category}"
            pattern_groups[key].append(issue)

        triggers = []

        for pattern_key, issues in pattern_groups.items():
            if not issues:
                continue

            # Calculate pattern metrics
            frequency = len(issues)
            avg_severity = sum(i.severity for i in issues) / len(issues)

            pattern = FalseNegativePattern(
                pattern_id=f"pattern_{pattern_key}_{datetime.now().strftime('%Y%m%d')}",
                pattern_name=pattern_key,
                issue_type=issues[0].issue_type,
                frequency=frequency,
                severity_average=avg_severity,
                examples=[i.issue_description[:100] for i in issues[:3]]
            )

            if pattern.needs_refinement():
                triggers.append(pattern)
                print(f"\n⚠️  REFINEMENT TRIGGER: {pattern_key}")
                print(f"   Frequency: {frequency} occurrences")
                print(f"   Average Severity: {avg_severity:.1f}")
                print(f"   Action: Add detection for this pattern to prompts")

        if triggers:
            self._generate_refinement_suggestions(triggers)

        return triggers

    def _generate_refinement_suggestions(self, patterns: List[FalseNegativePattern]):
        """Generate specific prompt additions for missed patterns."""
        print("\n" + "="*60)
        print("PROMPT REFINEMENT SUGGESTIONS")
        print("="*60)

        suggestions = {
            "authoring": [],
            "style": []
        }

        for pattern in patterns:
            # Determine which prompt to update
            if pattern.issue_type in ["pedagogical", "examples", "quiz", "scaffolding"]:
                prompt_type = "authoring"
            else:
                prompt_type = "style"

            # Generate specific detection rule
            if pattern.pattern_name == "pedagogical_structure":
                suggestion = "Check for appropriate chunking between concepts (gaps > 2 complexity levels)"
            elif pattern.pattern_name == "missing_examples":
                suggestion = "Verify each concept has at least one concrete, student-relevant example"
            elif pattern.pattern_name == "assessment_quality":
                suggestion = "Ensure quiz questions have clear feedback for all answer choices"
            elif pattern.pattern_name == "mathematical_accuracy":
                suggestion = "Validate all mathematical formulas and equations for correctness"
            elif pattern.pattern_name == "style_mechanics":
                suggestion = f"Additional {pattern.issue_type} checks needed"
            else:
                suggestion = f"Improve detection of {pattern.pattern_name.replace('_', ' ')}"

            suggestions[prompt_type].append({
                "pattern": pattern.pattern_name,
                "frequency": pattern.frequency,
                "severity": pattern.severity_average,
                "suggestion": suggestion,
                "examples": pattern.examples
            })

        # Save suggestions
        suggestions_file = self.storage_dir / "patterns" / f"refinement_suggestions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(suggestions_file, 'w') as f:
            json.dump(suggestions, f, indent=2)

        # Display suggestions
        for prompt_type, items in suggestions.items():
            if items:
                print(f"\n{prompt_type.upper()} PROMPT ADDITIONS:")
                for item in items:
                    print(f"\n• {item['suggestion']}")
                    print(f"  (Based on {item['frequency']} missed issues, avg severity {item['severity']:.1f})")

        print("\n✅ Suggestions saved to:", suggestions_file)

        return suggestions

    def get_accuracy_report(self) -> Dict:
        """Generate accuracy report comparing AI to human reviewers."""
        return {
            "precision": f"{self.metrics.precision:.1%}",
            "recall": f"{self.metrics.recall:.1%}",
            "f1_score": f"{self.metrics.f1_score:.2f}",
            "critical_miss_rate": f"{self.metrics.critical_miss_rate:.1%}",
            "total_ai_issues": self.metrics.total_ai_issues,
            "total_human_issues": self.metrics.total_human_issues,
            "true_positives": self.metrics.true_positives,
            "false_positives": self.metrics.false_positives,
            "false_negatives": self.metrics.false_negatives,
            "missed_critical": self.metrics.missed_critical,
            "missed_high": self.metrics.missed_high
        }

    def set_acceptable_miss_rate(self, rate: float = 0.15):
        """Set the acceptable miss rate (default 15%)."""
        self.acceptable_miss_rate = rate
        print(f"✅ Acceptable miss rate set to {rate:.0%}")
        print(f"   System will flag concern if miss rate exceeds this threshold")

    def _load_missed_issues(self) -> Dict[str, MissedIssue]:
        """Load existing missed issues from storage."""
        issues = {}
        missed_dir = self.storage_dir / "missed_issues"

        for filepath in missed_dir.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    issue = MissedIssue(
                        missed_issue_id=data["missed_issue_id"],
                        module_id=data["module_id"],
                        review_pass=data["review_pass"],
                        issue_description=data["issue_description"],
                        severity=data["severity"],
                        location=data["location"],
                        issue_type=data["issue_type"],
                        was_flagged_by_ai=data.get("was_flagged_by_ai", False),
                        ai_confidence_if_flagged=data.get("ai_confidence_if_flagged"),
                        timestamp=datetime.fromisoformat(data["timestamp"]),
                        pattern_category=data.get("pattern_category")
                    )
                    issues[issue.missed_issue_id] = issue
            except Exception as e:
                print(f"Error loading missed issue {filepath}: {e}")

        return issues

    def _load_patterns(self) -> List[FalseNegativePattern]:
        """Load identified patterns from storage."""
        patterns = []
        # Implementation for loading patterns
        return patterns

    def _load_metrics(self) -> ReviewerAccuracyMetrics:
        """Load accuracy metrics from storage."""
        metrics_file = self.storage_dir / "metrics" / "accuracy_metrics.json"

        if metrics_file.exists():
            try:
                with open(metrics_file, 'r') as f:
                    data = json.load(f)
                    metrics = ReviewerAccuracyMetrics(
                        total_ai_issues=data.get("total_ai_issues", 0),
                        total_human_issues=data.get("total_human_issues", 0),
                        true_positives=data.get("true_positives", 0),
                        false_positives=data.get("false_positives", 0),
                        false_negatives=data.get("false_negatives", 0),
                        missed_critical=data.get("missed_critical", 0),
                        missed_high=data.get("missed_high", 0)
                    )
                    return metrics
            except Exception as e:
                print(f"Error loading metrics: {e}")

        return ReviewerAccuracyMetrics()

    def _save_metrics(self):
        """Save current metrics to storage."""
        metrics_file = self.storage_dir / "metrics" / "accuracy_metrics.json"

        metrics_dict = {
            "total_ai_issues": self.metrics.total_ai_issues,
            "total_human_issues": self.metrics.total_human_issues,
            "true_positives": self.metrics.true_positives,
            "false_positives": self.metrics.false_positives,
            "false_negatives": self.metrics.false_negatives,
            "missed_critical": self.metrics.missed_critical,
            "missed_high": self.metrics.missed_high,
            "precision": self.metrics.precision,
            "recall": self.metrics.recall,
            "f1_score": self.metrics.f1_score,
            "critical_miss_rate": self.metrics.critical_miss_rate,
            "timestamp": datetime.now().isoformat()
        }

        with open(metrics_file, 'w') as f:
            json.dump(metrics_dict, f, indent=2)