"""
Synthetic reviewer module that evaluates content and makes progression decisions.
"""

import json
from typing import List, Dict, Tuple
from mock_agents import Feedback, Severity


class SyntheticReviewer:
    """Simulates Alex Rodriguez's review behavior."""

    def __init__(self, persona_file: str = "../synthetic_actors/reviewer_persona.json"):
        with open(persona_file, 'r') as f:
            self.persona = json.load(f)

    def review_content(self, content: str, feedback: List[Feedback], pass_number: int) -> Dict[str, any]:
        """
        Review content and make a progression decision.
        Returns review decision and commentary.
        """
        review = {
            "reviewer": self.persona["name"],
            "role": self.persona["role"],
            "pass_reviewed": pass_number,
            "decision": "",
            "rationale": "",
            "feedback_summary": self._summarize_feedback(feedback),
            "strengths": [],
            "concerns": [],
            "priority_fixes": [],
            "ready_for_copy_edit": False,
            "detailed_comments": ""
        }

        # Analyze severity distribution
        severity_counts = self._count_by_severity(feedback)

        # Identify strengths
        review["strengths"] = self._identify_strengths(content, feedback)

        # Identify remaining concerns
        review["concerns"] = self._identify_concerns(feedback, severity_counts)

        # Make decision based on approval criteria
        if severity_counts.get(5, 0) > 0 or severity_counts.get(4, 0) > 0:
            review["decision"] = "REQUEST_REVISION"
            review["ready_for_copy_edit"] = False
            review["rationale"] = (
                f"Found {severity_counts.get(5, 0)} critical and {severity_counts.get(4, 0)} high severity issues "
                f"that must be resolved before proceeding to copy editing."
            )
            review["priority_fixes"] = self._identify_priority_fixes(feedback)

        elif severity_counts.get(3, 0) > 5:
            review["decision"] = "REQUEST_REVISION"
            review["ready_for_copy_edit"] = False
            review["rationale"] = (
                f"While no critical issues remain, there are {severity_counts.get(3, 0)} medium severity issues "
                f"that should be addressed for pedagogical quality."
            )
            review["priority_fixes"] = self._identify_priority_fixes(feedback)

        else:
            review["decision"] = "APPROVE_FOR_COPY_EDIT"
            review["ready_for_copy_edit"] = True
            review["rationale"] = (
                "Content is pedagogically sound with no major issues. "
                "Minor style and formatting issues can be addressed in copy editing."
            )

        # Generate detailed comments
        review["detailed_comments"] = self._generate_detailed_comments(review, content)

        return review

    def _summarize_feedback(self, feedback: List[Feedback]) -> Dict[str, any]:
        """Summarize the feedback received."""
        summary = {
            "total_issues": len(feedback),
            "by_severity": {},
            "by_competency": {},
            "rubric_vs_generalist": {
                "rubric_caught": 0,
                "generalist_caught": 0
            }
        }

        for f in feedback:
            # Count by severity
            sev = f.severity.value
            summary["by_severity"][sev] = summary["by_severity"].get(sev, 0) + 1

            # Count by competency
            comp = f.competency.value
            summary["by_competency"][comp] = summary["by_competency"].get(comp, 0) + 1

            # Track rubric vs generalist
            if f.caught_by_rubric:
                summary["rubric_vs_generalist"]["rubric_caught"] += 1
            else:
                summary["rubric_vs_generalist"]["generalist_caught"] += 1

        return summary

    def _count_by_severity(self, feedback: List[Feedback]) -> Dict[int, int]:
        """Count issues by severity level."""
        counts = {}
        for f in feedback:
            sev = f.severity.value
            counts[sev] = counts.get(sev, 0) + 1
        return counts

    def _identify_strengths(self, content: str, feedback: List[Feedback]) -> List[str]:
        """Identify strengths in the content."""
        strengths = []

        # Check for good examples
        if "### Example" in content:
            example_count = content.count("### Example")
            if example_count >= 3:
                strengths.append(f"Good variety of examples ({example_count} provided)")

        # Check for real-world applications
        if "Real-World Applications" in content:
            strengths.append("Excellent inclusion of real-world applications")

        # Check for step-by-step instructions
        if "Step 1:" in content and "Step 2:" in content:
            strengths.append("Clear step-by-step breakdown for calculations")

        # Check for visual/conceptual explanations
        if "Think of it like" in content or "Imagine" in content:
            strengths.append("Good use of analogies and conceptual explanations")

        # Add some persona-specific observations
        if len(feedback) < 20:
            strengths.append("Content is relatively clean with few issues")

        if any("quiz" in f.competency.value.lower() for f in feedback) == False:
            strengths.append("Quiz questions are well-structured")

        return strengths

    def _identify_concerns(self, feedback: List[Feedback], severity_counts: Dict[int, int]) -> List[str]:
        """Identify remaining concerns."""
        concerns = []

        if severity_counts.get(5, 0) > 0:
            concerns.append(f"{severity_counts[5]} critical issues requiring immediate attention")

        if severity_counts.get(4, 0) > 0:
            concerns.append(f"{severity_counts[4]} high-priority issues affecting content quality")

        # Check for specific patterns
        contraction_issues = [f for f in feedback if "contraction" in f.issue.lower()]
        if len(contraction_issues) > 3:
            concerns.append(f"Multiple contractions ({len(contraction_issues)}) still present")

        voice_issues = [f for f in feedback if "imperative" in f.issue.lower() or "voice" in f.issue.lower()]
        if len(voice_issues) > 2:
            concerns.append(f"Voice and tone issues in {len(voice_issues)} locations")

        math_issues = [f for f in feedback if "latex" in f.issue.lower() or "mathematical" in f.issue.lower()]
        if math_issues:
            concerns.append("Mathematical notation needs proper LaTeX formatting")

        return concerns

    def _identify_priority_fixes(self, feedback: List[Feedback]) -> List[str]:
        """Identify priority fixes needed."""
        priority_fixes = []

        # Group by severity and take top issues
        high_severity = [f for f in feedback if f.severity.value >= 4]

        for f in high_severity[:5]:  # Top 5 high severity issues
            priority_fixes.append(f"{f.issue} ({f.location})")

        # Add any systematic issues
        if len([f for f in feedback if "contraction" in f.issue.lower()]) > 3:
            priority_fixes.append("Systematically remove all contractions throughout document")

        return priority_fixes

    def _generate_detailed_comments(self, review: Dict, content: str) -> str:
        """Generate detailed reviewer comments."""
        comments = []

        # Opening
        comments.append(f"Review by {self.persona['name']} - {self.persona['role']}")
        comments.append("=" * 60)
        comments.append("")

        # Positive feedback
        comments.append("What Works Well:")
        for strength in review["strengths"]:
            comments.append(f"  ✓ {strength}")
        comments.append("")

        # Decision and rationale
        comments.append(f"Decision: {review['decision'].replace('_', ' ')}")
        comments.append(f"Rationale: {review['rationale']}")
        comments.append("")

        # Concerns if any
        if review["concerns"]:
            comments.append("Remaining Concerns:")
            for concern in review["concerns"]:
                comments.append(f"  • {concern}")
            comments.append("")

        # Priority fixes if revision needed
        if review["priority_fixes"]:
            comments.append("Priority Fixes Required:")
            for i, fix in enumerate(review["priority_fixes"], 1):
                comments.append(f"  {i}. {fix}")
            comments.append("")

        # Personalized message
        if review["ready_for_copy_edit"]:
            comments.append("Additional Notes:")
            comments.append(
                "Great work on addressing the major pedagogical issues. The content is now "
                "ready for copy editing to polish the style and formatting. The remaining "
                "minor issues will be handled by our copy editing team."
            )
        else:
            comments.append("Encouragement:")
            comments.append(
                "You're making good progress! Please focus on the priority items listed above. "
                "Once these are resolved, the content will be ready for the copy editing phase. "
                "Don't hesitate to reach out if you need clarification on any feedback."
            )

        return "\n".join(comments)

    def format_review_report(self, review: Dict) -> str:
        """Format the review into a professional report."""
        report = "\n" + "="*80 + "\n"
        report += "CONTENT REVIEW REPORT\n"
        report += "="*80 + "\n\n"

        report += f"Reviewer: {review['reviewer']}\n"
        report += f"Role: {review['role']}\n"
        report += f"Pass Reviewed: Pass {review['pass_reviewed']}\n"
        report += f"Date: [Simulated Review Session]\n\n"

        report += "-"*80 + "\n"
        report += f"DECISION: {review['decision'].replace('_', ' ')}\n"
        report += "-"*80 + "\n\n"

        report += "FEEDBACK SUMMARY:\n"
        report += f"  Total Issues: {review['feedback_summary']['total_issues']}\n"
        report += f"  By Severity:\n"
        for sev, count in sorted(review['feedback_summary']['by_severity'].items(), reverse=True):
            report += f"    - Severity {sev}: {count} issues\n"

        report += f"\n  Issue Detection:\n"
        report += f"    - Rubric-focused agents: {review['feedback_summary']['rubric_vs_generalist']['rubric_caught']}\n"
        report += f"    - Generalist agents: {review['feedback_summary']['rubric_vs_generalist']['generalist_caught']}\n"

        report += "\n" + "-"*80 + "\n"
        report += "DETAILED REVIEW COMMENTS:\n"
        report += "-"*80 + "\n\n"
        report += review['detailed_comments']

        report += "\n\n" + "="*80 + "\n"

        return report


class SyntheticCopyEditor:
    """Simulates Dr. Margaret Thompson's EXTREMELY STRICT copy editing behavior."""

    def __init__(self, persona_file: str = "../synthetic_actors/copy_editor_persona.json"):
        with open(persona_file, 'r') as f:
            self.persona = json.load(f)

    def review_copy_edit(self, content: str, feedback: List[Feedback], pass_number: int) -> Dict[str, any]:
        """
        Perform ZERO TOLERANCE copy edit review.
        ANY violation = automatic rejection.
        """
        review = {
            "editor": self.persona["name"] + " (ZERO TOLERANCE MODE)",
            "role": self.persona["role"],
            "pass_reviewed": pass_number,
            "decision": "",
            "violations_found": [],
            "direct_fixes": [],  # NEVER fixes anything - author must learn
            "requires_author_fix": [],
            "final_approval": False,
            "strictness_level": "MAXIMUM - 100% compliance required",
            "tolerance": "ZERO",
            "comments": ""
        }

        # Check ALL issues - not just style
        # EXTREMELY STRICT means we care about EVERYTHING
        all_issues = feedback
        style_issues = [f for f in feedback if f.competency.value in ["style", "voice", "formatting"]]

        # Check for ANY contractions in the content directly (don't trust agents)
        contractions_to_check = ["don't", "doesn't", "won't", "can't", "let's", "it's",
                               "isn't", "aren't", "we'll", "you'll", "they'll", "we're",
                               "you're", "they're", "that's", "here's", "there's"]

        found_contractions = []
        for contraction in contractions_to_check:
            if contraction in content.lower():
                found_contractions.append(contraction)

        # Check for imperative voice patterns
        imperative_patterns = ["Calculate", "Find", "Look", "Think", "Remember", "Try",
                              "Use", "Apply", "Complete", "Graph", "Create", "Derive"]
        found_imperatives = []
        for pattern in imperative_patterns:
            if pattern in content:
                found_imperatives.append(pattern)

        # Determine if there are ANY violations
        total_violations = len(style_issues) + len(found_contractions) + len(found_imperatives)

        if total_violations == 0 and len(all_issues) == 0:
            # EXTREMELY RARE - perfect document
            review["decision"] = "APPROVED - PERFECT COMPLIANCE"
            review["final_approval"] = True
            review["comments"] = (
                "Document achieves 100% compliance with style guide. "
                "This is the expected standard. Approved for publication."
            )
        elif total_violations == 1:
            # Even ONE violation is unacceptable
            review["decision"] = "REJECTED - VIOLATION FOUND"
            review["final_approval"] = False
            review["violations_found"] = [f.issue for f in style_issues[:20]]
            review["requires_author_fix"] = ["ALL violations must be corrected"]
            review["comments"] = (
                "UNACCEPTABLE. Found style guide violation(s). "
                "This document is REJECTED. "
                "Zero tolerance means ZERO. Not one. ZERO. "
                "Review the style guide and resubmit only when achieving 100% compliance."
            )
        else:
            # Multiple violations - complete failure
            review["decision"] = "REJECTED - MULTIPLE VIOLATIONS"
            review["final_approval"] = False
            review["violations_found"] = (
                [f"{f.issue} at {f.location}" for f in style_issues[:10]] +
                [f"Contraction '{c}' found" for c in found_contractions[:5]] +
                [f"Imperative voice '{i}' found" for i in found_imperatives[:5]]
            )
            review["requires_author_fix"] = [
                "EVERY contraction must be removed",
                "ALL imperative voice must be eliminated",
                "EVERY mathematical expression must use LaTeX",
                "ALL formatting must be perfect",
                "Complete style guide compliance is mandatory"
            ]
            review["comments"] = (
                f"COMPLETELY UNACCEPTABLE. Found {total_violations} violations. "
                f"This demonstrates a fundamental failure to follow the style guide. "
                f"Did you even read the style guide? "
                f"Standards are non-negotiable. This needs complete revision. "
                f"Do not resubmit until you can guarantee 100% compliance."
            )

        # Add checklist status
        review["checklist_status"] = {
            "Zero contractions": "FAILED" if found_contractions else "PASSED",
            "Zero imperative voice": "FAILED" if found_imperatives else "PASSED",
            "Perfect formatting": "FAILED" if any(f.competency.value == "formatting" for f in feedback) else "PASSED",
            "100% compliance": "FAILED" if total_violations > 0 else "PASSED"
        }

        return review

    def format_copy_edit_report(self, review: Dict) -> str:
        """Format ZERO TOLERANCE copy edit review."""
        report = "\n" + "="*80 + "\n"
        report += "COPY EDIT REVIEW - ZERO TOLERANCE MODE\n"
        report += "="*80 + "\n\n"

        report += f"Copy Editor: {review['editor']}\n"
        report += f"Role: {review['role']}\n"
        report += f"Pass: {review['pass_reviewed']}\n"
        report += f"Strictness Level: {review['strictness_level']}\n"
        report += f"Tolerance: {review['tolerance']}\n\n"

        report += "="*80 + "\n"
        report += f"DECISION: {review['decision']}\n"
        report += "="*80 + "\n\n"

        # Show checklist status
        if "checklist_status" in review:
            report += "COMPLIANCE CHECKLIST:\n"
            for item, status in review["checklist_status"].items():
                symbol = "✓" if status == "PASSED" else "✗"
                report += f"  {symbol} {item}: {status}\n"
            report += "\n"

        if review["violations_found"]:
            report += "VIOLATIONS DETECTED:\n"
            report += "-"*40 + "\n"
            for i, violation in enumerate(review["violations_found"][:20], 1):
                report += f"  {i}. {violation}\n"
            if len(review["violations_found"]) > 20:
                report += f"  ... and {len(review["violations_found"]) - 20} more violations\n"
            report += "\n"

        if review["requires_author_fix"]:
            report += "MANDATORY CORRECTIONS:\n"
            report += "-"*40 + "\n"
            for fix in review["requires_author_fix"]:
                report += f"  ⚠️ {fix}\n"
            report += "\n"

        report += "EDITORIAL VERDICT:\n"
        report += "="*80 + "\n"
        report += review["comments"]
        report += "\n\n"

        if not review["final_approval"]:
            report += "REMINDER: Standards are non-negotiable. 100% compliance is mandatory.\n"
            report += "Do not resubmit until ALL violations are corrected.\n"

        report += "="*80 + "\n"

        return report


if __name__ == "__main__":
    # Test the reviewer
    import sys
    sys.path.append(".")
    from mock_agents import MockAgentSystem

    # Get mock feedback
    agent_system = MockAgentSystem()
    with open("../sample_content/draft_v1_original.md", "r") as f:
        content = f.read()

    feedback = agent_system.analyze_content(content, pass_number=2)

    # Review
    reviewer = SyntheticReviewer()
    review = reviewer.review_content(content, feedback, pass_number=2)
    print(reviewer.format_review_report(review))