"""
Data models for the Learnvia AI-Powered Content Revision System.
Supports 60 AI reviewers in a structured consensus approach.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional, Any
import json

class ReviewerRole(Enum):
    """Defines the type of review being performed."""
    AUTHORING = "authoring"
    STYLE = "style"

class ReviewPass(Enum):
    """Defines the 4-pass review process with independent passes."""
    CONTENT_PASS_1 = "content_pass_1"  # 20 agents: content + style, independent
    CONTENT_PASS_2 = "content_pass_2"  # Different 20 agents: content + style, independent
    COPY_PASS_1 = "copy_pass_1"        # 10 agents: copy edit only, independent
    COPY_PASS_2 = "copy_pass_2"        # Different 10 agents: copy edit only, independent

class SeverityLevel:
    """Severity levels for issues found in review."""
    CRITICAL = 5  # Must fix - incorrect math, missing components
    HIGH = 4      # Core pedagogy issues
    MEDIUM = 3    # Writing quality issues
    LOW = 2       # Style compliance
    MINOR = 1     # Polish suggestions

class ConfidenceLevel:
    """Confidence levels based on reviewer agreement."""
    @staticmethod
    def get_level(agreeing: int, total: int) -> str:
        """Returns confidence level based on reviewer agreement."""
        ratio = agreeing / total if total > 0 else 0

        if ratio >= 1.0:
            return "very_high"
        elif ratio >= 0.7:
            return "high"
        elif ratio >= 0.4:
            return "moderate"
        elif ratio >= 0.2:
            return "low"
        else:
            return "very_low"

    @staticmethod
    def get_description(level: str) -> str:
        """Returns human-readable description of confidence level."""
        descriptions = {
            "very_high": "Very high confidence - critical issue",
            "high": "High confidence - important issue",
            "moderate": "Moderate confidence - should consider",
            "low": "Low confidence - optional consideration",
            "very_low": "Very low confidence - FYI only"
        }
        return descriptions.get(level, "Unknown confidence level")

@dataclass
class ModuleContent:
    """Represents the educational module being reviewed."""
    content: str
    module_id: str = ""
    title: str = ""
    author: str = ""
    word_count: int = 0
    components: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        """Extract components if not provided."""
        if not self.components and self.content:
            self._extract_components()
        if not self.word_count:
            self.word_count = len(self.content.split())

    def _extract_components(self):
        """Extract module components from content."""
        # Simple extraction logic - can be enhanced
        self.components = {
            "framing": "",
            "lesson": "",
            "examples": "",
            "quiz": "",
            "homework": ""
        }
        # In real implementation, parse content to extract components

@dataclass
class ReviewFeedback:
    """Individual feedback from a single reviewer."""
    reviewer_id: str
    issue_type: str
    severity: int
    location: str
    issue: str
    suggestion: str
    confidence_contribution: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert feedback to dictionary format."""
        return {
            "reviewer_id": self.reviewer_id,
            "issue_type": self.issue_type,
            "severity": self.severity,
            "location": self.location,
            "issue": self.issue,
            "suggestion": self.suggestion,
            "confidence_contribution": self.confidence_contribution,
            "timestamp": self.timestamp.isoformat()
        }

    def to_student_success_framing(self) -> str:
        """Convert feedback to student-success framing.
        Focus on CONTENT quality (not author evaluation).
        Frame as 'helping students learn better' not 'author made errors'."""
        if self.severity >= 4:
            prefix = "Learning Opportunity"
        elif self.severity >= 3:
            prefix = "Improvement Suggestion"
        else:
            prefix = "Polish Recommendation"

        # Reframe to focus on student impact, not author error
        reframed_issue = self.issue.replace("ERROR:", "").replace("Missing", "Consider adding")
        reframed_issue = reframed_issue.replace("Too large", "Students might struggle with")
        reframed_issue = reframed_issue.replace("Incorrect", "Needs verification:")
        reframed_issue = reframed_issue.replace("You ", "The content ")
        reframed_issue = reframed_issue.replace("Your ", "The module's ")

        return f"{prefix}: {reframed_issue}. {self.suggestion}"

@dataclass
class ConsensusResult:
    """Aggregated feedback from multiple reviewers on the same issue."""
    issue: str
    severity: int
    confidence: float
    agreeing_reviewers: int
    total_reviewers: int
    location: str
    suggestions: List[str] = field(default_factory=list)
    issue_type: str = ""

    @property
    def confidence_level(self) -> str:
        """Get the confidence level category."""
        return ConfidenceLevel.get_level(self.agreeing_reviewers, self.total_reviewers)

    @property
    def should_provide_solution(self) -> bool:
        """Determine if specific solution should be provided.
        ONLY provide suggestions when BOTH high severity AND high confidence."""
        return self.confidence >= 0.7 and self.severity >= 4

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "issue": self.issue,
            "severity": self.severity,
            "confidence": self.confidence,
            "confidence_level": self.confidence_level,
            "agreeing_reviewers": self.agreeing_reviewers,
            "total_reviewers": self.total_reviewers,
            "location": self.location,
            "suggestions": self.suggestions,
            "issue_type": self.issue_type,
            "should_provide_solution": self.should_provide_solution
        }

    def get_priority_score(self) -> float:
        """Calculate priority score for sorting issues."""
        return self.severity * self.confidence

@dataclass
class ReviewReport:
    """Complete review report for an author."""
    module_id: str
    review_pass: ReviewPass
    timestamp: datetime
    consensus_results: List[ConsensusResult]
    strengths: List[str]
    estimated_revision_time: int  # in minutes
    author_experience_level: str = "new"

    def get_priority_matrix(self) -> Dict[str, List[ConsensusResult]]:
        """Organize issues into priority matrix."""
        matrix = {
            "immediate": [],  # High severity + high confidence
            "important": [],  # High severity or high confidence
            "consider": [],   # Medium severity/confidence
            "optional": []    # Low severity/confidence
        }

        for result in self.consensus_results:
            if result.severity >= 4 and result.confidence >= 0.7:
                matrix["immediate"].append(result)
            elif result.severity >= 4 or result.confidence >= 0.7:
                matrix["important"].append(result)
            elif result.severity >= 3 or result.confidence >= 0.4:
                matrix["consider"].append(result)
            else:
                matrix["optional"].append(result)

        return matrix

    def filter_for_experience_level(self) -> List[ConsensusResult]:
        """Filter results based on author experience level."""
        if self.author_experience_level == "new":
            # New authors see only high-confidence issues
            return [r for r in self.consensus_results if r.confidence >= 0.7]
        else:
            # Experienced authors see all feedback
            return self.consensus_results

    def to_json(self) -> str:
        """Convert report to JSON format."""
        return json.dumps({
            "module_id": self.module_id,
            "review_pass": self.review_pass.value,
            "timestamp": self.timestamp.isoformat(),
            "consensus_results": [r.to_dict() for r in self.consensus_results],
            "strengths": self.strengths,
            "estimated_revision_time": self.estimated_revision_time,
            "priority_matrix": {
                k: [r.to_dict() for r in v]
                for k, v in self.get_priority_matrix().items()
            }
        }, indent=2)

@dataclass
class ReviewSession:
    """Manages the entire review session for a module."""
    module: ModuleContent
    session_id: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    current_pass: Optional[ReviewPass] = None
    all_feedback: List[ReviewFeedback] = field(default_factory=list)
    reports: List[ReviewReport] = field(default_factory=list)
    api_calls_made: int = 0

    def __post_init__(self):
        """Initialize session ID if not provided."""
        if not self.session_id:
            self.session_id = f"session_{self.start_time.strftime('%Y%m%d_%H%M%S')}_{self.module.module_id}"

    def add_feedback(self, feedback: ReviewFeedback):
        """Add feedback from a reviewer."""
        self.all_feedback.append(feedback)

    def add_report(self, report: ReviewReport):
        """Add a completed report for a review pass."""
        self.reports.append(report)

    def complete_session(self):
        """Mark the session as complete."""
        self.end_time = datetime.now()

    def get_duration_minutes(self) -> float:
        """Get the session duration in minutes."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() / 60
        return 0

    def get_feedback_by_pass(self, review_pass: ReviewPass) -> List[ReviewFeedback]:
        """Get all feedback for a specific review pass."""
        pass_prefixes = {
            ReviewPass.CONTENT_PASS_1: "content_p1",
            ReviewPass.CONTENT_PASS_2: "content_p2",
            ReviewPass.COPY_PASS_1: "copy_p1",
            ReviewPass.COPY_PASS_2: "copy_p2"
        }
        prefix = pass_prefixes.get(review_pass, "")
        return [f for f in self.all_feedback if f.reviewer_id.startswith(prefix)]

@dataclass
class ReviewerConfig:
    """Configuration for individual AI reviewers."""
    reviewer_id: str
    role: ReviewerRole
    review_pass: ReviewPass
    focus_area: str
    prompt_variation: str = ""
    temperature: float = 0.7
    max_tokens: int = 2000

    def get_system_prompt(self, product_vision: str, guidelines: str) -> str:
        """Generate the system prompt for this reviewer."""
        base_prompt = f"""You are AI Reviewer {self.reviewer_id} for Learnvia educational modules.

PRODUCT VISION CONTEXT:
{product_vision}

YOUR ROLE: {self.role.value.upper()} REVIEWER
FOCUS AREA: {self.focus_area}
REVIEW PASS: {self.review_pass.value}

GUIDELINES TO EVALUATE AGAINST:
{guidelines}

{self.prompt_variation}

Provide structured feedback identifying issues with:
- Issue type and location
- Severity (1-5 scale)
- Specific problem description
- Actionable suggestion for improvement

Focus on student success and educational effectiveness.
Remember the target learner: studying home alone, low confidence, scared of failing, limited time.
"""
        return base_prompt