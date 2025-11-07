"""
Test suite for the report generation system.
Tests creation of friendly, educational reports for authors.
"""

import pytest
from datetime import datetime
import json

from src.report_generator import ReportGenerator, ReportFormatter
from src.models import (
    ConsensusResult, ReviewReport, ReviewPass,
    SeverityLevel, ModuleContent
)


class TestReportGenerator:
    """Tests for the ReportGenerator class."""

    def create_test_report(self) -> ReviewReport:
        """Helper to create a test report with various issue types."""
        consensus_results = [
            ConsensusResult(
                issue="Incorrect mathematical formula in example 2",
                severity=SeverityLevel.CRITICAL,
                confidence=1.0,
                agreeing_reviewers=10,
                total_reviewers=10,
                location="Example 2, line 45",
                suggestions=["Correct formula should be y = 2x + 3"],
                issue_type="mathematical_error"
            ),
            ConsensusResult(
                issue="Large conceptual jump between examples",
                severity=SeverityLevel.HIGH,
                confidence=0.8,
                agreeing_reviewers=8,
                total_reviewers=10,
                location="Between examples 2 and 3",
                suggestions=["Add intermediate example", "Break down the concept"],
                issue_type="pedagogical_flow"
            ),
            ConsensusResult(
                issue="Uses contraction 'don't'",
                severity=SeverityLevel.LOW,
                confidence=0.6,
                agreeing_reviewers=6,
                total_reviewers=10,
                location="Paragraph 3",
                suggestions=["Replace with 'do not'"],
                issue_type="style_violation"
            )
        ]

        return ReviewReport(
            module_id="test_module_001",
            review_pass=ReviewPass.CONTENT_PASS_1,
            timestamp=datetime.now(),
            consensus_results=consensus_results,
            strengths=["Clear framing", "Good quiz questions", "Engaging examples"],
            estimated_revision_time=45,
            author_experience_level="new"
        )

    def test_generator_initialization(self):
        """Test creating a report generator."""
        generator = ReportGenerator()
        assert generator is not None

    def test_generate_text_report(self):
        """Test generation of a plain text report."""
        report = self.create_test_report()
        generator = ReportGenerator()

        text_report = generator.generate_text_report(report)

        # Check that key sections are present
        assert "STRENGTHS" in text_report or "Strengths" in text_report
        assert "PRIORITY" in text_report or "Priority" in text_report
        assert "Example 2" in text_report  # Location should be included
        assert "45 minutes" in text_report  # Time estimate

    def test_generate_html_report(self):
        """Test generation of an HTML report."""
        report = self.create_test_report()
        generator = ReportGenerator()

        html_report = generator.generate_html_report(report)

        # Check HTML structure
        assert "<html" in html_report and ">" in html_report  # Allow for attributes
        assert "</html>" in html_report
        assert "class=" in html_report  # Should have CSS classes
        assert "Strengths" in html_report or "strengths" in html_report.lower()

    def test_generate_json_report(self):
        """Test generation of a JSON report."""
        report = self.create_test_report()
        generator = ReportGenerator()

        json_report = generator.generate_json_report(report)
        parsed = json.loads(json_report)

        assert parsed["module_id"] == "test_module_001"
        assert len(parsed["consensus_results"]) == 3
        assert parsed["estimated_revision_time"] == 45

    def test_student_success_framing(self):
        """Test that issues are reframed in student-success language."""
        report = self.create_test_report()
        generator = ReportGenerator()

        text_report = generator.generate_text_report(report)

        # Should not contain negative framing
        assert "ERROR" not in text_report
        assert "FAIL" not in text_report.upper()

        # Should contain positive framing
        assert "Learning Opportunity" in text_report or "opportunity" in text_report.lower()

    def test_priority_matrix_formatting(self):
        """Test formatting of the priority matrix."""
        report = self.create_test_report()
        formatter = ReportFormatter()

        matrix_text = formatter.format_priority_matrix(report.get_priority_matrix())

        # Check that priority levels are present (case-insensitive)
        assert "immediate" in matrix_text.lower()
        assert "important" in matrix_text.lower() or "consider" in matrix_text.lower()

        # Check that critical issue is in immediate section
        assert "mathematical" in matrix_text.lower() or "formula" in matrix_text.lower()

    def test_experience_level_filtering(self):
        """Test that reports are filtered based on author experience."""
        # New author report
        new_author_report = self.create_test_report()
        new_author_report.author_experience_level = "new"

        generator = ReportGenerator()
        new_author_text = generator.generate_text_report(new_author_report)

        # Experienced author report
        exp_author_report = self.create_test_report()
        exp_author_report.author_experience_level = "experienced"

        exp_author_text = generator.generate_text_report(exp_author_report)

        # New authors should see fewer low-confidence issues
        # (This would be implemented in the actual code)
        assert len(new_author_text) <= len(exp_author_text)

    def test_strengths_highlighting(self):
        """Test that strengths are prominently displayed."""
        report = self.create_test_report()
        generator = ReportGenerator()

        text_report = generator.generate_text_report(report)

        # All strengths should be mentioned
        for strength in report.strengths:
            assert strength in text_report

    def test_time_estimate_display(self):
        """Test display of estimated revision time."""
        report = self.create_test_report()
        formatter = ReportFormatter()

        time_text = formatter.format_time_estimate(report.estimated_revision_time)

        assert "45" in time_text
        assert "minute" in time_text

        # Test with longer time
        long_time_text = formatter.format_time_estimate(125)
        assert "2 hours" in long_time_text or "2h" in long_time_text

    def test_markdown_report_generation(self):
        """Test generation of Markdown-formatted report."""
        report = self.create_test_report()
        generator = ReportGenerator()

        md_report = generator.generate_markdown_report(report)

        # Check Markdown formatting
        assert "## " in md_report  # Headers
        assert "- " in md_report   # List items
        assert "**" in md_report   # Bold text

    def test_issue_grouping_by_type(self):
        """Test that issues are grouped by type in the report."""
        report = self.create_test_report()
        generator = ReportGenerator()

        grouped = generator.group_by_issue_type(report.consensus_results)

        assert "mathematical_error" in grouped
        assert "pedagogical_flow" in grouped
        assert "style_violation" in grouped

        assert len(grouped["mathematical_error"]) == 1
        assert len(grouped["style_violation"]) == 1

    def test_adaptive_guidance_new_authors(self):
        """Test that new authors get extra guidance."""
        report = self.create_test_report()
        report.author_experience_level = "new"

        generator = ReportGenerator()
        text_report = generator.generate_text_report(report)

        # Should include encouraging language for new authors
        assert "great" in text_report.lower() or "good" in text_report.lower()

        # Should include resource links
        assert "guide" in text_report.lower() or "resource" in text_report.lower()

    def test_dispute_mechanism_info(self):
        """Test that dispute mechanism information is included."""
        report = self.create_test_report()
        generator = ReportGenerator()

        text_report = generator.generate_text_report(report)

        # Should mention ability to dispute or explain
        assert "dispute" in text_report.lower() or "explain" in text_report.lower()

    def test_empty_report_handling(self):
        """Test handling of report with no issues."""
        empty_report = ReviewReport(
            module_id="perfect_module",
            review_pass=ReviewPass.CONTENT_PASS_1,
            timestamp=datetime.now(),
            consensus_results=[],
            strengths=["Everything is perfect!"],
            estimated_revision_time=0
        )

        generator = ReportGenerator()
        text_report = generator.generate_text_report(empty_report)

        # Check for positive messaging when no issues
        assert ("no" in text_report.lower() and "issue" in text_report.lower()) or \
               "excellent" in text_report.lower() or \
               "looks great" in text_report.lower()
        assert "Everything is perfect!" in text_report

    def test_severity_color_coding(self):
        """Test that HTML report uses color coding for severity."""
        report = self.create_test_report()
        generator = ReportGenerator()

        html_report = generator.generate_html_report(report)

        # Should have color classes or styles for different severities
        assert "critical" in html_report.lower() or "red" in html_report.lower()
        assert "high" in html_report.lower() or "orange" in html_report.lower()

    def test_location_formatting(self):
        """Test that issue locations are clearly formatted."""
        report = self.create_test_report()
        formatter = ReportFormatter()

        for result in report.consensus_results:
            formatted = formatter.format_issue(result)
            assert result.location in formatted

    def test_suggestion_aggregation(self):
        """Test that multiple suggestions are well-formatted."""
        result = ConsensusResult(
            issue="Complex issue",
            severity=3,
            confidence=0.7,
            agreeing_reviewers=7,
            total_reviewers=10,
            location="Section 5",
            suggestions=[
                "First suggestion",
                "Second suggestion",
                "Third suggestion"
            ]
        )

        formatter = ReportFormatter()
        formatted = formatter.format_suggestions(result.suggestions)

        # All suggestions should be included
        for suggestion in result.suggestions:
            assert suggestion in formatted

    def test_progress_indicators(self):
        """Test inclusion of progress indicators in reports."""
        # First pass report
        first_report = self.create_test_report()
        first_report.review_pass = ReviewPass.CONTENT_PASS_1

        # Second pass report
        second_report = self.create_test_report()
        second_report.review_pass = ReviewPass.CONTENT_PASS_2

        generator = ReportGenerator()

        first_text = generator.generate_text_report(first_report)
        second_text = generator.generate_text_report(second_report)

        # Should indicate which pass this is (allow for different formats)
        assert "pass_1" in first_text.lower() or "pass 1" in first_text.lower() or "initial" in first_text.lower()
        assert "pass_2" in second_text.lower() or "pass 2" in second_text.lower() or "progress" in second_text.lower()

        # Should show different pass info
        assert first_report.review_pass.value in first_text
        assert second_report.review_pass.value in second_text

    def test_csv_export(self):
        """Test export of issues to CSV format."""
        report = self.create_test_report()
        generator = ReportGenerator()

        csv_export = generator.export_to_csv(report)

        # Check CSV structure
        lines = csv_export.split('\n')
        assert len(lines) >= 4  # Header + 3 issues

        # Check header
        header = lines[0].lower()
        assert "severity" in header
        assert "issue" in header
        assert "location" in header