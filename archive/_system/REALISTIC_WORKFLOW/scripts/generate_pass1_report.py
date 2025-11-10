#!/usr/bin/env python3
"""
Generate beautiful HTML report for Pass 1 content review results
Creates a comprehensive, professional report with clear sections and visualizations
"""

import json
from pathlib import Path
from datetime import datetime


def generate_html_report(json_path: str = None) -> str:
    """Generate HTML report from Pass 1 results"""

    # Load results
    if json_path is None:
        json_path = Path(__file__).parent.parent / "outputs" / "pass1_real_module_results.json"
    else:
        json_path = Path(json_path)

    with open(json_path, 'r') as f:
        data = json.load(f)

    # Extract data
    module_info = data['module']
    pass1_info = data['pass1']
    consensus = data['consensus']
    competency_breakdown = data['competency_breakdown']

    # Generate HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pass 1 Content Review Report - {module_info['title']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        .header .subtitle {{
            font-size: 1.2rem;
            opacity: 0.95;
        }}

        .nav-tabs {{
            display: flex;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
            padding: 0 40px;
            overflow-x: auto;
        }}

        .nav-tab {{
            padding: 15px 25px;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 14px;
            font-weight: 500;
            color: #6c757d;
            white-space: nowrap;
            transition: all 0.3s ease;
            border-bottom: 3px solid transparent;
            margin-bottom: -2px;
        }}

        .nav-tab:hover {{
            color: #667eea;
        }}

        .nav-tab.active {{
            color: #667eea;
            border-bottom-color: #667eea;
        }}

        .content {{
            padding: 40px;
        }}

        .section {{
            display: none;
            animation: fadeIn 0.5s ease;
        }}

        .section.active {{
            display: block;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .section-header {{
            font-size: 1.8rem;
            color: #2c3e50;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e9ecef;
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .icon {{
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 20px;
        }}

        .metric-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .metric-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            border: 1px solid #e9ecef;
            transition: all 0.3s ease;
        }}

        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }}

        .metric-label {{
            font-size: 0.9rem;
            color: #6c757d;
            margin-bottom: 8px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .metric-value {{
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .metric-change {{
            font-size: 0.85rem;
            color: #28a745;
            margin-top: 5px;
        }}

        .funnel-diagram {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            margin: 30px 0;
        }}

        .funnel-stage {{
            margin: 20px auto;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            position: relative;
            transition: all 0.3s ease;
        }}

        .funnel-stage:hover {{
            transform: scale(1.02);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        }}

        .funnel-stage.stage-1 {{ width: 90%; background: #fff3cd; }}
        .funnel-stage.stage-2 {{ width: 70%; background: #d1ecf1; }}
        .funnel-stage.stage-3 {{ width: 50%; background: #d4edda; }}
        .funnel-stage.stage-4 {{ width: 35%; background: #cce5ff; }}

        .funnel-arrow {{
            font-size: 2rem;
            color: #667eea;
            margin: 10px 0;
        }}

        .agent-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 30px 0;
        }}

        .agent-card {{
            background: white;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #e9ecef;
            text-align: center;
            transition: all 0.3s ease;
        }}

        .agent-card:hover {{
            border-color: #667eea;
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }}

        .agent-card.authoring {{
            border-left: 4px solid #28a745;
        }}

        .agent-card.style {{
            border-left: 4px solid #17a2b8;
        }}

        .agent-type {{
            font-size: 0.75rem;
            color: #6c757d;
            text-transform: uppercase;
            margin-bottom: 5px;
            font-weight: 600;
        }}

        .agent-id {{
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 5px;
        }}

        .agent-findings {{
            font-size: 1.2rem;
            font-weight: 700;
            color: #667eea;
        }}

        .priority-matrix {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 30px 0;
        }}

        .priority-item {{
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-weight: 600;
            transition: all 0.3s ease;
        }}

        .priority-item:hover {{
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}

        .priority-critical {{
            background: linear-gradient(135deg, #d32f2f, #c62828);
        }}

        .priority-high {{
            background: linear-gradient(135deg, #f57c00, #ef6c00);
        }}

        .priority-medium {{
            background: linear-gradient(135deg, #fbc02d, #f9a825);
        }}

        .priority-low {{
            background: linear-gradient(135deg, #29b6f6, #039be5);
        }}

        .priority-stylistic {{
            background: linear-gradient(135deg, #9e9e9e, #757575);
        }}

        .priority-count {{
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}

        .priority-label {{
            font-size: 0.9rem;
            opacity: 0.95;
        }}

        .competency-chart {{
            margin: 30px 0;
        }}

        .competency-bar {{
            margin-bottom: 20px;
        }}

        .competency-label {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-weight: 500;
        }}

        .competency-progress {{
            height: 30px;
            background: #f0f0f0;
            border-radius: 15px;
            overflow: hidden;
            position: relative;
        }}

        .competency-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            color: white;
            font-weight: 600;
            font-size: 0.85rem;
            transition: width 1s ease;
            animation: fillBar 1.5s ease;
        }}

        @keyframes fillBar {{
            from {{ width: 0; }}
        }}

        .issues-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 30px 0;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
        }}

        .issues-table thead {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }}

        .issues-table th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .issues-table tbody tr {{
            background: white;
            transition: all 0.3s ease;
        }}

        .issues-table tbody tr:hover {{
            background: #f8f9fa;
            transform: scale(1.01);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }}

        .issues-table tbody tr:nth-child(even) {{
            background: #fafbfc;
        }}

        .issues-table td {{
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
        }}

        .severity-badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
        }}

        .severity-5 {{ background: #ffebee; color: #c62828; }}
        .severity-4 {{ background: #fff3e0; color: #e65100; }}
        .severity-3 {{ background: #fffde7; color: #f57f17; }}
        .severity-2 {{ background: #e3f2fd; color: #1565c0; }}
        .severity-1 {{ background: #f5f5f5; color: #616161; }}

        .confidence-meter {{
            width: 100px;
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
        }}

        .confidence-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.5s ease;
        }}

        .sample-issue {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }}

        .sample-issue:hover {{
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transform: translateY(-3px);
        }}

        .sample-issue-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }}

        .sample-issue-title {{
            font-size: 1.2rem;
            font-weight: 600;
            color: #2c3e50;
        }}

        .sample-issue-content {{
            margin: 15px 0;
        }}

        .sample-issue-field {{
            margin-bottom: 15px;
        }}

        .field-label {{
            font-weight: 600;
            color: #667eea;
            margin-bottom: 5px;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .field-value {{
            color: #495057;
            line-height: 1.8;
        }}

        .solution-box {{
            background: #f0f8ff;
            border-left: 4px solid #667eea;
            padding: 15px 20px;
            border-radius: 5px;
            margin-top: 15px;
        }}

        .collapsible {{
            background: #f8f9fa;
            border-radius: 10px;
            margin: 20px 0;
            overflow: hidden;
            border: 1px solid #e9ecef;
        }}

        .collapsible-header {{
            padding: 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.3s ease;
        }}

        .collapsible-header:hover {{
            background: #e9ecef;
        }}

        .collapsible-content {{
            padding: 0 20px;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.5s ease, padding 0.5s ease;
        }}

        .collapsible.active .collapsible-content {{
            max-height: 2000px;
            padding: 20px;
        }}

        .collapsible-arrow {{
            transition: transform 0.3s ease;
            font-size: 1.2rem;
            color: #667eea;
        }}

        .collapsible.active .collapsible-arrow {{
            transform: rotate(180deg);
        }}

        .next-steps {{
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
        }}

        .step-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }}

        .step-card:hover {{
            transform: translateX(10px);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        }}

        .step-number {{
            display: inline-block;
            width: 30px;
            height: 30px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-align: center;
            line-height: 30px;
            border-radius: 50%;
            margin-right: 15px;
            font-weight: 600;
        }}

        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 30px;
            margin-top: 50px;
        }}

        .footer-text {{
            opacity: 0.9;
            font-size: 0.9rem;
        }}

        .search-filter {{
            margin-bottom: 20px;
            padding: 12px 20px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 1rem;
            width: 100%;
            transition: border-color 0.3s ease;
        }}

        .search-filter:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8rem;
            }}

            .metric-cards {{
                grid-template-columns: 1fr;
            }}

            .agent-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}

            .priority-matrix {{
                grid-template-columns: 1fr;
            }}
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}

            .container {{
                box-shadow: none;
                border-radius: 0;
            }}

            .nav-tabs {{
                display: none;
            }}

            .section {{
                display: block !important;
                page-break-before: always;
            }}

            .collapsible-content {{
                max-height: none !important;
                padding: 20px !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Pass 1 Content Review Report</h1>
            <div class="subtitle">{module_info['title']}</div>
        </div>

        <div class="nav-tabs">
            <button class="nav-tab active" onclick="showSection('overview')">Overview</button>
            <button class="nav-tab" onclick="showSection('process')">Review Process</button>
            <button class="nav-tab" onclick="showSection('aggregation')">Consensus</button>
            <button class="nav-tab" onclick="showSection('priority')">Priority Matrix</button>
            <button class="nav-tab" onclick="showSection('competency')">Competencies</button>
            <button class="nav-tab" onclick="showSection('issues')">Detailed Issues</button>
            <button class="nav-tab" onclick="showSection('samples')">Sample Issues</button>
            <button class="nav-tab" onclick="showSection('deep-dive')">Deep Dive</button>
            <button class="nav-tab" onclick="showSection('next-steps')">Next Steps</button>
        </div>

        <div class="content">
            <!-- Section 1: Module Overview -->
            <section id="overview" class="section active">
                <h2 class="section-header">
                    <div class="icon">📚</div>
                    Module Overview
                </h2>

                <div class="metric-cards">
                    <div class="metric-card">
                        <div class="metric-label">Word Count</div>
                        <div class="metric-value">{module_info['word_count']:,}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Line Count</div>
                        <div class="metric-value">{module_info['line_count']:,}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Review Time</div>
                        <div class="metric-value">{data['execution_time']:.1f}s</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Consensus Issues</div>
                        <div class="metric-value">{consensus['metrics']['consensus_count']}</div>
                    </div>
                </div>

                <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 30px 0;">
                    <h3 style="margin-bottom: 15px; color: #667eea;">Content Preview</h3>
                    <p style="line-height: 1.8; color: #495057;">{module_info['preview']}</p>
                </div>

                <div style="background: #e7f3ff; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;">
                    <strong>Scope Note:</strong> This review covers authoring quality and style compliance. Animation scripting and technical specifications are evaluated through separate specialized processes.
                </div>
            </section>

            <!-- Section 2: Review Process -->
            <section id="process" class="section">
                <h2 class="section-header">
                    <div class="icon">🤖</div>
                    Review Process
                </h2>

                <div style="text-align: center; margin-bottom: 30px;">
                    <h3 style="color: #667eea; margin-bottom: 10px;">Hybrid Agent Approach</h3>
                    <p style="color: #6c757d;">30 specialized AI agents analyze content from multiple perspectives</p>
                </div>

                <div class="agent-grid">
"""

    # Add agent cards
    for agent in pass1_info['agents']:
        agent_class = "authoring" if agent['role'] == "authoring" else "style"
        html_content += f"""
                    <div class="agent-card {agent_class}">
                        <div class="agent-type">{agent['type']}</div>
                        <div class="agent-id">{agent['agent_id']}</div>
                        <div class="agent-findings">{agent['findings']}</div>
                        <small style="color: #6c757d;">findings</small>
                    </div>
"""

    html_content += """
                </div>

                <div style="margin-top: 40px;">
                    <h3 style="margin-bottom: 20px;">Agent Distribution</h3>
                    <div class="metric-cards">
                        <div class="metric-card">
                            <div class="metric-label">Rubric-Focused Authoring</div>
                            <div class="metric-value">9</div>
                            <div class="metric-change">Competency specialists</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Generalist Authoring</div>
                            <div class="metric-value">6</div>
                            <div class="metric-change">Holistic reviewers</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Rubric-Focused Style</div>
                            <div class="metric-value">9</div>
                            <div class="metric-change">Format specialists</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Generalist Style</div>
                            <div class="metric-value">6</div>
                            <div class="metric-change">Overall consistency</div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Section 3: Consensus Aggregation -->
            <section id="aggregation" class="section">
                <h2 class="section-header">
                    <div class="icon">🔄</div>
                    Consensus Aggregation
                </h2>

                <div class="funnel-diagram">
                    <div class="funnel-stage stage-1">
                        <strong style="font-size: 1.5rem;">{consensus['metrics']['total_findings']}+ Individual Findings</strong>
                        <br>Raw agent outputs
                    </div>
                    <div class="funnel-arrow">⬇</div>
                    <div class="funnel-stage stage-2">
                        <strong>Deduplication & Grouping</strong>
                        <br>Similar issues merged
                    </div>
                    <div class="funnel-arrow">⬇</div>
                    <div class="funnel-stage stage-3">
                        <strong>Confidence Scoring</strong>
                        <br>Multi-agent validation
                    </div>
                    <div class="funnel-arrow">⬇</div>
                    <div class="funnel-stage stage-4">
                        <strong style="font-size: 1.5rem;">{consensus['metrics']['consensus_count']} Consensus Issues</strong>
                        <br>High-confidence findings
                    </div>
                </div>

                <div class="metric-cards">
                    <div class="metric-card">
                        <div class="metric-label">Total Findings</div>
                        <div class="metric-value">{consensus['metrics']['total_findings']}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Consensus Issues</div>
                        <div class="metric-value">{consensus['metrics']['consensus_count']}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Noise Reduction</div>
                        <div class="metric-value">{consensus['metrics']['noise_reduction']:.1f}%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Avg Confidence</div>
                        <div class="metric-value">{consensus['metrics']['average_confidence']:.0f}%</div>
                    </div>
                </div>
            </section>

            <!-- Section 4: Priority Matrix -->
            <section id="priority" class="section">
                <h2 class="section-header">
                    <div class="icon">⚠️</div>
                    Issues by Priority
                </h2>

                <div class="priority-matrix">
"""

    # Add priority items
    severity_labels = {
        5: ("Critical", "priority-critical"),
        4: ("High", "priority-high"),
        3: ("Medium", "priority-medium"),
        2: ("Low", "priority-low"),
        1: ("Stylistic", "priority-stylistic")
    }

    for severity in range(5, 0, -1):
        count = consensus['severity_breakdown'].get(str(severity), 0)
        label, css_class = severity_labels[severity]
        html_content += f"""
                    <div class="priority-item {css_class}">
                        <div class="priority-count">{count}</div>
                        <div class="priority-label">{label} (Severity {severity})</div>
                    </div>
"""

    html_content += """
                </div>

                <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                    <h4>Priority Guidelines</h4>
                    <p style="margin-top: 10px;">• <strong>Critical & High:</strong> Must be addressed before publication</p>
                    <p>• <strong>Medium:</strong> Should be addressed to improve quality</p>
                    <p>• <strong>Low & Stylistic:</strong> Nice to fix for polish</p>
                </div>
            </section>

            <!-- Section 5: Competency Breakdown -->
            <section id="competency" class="section">
                <h2 class="section-header">
                    <div class="icon">📊</div>
                    Issues by Competency
                </h2>

                <div class="competency-chart">
"""

    # Add competency bars
    max_issues = max(competency_breakdown.values()) if competency_breakdown.values() else 1
    for comp_name, count in sorted(competency_breakdown.items(), key=lambda x: x[1], reverse=True):
        width_pct = (count / max_issues * 100) if max_issues > 0 else 0
        html_content += f"""
                    <div class="competency-bar">
                        <div class="competency-label">
                            <span>{comp_name}</span>
                            <span>{count} issues</span>
                        </div>
                        <div class="competency-progress">
                            <div class="competency-fill" style="width: {width_pct}%;">
                                {count}
                            </div>
                        </div>
                    </div>
"""

    html_content += """
                </div>

                <div style="margin-top: 30px;">
                    <h3>Competency Categories</h3>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 20px;">
                        <div style="background: #f0f8ff; padding: 20px; border-radius: 10px;">
                            <h4 style="color: #28a745; margin-bottom: 10px;">Authoring Competencies</h4>
                            <ul style="list-style: none; padding: 0;">
                                <li>• Structural Integrity</li>
                                <li>• Pedagogical Flow</li>
                                <li>• Conceptual Clarity</li>
                                <li>• Assessment Quality</li>
                                <li>• Student Engagement</li>
                            </ul>
                        </div>
                        <div style="background: #f0ffff; padding: 20px; border-radius: 10px;">
                            <h4 style="color: #17a2b8; margin-bottom: 10px;">Style Competencies</h4>
                            <ul style="list-style: none; padding: 0;">
                                <li>• Mechanical Compliance</li>
                                <li>• Mathematical Formatting</li>
                                <li>• Punctuation & Grammar</li>
                                <li>• Accessibility</li>
                                <li>• Consistency</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Section 6: Detailed Issues Table -->
            <section id="issues" class="section">
                <h2 class="section-header">
                    <div class="icon">📋</div>
                    Detailed Issues
                </h2>

                <input type="text" class="search-filter" placeholder="Search issues..." onkeyup="filterTable(this.value)">

                <table class="issues-table" id="issuesTable">
                    <thead>
                        <tr>
                            <th>Severity</th>
                            <th>Issue</th>
                            <th>Location</th>
                            <th>Confidence</th>
                            <th>Solution</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    # Add issue rows (limit to first 20 for brevity)
    for i, issue in enumerate(consensus['consensus_issues'][:20]):
        severity = issue.get('severity', 1)
        confidence = issue.get('confidence', 0) * 100  # Convert to percentage

        # Get solution from suggestions list
        suggestions = issue.get('suggestions', [])
        solution = suggestions[0] if suggestions else issue.get('solution', '')

        # Only show solution for high severity and high confidence
        if not solution or severity < 4 or confidence < 70:
            solution = "Further review required"

        html_content += f"""
                        <tr>
                            <td><span class="severity-badge severity-{severity}">Severity {severity}</span></td>
                            <td>{issue.get('issue', 'Unknown issue')}</td>
                            <td>{issue.get('location', 'Unknown')}</td>
                            <td>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <div class="confidence-meter">
                                        <div class="confidence-fill" style="width: {confidence}%;"></div>
                                    </div>
                                    <span>{confidence:.0f}%</span>
                                </div>
                            </td>
                            <td>{solution[:100]}...</td>
                        </tr>
"""

    html_content += """
                    </tbody>
                </table>
            </section>

            <!-- Section 7: Sample Issues -->
            <section id="samples" class="section">
                <h2 class="section-header">
                    <div class="icon">🔍</div>
                    Top Priority Issues
                </h2>
"""

    # Add top 5 issues
    top_issues = sorted(consensus['consensus_issues'],
                       key=lambda x: (x.get('severity', 0), x.get('confidence', 0)),
                       reverse=True)[:5]

    for i, issue in enumerate(top_issues, 1):
        html_content += f"""
                <div class="sample-issue">
                    <div class="sample-issue-header">
                        <div class="sample-issue-title">Issue #{i}</div>
                        <span class="severity-badge severity-{issue.get('severity', 1)}">
                            Severity {issue.get('severity', 1)}
                        </span>
                    </div>

                    <div class="sample-issue-content">
                        <div class="sample-issue-field">
                            <div class="field-label">Description</div>
                            <div class="field-value">{issue.get('issue', 'Unknown issue')}</div>
                        </div>

                        <div class="sample-issue-field">
                            <div class="field-label">Location</div>
                            <div class="field-value">{issue.get('location', 'Unknown location')}</div>
                        </div>

                        <div class="sample-issue-field">
                            <div class="field-label">Confidence Score</div>
                            <div class="field-value">{issue.get('confidence', 0) * 100:.0f}%</div>
                        </div>

                        <div class="solution-box">
                            <div class="field-label">Recommended Solution</div>
                            <div class="field-value">{issue.get('suggestions', ['Review needed'])[0] if issue.get('suggestions') else 'Review needed'}</div>
                        </div>
                    </div>
                </div>
"""

    html_content += """
            </section>

            <!-- Section 8: Competency Deep Dive -->
            <section id="deep-dive" class="section">
                <h2 class="section-header">
                    <div class="icon">🎯</div>
                    Competency Deep Dive
                </h2>
"""

    # Add collapsible sections for each competency
    for comp_name in sorted(competency_breakdown.keys()):
        comp_issues = [issue for issue in consensus['consensus_issues']
                      if comp_name.lower() in str(issue).lower()][:3]

        html_content += f"""
                <div class="collapsible">
                    <div class="collapsible-header" onclick="toggleCollapsible(this.parentElement)">
                        <div>
                            <strong>{comp_name}</strong>
                            <span style="color: #6c757d; margin-left: 10px;">
                                ({competency_breakdown[comp_name]} issues)
                            </span>
                        </div>
                        <span class="collapsible-arrow">▼</span>
                    </div>
                    <div class="collapsible-content">
                        <h4>Common Patterns</h4>
                        <ul style="margin: 15px 0; line-height: 1.8;">
"""

        for issue in comp_issues[:3]:
            html_content += f"""
                            <li>{issue.get('issue', 'Issue details')[:100]}...</li>
"""

        html_content += """
                        </ul>
                        <h4>Recommendations</h4>
                        <p style="line-height: 1.8;">
                            Focus on addressing high-severity issues in this competency area first.
                            Consider reviewing the rubric guidelines for this competency to ensure
                            all requirements are met.
                        </p>
                    </div>
                </div>
"""

    html_content += """
            </section>

            <!-- Section 9: Next Steps -->
            <section id="next-steps" class="section">
                <h2 class="section-header">
                    <div class="icon">🚀</div>
                    Next Steps
                </h2>

                <div class="next-steps">
                    <h3 style="margin-bottom: 20px;">Priority Action Items</h3>

                    <div class="step-card">
                        <span class="step-number">1</span>
                        <strong>Address Critical Issues</strong>
                        <p style="margin-top: 10px; margin-left: 45px;">
                            Focus on severity 5 and 4 issues first. These impact core learning objectives
                            and must be resolved before publication.
                        </p>
                    </div>

                    <div class="step-card">
                        <span class="step-number">2</span>
                        <strong>Review High-Confidence Findings</strong>
                        <p style="margin-top: 10px; margin-left: 45px;">
                            Issues with confidence scores above 70% represent clear consensus among reviewers
                            and should be prioritized.
                        </p>
                    </div>

                    <div class="step-card">
                        <span class="step-number">3</span>
                        <strong>Improve Problem Competencies</strong>
                        <p style="margin-top: 10px; margin-left: 45px;">
                            Focus on the top 3 competencies with the most issues to maximize improvement impact.
                        </p>
                    </div>

                    <div class="step-card">
                        <span class="step-number">4</span>
                        <strong>Prepare for Pass 2</strong>
                        <p style="margin-top: 10px; margin-left: 45px;">
                            After addressing issues, the module will undergo Pass 2 review to verify improvements
                            and catch any remaining issues.
                        </p>
                    </div>
                </div>

                <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin-top: 30px;">
                    <h4 style="color: #856404;">Important Notes</h4>
                    <ul style="margin-top: 10px; line-height: 1.8; color: #856404;">
                        <li>This review covers authoring and style compliance only</li>
                        <li>Animation scripting is evaluated through a separate process</li>
                        <li>Pass 2 will re-evaluate the module after revisions</li>
                        <li>All high-severity issues must be addressed before publication</li>
                    </ul>
                </div>
            </section>
        </div>

        <div class="footer">
            <div class="footer-text">
                Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
                <br>
                Pass 1 Content Review System • Learnvia
            </div>
        </div>
    </div>

    <script>
        function showSection(sectionId) {{
            // Hide all sections
            const sections = document.querySelectorAll('.section');
            sections.forEach(section => {{
                section.classList.remove('active');
            }});

            // Remove active from all tabs
            const tabs = document.querySelectorAll('.nav-tab');
            tabs.forEach(tab => {{
                tab.classList.remove('active');
            }});

            // Show selected section
            document.getElementById(sectionId).classList.add('active');

            // Mark tab as active
            event.target.classList.add('active');
        }}

        function toggleCollapsible(element) {{
            element.classList.toggle('active');
        }}

        function filterTable(searchTerm) {{
            const table = document.getElementById('issuesTable');
            const rows = table.getElementsByTagName('tr');

            for (let i = 1; i < rows.length; i++) {{
                const row = rows[i];
                const text = row.textContent.toLowerCase();

                if (text.includes(searchTerm.toLowerCase())) {{
                    row.style.display = '';
                }} else {{
                    row.style.display = 'none';
                }}
            }}
        }}

        // Animate progress bars on load
        window.addEventListener('load', function() {{
            const bars = document.querySelectorAll('.competency-fill');
            bars.forEach(bar => {{
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(() => {{
                    bar.style.width = width;
                }}, 100);
            }});
        }});
    </script>
</body>
</html>
"""

    # Save HTML report
    output_path = Path(__file__).parent.parent / "outputs" / "PASS1_REAL_MODULE_REPORT.html"
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(html_content)

    print(f"✓ HTML report generated: {output_path}")
    return str(output_path)


if __name__ == "__main__":
    # Generate report from existing results
    generate_html_report()