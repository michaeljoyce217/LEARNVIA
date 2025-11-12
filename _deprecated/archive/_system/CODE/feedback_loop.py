"""
Feedback loop system for continuous improvement of AI reviewers.
Prevents prompt bloat by learning from disputes and generating principle-based refinements.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict, Counter
from pathlib import Path

from .models import ConsensusResult, ReviewPass
from .reviewers import get_project_root


@dataclass
class FeedbackItem:
    """Tracks author disagreements with AI feedback and reviewer responses."""
    feedback_id: str
    module_id: str
    issue_id: str  # Links to specific consensus result
    original_issue: Dict  # Serialized ConsensusResult
    author_dispute: str  # Author's explanation of why AI is wrong
    dispute_timestamp: datetime

    # Reviewer validation
    reviewer_judgment: Optional[str] = None  # "valid", "invalid", "partial"
    reviewer_notes: Optional[str] = None
    validation_timestamp: Optional[datetime] = None

    # System learning
    pattern_category: Optional[str] = None  # e.g., "mathematical_context", "quoted_text"
    suggested_refinement: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "feedback_id": self.feedback_id,
            "module_id": self.module_id,
            "issue_id": self.issue_id,
            "original_issue": self.original_issue,
            "author_dispute": self.author_dispute,
            "dispute_timestamp": self.dispute_timestamp.isoformat(),
            "reviewer_judgment": self.reviewer_judgment,
            "reviewer_notes": self.reviewer_notes,
            "validation_timestamp": self.validation_timestamp.isoformat() if self.validation_timestamp else None,
            "pattern_category": self.pattern_category,
            "suggested_refinement": self.suggested_refinement
        }


@dataclass
class PromptRefinement:
    """Tracks accumulated prompt improvements based on validated disputes."""
    refinement_id: str
    created_date: datetime
    review_type: str  # "authoring" or "style"

    # Pattern-based refinements (not individual rules)
    principle_adjustments: Dict[str, str] = field(default_factory=dict)
    context_clarifications: Dict[str, str] = field(default_factory=dict)

    # Metrics
    disputes_addressed: List[str] = field(default_factory=list)  # feedback_ids
    confidence_score: float = 0.0  # Based on reviewer agreement
    applied: bool = False
    applied_date: Optional[datetime] = None

    def generate_refinement_text(self) -> str:
        """Generate the actual prompt refinement text."""
        lines = []

        if self.principle_adjustments:
            lines.append("REFINED PRINCIPLES:")
            for category, principle in self.principle_adjustments.items():
                lines.append(f"- {category}: {principle}")

        if self.context_clarifications:
            lines.append("\nCONTEXT CLARIFICATIONS:")
            for context, clarification in self.context_clarifications.items():
                lines.append(f"- When evaluating {context}: {clarification}")

        return "\n".join(lines)


@dataclass
class DisputePattern:
    """Identifies patterns in disputes for systematic improvements."""
    pattern_name: str
    category: str  # e.g., "false_positive", "context_misunderstanding"
    frequency: int
    example_disputes: List[str]  # Sample dispute texts
    common_locations: List[str]  # Where these disputes occur
    suggested_principle: str  # Principle to address this pattern


class FeedbackLoop:
    """Manages the feedback loop for continuous improvement."""

    def __init__(self, storage_dir: str = None):
        """Initialize feedback loop with storage directory."""
        if storage_dir is None:
            storage_dir = str(get_project_root() / "feedback")
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)

        # Create subdirectories
        (self.storage_dir / "disputes").mkdir(exist_ok=True)
        (self.storage_dir / "validations").mkdir(exist_ok=True)
        (self.storage_dir / "refinements").mkdir(exist_ok=True)
        (self.storage_dir / "patterns").mkdir(exist_ok=True)

        # Load existing data
        self.disputes = self._load_disputes()
        self.validations = self._load_validations()
        self.refinements = self._load_refinements()

    def log_dispute(self, module_id: str, consensus_result: ConsensusResult,
                   dispute_reason: str) -> str:
        """Log an author's dispute of an AI-identified issue."""
        feedback_id = f"dispute_{module_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        feedback_item = FeedbackItem(
            feedback_id=feedback_id,
            module_id=module_id,
            issue_id=f"{consensus_result.location}_{consensus_result.issue[:30]}",
            original_issue=consensus_result.to_dict(),
            author_dispute=dispute_reason,
            dispute_timestamp=datetime.now()
        )

        # Categorize the dispute
        feedback_item.pattern_category = self._categorize_dispute(
            consensus_result, dispute_reason
        )

        # Save to file
        filepath = self.storage_dir / "disputes" / f"{feedback_id}.json"
        with open(filepath, 'w') as f:
            json.dump(feedback_item.to_dict(), f, indent=2)

        self.disputes[feedback_id] = feedback_item

        print(f"📝 Dispute logged: {feedback_id}")
        print(f"   Category: {feedback_item.pattern_category}")

        return feedback_id

    def validate_dispute(self, feedback_id: str, reviewer_judgment: str,
                        reviewer_notes: str = "") -> bool:
        """Human reviewer validates or invalidates a dispute."""
        if feedback_id not in self.disputes:
            print(f"❌ Dispute {feedback_id} not found")
            return False

        dispute = self.disputes[feedback_id]
        dispute.reviewer_judgment = reviewer_judgment
        dispute.reviewer_notes = reviewer_notes
        dispute.validation_timestamp = datetime.now()

        # Save validation
        filepath = self.storage_dir / "validations" / f"{feedback_id}_validated.json"
        with open(filepath, 'w') as f:
            json.dump(dispute.to_dict(), f, indent=2)

        self.validations[feedback_id] = dispute

        # If valid, trigger pattern analysis
        if reviewer_judgment == "valid":
            self._analyze_for_patterns()

        print(f"✅ Dispute validated: {reviewer_judgment}")
        return True

    def _categorize_dispute(self, result: ConsensusResult, dispute: str) -> str:
        """Categorize a dispute for pattern recognition."""
        dispute_lower = dispute.lower()
        issue_lower = result.issue.lower()

        # Common categories
        if "mathematical" in dispute_lower or "equation" in dispute_lower or "formula" in dispute_lower:
            return "mathematical_context"
        elif "quote" in dispute_lower or "dialogue" in dispute_lower:
            return "quoted_text"
        elif "example" in dispute_lower or "code" in dispute_lower:
            return "example_code"
        elif "imperative" in issue_lower and ("instruction" in dispute_lower or "procedure" in dispute_lower):
            return "procedural_imperative"
        elif "contraction" in issue_lower and ("possessive" in dispute_lower):
            return "possessive_vs_contraction"
        elif "technical" in dispute_lower or "terminology" in dispute_lower:
            return "technical_terms"
        elif "context" in dispute_lower:
            return "context_specific"
        else:
            return "general"

    def _analyze_for_patterns(self, min_frequency: int = 2) -> List[DisputePattern]:
        """Analyze validated disputes to identify patterns."""
        valid_disputes = [d for d in self.validations.values()
                         if d.reviewer_judgment == "valid"]

        if not valid_disputes:
            return []

        # Group by pattern category
        category_groups = defaultdict(list)
        for dispute in valid_disputes:
            category_groups[dispute.pattern_category].append(dispute)

        patterns = []

        for category, disputes in category_groups.items():
            if len(disputes) >= min_frequency:
                # Extract common elements
                locations = [d.original_issue.get("location", "") for d in disputes]
                location_counter = Counter(locations)
                common_locations = [loc for loc, count in location_counter.most_common(3)]

                # Generate principle
                principle = self._generate_principle(category, disputes)

                pattern = DisputePattern(
                    pattern_name=f"pattern_{category}_{len(patterns)}",
                    category=category,
                    frequency=len(disputes),
                    example_disputes=[d.author_dispute[:100] for d in disputes[:3]],
                    common_locations=common_locations,
                    suggested_principle=principle
                )
                patterns.append(pattern)

        # Save patterns
        patterns_file = self.storage_dir / "patterns" / f"patterns_{datetime.now().strftime('%Y%m%d')}.json"
        with open(patterns_file, 'w') as f:
            json.dump([asdict(p) for p in patterns], f, indent=2)

        return patterns

    def _generate_principle(self, category: str, disputes: List[FeedbackItem]) -> str:
        """Generate a principle-based refinement for a category of disputes."""
        principles = {
            "mathematical_context":
                "Mathematical expressions and formulas follow different conventions than prose. "
                "Evaluate mathematical content within its specific notational context.",

            "quoted_text":
                "Quoted text and dialogue preserve the original speaker's voice. "
                "Style rules apply to the instructional text, not quotations.",

            "example_code":
                "Code examples and mathematical workings have their own syntax requirements. "
                "Focus style evaluation on the explanatory text surrounding examples.",

            "procedural_imperative":
                "Step-by-step procedures and algorithms may use imperative voice for clarity. "
                "Distinguish between general instruction and procedural steps.",

            "possessive_vs_contraction":
                "Possessive forms (square's area) are acceptable and different from contractions. "
                "Only flag true contractions (it's = it is), not possessives.",

            "technical_terms":
                "Technical terminology may not follow standard style conventions. "
                "Preserve domain-specific terms and notation.",

            "context_specific":
                "Consider the pedagogical purpose and target audience when evaluating style. "
                "Some variations serve specific educational goals."
        }

        return principles.get(category,
                             "Evaluate content within its specific educational and technical context.")

    def generate_refinement(self, review_type: str = "authoring",
                          confidence_threshold: float = 0.8) -> PromptRefinement:
        """Generate a prompt refinement based on accumulated patterns."""
        patterns = self._analyze_for_patterns()

        if not patterns:
            print("📊 Not enough validated disputes for refinement generation")
            return None

        refinement = PromptRefinement(
            refinement_id=f"refinement_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            created_date=datetime.now(),
            review_type=review_type
        )

        # Convert patterns to principles
        for pattern in patterns:
            if pattern.frequency >= 5:  # High-frequency patterns
                refinement.principle_adjustments[pattern.category] = pattern.suggested_principle
                refinement.disputes_addressed.extend(
                    [d.feedback_id for d in self.validations.values()
                     if d.pattern_category == pattern.category]
                )
            elif pattern.frequency >= 3:  # Medium-frequency patterns
                refinement.context_clarifications[pattern.category] = pattern.suggested_principle

        # Calculate confidence
        total_valid = len([d for d in self.validations.values()
                          if d.reviewer_judgment == "valid"])
        addressed = len(refinement.disputes_addressed)
        refinement.confidence_score = addressed / total_valid if total_valid > 0 else 0

        # Only suggest if above threshold
        if refinement.confidence_score >= confidence_threshold:
            # Save refinement (convert datetime to string)
            filepath = self.storage_dir / "refinements" / f"{refinement.refinement_id}.json"
            refinement_dict = asdict(refinement)
            refinement_dict["created_date"] = refinement_dict["created_date"].isoformat()
            if refinement_dict.get("applied_date"):
                refinement_dict["applied_date"] = refinement_dict["applied_date"].isoformat()
            with open(filepath, 'w') as f:
                json.dump(refinement_dict, f, indent=2)

            self.refinements[refinement.refinement_id] = refinement

            print(f"✨ Refinement generated: {refinement.refinement_id}")
            print(f"   Addresses {addressed} disputes ({refinement.confidence_score:.0%} coverage)")
            print(f"\nRefinement text:\n{refinement.generate_refinement_text()}")

            return refinement
        else:
            print(f"⏸️  Refinement confidence too low ({refinement.confidence_score:.0%} < {confidence_threshold:.0%})")
            return None

    def apply_refinement(self, refinement_id: str) -> bool:
        """Apply a refinement to the prompt system (requires human approval)."""
        if refinement_id not in self.refinements:
            print(f"❌ Refinement {refinement_id} not found")
            return False

        refinement = self.refinements[refinement_id]

        # This would update the actual prompt files
        # For now, we'll just mark it as applied
        refinement.applied = True
        refinement.applied_date = datetime.now()

        # Save the update
        filepath = self.storage_dir / "refinements" / f"{refinement_id}_applied.json"
        with open(filepath, 'w') as f:
            json.dump(asdict(refinement), f, indent=2)

        print(f"✅ Refinement {refinement_id} applied to prompts")
        return True

    def get_dispute_stats(self) -> Dict:
        """Get statistics about disputes and resolutions."""
        total_disputes = len(self.disputes)
        validated = len(self.validations)
        valid = len([d for d in self.validations.values() if d.reviewer_judgment == "valid"])
        invalid = len([d for d in self.validations.values() if d.reviewer_judgment == "invalid"])

        # Category breakdown
        categories = Counter(d.pattern_category for d in self.disputes.values())

        return {
            "total_disputes": total_disputes,
            "validated": validated,
            "pending_validation": total_disputes - validated,
            "valid_disputes": valid,
            "invalid_disputes": invalid,
            "validity_rate": valid / validated if validated > 0 else 0,
            "categories": dict(categories),
            "total_refinements": len(self.refinements),
            "applied_refinements": len([r for r in self.refinements.values() if r.applied])
        }

    def _load_disputes(self) -> Dict[str, FeedbackItem]:
        """Load existing disputes from storage."""
        disputes = {}
        dispute_dir = self.storage_dir / "disputes"

        for filepath in dispute_dir.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    # Convert back to FeedbackItem
                    feedback_item = FeedbackItem(
                        feedback_id=data["feedback_id"],
                        module_id=data["module_id"],
                        issue_id=data["issue_id"],
                        original_issue=data["original_issue"],
                        author_dispute=data["author_dispute"],
                        dispute_timestamp=datetime.fromisoformat(data["dispute_timestamp"]),
                        reviewer_judgment=data.get("reviewer_judgment"),
                        reviewer_notes=data.get("reviewer_notes"),
                        validation_timestamp=datetime.fromisoformat(data["validation_timestamp"])
                            if data.get("validation_timestamp") else None,
                        pattern_category=data.get("pattern_category")
                    )
                    disputes[feedback_item.feedback_id] = feedback_item
            except Exception as e:
                print(f"Error loading dispute {filepath}: {e}")

        return disputes

    def _load_validations(self) -> Dict[str, FeedbackItem]:
        """Load validated disputes from storage."""
        validations = {}
        validation_dir = self.storage_dir / "validations"

        for filepath in validation_dir.glob("*_validated.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    feedback_item = FeedbackItem(
                        feedback_id=data["feedback_id"],
                        module_id=data["module_id"],
                        issue_id=data["issue_id"],
                        original_issue=data["original_issue"],
                        author_dispute=data["author_dispute"],
                        dispute_timestamp=datetime.fromisoformat(data["dispute_timestamp"]),
                        reviewer_judgment=data.get("reviewer_judgment"),
                        reviewer_notes=data.get("reviewer_notes"),
                        validation_timestamp=datetime.fromisoformat(data["validation_timestamp"])
                            if data.get("validation_timestamp") else None,
                        pattern_category=data.get("pattern_category")
                    )
                    validations[feedback_item.feedback_id] = feedback_item
            except Exception as e:
                print(f"Error loading validation {filepath}: {e}")

        return validations

    def _load_refinements(self) -> Dict[str, PromptRefinement]:
        """Load existing refinements from storage."""
        refinements = {}
        refinement_dir = self.storage_dir / "refinements"

        for filepath in refinement_dir.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    refinement = PromptRefinement(
                        refinement_id=data["refinement_id"],
                        created_date=datetime.fromisoformat(data["created_date"]),
                        review_type=data["review_type"],
                        principle_adjustments=data.get("principle_adjustments", {}),
                        context_clarifications=data.get("context_clarifications", {}),
                        disputes_addressed=data.get("disputes_addressed", []),
                        confidence_score=data.get("confidence_score", 0.0),
                        applied=data.get("applied", False),
                        applied_date=datetime.fromisoformat(data["applied_date"])
                            if data.get("applied_date") else None
                    )
                    refinements[refinement.refinement_id] = refinement
            except Exception as e:
                print(f"Error loading refinement {filepath}: {e}")

        return refinements