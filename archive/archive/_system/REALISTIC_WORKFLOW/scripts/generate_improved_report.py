#!/usr/bin/env python3
"""
Generate improved HTML report for Pass 1 review with all feedback incorporated
"""
import json
from pathlib import Path
from datetime import datetime


def generate_html_report(results_path: Path, output_path: Path):
    """Generate comprehensive HTML report from JSON results"""

    with open(results_path, 'r') as f:
        data = json.load(f)

    module = data['module']
    pass1 = data['pass1']
    consensus = data['consensus']

    # Get current timestamp for report generation
    report_timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    # Separate issues by type
    deferred_issues = [i for i in consensus['issues'] if i['issue_type'] in ['accessibility', 'animation', 'visual', 'figure']]
    active_issues = [i for i in consensus['issues'] if i['issue_type'] not in ['accessibility', 'animation', 'visual', 'figure']]

    # Sort active issues by priority (severity * confidence)
    active_issues.sort(key=lambda x: x['severity'] * x['confidence'], reverse=True)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pass 1 Review Report - {module['title']}</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']]
            }}
        }};
    </script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
        }}

        .header h1 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}

        .header .meta {{
            opacity: 0.9;
            font-size: 0.95em;
        }}

        .section {{
            padding: 40px;
            border-bottom: 1px solid #e0e0e0;
        }}

        .section:last-child {{
            border-bottom: none;
        }}

        .section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}

        .section h3 {{
            color: #764ba2;
            margin: 25px 0 15px 0;
            font-size: 1.3em;
        }}

        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}

        .metric-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}

        .metric-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}

        .metric-card .label {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}

        .content-preview {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #28a745;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            white-space: pre-wrap;
            word-wrap: break-word;
            max-height: 600px;
            overflow-y: scroll;
            overflow-x: auto;
        }}

        .info-box {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}

        .info-box.warning {{
            background: #fff3e0;
            border-left-color: #ff9800;
        }}

        .info-box.deferred {{
            background: #f3e5f5;
            border-left-color: #9c27b0;
        }}

        .issue-card {{
            background: #fff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}

        .issue-card.severity-5 {{ border-left: 5px solid #d32f2f; }}
        .issue-card.severity-4 {{ border-left: 5px solid #f57c00; }}
        .issue-card.severity-3 {{ border-left: 5px solid #fbc02d; }}
        .issue-card.severity-2 {{ border-left: 5px solid #0288d1; }}
        .issue-card.severity-1 {{ border-left: 5px solid #388e3c; }}

        .issue-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
        }}

        .issue-title {{
            flex: 1;
            font-size: 1.1em;
            font-weight: 600;
            color: #333;
        }}

        .badges {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .badge {{
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }}

        .badge.severity-5 {{ background: #ffebee; color: #d32f2f; }}
        .badge.severity-4 {{ background: #fff3e0; color: #f57c00; }}
        .badge.severity-3 {{ background: #fffde7; color: #f9a825; }}
        .badge.severity-2 {{ background: #e1f5fe; color: #0288d1; }}
        .badge.severity-1 {{ background: #e8f5e9; color: #388e3c; }}

        .badge.confidence {{
            background: #f3e5f5;
            color: #7b1fa2;
        }}

        .issue-location {{
            color: #666;
            font-size: 0.9em;
            margin: 10px 0;
            font-style: italic;
        }}

        .suggestions {{
            background: #f1f8e9;
            padding: 15px;
            border-radius: 6px;
            margin-top: 15px;
        }}

        .suggestions h4 {{
            color: #558b2f;
            margin-bottom: 10px;
            font-size: 1em;
        }}

        .suggestions ul {{
            margin-left: 20px;
        }}

        .suggestions li {{
            margin: 8px 0;
            color: #333;
        }}

        .explanation {{
            background: #fafafa;
            padding: 15px;
            border-radius: 6px;
            margin: 15px 0;
            font-size: 0.95em;
            line-height: 1.7;
        }}

        .competency-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}

        .competency-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            border-left: 3px solid #667eea;
        }}

        .competency-item strong {{
            color: #667eea;
        }}

        .footer {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #666;
            font-size: 0.9em;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}

        th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
        }}

        tr:hover {{
            background: #f8f9fa;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>Pass 1 Content Review Report</h1>
            <div class="meta">
                <strong>Module:</strong> {module['title']}<br>
                <strong>Module ID:</strong> {module['module_id']}<br>
                <strong>Review Date:</strong> {data['timestamp'][:10]}<br>
                <strong>Format:</strong> {module['format']}
            </div>
        </div>

        <!-- Section 1: Overview -->
        <div class="section">
            <h2>1. Overview</h2>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="value">{pass1['total_agents']}</div>
                    <div class="label">Total Reviewers</div>
                </div>
                <div class="metric-card">
                    <div class="value">{pass1['total_findings']}</div>
                    <div class="label">Individual Findings</div>
                </div>
                <div class="metric-card">
                    <div class="value">{consensus['total_issues']}</div>
                    <div class="label">Consensus Issues</div>
                </div>
                <div class="metric-card">
                    <div class="value">{consensus['noise_reduction_pct']:.1f}%</div>
                    <div class="label">Noise Reduction</div>
                </div>
            </div>

            <h3>Full Module Content (XML)</h3>
            <div class="content-preview">{module.get('preview', 'Content preview not available').replace('<', '&lt;').replace('>', '&gt;')}</div>

            <div class="info-box deferred">
                <strong>Deferred for Later Review:</strong> Visual elements (figures, animations, graphics) and accessibility features will be reviewed in a separate pass. These are important but require specialized review processes.
            </div>
        </div>

        <!-- Section 2: Review Process -->
        <div class="section">
            <h2>2. Review Process</h2>

            <h3>Hybrid Multi-Agent Approach</h3>
            <div class="explanation">
                <p><strong>Why Multiple Agents?</strong> A single reviewer has biases and blind spots. By using 30 independent AI agents, we achieve more comprehensive coverage and reduce individual reviewer bias.</p>

                <p><strong>Why Hybrid?</strong> Our system uses two complementary approaches:</p>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li><strong>Rubric-Focused Agents (60%):</strong> Specialists trained on specific competency rubrics (e.g., Pedagogical Flow, Conceptual Clarity). These agents dive deep into their domain.</li>
                    <li><strong>Generalist Agents (40%):</strong> Holistic reviewers evaluating overall quality across all dimensions. These catch issues that fall between specialist domains.</li>
                </ul>

                <p style="margin-top: 10px;"><strong>Agent Distribution for This Review:</strong></p>
                <ul style="margin-left: 20px;">
                    <li><strong>{pass1['authoring_agents']} Authoring Agents</strong> (pedagogical quality, content structure, learning effectiveness)</li>
                    <li><strong>{pass1['style_agents']} Style Agents</strong> (writing mechanics, formatting, style guide compliance)</li>
                </ul>

                <p style="margin-top: 15px;"><strong>Important: Agents vs Competencies</strong></p>
                <p>We have <strong>10 total competencies</strong> (5 authoring + 5 style), but <strong>30 agents</strong> reviewing this module. This is intentional:</p>
                <ul style="margin-left: 20px; margin-top: 5px;">
                    <li><strong>Rubric-focused agents</strong> each specialize in ONE competency and review deeply</li>
                    <li><strong>Generalist agents</strong> each review ALL competencies holistically</li>
                    <li>Multiple agents per competency provide redundancy and catch more issues</li>
                    <li>Example: 3-4 different agents might all review "Pedagogical Flow" from slightly different angles</li>
                </ul>
            </div>

            <h3>Consensus Aggregation</h3>
            <div class="explanation">
                <p><strong>From {pass1['total_findings']} Individual Findings to {consensus['total_issues']} Consensus Issues</strong></p>

                <p>After all agents complete their reviews, we aggregate similar findings through a multi-step process:</p>

                <ol style="margin-left: 20px; margin-top: 10px; line-height: 1.8;">
                    <li><strong>Deduplication:</strong> Similar issues reported by multiple agents are grouped together (e.g., 5 agents all flag "missing learning objectives" → 1 consensus issue)</li>

                    <li><strong>Confidence Scoring:</strong> The more agents that agree on the same issue, the higher the <strong>confidence score</strong>. This indicates how certain we are that this is a real issue.
                        <ul style="margin-left: 20px; margin-top: 5px;">
                            <li>High confidence (≥70%): Many agents independently found this issue</li>
                            <li>Moderate confidence (40-70%): Several agents found this issue</li>
                            <li>Low confidence (&lt;40%): Few agents found this issue</li>
                        </ul>
                    </li>

                    <li><strong>Severity Rating (1-5):</strong> Separate from confidence, severity indicates <strong>impact on learning</strong>:
                        <ul style="margin-left: 20px; margin-top: 5px;">
                            <li><strong>5 (Critical):</strong> Incorrect content, missing essential components, blocks student learning</li>
                            <li><strong>4 (High):</strong> Core pedagogy issues, significant gaps in explanation</li>
                            <li><strong>3 (Medium):</strong> Writing quality issues, moderate clarity problems</li>
                            <li><strong>2 (Low):</strong> Style compliance, minor formatting issues</li>
                            <li><strong>1 (Minor):</strong> Polish suggestions, stylistic preferences</li>
                        </ul>
                    </li>
                </ol>

                <p style="margin-top: 15px;"><strong>Result:</strong> High confidence + high severity = prioritize. Low confidence or low severity = still flagged but lower priority.</p>
            </div>
        </div>

        <!-- Section 3: Competency Framework -->
        <div class="section">
            <h2>3. Competency Framework</h2>

            <div class="explanation">
                <p><strong>Where These Competencies Come From:</strong></p>
                <p>These 10 competencies were derived from Learnvia's authoring and style guides, refined through iterative testing with real modules, and validated against pedagogical research. They represent the dimensions most critical to student success in online, self-paced learning.</p>
            </div>

            <h3>Authoring Competencies (Pedagogical Quality)</h3>
            <div class="competency-grid">
                <div class="competency-item">
                    <strong>Structural Integrity:</strong> Proper organization, complete sections, logical flow
                </div>
                <div class="competency-item">
                    <strong>Pedagogical Flow:</strong> Scaffolding, prerequisites, concept sequencing
                </div>
                <div class="competency-item">
                    <strong>Conceptual Clarity:</strong> Clear definitions, examples, explanations
                </div>
                <div class="competency-item">
                    <strong>Assessment Quality:</strong> Practice problems aligned with content
                </div>
                <div class="competency-item">
                    <strong>Student Engagement:</strong> Motivating, relevant, appropriate difficulty
                </div>
            </div>

            <h3>Style Competencies (Writing & Presentation)</h3>
            <div class="competency-grid">
                <div class="competency-item">
                    <strong>Mechanical Compliance:</strong> Grammar, punctuation, sentence structure
                </div>
                <div class="competency-item">
                    <strong>Mathematical Formatting:</strong> Correct notation, LaTeX rendering
                </div>
                <div class="competency-item">
                    <strong>Punctuation & Grammar:</strong> Professional writing standards
                </div>
                <div class="competency-item">
                    <strong>Accessibility:</strong> Clear language, alt text (deferred for now)
                </div>
                <div class="competency-item">
                    <strong>Consistency:</strong> Terminology, formatting, style throughout
                </div>
            </div>

            <div class="info-box">
                <strong>Note on Severity Ratings:</strong> All competencies use the same 1-5 severity scale based on impact to student learning. Style issues can be severity 5 if they block comprehension (e.g., broken math rendering). Pedagogical issues can be severity 1 if they're minor polish suggestions.
            </div>
        </div>

        <!-- Section 4: All Issues Identified -->
        <div class="section">
            <h2>4. All Issues Identified</h2>

            <div class="explanation">
                <p><strong>What You're Seeing:</strong> All {len(active_issues)} consensus issues are listed below, sorted by priority (severity × confidence). Even low-severity or low-confidence issues are included because they may indicate real concerns.</p>

                <p><strong>Your Task:</strong> Review each issue and mark your decision:</p>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li><strong>Accept & Fix:</strong> This is a real issue that needs addressing</li>
                    <li><strong>False Positive:</strong> The review system misunderstood; this is not actually an issue</li>
                    <li><strong>Already Addressed:</strong> This was fixed in a version the system didn't see</li>
                </ul>

                <p style="margin-top: 10px;"><strong>All issues must be addressed before publication</strong> (even if your decision is "false positive").</p>
            </div>
"""

    # Add all active issues
    for idx, issue in enumerate(active_issues, 1):
        severity = issue['severity']
        confidence = issue['confidence']
        priority_score = severity * confidence

        suggestions_html = ""
        if issue['suggestions']:
            suggestions_html = """
                <div class="suggestions">
                    <h4>Suggested Actions:</h4>
                    <ul>
"""
            for suggestion in issue['suggestions']:
                suggestions_html += f"                        <li>{suggestion}</li>\n"
            suggestions_html += """                    </ul>
                </div>
"""
        elif severity >= 3:  # Provide generic guidance for medium+ severity even without specific suggestions
            suggestions_html = """
                <div class="suggestions">
                    <h4>Suggested Actions:</h4>
                    <ul>
                        <li>Review the content at the specified location</li>
                        <li>Consider how this issue impacts student comprehension</li>
                        <li>Consult the relevant rubric for specific guidance</li>
                    </ul>
                </div>
"""

        severity_label = {5: "Critical", 4: "High", 3: "Medium", 2: "Low", 1: "Minor"}[severity]

        html += f"""
            <div class="issue-card severity-{severity}">
                <div class="issue-header">
                    <div class="issue-title">Issue #{idx}: {issue['issue']}</div>
                    <div class="badges">
                        <span class="badge severity-{severity}">Severity: {severity} ({severity_label})</span>
                        <span class="badge confidence">Confidence: {confidence:.0%}</span>
                    </div>
                </div>

                <div class="issue-location">
                    <strong>Location:</strong> {issue['location']}<br>
                    <strong>Type:</strong> {issue['issue_type']}<br>
                    <strong>Agreement:</strong> {issue['agreeing_reviewers']}/{pass1['total_agents']} reviewers identified this issue<br>
                    <strong>Priority Score:</strong> {priority_score:.2f}
                </div>

                {suggestions_html}
            </div>
"""

    # Add deferred issues if any
    if deferred_issues:
        html += f"""
            <h3 style="margin-top: 40px;">Deferred Issues (Visual & Accessibility)</h3>
            <div class="info-box deferred">
                <strong>These {len(deferred_issues)} issue(s) relate to visual elements or accessibility features.</strong> They will be addressed in a separate review pass with specialized tools and processes. For now, they are documented but not requiring immediate action.
            </div>
"""
        for idx, issue in enumerate(deferred_issues, len(active_issues) + 1):
            html += f"""
            <div class="issue-card severity-{issue['severity']}" style="opacity: 0.7;">
                <div class="issue-header">
                    <div class="issue-title">Issue #{idx} (DEFERRED): {issue['issue']}</div>
                    <div class="badges">
                        <span class="badge severity-{issue['severity']}">Severity: {issue['severity']}</span>
                        <span style="background: #9c27b0; color: white;" class="badge">DEFERRED</span>
                    </div>
                </div>
                <div class="issue-location">
                    <strong>Location:</strong> {issue['location']}<br>
                    <strong>Type:</strong> {issue['issue_type']}
                </div>
            </div>
"""

    html += """
        </div>

        <!-- Section 5: Patterns & Insights -->
        <div class="section">
            <h2>5. Patterns & Systemic Observations</h2>

            <div class="explanation">
                <p><strong>Purpose:</strong> This section identifies <strong>patterns</strong> across multiple issues that suggest systemic opportunities for improvement. These aren't additional errors to fix, but rather themes to be aware of as you revise.</p>

                <p><strong>Focus Areas:</strong> When patterns emerge in particular competencies, it may indicate areas where additional attention during revision would be beneficial.</p>
            </div>
"""

    # Group issues by competency to identify patterns
    competency_groups = {}
    for issue in active_issues:
        comp = issue.get('issue_type', 'general')
        if comp not in competency_groups:
            competency_groups[comp] = []
        competency_groups[comp].append(issue)

    if competency_groups:
        html += """
            <h3>Issue Distribution by Competency</h3>
            <table>
                <tr>
                    <th>Competency</th>
                    <th>Issues Found</th>
                    <th>Avg Severity</th>
                    <th>Avg Confidence</th>
                </tr>
"""
        for comp, issues in sorted(competency_groups.items(), key=lambda x: len(x[1]), reverse=True):
            avg_sev = sum(i['severity'] for i in issues) / len(issues)
            avg_conf = sum(i['confidence'] for i in issues) / len(issues)
            html += f"""
                <tr>
                    <td><strong>{comp.replace('_', ' ').title()}</strong></td>
                    <td>{len(issues)}</td>
                    <td>{avg_sev:.1f}</td>
                    <td>{avg_conf:.0%}</td>
                </tr>
"""
        html += """
            </table>
"""

    html += """
            <div class="info-box">
                <strong>Interpreting This Data:</strong> Higher concentrations of issues in specific competencies suggest areas where the module might benefit from focused attention during revision. This is about strengthening the module, not about deficiency.
            </div>
        </div>

        <!-- Section 6: Next Steps -->
        <div class="section">
            <h2>6. Next Steps</h2>

            <div class="explanation">
                <h3>Review & Decision Phase</h3>
                <ol style="margin-left: 20px; line-height: 1.8;">
                    <li><strong>Review Each Issue:</strong> Go through all issues listed in Section 4</li>
                    <li><strong>Make Decisions:</strong> For each issue, mark as:
                        <ul style="margin-left: 20px; margin-top: 5px;">
                            <li>Accept & Fix</li>
                            <li>False Positive (explain why)</li>
                            <li>Already Addressed</li>
                        </ul>
                    </li>
                    <li><strong>Prioritize:</strong> Start with highest priority scores, but all issues must be addressed</li>
                </ol>

                <h3 style="margin-top: 25px;">Revision Phase</h3>
                <ol style="margin-left: 20px; line-height: 1.8;">
                    <li><strong>Address Accepted Issues:</strong> Make necessary changes to the module</li>
                    <li><strong>Document False Positives:</strong> Help improve future reviews by noting where the system misunderstood</li>
                    <li><strong>Request Re-Review:</strong> After revisions, the module can go through Pass 2 for validation</li>
                </ol>

                <div class="info-box warning" style="margin-top: 20px;">
                    <strong>Important:</strong> All issues must be addressed before publication. This doesn't mean all must be "fixed" – you can mark false positives – but each requires a conscious decision and documentation.
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>Generated on """ + report_timestamp + """</p>
            <p style="margin-top: 10px;">Learnvia AI-Powered Content Review System | Pass 1: Content Review</p>
        </div>
    </div>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ HTML report generated: {output_path}")
    print(f"  Active issues: {len(active_issues)}")
    print(f"  Deferred issues: {len(deferred_issues)}")


if __name__ == "__main__":
    results_path = Path(__file__).parent.parent / "outputs" / "pass1_module35_results.json"
    output_path = Path(__file__).parent.parent / "outputs" / "PASS1_MODULE35_REPORT.html"

    generate_html_report(results_path, output_path)
