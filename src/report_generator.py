"""
Report generation module for the Learnvia content revision system.
Creates friendly, educational reports for authors from consensus results.
"""

import json
from typing import List, Dict, Any
from datetime import datetime
import csv
from io import StringIO

from .models import (
    ReviewReport, ConsensusResult, ReviewPass,
    SeverityLevel, ConfidenceLevel
)


class ReportFormatter:
    """Handles formatting of report components."""

    @staticmethod
    def format_issue(result: ConsensusResult) -> str:
        """Format a single issue in student-success framing."""
        # Choose framing based on severity
        if result.severity >= SeverityLevel.CRITICAL:
            prefix = "🔴 Critical Learning Blocker"
        elif result.severity >= SeverityLevel.HIGH:
            prefix = "🟠 Important Learning Opportunity"
        elif result.severity >= SeverityLevel.MEDIUM:
            prefix = "🟡 Improvement Suggestion"
        else:
            prefix = "🟢 Polish Recommendation"

        # Reframe the issue positively
        issue = result.issue.replace("ERROR:", "").replace("WRONG:", "")
        issue = issue.replace("Missing", "Consider adding")
        issue = issue.replace("Too large", "Students might benefit from smaller")
        issue = issue.replace("Incorrect", "Needs verification:")

        formatted = f"{prefix}: {issue}\n"
        formatted += f"   Location: {result.location}\n"
        formatted += f"   Confidence: {result.confidence_level} ({result.agreeing_reviewers}/{result.total_reviewers} reviewers)\n"

        # ONLY provide suggestions when BOTH high severity AND high confidence
        if result.should_provide_solution and result.suggestions:
            formatted += "   Suggestions:\n"
            for suggestion in result.suggestions[:3]:  # Limit to top 3
                formatted += f"   • {suggestion}\n"
        elif not result.should_provide_solution:
            formatted += "   (Issue flagged for awareness - no specific solution provided)\n"

        return formatted

    @staticmethod
    def format_priority_matrix(matrix: Dict[str, List[ConsensusResult]]) -> str:
        """Format the priority matrix for display."""
        output = []

        sections = [
            ("🔥 IMMEDIATE ACTION", "immediate"),
            ("⚠️  IMPORTANT", "important"),
            ("💡 CONSIDER", "consider"),
            ("✨ OPTIONAL POLISH", "optional")
        ]

        for title, key in sections:
            if matrix.get(key):
                output.append(f"\n{title} ({len(matrix[key])} items):")
                output.append("-" * 40)
                for result in matrix[key][:5]:  # Show top 5 per category
                    output.append(f"• {result.issue[:80]}...")
                    output.append(f"  📍 {result.location}")

        return "\n".join(output)

    @staticmethod
    def format_time_estimate(minutes: int) -> str:
        """Format time estimate in human-readable form."""
        if minutes < 60:
            return f"{minutes} minutes"
        else:
            hours = minutes // 60
            remaining_minutes = minutes % 60
            if remaining_minutes > 0:
                return f"{hours} hours {remaining_minutes} minutes"
            else:
                return f"{hours} hours"

    @staticmethod
    def format_suggestions(suggestions: List[str]) -> str:
        """Format a list of suggestions."""
        if not suggestions:
            return "No specific suggestions provided."

        formatted = []
        for i, suggestion in enumerate(suggestions, 1):
            formatted.append(f"{i}. {suggestion}")

        return "\n".join(formatted)

    @staticmethod
    def format_confidence_explanation(level: str) -> str:
        """Explain what a confidence level means."""
        explanations = {
            "very_high": "All reviewers identified this issue - definitely needs attention",
            "high": "Most reviewers agree - important to address",
            "moderate": "Several reviewers noticed - worth considering",
            "low": "A few reviewers mentioned - optional improvement",
            "very_low": "Single reviewer flagged - may be fine as is"
        }
        return explanations.get(level, "")


class ReportGenerator:
    """Generates various report formats from review results."""

    def __init__(self):
        """Initialize the report generator."""
        self.formatter = ReportFormatter()

    def generate_text_report(self, report: ReviewReport) -> str:
        """Generate a plain text report for console or file output."""
        lines = []

        # Header
        lines.append("=" * 70)
        lines.append("LEARNVIA MODULE REVIEW REPORT")
        lines.append("=" * 70)
        lines.append(f"Module ID: {report.module_id}")
        lines.append(f"Review Pass: {report.review_pass.value}")
        lines.append(f"Date: {report.timestamp.strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"Estimated Revision Time: {self.formatter.format_time_estimate(report.estimated_revision_time)}")
        lines.append("")

        # Content strengths section (not author strengths - important distinction!)
        lines.append("🌟 CONTENT STRENGTHS - What's Working Well:")
        lines.append("-" * 40)
        for strength in report.strengths:
            lines.append(f"✓ {strength}")
        lines.append("")

        # Filter results for experience level
        filtered_results = report.filter_for_experience_level()

        if not filtered_results:
            lines.append("🎉 Excellent work! No significant issues found.")
            lines.append("Your module is ready for the next review stage.")
        else:
            # Priority matrix
            lines.append("📊 PRIORITY MATRIX:")
            matrix = report.get_priority_matrix()
            lines.append(self.formatter.format_priority_matrix(matrix))
            lines.append("")

            # Detailed issues by category
            lines.append("📝 DETAILED FEEDBACK:")
            lines.append("-" * 40)

            grouped = self.group_by_issue_type(filtered_results)
            for issue_type, issues in grouped.items():
                reframed_type = self._reframe_issue_type(issue_type).upper()
                lines.append(f"\n{reframed_type}:")
                for result in issues[:10]:  # Limit to 10 per type
                    lines.append(self.formatter.format_issue(result))

        # Footer with guidance
        lines.append("")
        lines.append("💭 NEXT STEPS:")
        lines.append("-" * 40)

        if report.author_experience_level == "new":
            lines.append("• Focus on 🔴 Critical and 🟠 Important issues first")
            lines.append("• Don't worry about getting everything perfect on the first try")
            lines.append("• Review the authoring guidelines for additional context")
            lines.append("• Remember: You're learning and improving with each module!")
        else:
            lines.append("• Address issues in priority order")
            lines.append("• Use bulk operations where appropriate")
            lines.append("• Consider the pedagogical impact of each change")

        lines.append("")
        lines.append("📚 RESOURCES:")
        lines.append("• Authoring Guidelines: /txt_guides/Learnvia authoring guidelines (2025).txt")
        lines.append("• Style Guide: /txt_guides/Learnvia style guide_091625.txt")
        lines.append("• Product Vision: /txt_guides/Learnvia_Product_Vision (2025).txt")

        lines.append("")
        lines.append("🔄 FEEDBACK SYSTEM:")
        lines.append("• Disagree with an issue? Use: python dispute_issue.py <issue_id> '<reason>'")
        lines.append("• Your disputes help improve the system for everyone")
        lines.append("• Valid disputes lead to prompt refinements, not just exceptions")

        lines.append("")
        lines.append("💬 Questions? You can explain your reasoning for any flagged issue.")
        lines.append("The system is here to support you, not gatekeep!")

        return "\n".join(lines)

    def generate_markdown_report(self, report: ReviewReport) -> str:
        """Generate a Markdown-formatted report."""
        lines = []

        # Header
        lines.append("# Learnvia Module Review Report")
        lines.append("")
        lines.append(f"**Module ID:** {report.module_id}")
        lines.append(f"**Review Pass:** {report.review_pass.value}")
        lines.append(f"**Date:** {report.timestamp.strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"**Estimated Revision Time:** {self.formatter.format_time_estimate(report.estimated_revision_time)}")
        lines.append("")

        # Content Strengths (evaluating the work, not the person)
        lines.append("## 🌟 Content Strengths")
        lines.append("")
        for strength in report.strengths:
            lines.append(f"- ✓ {strength}")
        lines.append("")

        # Priority Matrix
        lines.append("## 📊 Priority Matrix")
        lines.append("")
        matrix = report.get_priority_matrix()

        if matrix.get("immediate"):
            lines.append("### 🔥 Immediate Action Required")
            for result in matrix["immediate"]:
                lines.append(f"- **{result.issue}** ({result.location})")

        if matrix.get("important"):
            lines.append("### ⚠️ Important Issues")
            for result in matrix["important"]:
                lines.append(f"- **{result.issue}** ({result.location})")

        if matrix.get("consider"):
            lines.append("### 💡 Consider Addressing")
            for result in matrix["consider"]:
                lines.append(f"- {result.issue} ({result.location})")

        lines.append("")

        # Detailed feedback
        lines.append("## 📝 Detailed Feedback")
        lines.append("")

        filtered_results = report.filter_for_experience_level()
        grouped = self.group_by_issue_type(filtered_results)

        for issue_type, issues in grouped.items():
            reframed_type = self._reframe_issue_type(issue_type)
            lines.append(f"### {reframed_type}")
            lines.append("")

            for result in issues[:5]:
                severity_emoji = self._get_severity_emoji(result.severity)
                lines.append(f"#### {severity_emoji} {result.issue}")
                lines.append(f"- **Location:** {result.location}")
                lines.append(f"- **Confidence:** {result.confidence_level} ({result.agreeing_reviewers}/{result.total_reviewers} reviewers)")

                # ONLY provide suggestions when BOTH high severity AND high confidence
                if result.should_provide_solution and result.suggestions:
                    lines.append("- **Suggestions:**")
                    for suggestion in result.suggestions[:3]:
                        lines.append(f"  - {suggestion}")
                elif not result.should_provide_solution:
                    lines.append("- *(Issue flagged for awareness - no specific solution provided)*")
                lines.append("")

        # Next steps
        lines.append("## 💭 Next Steps")
        lines.append("")
        lines.append("1. Address critical and high-priority issues first")
        lines.append("2. Review suggestions and implement improvements")
        lines.append("3. Re-run the review to verify fixes")
        lines.append("")

        return "\n".join(lines)

    def generate_html_report(self, report: ReviewReport) -> str:
        """Generate an HTML report with styling."""
        html = []

        # HTML header with embedded CSS
        html.append("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Learnvia Module Review Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .section {
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .strength {
            color: #22c55e;
            margin: 10px 0;
        }
        .critical { color: #dc2626; font-weight: bold; }
        .high { color: #f97316; font-weight: bold; }
        .medium { color: #eab308; }
        .low { color: #22c55e; }
        .issue-card {
            border-left: 4px solid #667eea;
            padding: 15px;
            margin: 15px 0;
            background: #f8f9ff;
        }
        .confidence-badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.85em;
            background: #e5e7eb;
        }
        .high-confidence { background: #fee2e2; color: #dc2626; }
        .medium-confidence { background: #fef3c7; color: #d97706; }
        .low-confidence { background: #dcfce7; color: #16a34a; }
        .dispute-section {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e5e7eb;
        }
        .dispute-btn {
            background: #fff;
            border: 2px solid #dc2626;
            color: #dc2626;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
        }
        .dispute-btn:hover {
            background: #dc2626;
            color: white;
        }
        .dispute-form {
            margin-top: 15px;
            padding: 15px;
            background: #f9fafb;
            border-radius: 6px;
        }
        .dispute-form textarea {
            width: 100%;
            min-height: 100px;
            padding: 10px;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            margin-bottom: 10px;
            font-family: inherit;
        }
        .dispute-form button {
            margin-right: 10px;
            padding: 8px 16px;
            border-radius: 4px;
            border: none;
            cursor: pointer;
            font-weight: 500;
        }
        .dispute-form button:first-of-type {
            background: #22c55e;
            color: white;
        }
        .dispute-form button:last-of-type {
            background: #e5e7eb;
            color: #374151;
        }
    </style>
    <script>
        function disputeIssue(issueId) {
            document.getElementById('dispute-form-' + issueId).style.display = 'block';
        }

        function cancelDispute(issueId) {
            document.getElementById('dispute-form-' + issueId).style.display = 'none';
        }

        function submitDispute(issueId) {
            const form = document.getElementById('dispute-form-' + issueId);
            const textarea = form.querySelector('textarea');
            const reason = textarea.value;

            if (!reason.trim()) {
                alert('Please explain why you disagree with this issue.');
                return;
            }

            // In production, this would send to an API
            const disputeData = {
                issue_id: issueId,
                reason: reason,
                timestamp: new Date().toISOString()
            };

            console.log('Dispute submitted:', disputeData);
            alert('Thank you! Your dispute has been logged and will help improve the system.');

            // Reset form
            textarea.value = '';
            form.style.display = 'none';

            // Visual feedback
            const card = document.querySelector(`[data-issue-id="${issueId}"]`);
            card.style.opacity = '0.6';
            card.querySelector('.dispute-btn').textContent = '✓ Disputed';
            card.querySelector('.dispute-btn').disabled = true;
        }
    </script>
</head>
<body>""")

        # Header
        html.append(f"""
    <div class="header">
        <h1>Module Review Report</h1>
        <p><strong>Module ID:</strong> {report.module_id}</p>
        <p><strong>Review Pass:</strong> {report.review_pass.value}</p>
        <p><strong>Date:</strong> {report.timestamp.strftime('%Y-%m-%d %H:%M')}</p>
        <p><strong>Estimated Revision Time:</strong> {self.formatter.format_time_estimate(report.estimated_revision_time)}</p>
    </div>""")

        # Content strengths section (focus on the work, not the person)
        html.append("""
    <div class="section">
        <h2>🌟 Content Strengths - What's Working Well in This Module</h2>""")
        for strength in report.strengths:
            html.append(f'        <p class="strength">✓ {strength}</p>')
        html.append("    </div>")

        # Issues section
        filtered_results = report.filter_for_experience_level()
        if filtered_results:
            html.append("""
    <div class="section">
        <h2>📝 Issues to Address</h2>""")

            for i, result in enumerate(filtered_results[:20]):
                severity_class = self._get_severity_class(result.severity)
                confidence_class = self._get_confidence_class(result.confidence_level)

                # Generate unique issue ID
                issue_id = f"issue_{i}_{result.location.replace(' ', '_')[:20]}"

                html.append(f"""
        <div class="issue-card" data-issue-id="{issue_id}">
            <h3 class="{severity_class}">{result.issue}</h3>
            <p><strong>Location:</strong> {result.location}</p>
            <p><span class="confidence-badge {confidence_class}">
                {result.confidence_level} ({result.agreeing_reviewers}/{result.total_reviewers} reviewers)
            </span></p>""")

                # ONLY provide suggestions when BOTH high severity AND high confidence
                if result.should_provide_solution and result.suggestions:
                    html.append("            <p><strong>Suggestions:</strong></p><ul>")
                    for suggestion in result.suggestions[:3]:
                        html.append(f"                <li>{suggestion}</li>")
                    html.append("            </ul>")
                elif not result.should_provide_solution:
                    html.append("            <p><em>(Issue flagged for awareness - no specific solution provided)</em></p>")

                html.append(f"""
            <div class="dispute-section">
                <button class="dispute-btn" onclick="disputeIssue('{issue_id}')">
                    ❌ Dispute This Issue
                </button>
                <div id="dispute-form-{issue_id}" class="dispute-form" style="display:none;">
                    <textarea placeholder="Explain why this issue is incorrect or doesn't apply..."></textarea>
                    <button onclick="submitDispute('{issue_id}')">Submit Dispute</button>
                    <button onclick="cancelDispute('{issue_id}')">Cancel</button>
                </div>
            </div>""")

                html.append("        </div>")

            html.append("    </div>")

        # Footer
        html.append("""
</body>
</html>""")

        return "\n".join(html)

    def generate_json_report(self, report: ReviewReport) -> str:
        """Generate a JSON report for API consumption."""
        return report.to_json()

    def export_to_csv(self, report: ReviewReport) -> str:
        """Export issues to CSV format."""
        output = StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow([
            "Severity", "Issue", "Location", "Confidence",
            "Agreeing Reviewers", "Total Reviewers", "Suggestions"
        ])

        # Write issues
        for result in report.consensus_results:
            writer.writerow([
                result.severity,
                result.issue,
                result.location,
                result.confidence_level,
                result.agreeing_reviewers,
                result.total_reviewers,
                "; ".join(result.suggestions)
            ])

        return output.getvalue()

    def _reframe_issue_type(self, issue_type: str) -> str:
        """Reframe issue type in student-success language (avoid negative framing)."""
        # Map negative terms to student-success language
        reframe_map = {
            "error": "needs verification",
            "mistake": "learning opportunity",
            "wrong": "needs adjustment",
            "incorrect": "needs verification",
            "fail": "opportunity",
            "bad": "could be improved"
        }

        # Convert to title case and replace underscores
        formatted = issue_type.replace('_', ' ').title()

        # Replace negative words with positive framing
        for negative, positive in reframe_map.items():
            if negative in issue_type.lower():
                formatted = formatted.replace(negative.title(), positive.title())

        return formatted

    def group_by_issue_type(self, results: List[ConsensusResult]) -> Dict[str, List[ConsensusResult]]:
        """Group consensus results by issue type."""
        grouped = {}
        for result in results:
            issue_type = result.issue_type or "general"
            if issue_type not in grouped:
                grouped[issue_type] = []
            grouped[issue_type].append(result)
        return grouped

    def _get_severity_emoji(self, severity: int) -> str:
        """Get emoji for severity level."""
        if severity >= 5:
            return "🔴"
        elif severity >= 4:
            return "🟠"
        elif severity >= 3:
            return "🟡"
        else:
            return "🟢"

    def _get_severity_class(self, severity: int) -> str:
        """Get CSS class for severity level."""
        if severity >= 5:
            return "critical"
        elif severity >= 4:
            return "high"
        elif severity >= 3:
            return "medium"
        else:
            return "low"

    def _get_confidence_class(self, confidence_level: str) -> str:
        """Get CSS class for confidence level."""
        if "high" in confidence_level:
            return "high-confidence"
        elif "moderate" in confidence_level:
            return "medium-confidence"
        else:
            return "low-confidence"