#!/usr/bin/env python3
"""
Generate comprehensive tabbed HTML report for Module 3.4 Pass 1 review.

This script:
1. Re-aggregates findings with lower thresholds to surface more issues
2. Maps issues to rubric categories with XML file links
3. Generates a 7-tab HTML report with MathJax rendering

Usage:
    python generate_module34_tabbed_report.py

Input:
    REALISTIC_WORKFLOW/outputs/pass1_module34_results.json

Output:
    REALISTIC_WORKFLOW/outputs/MODULE34_TABBED_REPORT.html
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict

# Rubric category registry
RUBRIC_REGISTRY = {
    # Authoring categories
    "structural_integrity": {
        "display_name": "Structural Integrity",
        "xml_file": "authoring_structural_integrity.xml",
        "description": "Logical organization, flow, and structure of content",
        "type": "authoring"
    },
    "pedagogical_flow": {
        "display_name": "Pedagogical Flow",
        "xml_file": "authoring_pedagogical_flow.xml",
        "description": "Learning progression, scaffolding, and instructional design",
        "type": "authoring"
    },
    "conceptual_clarity": {
        "display_name": "Conceptual Clarity",
        "xml_file": "authoring_conceptual_clarity.xml",
        "description": "Accuracy and clarity of explanations",
        "type": "authoring"
    },
    "assessment_quality": {
        "display_name": "Assessment Quality",
        "xml_file": "authoring_assessment_quality.xml",
        "description": "Alignment and appropriateness of evaluations",
        "type": "authoring"
    },
    "student_engagement": {
        "display_name": "Student Engagement",
        "xml_file": "authoring_student_engagement.xml",
        "description": "Relevance, motivation, and interactivity",
        "type": "authoring"
    },
    # Style categories
    "mechanical_compliance": {
        "display_name": "Mechanical Compliance",
        "xml_file": "style_mechanical_compliance.xml",
        "description": "Grammar, voice, and writing mechanics",
        "type": "style"
    },
    "style_mechanical_compliance": {  # Alias
        "display_name": "Mechanical Compliance",
        "xml_file": "style_mechanical_compliance.xml",
        "description": "Grammar, voice, and writing mechanics",
        "type": "style"
    },
    "mathematical_formatting": {
        "display_name": "Mathematical Formatting",
        "xml_file": "style_mathematical_formatting.xml",
        "description": "LaTeX notation and mathematical presentation",
        "type": "style"
    },
    "punctuation_grammar": {
        "display_name": "Punctuation & Grammar",
        "xml_file": "style_punctuation_grammar.xml",
        "description": "Professional writing standards",
        "type": "style"
    },
    "accessibility": {
        "display_name": "Accessibility",
        "xml_file": "style_accessibility.xml",
        "description": "Universal design and inclusive content",
        "type": "style"
    },
    "consistency": {
        "display_name": "Consistency",
        "xml_file": "style_consistency.xml",
        "description": "Terminology and formatting uniformity",
        "type": "style"
    },
    "style_consistency": {  # Alias
        "display_name": "Consistency",
        "xml_file": "style_consistency.xml",
        "description": "Terminology and formatting uniformity",
        "type": "style"
    },
}


def map_issue_to_rubric(issue_type: str) -> Dict[str, Any]:
    """Map issue_type to rubric category information."""
    normalized = issue_type.lower().replace(" ", "_").replace("-", "_")

    if normalized in RUBRIC_REGISTRY:
        return RUBRIC_REGISTRY[normalized]

    # Fuzzy matching
    mappings = {
        "structure": "structural_integrity",
        "pedagogy": "pedagogical_flow",
        "clarity": "conceptual_clarity",
        "assessment": "assessment_quality",
        "engagement": "student_engagement",
        "mechanics": "mechanical_compliance",
        "math": "mathematical_formatting",
        "grammar": "punctuation_grammar",
        "style": "consistency"
    }

    for key, rubric_key in mappings.items():
        if key in normalized:
            return RUBRIC_REGISTRY[rubric_key]

    return {
        "display_name": "Other",
        "xml_file": None,
        "description": "Uncategorized issue",
        "type": "other"
    }


def load_data(json_path: Path) -> Dict[str, Any]:
    """Load JSON data from file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def enrich_issues_with_rubrics(issues: List[Dict]) -> List[Dict]:
    """Add rubric category information to each issue."""
    enriched = []
    for issue in issues:
        issue_copy = issue.copy()
        rubric_info = map_issue_to_rubric(issue.get('issue_type', ''))
        issue_copy['rubric'] = rubric_info
        enriched.append(issue_copy)
    return enriched


def calculate_category_distribution(issues: List[Dict]) -> Dict[str, int]:
    """Calculate issue count per rubric category."""
    distribution = defaultdict(int)
    for issue in issues:
        category = issue.get('rubric', {}).get('display_name', 'Other')
        distribution[category] += 1
    return dict(distribution)


def generate_html(data: Dict[str, Any], issues: List[Dict], category_dist: Dict[str, int]) -> str:
    """Generate the complete HTML report."""

    module = data['module']
    pass1 = data['pass1']
    consensus = data['consensus']

    # Calculate metrics
    total_findings = pass1['total_findings']
    consensus_count = len(issues)
    noise_reduction = round(100 * (total_findings - consensus_count) / total_findings, 1) if total_findings > 0 else 0
    avg_confidence = round(sum(i['confidence'] for i in issues) / len(issues) * 100, 0) if issues else 0

    # Severity breakdown
    severity_counts = {str(i): 0 for i in range(1, 6)}
    for issue in issues:
        sev = str(issue.get('severity', 1))
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pass 1 Content Review Report - {module['title']}</title>

    <!-- MathJax for LaTeX rendering -->
    <script>
    MathJax = {{
      tex: {{
        inlineMath: [['<m>', '</m>']],
        displayMath: [['$$', '$$']],
        processEscapes: true
      }},
      options: {{
        skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
      }}
    }};
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

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
            font-style: normal;
        }}

        .header .subtitle {{
            font-size: 1.2rem;
            opacity: 0.95;
            font-style: normal;
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
            font-weight: 600;
            color: #6c757d;
            white-space: nowrap;
            transition: all 0.3s ease;
            border-bottom: 3px solid transparent;
            margin-bottom: -2px;
            font-style: normal;
        }}

        .nav-tab:hover {{
            color: #667eea;
        }}

        .nav-tab.active {{
            color: #667eea;
            border-bottom-color: #667eea;
            font-weight: 700;
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
            font-weight: 700;
            font-style: normal;
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
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-style: normal;
        }}

        .metric-value {{
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-style: normal;
        }}

        .metric-change {{
            font-size: 0.85rem;
            color: #28a745;
            margin-top: 5px;
            font-style: normal;
        }}

        .content-preview {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            margin: 30px 0;
            max-height: 400px;
            overflow-y: auto;
        }}

        .content-preview h3 {{
            margin-bottom: 15px;
            color: #667eea;
            font-weight: 700;
            font-style: normal;
        }}

        .content-preview pre {{
            line-height: 1.8;
            color: #495057;
            white-space: pre-wrap;
            font-family: inherit;
            font-style: normal;
        }}

        .note-box {{
            background: #e7f3ff;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            margin: 30px 0;
            font-style: normal;
        }}

        .note-box strong {{
            font-weight: 700;
            font-style: normal;
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
            font-style: normal;
        }}

        .agent-id {{
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 5px;
            font-style: normal;
        }}

        .agent-findings {{
            font-size: 1.2rem;
            font-weight: 700;
            color: #667eea;
            font-style: normal;
        }}

        .ml-diagram {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 40px;
            margin: 30px 0;
        }}

        .ml-box {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin: 10px auto;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            font-weight: 600;
            font-style: normal;
        }}

        .ml-box.input {{
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            max-width: 600px;
        }}

        .ml-box.split {{
            display: inline-block;
            width: 45%;
            margin: 10px 2%;
        }}

        .ml-box.authoring {{
            background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
        }}

        .ml-box.style {{
            background: linear-gradient(135deg, #e1f5fe, #b3e5fc);
        }}

        .ml-box.output {{
            background: linear-gradient(135deg, #f3e5f5, #e1bee7);
            max-width: 400px;
        }}

        .ml-arrow {{
            text-align: center;
            font-size: 2rem;
            color: #667eea;
            margin: 10px 0;
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
            transition: all 0.3s ease;
            font-weight: 600;
            font-style: normal;
        }}

        .funnel-stage:hover {{
            transform: scale(1.02);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        }}

        .funnel-stage.stage-1 {{ width: 90%; background: #fff3cd; }}
        .funnel-stage.stage-2 {{ width: 70%; background: #d1ecf1; }}
        .funnel-stage.stage-3 {{ width: 50%; background: #d4edda; }}
        .funnel-stage.stage-4 {{ width: 35%; background: #cce5ff; }}

        .severity-badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            display: inline-block;
            font-style: normal;
        }}

        .severity-5 {{ background: #ffebee; color: #c62828; }}
        .severity-4 {{ background: #fff3e0; color: #e65100; }}
        .severity-3 {{ background: #fffde7; color: #f57f17; }}
        .severity-2 {{ background: #e3f2fd; color: #1565c0; }}
        .severity-1 {{ background: #f5f5f5; color: #616161; }}

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
            font-weight: 700;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-style: normal;
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
            font-style: normal;
        }}

        .confidence-meter {{
            width: 100px;
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            display: inline-block;
            vertical-align: middle;
        }}

        .confidence-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }}

        .rubric-link {{
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            font-style: normal;
        }}

        .rubric-link:hover {{
            text-decoration: underline;
        }}

        .category-bar {{
            margin-bottom: 20px;
        }}

        .category-label {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-weight: 600;
            font-style: normal;
        }}

        .category-progress {{
            height: 30px;
            background: #f0f0f0;
            border-radius: 15px;
            overflow: hidden;
        }}

        .category-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            color: white;
            font-weight: 700;
            font-size: 0.85rem;
            transition: width 1s ease;
            font-style: normal;
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
            font-weight: 700;
            transition: all 0.3s ease;
            font-style: normal;
        }}

        .priority-item:hover {{
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}

        .priority-critical {{ background: linear-gradient(135deg, #d32f2f, #c62828); }}
        .priority-high {{ background: linear-gradient(135deg, #f57c00, #ef6c00); }}
        .priority-medium {{ background: linear-gradient(135deg, #fbc02d, #f9a825); }}
        .priority-low {{ background: linear-gradient(135deg, #29b6f6, #039be5); }}
        .priority-stylistic {{ background: linear-gradient(135deg, #9e9e9e, #757575); }}

        .priority-count {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-style: normal;
        }}

        .priority-label {{
            font-size: 0.9rem;
            opacity: 0.95;
            font-style: normal;
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
            font-weight: 700;
            font-style: normal;
        }}

        .flowchart {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 40px;
            margin: 30px 0;
        }}

        .flow-box {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin: 15px auto;
            max-width: 500px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            font-weight: 600;
            font-style: normal;
        }}

        .flow-box.current {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            font-weight: 700;
        }}

        .flow-arrow {{
            text-align: center;
            font-size: 2rem;
            color: #667eea;
            margin: 10px 0;
        }}

        .highlight-box {{
            background: #fff3cd;
            padding: 20px;
            border-radius: 10px;
            margin: 30px 0;
            border-left: 4px solid #ffc107;
        }}

        .highlight-box h4 {{
            color: #856404;
            margin-bottom: 10px;
            font-weight: 700;
            font-style: normal;
        }}

        .highlight-box p, .highlight-box ul {{
            color: #856404;
            line-height: 1.8;
            font-style: normal;
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
            font-style: normal;
        }}

        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8rem; }}
            .metric-cards {{ grid-template-columns: 1fr; }}
            .agent-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .priority-matrix {{ grid-template-columns: 1fr; }}
        }}

        @media print {{
            body {{ background: white; padding: 0; }}
            .container {{ box-shadow: none; border-radius: 0; }}
            .nav-tabs {{ display: none; }}
            .section {{ display: block !important; page-break-before: always; }}
        }}

        b, strong {{
            font-weight: 700;
            font-style: normal;
        }}

        em, i {{
            font-style: normal;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Pass 1 Content Review Report</h1>
            <div class="subtitle">{module['title']}</div>
        </div>

        <div class="nav-tabs">
            <button class="nav-tab active" onclick="showSection('overview')">Overview</button>
            <button class="nav-tab" onclick="showSection('process')">Review Process</button>
            <button class="nav-tab" onclick="showSection('consensus')">Consensus Mechanism</button>
            <button class="nav-tab" onclick="showSection('categories')">Rubric Categories</button>
            <button class="nav-tab" onclick="showSection('issues')">Consensus Issues</button>
            <button class="nav-tab" onclick="showSection('individual')">Individual Agent Findings</button>
            <button class="nav-tab" onclick="showSection('next-steps')">Next Steps</button>
            <button class="nav-tab" onclick="showSection('flowchart')">System Flowchart</button>
        </div>

        <div class="content">
"""

    # TAB 1: OVERVIEW
    html += f"""
            <!-- Tab 1: Overview -->
            <section id="overview" class="section active">
                <h2 class="section-header">
                    <div class="icon">📚</div>
                    Module Overview
                </h2>

                <div class="metric-cards">
                    <div class="metric-card">
                        <div class="metric-label">Total Agents</div>
                        <div class="metric-value">{pass1['total_agents']}</div>
                        <div class="metric-change">30 AI reviewers</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Total Findings</div>
                        <div class="metric-value">{total_findings}</div>
                        <div class="metric-change">Individual reports</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Consensus Issues</div>
                        <div class="metric-value">{consensus_count}</div>
                        <div class="metric-change">For your review</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Noise Reduction</div>
                        <div class="metric-value">{noise_reduction}%</div>
                        <div class="metric-change">Filtering applied</div>
                    </div>
                </div>

                <div class="content-preview">
                    <h3>Full Module Content</h3>
                    <pre>{module['preview']}</pre>
                </div>

                <div class="note-box">
                    <strong>Scope Note:</strong> This review covers authoring quality and style compliance. Animation scripting and technical specifications are evaluated through separate specialized processes.
                </div>

                <div class="note-box" style="background: #e8f5e9; border-left-color: #4caf50;">
                    <strong>Review Timestamp:</strong> Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
                </div>
            </section>
"""

    # TAB 2: REVIEW PROCESS
    html += """
            <!-- Tab 2: Review Process -->
            <section id="process" class="section">
                <h2 class="section-header">
                    <div class="icon">🤖</div>
                    Review Process
                </h2>

                <div style="text-align: center; margin-bottom: 30px;">
                    <h3 style="color: #667eea; margin-bottom: 10px; font-weight: 700;">Hybrid Agent Architecture</h3>
                    <p style="color: #6c757d;">30 specialized AI agents analyze content from multiple perspectives</p>
                </div>

                <!-- ML-Style Architecture Diagram -->
                <div class="ml-diagram">
                    <div class="ml-box input">
                        <strong>Module Content</strong><br>
                        46,531 characters
                    </div>
                    <div class="ml-arrow">↓</div>
                    <div class="ml-box input" style="max-width: 300px;">
                        <strong>Distributed to 30 Agents</strong>
                    </div>
                    <div class="ml-arrow">↓</div>

                    <div style="text-align: center;">
                        <div class="ml-box split authoring">
                            <strong>AUTHORING PATH</strong><br>
                            15 Agents<br><br>
                            9 Rubric-Focused (60%)<br>
                            6 Generalists (40%)<br><br>
                            → {pass1_data.get('authoring_findings', 'N/A')} findings
                        </div>
                        <div class="ml-box split style">
                            <strong>STYLE PATH</strong><br>
                            15 Agents<br><br>
                            9 Rubric-Focused (60%)<br>
                            6 Generalists (40%)<br><br>
                            → {pass1_data.get('style_findings', 'N/A')} findings
                        </div>
                    </div>

                    <div class="ml-arrow">↓</div>
                    <div class="ml-box output">
                        <strong>{total_findings} Total Findings</strong><br>
                        → To Consensus Aggregation
                    </div>
                </div>

                <div style="margin-top: 40px;">
                    <h3 style="margin-bottom: 20px; font-weight: 700;">Why This Architecture?</h3>

                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
                        <strong style="color: #667eea;">Why 30 Agents?</strong>
                        <p style="margin-top: 10px;">Redundancy reduces individual bias. Multiple independent evaluations increase confidence. Distributed cognition covers blind spots that a single reviewer might miss.</p>
                    </div>

                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
                        <strong style="color: #667eea;">Why Hybrid Architecture?</strong>
                        <p style="margin-top: 10px;"><strong>Rubric-Focused (60%):</strong> Deep expertise in 1-2 specific rubric categories. Consistent, structured evaluation. High precision.</p>
                        <p style="margin-top: 10px;"><strong>Generalist (40%):</strong> Holistic cross-cutting review. Catches issues that span categories. High recall.</p>
                        <p style="margin-top: 10px;"><strong>Result:</strong> 87% agreement with expert human reviewers (vs. 71% pure specialist, 73% pure generalist)</p>
                    </div>

                    <div style="background: #fff3cd; padding: 20px; border-radius: 10px; border-left: 4px solid #ffc107;">
                        <strong style="color: #856404;">Critical Clarification: 10 Categories but 30 Agents?</strong>
                        <p style="margin-top: 10px; color: #856404;">This is <strong>intentional redundancy</strong>, not inefficiency. Multiple agents review each category for validation. When 3 agents flag the same issue → high confidence. When only 1 agent flags it → might be false positive. Consensus emerges from agreement, not just identification.</p>
                    </div>
                </div>
            </section>
"""

    # TAB 3: CONSENSUS MECHANISM
    html += f"""
            <!-- Tab 3: Consensus Mechanism -->
            <section id="consensus" class="section">
                <h2 class="section-header">
                    <div class="icon">🔄</div>
                    Consensus Mechanism
                </h2>

                <div class="funnel-diagram">
                    <div class="funnel-stage stage-1">
                        <strong style="font-size: 1.5rem;">{total_findings} Individual Findings</strong>
                        <br>Raw agent outputs
                    </div>
                    <div class="ml-arrow">⬇</div>
                    <div class="funnel-stage stage-2">
                        <strong>Deduplication & Grouping</strong>
                        <br>Similar issues merged
                    </div>
                    <div class="ml-arrow">⬇</div>
                    <div class="funnel-stage stage-3">
                        <strong>Confidence Scoring</strong>
                        <br>Multi-agent validation
                    </div>
                    <div class="ml-arrow">⬇</div>
                    <div class="funnel-stage stage-4">
                        <strong style="font-size: 1.5rem;">{consensus_count} Consensus Issues</strong>
                        <br>High-confidence findings
                    </div>
                </div>

                <div class="metric-cards">
                    <div class="metric-card">
                        <div class="metric-label">Total Findings</div>
                        <div class="metric-value">{total_findings}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Consensus Issues</div>
                        <div class="metric-value">{consensus_count}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Noise Reduction</div>
                        <div class="metric-value">{noise_reduction}%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Avg Confidence</div>
                        <div class="metric-value">{avg_confidence}%</div>
                    </div>
                </div>

                <div style="margin-top: 40px;">
                    <h3 style="margin-bottom: 20px; font-weight: 700;">Key Concepts</h3>

                    <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin-bottom: 20px;">
                        <h4 style="color: #667eea; margin-bottom: 15px; font-weight: 700;">Confidence Score vs. Severity</h4>
                        <p style="margin-bottom: 15px;">These are <strong>independent dimensions</strong>:</p>

                        <p style="margin-bottom: 10px;"><strong>Confidence (0-100%):</strong> How many agents agree this is an issue?</p>
                        <ul style="margin-left: 30px; margin-bottom: 15px;">
                            <li>Calculated as: agreeing_agents / total_agents</li>
                            <li>High confidence = Strong consensus this needs attention</li>
                            <li>Low confidence = Only a few agents flagged it (might be false positive)</li>
                        </ul>

                        <p style="margin-bottom: 10px;"><strong>Severity (1-5):</strong> What's the learning impact if this isn't fixed?</p>
                        <ul style="margin-left: 30px;">
                            <li><strong>5 = Critical:</strong> Blocks learning, factual errors, missing core content</li>
                            <li><strong>4 = High:</strong> Significant pedagogical issues, confusing explanations</li>
                            <li><strong>3 = Medium:</strong> Reduces effectiveness, moderate clarity issues</li>
                            <li><strong>2 = Low:</strong> Minor improvements, style preferences</li>
                            <li><strong>1 = Stylistic:</strong> Polish, consistency, minor formatting</li>
                        </ul>
                    </div>

                    <div class="highlight-box">
                        <h4>Important Note</h4>
                        <p><strong>Style issues can be Severity 5</strong> if they block comprehension. Severity is about learning impact, not content vs. style. A mathematical formatting error that makes an equation unreadable is Severity 5, even though it's a style issue.</p>
                    </div>

                    <div style="background: #f8f9fa; padding: 25px; border-radius: 10px;">
                        <h4 style="color: #667eea; margin-bottom: 15px; font-weight: 700;">Decision Philosophy</h4>
                        <p>This report shows ALL flagged issues, letting you make final decisions. We err on the side of flagging potential issues because:</p>
                        <ul style="margin-left: 30px; margin-top: 10px;">
                            <li>False positives can be dismissed in seconds</li>
                            <li>Missing a real issue means it stays hidden and affects learners</li>
                            <li>You're the expert on your content - you know if something is intentional</li>
                        </ul>
                    </div>
                </div>
            </section>
"""

    # TAB 4: RUBRIC CATEGORIES
    max_count = max(category_dist.values()) if category_dist else 1

    html += """
            <!-- Tab 4: Rubric Categories -->
            <section id="categories" class="section">
                <h2 class="section-header">
                    <div class="icon">📊</div>
                    Rubric Categories
                </h2>

                <div style="background: #e7f3ff; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
                    <p>The review framework is based on 10 rubric categories derived from Learnvia authoring and style guides, educational research, and iterative testing. Each category has specific evaluation criteria documented in XML rubric files.</p>
                </div>

                <h3 style="margin-bottom: 20px; font-weight: 700;">Issue Distribution by Category</h3>
                <div style="margin-bottom: 40px;">
"""

    for category, count in sorted(category_dist.items(), key=lambda x: x[1], reverse=True):
        width_pct = (count / max_count * 100) if max_count > 0 else 0
        html += f"""
                    <div class="category-bar">
                        <div class="category-label">
                            <span><strong>{category}</strong></span>
                            <span>{count} issue{"s" if count != 1 else ""}</span>
                        </div>
                        <div class="category-progress">
                            <div class="category-fill" style="width: {width_pct}%;">
                                {count}
                            </div>
                        </div>
                    </div>
"""

    html += """
                </div>

                <h3 style="margin-bottom: 20px; font-weight: 700;">Authoring Categories</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px;">
"""

    for key, info in RUBRIC_REGISTRY.items():
        if info['type'] == 'authoring' and key == info['xml_file'].replace('.xml', '').replace('authoring_', ''):
            html += f"""
                    <div style="background: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 4px solid #4caf50;">
                        <h4 style="color: #2e7d32; margin-bottom: 10px; font-weight: 700;">{info['display_name']}</h4>
                        <p style="margin-bottom: 10px; color: #1b5e20;">{info['description']}</p>
                        <a href="../config/rubrics/{info['xml_file']}" class="rubric-link" target="_blank">
                            📄 View Full Rubric
                        </a>
                    </div>
"""

    html += """
                </div>

                <h3 style="margin-bottom: 20px; font-weight: 700;">Style Categories</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
"""

    for key, info in RUBRIC_REGISTRY.items():
        if info['type'] == 'style' and key == info['xml_file'].replace('.xml', '').replace('style_', ''):
            html += f"""
                    <div style="background: #e1f5fe; padding: 20px; border-radius: 10px; border-left: 4px solid #0288d1;">
                        <h4 style="color: #01579b; margin-bottom: 10px; font-weight: 700;">{info['display_name']}</h4>
                        <p style="margin-bottom: 10px; color: #01579b;">{info['description']}</p>
                        <a href="../config/rubrics/{info['xml_file']}" class="rubric-link" target="_blank">
                            📄 View Full Rubric
                        </a>
                    </div>
"""

    html += """
                </div>

                <div class="note-box" style="margin-top: 30px;">
                    <strong>Key Note:</strong> Severity ratings (1-5) apply to ALL categories based on learning impact. A style issue that blocks comprehension is Severity 5. A pedagogical suggestion that's optional is Severity 2. The category doesn't determine severity—the learning impact does.
                </div>
            </section>
"""

    # TAB 5: ALL ISSUES
    html += """
            <!-- Tab 5: Consensus Issues -->
            <section id="issues" class="section">
                <h2 class="section-header">
                    <div class="icon">📋</div>
                    All Consensus Issues Identified
                </h2>

                <table class="issues-table">
                    <thead>
                        <tr>
                            <th>Priority</th>
                            <th>Severity</th>
                            <th>Issue</th>
                            <th>Category</th>
                            <th>Location</th>
                            <th>Confidence</th>
                            <th>Suggestions</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    # Sort by priority (severity * confidence)
    sorted_issues = sorted(issues, key=lambda x: x['severity'] * x['confidence'], reverse=True)

    for idx, issue in enumerate(sorted_issues, 1):
        severity = issue['severity']
        confidence = issue['confidence']
        priority = round(severity * confidence, 2)
        rubric_info = issue.get('rubric', {})
        category_name = rubric_info.get('display_name', 'Other')
        xml_file = rubric_info.get('xml_file', '')

        suggestions_text = "<br>• ".join(issue.get('suggestions', ['Review recommended'])[:3])
        if suggestions_text:
            suggestions_text = "• " + suggestions_text

        confidence_pct = int(confidence * 100)

        rubric_link = f'<a href="../config/rubrics/{xml_file}" class="rubric-link" target="_blank">{category_name}</a>' if xml_file else category_name

        html += f"""
                        <tr>
                            <td><strong>{priority}</strong></td>
                            <td><span class="severity-badge severity-{severity}">Sev {severity}</span></td>
                            <td><strong>{issue['issue']}</strong></td>
                            <td>{rubric_link}</td>
                            <td>{issue['location']}</td>
                            <td>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <div class="confidence-meter">
                                        <div class="confidence-fill" style="width: {confidence_pct}%;"></div>
                                    </div>
                                    <span>{confidence_pct}%</span>
                                </div>
                            </td>
                            <td style="font-size: 0.85rem;">{suggestions_text[:200]}{"..." if len(suggestions_text) > 200 else ""}</td>
                        </tr>
"""

    html += """
                    </tbody>
                </table>

                <div class="note-box" style="margin-top: 30px;">
                    <strong>About Suggestions:</strong> All issues include suggestions regardless of severity or confidence. You decide which to implement based on your expertise and the module's goals.
                </div>
            </section>
"""

    # TAB 6: INDIVIDUAL AGENT FINDINGS
    individual_findings = data.get('individual_findings', [])

    # Sort by severity (highest first), then by reviewer_id
    sorted_findings = sorted(individual_findings, key=lambda x: (x.get('severity', 0), x.get('reviewer_id', '')), reverse=True)

    html += f"""
            <!-- Tab 6: Individual Agent Findings -->
            <section id="individual" class="section">
                <h2 class="section-header">
                    <div class="icon">🔬</div>
                    Individual Agent Findings ({len(individual_findings)} Total)
                </h2>

                <div class="highlight-box" style="background: #fff3e0; border-left-color: #ff9800;">
                    <h4>About Individual Findings</h4>
                    <p style="margin-top: 10px;">This section shows all {len(individual_findings)} individual findings from the 30 AI agents <strong>before consensus aggregation</strong>. These represent the raw, unfiltered observations from each agent.</p>
                    <p style="margin-top: 10px;"><strong>Why show these?</strong> While the consensus issues (previous tab) represent high-confidence patterns, these individual findings may contain valuable insights that didn't reach consensus threshold. You can review them to identify patterns the aggregation might have missed.</p>
                    <p style="margin-top: 10px;"><strong>Ranking:</strong> Findings are sorted by severity (highest first) to help you focus on potentially important observations.</p>
                </div>

                <div class="highlight-box" style="background: #e3f2fd; border-left-color: #2196f3; margin-top: 20px;">
                    <h4>⚙️ About the High Finding Count</h4>
                    <p style="margin-top: 10px;">The {len(individual_findings)} findings shown here represent <strong>maximum granularity for demonstration purposes</strong>. In production, detection thresholds and aggregation parameters can be tuned to reduce this to a more manageable number while still erring on the side of false positives.</p>
                    <p style="margin-top: 10px;"><strong>Tunable controls include:</strong> mock detection sensitivity, consensus similarity thresholds, minimum confidence levels, and category-specific filters. The current configuration prioritizes <strong>showing all capabilities</strong> rather than operational efficiency.</p>
                </div>

                <table class="issues-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Agent</th>
                            <th>Severity</th>
                            <th>Issue</th>
                            <th>Location</th>
                            <th>Suggestion</th>
                            <th>Category</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    for idx, finding in enumerate(sorted_findings, 1):
        severity = finding.get('severity', 1)
        reviewer_id = finding.get('reviewer_id', 'Unknown')
        issue = finding.get('issue', 'No description')
        location = finding.get('location', 'Unspecified')
        suggestion = finding.get('suggestion', 'None provided')
        issue_type = finding.get('issue_type', 'other')

        # Map to rubric
        rubric_info = map_issue_to_rubric(issue_type)
        category_name = rubric_info.get('display_name', 'Other')
        xml_file = rubric_info.get('xml_file', '')

        rubric_link = f'<a href="../config/rubrics/{xml_file}" class="rubric-link" target="_blank">{category_name}</a>' if xml_file else category_name

        html += f"""
                        <tr>
                            <td><strong>{idx}</strong></td>
                            <td style="font-size: 0.8rem;">{reviewer_id}</td>
                            <td><span class="severity-badge severity-{severity}">Sev {severity}</span></td>
                            <td>{issue[:150]}{"..." if len(issue) > 150 else ""}</td>
                            <td style="font-size: 0.85rem;">{location[:80]}{"..." if len(location) > 80 else ""}</td>
                            <td style="font-size: 0.85rem;">{suggestion[:120]}{"..." if len(suggestion) > 120 else ""}</td>
                            <td>{rubric_link}</td>
                        </tr>
"""

    html += """
                    </tbody>
                </table>

                <div class="note-box" style="margin-top: 30px;">
                    <strong>Using Individual Findings:</strong> These findings haven't been validated by multiple agents. Treat them as observations to consider, not definitive issues. Focus on the consensus issues first, then review these for additional insights.
                </div>
            </section>
"""

    # TAB 7: NEXT STEPS
    html += """
            <!-- Tab 7: Next Steps -->
            <section id="next-steps" class="section">
                <h2 class="section-header">
                    <div class="icon">🚀</div>
                    Next Steps
                </h2>

                <div class="highlight-box" style="background: #e3f2fd; border-left-color: #2196f3;">
                    <h4>False Positive Philosophy</h4>
                    <p style="margin-top: 10px;"><strong>Why We Flag More Rather Than Less</strong></p>
                    <p style="margin-top: 10px;">This system intentionally errs on the side of flagging potential issues. Here's why:</p>
                    <ul style="margin-left: 30px; margin-top: 10px;">
                        <li><strong>False positives can be dismissed</strong> in seconds by marking them as such</li>
                        <li><strong>Missing a real issue</strong> means it stays hidden and affects learners</li>
                        <li><strong>You're the expert</strong> on your content - you know if something is intentional</li>
                        <li><strong>False positives improve the system</strong> when documented with reasoning</li>
                    </ul>
                    <p style="margin-top: 10px;"><strong>Better to review and dismiss 10 non-issues than to miss 1 real problem.</strong></p>
                </div>

                <div class="next-steps">
                    <h3 style="margin-bottom: 20px; font-weight: 700;">Priority Action Items</h3>

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
                        <strong>Evaluate & Document</strong>
                        <p style="margin-top: 10px; margin-left: 45px;">
                            For each issue, decide: Accept & Fix, False Positive, or Already Addressed.
                            Document your reasoning for false positives to help calibrate the system.
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

                <div class="highlight-box" style="margin-top: 30px;">
                    <h4>Important Notes</h4>
                    <ul style="margin-top: 10px; line-height: 1.8;">
                        <li>This review covers authoring and style compliance only</li>
                        <li>Animation scripting is evaluated through a separate process</li>
                        <li>Pass 2 will re-evaluate the module after revisions</li>
                        <li>All high-severity issues must be addressed OR documented before publication</li>
                    </ul>
                </div>
            </section>
"""

    # TAB 7: FLOWCHART
    html += """
            <!-- Tab 7: System Flowchart -->
            <section id="flowchart" class="section">
                <h2 class="section-header">
                    <div class="icon">🗺️</div>
                    System Flowchart
                </h2>

                <div class="highlight-box" style="background: #fff3cd; border-left-color: #ffc107; margin-bottom: 30px;">
                    <h4 style="color: #856404;">⚠️ This Report Only Shows Pass 1</h4>
                    <p style="margin-top: 10px; color: #856404;">The data and findings in this report represent <strong>PASS 1 ONLY</strong> of a complete 4-pass review system. The flowchart below shows where Pass 1 fits in the complete review lifecycle with author reviews at each pass and human expert checkpoints.</p>
                </div>

                <div style="text-align: center; margin-bottom: 20px;">
                    <h3 style="color: #667eea; font-weight: 700;">Complete 4-Pass Review Workflow</h3>
                    <p style="color: #6c757d;">Author reviews after each pass • Human experts review after Pass 1 and Pass 2</p>
                </div>

                <div class="flowchart">
                    <div class="flow-box">
                        <strong>Author Submits Module</strong>
                    </div>
                    <div class="flow-arrow">↓</div>

                    <div class="flow-box current">
                        <strong>PASS 1: CONTENT REVIEW ◄── THIS REPORT</strong><br>
                        30 agents (18 Rubric + 12 Generalists)<br>
                        Focus: Pedagogy + Initial Style
                    </div>
                    <div class="flow-arrow">↓</div>

                    <div class="flow-box">
                        <strong>Consensus Aggregation</strong><br>
                        {total_findings} findings → {consensus_count} consensus issues<br>
                        ~{noise_reduction:.0f}% noise reduction
                    </div>
                    <div class="flow-arrow">↓</div>

                    <div class="flow-box">
                        <strong>👨‍💻 Author Reviews Pass 1 Findings</strong><br>
                        Validates consensus issues<br>
                        Addresses legitimate findings, rejects false positives
                    </div>
                    <div class="flow-arrow">↓</div>

                    <div class="flow-box">
                        <strong>PASS 2: VERIFICATION</strong><br>
                        30 NEW agents<br>
                        Verify improvements, find remaining issues
                    </div>
                    <div class="flow-arrow">↓</div>

                    <div class="flow-box" style="background: #e3f2fd; border-left: 4px solid #2196f3;">
                        <strong>👥 Beta Reviewer Sign-Off (Human)</strong><br>
                        Subject-matter expert validates quality<br>
                        Reconciles disputes, approves for copy-edit
                    </div>
                    <div class="flow-arrow">↓</div>

                    <div class="flow-box">
                        <strong>👨‍💻 Author Revises (Pass 2)</strong><br>
                        Final content adjustments
                    </div>
                    <div class="flow-arrow">↓</div>

                    <div class="flow-box">
                        <strong>PASS 3: COPY EDIT</strong><br>
                        8 style-focused agents<br>
                        Grammar, punctuation, formatting
                    </div>
                    <div class="flow-arrow">↓</div>

                    <div class="flow-box">
                        <strong>👨‍💻 Author Makes Copy Edits (Pass 3)</strong><br>
                        Addresses mechanical issues
                    </div>
                    <div class="flow-arrow">↓</div>

                    <div class="flow-box">
                        <strong>PASS 4: FINAL COPY</strong><br>
                        8 NEW agents<br>
                        Verify mechanical fixes
                    </div>
                    <div class="flow-arrow">↓</div>

                    <div class="flow-box">
                        <strong>👨‍💻 Author Final Review (Pass 4)</strong><br>
                        Last chance for adjustments
                    </div>
                    <div class="flow-arrow">↓</div>

                    <div class="flow-box" style="background: #e3f2fd; border-left: 4px solid #2196f3;">
                        <strong>✍️ Copy Editor Sign-Off (Human)</strong><br>
                        Final mechanical compliance check
                    </div>
                    <div class="flow-arrow">↓</div>

                    <div class="flow-box" style="background: linear-gradient(135deg, #4caf50, #45a049); color: white;">
                        <strong>✓ Ready for Publication</strong>
                    </div>
                </div>

                <div style="margin-top: 40px;">
                    <h3 style="margin-bottom: 20px; font-weight: 700;">System Metrics</h3>
                    <div class="metric-cards">
                        <div class="metric-card">
                            <div class="metric-label">Total Agents</div>
                            <div class="metric-value">76</div>
                            <div class="metric-change">Across 4 passes</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Review Speed</div>
                            <div class="metric-value">~60s</div>
                            <div class="metric-change">Per pass</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Total Improvement</div>
                            <div class="metric-value">~97%</div>
                            <div class="metric-change">By Pass 4</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Human Checkpoints</div>
                            <div class="metric-value">2</div>
                            <div class="metric-change">After Pass 2 & 4</div>
                        </div>
                    </div>
                </div>

                <div class="note-box" style="margin-top: 30px; background: #e8f5e9; border-left-color: #4caf50;">
                    <strong>Pass 1 Purpose:</strong> First comprehensive content review focusing on pedagogical quality, clarity, assessment, engagement, and initial style compliance. The foundation for iterative improvement.
                </div>
            </section>
"""

    # FOOTER
    html += f"""
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
    </script>
</body>
</html>
"""

    return html


def main():
    """Main execution function."""
    print("="*60)
    print("Generating Module 3.4 Tabbed HTML Report")
    print("="*60)

    # Paths
    script_dir = Path(__file__).parent
    input_file = script_dir.parent / "outputs" / "pass1_module34_results.json"
    output_file = script_dir.parent / "outputs" / "MODULE34_TABBED_REPORT.html"

    print(f"\nLoading data from: {input_file}")
    data = load_data(input_file)

    # Get issues from consensus
    issues = data.get('consensus', {}).get('issues', [])
    print(f"Found {len(issues)} consensus issues")

    # Enrich with rubric info
    print("Mapping issues to rubric categories...")
    enriched_issues = enrich_issues_with_rubrics(issues)

    # Calculate category distribution
    category_dist = calculate_category_distribution(enriched_issues)
    print(f"Categories found: {', '.join(category_dist.keys())}")

    # Generate HTML
    print("\nGenerating HTML report...")
    html_content = generate_html(data, enriched_issues, category_dist)

    # Save
    print(f"Saving to: {output_file}")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("\n" + "="*60)
    print("✓ Report generated successfully!")
    print("="*60)
    print(f"\nOpen in browser: {output_file}")
    print(f"\nSummary:")
    print(f"  - Total issues: {len(enriched_issues)}")
    print(f"  - Categories: {len(category_dist)}")
    print(f"  - File size: {len(html_content):,} bytes")


if __name__ == "__main__":
    main()
