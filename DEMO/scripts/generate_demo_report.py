"""
Generate comprehensive demo report showing the entire review workflow.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any


class DemoReportGenerator:
    """Generates comprehensive HTML and Markdown reports of the demo workflow."""

    def __init__(self):
        self.report_data = {
            "timestamp": datetime.now().isoformat(),
            "passes": [],
            "statistics": {},
            "final_metrics": {}
        }

    def add_pass_data(self, pass_number: int, data: Dict[str, Any]):
        """Add data from a specific pass."""
        self.report_data["passes"].append({
            "pass_number": pass_number,
            "data": data
        })

    def generate_html_report(self, output_path: str):
        """Generate an HTML report with styling."""
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Learnvia Review System Demo Report</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }

        h1 {
            margin: 0;
            font-size: 2.5em;
        }

        .subtitle {
            margin-top: 10px;
            opacity: 0.9;
            font-size: 1.2em;
        }

        .pass-container {
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .pass-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #eee;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }

        .pass-title {
            font-size: 1.8em;
            color: #667eea;
            font-weight: bold;
        }

        .pass-type {
            background: #f0f0f0;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .stat-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }

        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }

        .stat-label {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }

        .severity-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
            margin-right: 5px;
        }

        .severity-5 { background: #ff4444; color: white; }
        .severity-4 { background: #ff8800; color: white; }
        .severity-3 { background: #ffbb00; color: black; }
        .severity-2 { background: #88dd00; color: black; }
        .severity-1 { background: #00aa00; color: white; }

        .feedback-item {
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #ddd;
        }

        .feedback-critical { border-left-color: #ff4444; }
        .feedback-high { border-left-color: #ff8800; }
        .feedback-medium { border-left-color: #ffbb00; }
        .feedback-low { border-left-color: #88dd00; }
        .feedback-minor { border-left-color: #00aa00; }

        .agent-badge {
            background: #e3f2fd;
            color: #1976d2;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-right: 5px;
        }

        .generalist-badge {
            background: #f3e5f5;
            color: #7b1fa2;
        }

        .decision-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }

        .decision-box h3 {
            margin-top: 0;
        }

        .code-block {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }

        .progress-bar {
            width: 100%;
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin: 20px 0;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            transition: width 0.3s ease;
        }

        .workflow-diagram {
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin: 30px 0;
            text-align: center;
        }

        .workflow-step {
            display: inline-block;
            background: #f0f0f0;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 20px;
            position: relative;
        }

        .workflow-step.completed {
            background: #667eea;
            color: white;
        }

        .arrow {
            display: inline-block;
            margin: 0 10px;
            color: #999;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }

        th, td {
            text-align: left;
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }

        th {
            background: #f8f9fa;
            font-weight: bold;
        }

        .final-summary {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-top: 30px;
            text-align: center;
        }

        .metric-highlight {
            font-size: 3em;
            font-weight: bold;
            margin: 20px 0;
        }
    </style>
</head>
<body>
"""

        # Add header
        html += """
    <div class="header">
        <h1>Learnvia Review System Demo</h1>
        <div class="subtitle">Multi-Pass Hybrid Architecture Demonstration</div>
        <div style="margin-top: 20px; opacity: 0.8;">
            Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
        </div>
    </div>
"""

        # Add workflow diagram
        html += """
    <div class="workflow-diagram">
        <h2>Review Workflow Progress</h2>
        <div style="margin: 30px 0;">
"""

        workflow_steps = [
            ("Draft Submitted", True),
            ("Pass 1 Review", True),
            ("Author Revision", True),
            ("Pass 2 Review", True),
            ("Human Review", True),
            ("Pass 3 Copy Edit", True),
            ("Copy Editor Review", True),
            ("Pass 4 Final", True),
            ("Published", True)
        ]

        for i, (step_name, completed) in enumerate(workflow_steps):
            class_name = "completed" if completed else ""
            html += f'            <span class="workflow-step {class_name}">{step_name}</span>'
            if i < len(workflow_steps) - 1:
                html += '<span class="arrow">→</span>'

        html += """
        </div>
    </div>
"""

        # Add statistics summary
        if self.report_data.get("statistics"):
            html += self._generate_statistics_html()

        # Add passes
        for pass_data in self.report_data["passes"]:
            html += self._generate_pass_html(pass_data)

        # Add final summary
        html += self._generate_final_summary_html()

        # Close HTML
        html += """
</body>
</html>
"""

        with open(output_path, 'w') as f:
            f.write(html)

    def _generate_statistics_html(self) -> str:
        """Generate statistics section HTML."""
        stats = self.report_data["statistics"]
        html = '<div class="pass-container">\n'
        html += '    <h2>Overall Statistics</h2>\n'
        html += '    <div class="stats-grid">\n'

        stat_items = [
            ("Total Issues Found", stats.get("total_issues_found", 0)),
            ("Issues Fixed", stats.get("total_issues_fixed", 0)),
            ("Fix Rate", f"{stats.get('fix_rate', 0):.1f}%"),
            ("Passes Completed", len(self.report_data["passes"]))
        ]

        for label, value in stat_items:
            html += f"""
        <div class="stat-card">
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
        </div>
"""

        html += '    </div>\n'
        html += '</div>\n'
        return html

    def _generate_pass_html(self, pass_data: Dict) -> str:
        """Generate HTML for a single pass."""
        pass_num = pass_data["pass_number"]
        data = pass_data["data"]

        pass_types = {
            1: "Initial Review (30 Agents)",
            2: "Second Review (30 Agents)",
            3: "Copy Edit (8 Agents)",
            4: "Final Copy Edit (8 Agents)"
        }

        html = f'<div class="pass-container">\n'
        html += f'    <div class="pass-header">\n'
        html += f'        <div class="pass-title">Pass {pass_num}</div>\n'
        html += f'        <div class="pass-type">{pass_types.get(pass_num, "Review")}</div>\n'
        html += f'    </div>\n'

        # Add feedback summary if available
        if "feedback_summary" in data:
            html += self._generate_feedback_summary_html(data["feedback_summary"])

        # Add decision if available
        if "decision" in data:
            html += self._generate_decision_html(data["decision"])

        # Add sample feedback items
        if "sample_feedback" in data:
            html += self._generate_sample_feedback_html(data["sample_feedback"])

        html += '</div>\n'
        return html

    def _generate_feedback_summary_html(self, summary: Dict) -> str:
        """Generate feedback summary HTML."""
        html = '<div style="margin: 20px 0;">\n'
        html += '    <h3>Feedback Summary</h3>\n'

        # Severity breakdown
        html += '    <div style="margin: 15px 0;">\n'
        for sev in [5, 4, 3, 2, 1]:
            count = summary.get("by_severity", {}).get(sev, 0)
            if count > 0:
                html += f'        <span class="severity-badge severity-{sev}">Severity {sev}: {count}</span>\n'
        html += '    </div>\n'

        # Agent type breakdown
        if "rubric_vs_generalist" in summary:
            html += '    <table>\n'
            html += '        <tr><th>Agent Type</th><th>Issues Found</th></tr>\n'
            html += f'        <tr><td>Rubric-Focused Agents</td><td>{summary["rubric_vs_generalist"]["rubric_caught"]}</td></tr>\n'
            html += f'        <tr><td>Generalist Agents</td><td>{summary["rubric_vs_generalist"]["generalist_caught"]}</td></tr>\n'
            html += '    </table>\n'

        html += '</div>\n'
        return html

    def _generate_decision_html(self, decision: str) -> str:
        """Generate decision box HTML."""
        html = '<div class="decision-box">\n'
        html += '    <h3>Review Decision</h3>\n'
        html += f'    <div>{decision}</div>\n'
        html += '</div>\n'
        return html

    def _generate_sample_feedback_html(self, feedback_items: List) -> str:
        """Generate sample feedback HTML."""
        html = '<div style="margin: 20px 0;">\n'
        html += '    <h3>Sample Feedback</h3>\n'

        for item in feedback_items[:5]:  # Show first 5 items
            severity_class = f"feedback-{item['severity'].lower()}"
            agent_class = "generalist-badge" if "generalist" in item.get("agent_type", "") else "agent-badge"

            html += f'    <div class="feedback-item {severity_class}">\n'
            html += f'        <div><span class="{agent_class}">{item["agent_id"]}</span>'
            html += f'<strong>{item["issue"]}</strong></div>\n'
            html += f'        <div style="margin-top: 5px; color: #666;">Location: {item["location"]}</div>\n'
            html += f'        <div style="margin-top: 5px; font-style: italic;">Suggestion: {item["suggestion"]}</div>\n'
            html += '    </div>\n'

        html += '</div>\n'
        return html

    def _generate_final_summary_html(self) -> str:
        """Generate final summary HTML."""
        html = '<div class="final-summary">\n'
        html += '    <h2>Demo Complete!</h2>\n'
        html += '    <div class="metric-highlight">4 Passes</div>\n'
        html += '    <div>Successfully demonstrated the multi-pass hybrid review system</div>\n'
        html += '    <div style="margin-top: 20px;">\n'
        html += '        <strong>Key Achievements:</strong><br>\n'
        html += '        ✓ Rubric-focused agents caught specialized issues<br>\n'
        html += '        ✓ Generalist agents identified cross-cutting concerns<br>\n'
        html += '        ✓ Human reviewers provided critical oversight<br>\n'
        html += '        ✓ Multi-pass approach ensured quality improvement\n'
        html += '    </div>\n'
        html += '</div>\n'
        return html

    def generate_markdown_report(self, output_path: str):
        """Generate a Markdown report."""
        md = "# Learnvia Review System Demo Report\n\n"
        md += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        md += "## Workflow Overview\n\n"
        md += "```\n"
        md += "Draft → Pass 1 → Revision → Pass 2 → Human Review → Pass 3 → Copy Edit → Pass 4 → Final\n"
        md += "```\n\n"

        # Add statistics
        if self.report_data.get("statistics"):
            md += "## Overall Statistics\n\n"
            stats = self.report_data["statistics"]
            md += f"- **Total Issues Found**: {stats.get('total_issues_found', 0)}\n"
            md += f"- **Issues Fixed**: {stats.get('total_issues_fixed', 0)}\n"
            md += f"- **Fix Rate**: {stats.get('fix_rate', 0):.1f}%\n"
            md += f"- **Passes Completed**: {len(self.report_data['passes'])}\n\n"

        # Add passes
        for pass_data in self.report_data["passes"]:
            md += f"## Pass {pass_data['pass_number']}\n\n"
            data = pass_data["data"]

            if "feedback_summary" in data:
                md += "### Feedback Summary\n\n"
                summary = data["feedback_summary"]
                md += f"- Total issues: {summary.get('total_issues', 0)}\n"
                if "by_severity" in summary:
                    md += "- By severity:\n"
                    for sev, count in sorted(summary["by_severity"].items(), reverse=True):
                        md += f"  - Severity {sev}: {count}\n"
                md += "\n"

            if "decision" in data:
                md += f"### Decision\n\n{data['decision']}\n\n"

        # Add final thoughts
        md += "## Key Insights\n\n"
        md += "1. **Hybrid Architecture Value**: Rubric-focused agents caught specific violations while generalists identified holistic issues\n"
        md += "2. **Multi-Pass Benefits**: Each pass progressively improved quality, catching different issue types\n"
        md += "3. **Human Oversight**: Critical for pedagogical quality and nuanced decisions\n"
        md += "4. **Efficiency**: Automated agents handle bulk of review, humans focus on high-value decisions\n"

        with open(output_path, 'w') as f:
            f.write(md)


if __name__ == "__main__":
    # Test report generation
    generator = DemoReportGenerator()

    # Add sample data
    generator.report_data["statistics"] = {
        "total_issues_found": 47,
        "total_issues_fixed": 41,
        "fix_rate": 87.2
    }

    # Add sample pass
    generator.add_pass_data(1, {
        "feedback_summary": {
            "total_issues": 25,
            "by_severity": {5: 2, 4: 5, 3: 8, 2: 7, 1: 3},
            "rubric_vs_generalist": {"rubric_caught": 22, "generalist_caught": 3}
        },
        "decision": "REQUEST_REVISION - Multiple high-severity issues found"
    })

    # Generate reports
    generator.generate_html_report("../outputs/demo_report.html")
    generator.generate_markdown_report("../outputs/demo_report.md")