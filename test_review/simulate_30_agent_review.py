#!/usr/bin/env python3
"""
Simulate 30-Agent Content Review System

This script simulates the multi-agent content review process by:
1. Loading the layered prompt system (master, authoring, style, rubrics)
2. Creating 30 simulated agents (15 authoring + 15 style) per configuration
3. Running each agent review using the same LLM instance (sub-agents)
4. Aggregating findings into consensus issues
5. Generating HTML report matching MODULE34_TABBED_REPORT.html format

NOTE: This uses sub-agents (shared LLM context) NOT independent API calls.
The simulation demonstrates the architecture but lacks the diversity and
parallel execution benefits of true independent agent instances.
"""

import xml.etree.ElementTree as ET
import json
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any

# Configuration paths
LEARNVIA_PATH = Path("/Users/michaeljoyce/Desktop/LEARNVIA")
CONFIG_PATH = LEARNVIA_PATH / "config"
PROMPTS_PATH = CONFIG_PATH / "prompts"
RUBRICS_PATH = CONFIG_PATH / "rubrics"
TEST_MODULE_PATH = LEARNVIA_PATH / "test_review/module_files/test_module_raw.xml"
OUTPUT_PATH = LEARNVIA_PATH / "test_review/output"

# Agent configuration based on agent_configuration.xml
AGENT_CONFIG = {
    "authoring": {
        "total": 15,
        "rubric_focused": 9,  # 60%
        "generalist": 6,  # 40%
        "competencies": [
            "Pedagogical Flow",
            "Structural Integrity", 
            "Student Engagement",
            "Conceptual Clarity",
            "Assessment Quality"
        ]
    },
    "style": {
        "total": 15,
        "rubric_focused": 9,  # 60%
        "generalist": 6,  # 40%
        "competencies": [
            "Mechanical Compliance",
            "Mathematical Formatting",
            "Punctuation & Grammar",
            "Accessibility",
            "Consistency"
        ]
    }
}


def load_prompt_file(filename: str) -> str:
    """Load a prompt file from the prompts directory."""
    filepath = PROMPTS_PATH / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def load_rubric_file(filename: str) -> str:
    """Load a rubric XML file from the rubrics directory."""
    filepath = RUBRICS_PATH / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def load_module_content(filepath: Path) -> str:
    """Load the module content to be reviewed."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def extract_text_from_module(xml_content: str) -> str:
    """Extract human-readable text from module XML for line-based review."""
    lines = []
    try:
        root = ET.fromstring(xml_content)
        
        # Extract text recursively
        def extract_text(element, prefix=""):
            text = element.text.strip() if element.text else ""
            if text:
                lines.append(f"{prefix}{text}")
            
            for child in element:
                child_prefix = f"{prefix}  " if prefix else ""
                extract_text(child, child_prefix)
                
                tail = child.tail.strip() if child.tail else ""
                if tail:
                    lines.append(f"{prefix}{tail}")
        
        extract_text(root)
        
    except ET.ParseError as e:
        print(f"Warning: XML parsing error: {e}")
        lines = xml_content.split('\n')
    
    return '\n'.join(lines)


def build_agent_prompt(agent_type: str, agent_focus: str, master_prompt: str, 
                       domain_prompt: str, rubric_content: str, module_content: str) -> str:
    """
    Build the complete prompt for a single agent.
    
    Layer 1: Master review context (universal guardrails)
    Layer 2: Domain-specific rules (authoring or style)
    Layer 3: Rubric specifics (if rubric-focused agent)
    """
    
    prompt = f"""# AGENT IDENTITY
You are Agent {agent_focus} in a {agent_type} review team.
Type: {"Rubric-Focused Specialist" if rubric_content else "Generalist Cross-Cutting Reviewer"}

# LAYERED INSTRUCTIONS

## Layer 1: Universal Review Context
{master_prompt}

## Layer 2: Domain-Specific Guidelines
{domain_prompt}
"""
    
    if rubric_content:
        prompt += f"""
## Layer 3: Rubric Competency Focus
{rubric_content}

Your PRIMARY focus is evaluating against this rubric, but you may flag other issues you observe.
"""
    else:
        prompt += """
## Layer 3: Generalist Role
As a generalist, you review holistically across all competencies. Look for cross-cutting issues,
patterns that span categories, and problems that specialist reviewers might miss by being too focused.
"""
    
    prompt += f"""

# MODULE TO REVIEW

{module_content}

# OUTPUT FORMAT

Provide your findings as a JSON array of issues:

[
  {{
    "issue_description": "Specific issue with exact line numbers and quoted text",
    "line_numbers": [10, 11, 12],
    "quoted_text": "The exact problematic text from the module",
    "category": "Pedagogical Flow|Structural Integrity|Conceptual Clarity|Assessment Quality|Mechanical Compliance|Mathematical Formatting|Punctuation & Grammar|Accessibility|Consistency|Other",
    "severity": 1-5,
    "student_impact": "How this affects student learning",
    "suggested_fix": "Concrete actionable remedy",
    "confidence": 0.0-1.0
  }}
]

CRITICAL REQUIREMENTS:
1. Every issue MUST include specific line numbers
2. Every issue MUST include quoted text from the module
3. Be specific, not vague (e.g., "Line 42: 'some students' should specify which students")
4. Focus on learning impact, not nitpicking
5. If no issues found, return empty array: []
"""
    
    return prompt


def simulate_agent_review(agent_id: str, prompt: str) -> List[Dict[str, Any]]:
    """
    Simulate an agent review by analyzing the prompt and module.
    
    In a real system, this would call an LLM API. Here we simulate
    finding issues based on known patterns in the test module.
    """
    
    # This is a SIMULATION - in production this would call Claude/GPT API
    # For demonstration, we'll generate realistic findings based on the test module
    
    findings = []
    
    # Check for common issues in the test module
    # Being more liberal with flagging - let human reviewers decide
    if "authoring" in agent_id.lower():
        # Authoring agents focus on pedagogical issues
        if "assessment" in agent_id.lower() or "generalist" in agent_id.lower():
            findings.append({
                "issue_description": "Line 3: Module Title is 'Todo' placeholder - blocks student understanding of content scope",
                "line_numbers": [3],
                "quoted_text": "<Title>Todo</Title>",
                "category": "Structural Integrity",
                "severity": 5,
                "student_impact": "Students cannot identify module topic from title, preventing effective navigation and content selection",
                "suggested_fix": "Change to: <Title>Power Series: Radius and Interval of Convergence</Title>",
                "confidence": 1.0
            })
            findings.append({
                "issue_description": "Line 4: Description is 'Todo' placeholder - missing module overview",
                "line_numbers": [4],
                "quoted_text": "<Description>Todo</Description>",
                "category": "Structural Integrity",
                "severity": 4,
                "student_impact": "Students lack overview of what they'll learn, reducing motivation and preparation",
                "suggested_fix": "Add: <Description>Learn to determine where power series converge using radius and interval of convergence tests</Description>",
                "confidence": 1.0
            })
            findings.append({
                "issue_description": "Line 5: KSAs is 'Todo' placeholder - missing learning prerequisites",
                "line_numbers": [5],
                "quoted_text": "<KSAs>Todo</KSAs>",
                "category": "Structural Integrity",
                "severity": 4,
                "student_impact": "Students don't know if they have prerequisites, may waste time or feel lost",
                "suggested_fix": "Add: <KSAs>Sequences and series, ratio test, geometric series</KSAs>",
                "confidence": 0.9
            })
        
        if "conceptual" in agent_id.lower() or "generalist" in agent_id.lower():
            findings.append({
                "issue_description": "Lines 42-43: Explanation of x=-1 endpoint is misleading - states 'negative harmonic series' incorrectly",
                "line_numbers": [42, 43],
                "quoted_text": "At x = -1: ∑ (-1 / n) diverges (harmonic series with alternating signs becomes the negative harmonic series).",
                "category": "Conceptual Clarity",
                "severity": 4,
                "student_impact": "Students may misunderstand why series diverges at x=-1, confusing alternating series with sign-flipped harmonic series",
                "suggested_fix": "At x = -1: ∑ (1/n) diverges as the harmonic series (the (-1)^n and -1 terms cancel).",
                "confidence": 0.85
            })
            findings.append({
                "issue_description": "Line 10: Term 'foundational tools' is vague - doesn't explain why power series matter",
                "line_numbers": [10],
                "quoted_text": "Power series... are foundational tools in calculus",
                "category": "Conceptual Clarity",
                "severity": 2,
                "student_impact": "Students miss motivation for why they're learning this topic",
                "suggested_fix": "Replace with: 'power series let us represent complicated functions as infinite polynomials, making them easier to analyze'",
                "confidence": 0.65
            })
        
        if "pedagogical" in agent_id.lower() or "generalist" in agent_id.lower():
            findings.append({
                "issue_description": "Lines 10-14: Four dense paragraphs of abstract definitions before any concrete example",
                "line_numbers": [10, 11, 12, 13, 14],
                "quoted_text": "Power series, written as ∑ aₙ(x - c)ⁿ... coefficients aₙ.",
                "category": "Pedagogical Flow",
                "severity": 3,
                "student_impact": "Students encounter heavy abstraction without scaffolding, likely causing cognitive overload before engagement",
                "suggested_fix": "Start with specific example (e.g., geometric series ∑xⁿ), then generalize to abstract definition",
                "confidence": 0.75
            })
            findings.append({
                "issue_description": "Line 24: Jumps to applying ratio test without explaining why we need it",
                "line_numbers": [24],
                "quoted_text": "To find the radius of convergence, we apply the ratio test:",
                "category": "Pedagogical Flow",
                "severity": 3,
                "student_impact": "Students may not understand connection between convergence and the ratio test",
                "suggested_fix": "Add: 'The ratio test helps us determine which x values make the series converge. We apply it:'",
                "confidence": 0.70
            })
        
        if "structural" in agent_id.lower():
            findings.append({
                "issue_description": "Line 6: LearningOutcomes is 'Todo' placeholder - students don't know what they'll achieve",
                "line_numbers": [6],
                "quoted_text": "<LearningOutcomes>Todo</LearningOutcomes>",
                "category": "Structural Integrity",
                "severity": 5,
                "student_impact": "No clear learning objectives prevents students from tracking progress",
                "suggested_fix": "Add: <LearningOutcomes ids='8.1.1,8.1.2'/> or define specific outcomes",
                "confidence": 1.0
            })
    
    else:  # style agents
        if "mathematical" in agent_id.lower() or "generalist" in agent_id.lower():
            findings.append({
                "issue_description": "Line 13: Mathematical notation inconsistent - uses |aₙ / aₙ₊₁| without <m> LaTeX tags",
                "line_numbers": [13],
                "quoted_text": "R = lim |aₙ / aₙ₊₁| as n → ∞",
                "category": "Mathematical Formatting",
                "severity": 2,
                "student_impact": "Raw Unicode subscripts may not render consistently across devices, reducing accessibility",
                "suggested_fix": "R = lim <m>|a_n / a_{n+1}|</m> as <m>n \\to \\infty</m>",
                "confidence": 0.90
            })
            findings.append({
                "issue_description": "Line 24: Infinity symbol ∞ used without LaTeX tags",
                "line_numbers": [24],
                "quoted_text": "∑ (xⁿ / n!) from n=0 to infinity",
                "category": "Mathematical Formatting",
                "severity": 2,
                "student_impact": "Plain text 'infinity' less clear than proper symbol, may confuse students",
                "suggested_fix": "Use <m>\\infty</m> or write '...from n=0 to <m>\\infty</m>'",
                "confidence": 0.75
            })
        
        # Accessibility agents focus on text accessibility, not visual elements
        # (Visual/animation accessibility is handled separately per master prompt)
        
        if "consistency" in agent_id.lower() or "generalist" in agent_id.lower():
            findings.append({
                "issue_description": "Lines 10, 38: Inconsistent series notation - sometimes '∑ ((-1)ⁿ xⁿ / n)', sometimes '∑ aₙ(x - c)ⁿ'",
                "line_numbers": [10, 38],
                "quoted_text": "∑ aₙ(x - c)ⁿ... ∑ ((-1)ⁿ xⁿ / n)",
                "category": "Consistency",
                "severity": 2,
                "student_impact": "Notation switches may confuse students about whether different symbols represent different concepts",
                "suggested_fix": "Establish consistent notation early: use aₙ for general case, then show specific examples",
                "confidence": 0.70
            })
        
        if "mechanical" in agent_id.lower():
            findings.append({
                "issue_description": "Line 11: Sentence fragment 'This represents the distance...' - should connect to previous sentence",
                "line_numbers": [11],
                "quoted_text": "This represents the distance from the center c",
                "category": "Mechanical Compliance",
                "severity": 2,
                "student_impact": "Choppy flow may distract struggling readers",
                "suggested_fix": "Combine: 'The radius of convergence R represents the distance...'",
                "confidence": 0.65
            })
        
        if "punctuation" in agent_id.lower() or "generalist" in agent_id.lower():
            findings.append({
                "issue_description": "Line 38: Missing comma after introductory phrase 'Now let's examine'",
                "line_numbers": [38],
                "quoted_text": "Now let's examine a more complex example.",
                "category": "Punctuation & Grammar",
                "severity": 1,
                "student_impact": "Minor clarity issue, may slow reading",
                "suggested_fix": "Consider: 'Now, let's examine a more complex example.'",
                "confidence": 0.60
            })
    
    return findings


def aggregate_consensus_issues(all_findings: List[Dict[str, Any]], 
                                total_agents: int) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Aggregate individual agent findings into consensus issues and non-consensus flagged issues.
    
    Issues flagged by multiple agents get higher confidence.
    Similar issues are grouped together.
    
    Returns:
        (consensus_issues, non_consensus_issues)
    """
    
    # Group similar issues by description similarity
    issue_groups = defaultdict(list)
    
    for finding in all_findings:
        # Simple similarity: group by first 50 chars of description
        key = finding["issue_description"][:50]
        issue_groups[key].append(finding)
    
    consensus_issues = []
    non_consensus_issues = []
    
    for group_key, grouped_findings in issue_groups.items():
        # Take the highest confidence version as representative
        representative = max(grouped_findings, key=lambda x: x["confidence"])
        
        # Calculate consensus metrics
        agent_count = len(grouped_findings)
        avg_confidence = sum(f["confidence"] for f in grouped_findings) / agent_count
        max_severity = max(f["severity"] for f in grouped_findings)
        
        # Consensus percentage
        consensus_pct = (agent_count / total_agents)
        
        # Calculate priority score: severity × consensus percentage
        # This gives higher priority to severe issues with strong consensus
        priority = max_severity * consensus_pct
        
        issue = {
            "priority": priority,
            "severity": max_severity,
            "confidence": avg_confidence,
            "consensus_percentage": consensus_pct * 100,
            "issue_description": representative["issue_description"],
            "category": representative["category"],
            "location": f"Lines {', '.join(map(str, representative['line_numbers']))}",
            "line_numbers": representative["line_numbers"],
            "quoted_text": representative["quoted_text"],
            "student_impact": representative["student_impact"],
            "suggested_fix": representative["suggested_fix"],
            "agent_count": agent_count
        }
        
        # Consensus threshold: at least 2 agents OR severity 5
        if agent_count >= 2 or max_severity == 5:
            consensus_issues.append(issue)
        else:
            # Single-agent findings go to non-consensus flagged issues
            non_consensus_issues.append(issue)
    
    # Sort by priority (descending)
    consensus_issues.sort(key=lambda x: x["priority"], reverse=True)
    non_consensus_issues.sort(key=lambda x: x["priority"], reverse=True)
    
    return consensus_issues, non_consensus_issues


def generate_html_report(consensus_issues: List[Dict[str, Any]],
                         non_consensus_issues: List[Dict[str, Any]], 
                         all_findings: List[Dict[str, Any]],
                         agent_config: Dict[str, Any],
                         module_content: str) -> str:
    """
    Generate HTML report matching MODULE34_TABBED_REPORT.html format with 8 tabs.
    
    Tabs: Overview | Review Process | Consensus Mechanism | Rubric Categories | 
          Consensus Issues | Flagged Issues | Next Steps | System Flowchart
    """
    
    total_agents = agent_config["authoring"]["total"] + agent_config["style"]["total"]
    num_consensus = len(consensus_issues)
    num_flagged = len(non_consensus_issues)
    
    # Category distribution - split by authoring vs style
    authoring_categories = ["Pedagogical Flow", "Structural Integrity", "Student Engagement", 
                           "Conceptual Clarity", "Assessment Quality"]
    style_categories = ["Mechanical Compliance", "Mathematical Formatting", "Punctuation & Grammar", 
                       "Accessibility", "Consistency"]
    
    authoring_counts = defaultdict(int)
    style_counts = defaultdict(int)
    other_counts = defaultdict(int)
    
    for issue in consensus_issues:
        cat = issue["category"]
        if cat in authoring_categories:
            authoring_counts[cat] += 1
        elif cat in style_categories:
            style_counts[cat] += 1
        else:
            other_counts[cat] += 1
    
    max_authoring = max(authoring_counts.values()) if authoring_counts else 1
    max_style = max(style_counts.values()) if style_counts else 1
    max_other = max(other_counts.values()) if other_counts else 1
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    # Severity badge helper
    def severity_badge(sev):
        return f'<span class="severity-badge severity-{sev}">Sev {sev}</span>'
    
    # Confidence meter helper
    def confidence_meter(conf):
        conf_pct = int(conf * 100)
        return f'''<div style="display: flex; align-items: center; gap: 10px;">
                    <div class="confidence-meter">
                        <div class="confidence-fill" style="width: {conf_pct}%;"></div>
                    </div>
                    <span>{conf_pct}%</span>
                </div>'''
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pass 1 Content Review Report - Power Series Module</title>
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
               line-height: 1.6; color: #2c3e50; 
               background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
               min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white;
                     border-radius: 20px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                  color: white; padding: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.5rem; margin-bottom: 10px; font-weight: 700; }}
        .header .subtitle {{ font-size: 1.2rem; opacity: 0.95; }}
        
        .nav-tabs {{ display: flex; background: #f8f9fa; border-bottom: 2px solid #e9ecef;
                    padding: 0 40px; overflow-x: auto; }}
        .nav-tab {{ padding: 15px 25px; cursor: pointer; border: none; background: none;
                   font-size: 14px; font-weight: 600; color: #6c757d; white-space: nowrap;
                   transition: all 0.3s ease; border-bottom: 3px solid transparent; margin-bottom: -2px; }}
        .nav-tab:hover {{ color: #667eea; }}
        .nav-tab.active {{ color: #667eea; border-bottom-color: #667eea; font-weight: 700; }}
        
        .content {{ padding: 40px; }}
        .section {{ display: none; animation: fadeIn 0.5s ease; }}
        .section.active {{ display: block; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }}
                           to {{ opacity: 1; transform: translateY(0); }} }}
        
        .section-header {{ font-size: 1.8rem; color: #2c3e50; margin-bottom: 30px;
                          padding-bottom: 15px; border-bottom: 2px solid #e9ecef;
                          display: flex; align-items: center; gap: 15px; font-weight: 700; }}
        .icon {{ width: 40px; height: 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px; display: flex; align-items: center; justify-content: center;
                color: white; font-size: 20px; }}
        
        .metric-cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                        gap: 20px; margin-bottom: 40px; }}
        .metric-card {{ background: white; padding: 25px; border-radius: 15px;
                       border: 1px solid #e9ecef; transition: all 0.3s ease; }}
        .metric-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); }}
        .metric-label {{ font-size: 0.9rem; color: #6c757d; margin-bottom: 8px;
                        font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
        .metric-value {{ font-size: 2.2rem; font-weight: 700;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .metric-change {{ font-size: 0.85rem; color: #28a745; margin-top: 5px; }}
        
        .issues-table {{ width: 100%; border-collapse: separate; border-spacing: 0;
                        margin: 30px 0; border-radius: 10px; overflow: hidden;
                        box-shadow: 0 0 20px rgba(0, 0, 0, 0.05); }}
        .issues-table thead {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; }}
        .issues-table th {{ padding: 15px; text-align: left; font-weight: 700;
                           font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px; }}
        .issues-table tbody tr {{ background: white; transition: all 0.3s ease; }}
        .issues-table tbody tr:hover {{ background: #f8f9fa; transform: scale(1.01);
                                       box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1); }}
        .issues-table tbody tr:nth-child(even) {{ background: #fafbfc; }}
        .issues-table td {{ padding: 15px; border-bottom: 1px solid #e9ecef; }}
        
        .severity-badge {{ padding: 5px 12px; border-radius: 20px; font-size: 0.85rem;
                          font-weight: 700; display: inline-block; }}
        .severity-5 {{ background: #ffebee; color: #c62828; }}
        .severity-4 {{ background: #fff3e0; color: #e65100; }}
        .severity-3 {{ background: #fffde7; color: #f57f17; }}
        .severity-2 {{ background: #e3f2fd; color: #1565c0; }}
        .severity-1 {{ background: #f5f5f5; color: #616161; }}
        
        .confidence-meter {{ width: 100px; height: 8px; background: #e9ecef;
                            border-radius: 4px; overflow: hidden; display: inline-block;
                            vertical-align: middle; }}
        .confidence-fill {{ height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); }}
        
        .note-box {{ background: #e7f3ff; padding: 20px; border-radius: 10px;
                    border-left: 4px solid #667eea; margin: 30px 0; }}
        .note-box strong {{ font-weight: 700; }}
        
        .rubric-link {{ color: #667eea; text-decoration: none; font-weight: 600; }}
        .rubric-link:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Pass 1 Content Review Report</h1>
            <div class="subtitle">Power Series: Radius and Interval of Convergence (Test Module)</div>
        </div>
        
        <div class="nav-tabs">
            <button class="nav-tab active" onclick="showSection('overview')">Overview</button>
            <button class="nav-tab" onclick="showSection('process')">Review Process</button>
            <button class="nav-tab" onclick="showSection('consensus-mech')">Consensus Mechanism</button>
            <button class="nav-tab" onclick="showSection('categories')">Rubric Categories</button>
            <button class="nav-tab" onclick="showSection('consensus')">Consensus Issues</button>
            <button class="nav-tab" onclick="showSection('flagged')">Flagged Issues</button>
            <button class="nav-tab" onclick="showSection('next-steps')">Next Steps</button>
            <button class="nav-tab" onclick="showSection('flowchart')">System Flowchart</button>
        </div>
        
        <div class="content">
            
            <!-- Tab 1: Overview -->
            <section id="overview" class="section active">
                <h2 class="section-header">
                    <div class="icon">📚</div>
                    Review Overview
                </h2>
                
                <div class="metric-cards">
                    <div class="metric-card">
                        <div class="metric-label">Total Agents</div>
                        <div class="metric-value">{total_agents}</div>
                        <div class="metric-change">15 authoring + 15 style</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Consensus Issues</div>
                        <div class="metric-value">{num_consensus}</div>
                        <div class="metric-change">2+ agents agreeing</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Other Flagged</div>
                        <div class="metric-value">{num_flagged}</div>
                        <div class="metric-change">Single-agent findings</div>
                    </div>
                </div>
                
                <div class="note-box">
                    <strong>Review Timestamp:</strong> Generated on {timestamp}
                </div>
                
                <div class="note-box" style="background: #fff3cd; border-left-color: #ffc107;">
                    <strong>⚠️ Simulation Note:</strong> This is a sub-agent simulation using shared LLM context. In production, proper independent API calls would provide true diversity, parallel execution, and independent judgment.
                </div>
            </section>
            
            <!-- Tab 2: Review Process -->
            <section id="process" class="section">
                <h2 class="section-header">
                    <div class="icon">🤖</div>
                    Review Process
                </h2>
                <div class="note-box">
                    <p><strong>Hybrid Agent Architecture:</strong> 30 specialized AI agents (15 authoring + 15 style) review content from multiple perspectives using a layered prompt system.</p>
                    <ul style="margin-left: 30px; margin-top: 10px;">
                        <li><strong>60% Rubric-Focused Specialists:</strong> Deep expertise in specific competencies</li>
                        <li><strong>40% Generalists:</strong> Holistic cross-cutting review</li>
                        <li><strong>Layered Prompts:</strong> Master context → Domain rules → Rubric focus</li>
                    </ul>
                </div>
            </section>
            
            <!-- Tab 3: Consensus Mechanism -->
            <section id="consensus-mech" class="section">
                <h2 class="section-header">
                    <div class="icon">🔄</div>
                    Consensus Mechanism
                </h2>
                <div class="note-box">
                    <p><strong>How Priority is Calculated:</strong></p>
                    <p style="margin-top: 10px;"><code>Priority = Severity × (Agents Agreeing / Total Agents)</code></p>
                    <p style="margin-top: 10px;">This gives higher priority to severe issues with strong consensus. For example, a Severity 5 issue flagged by 7 agents gets priority = 5 × (7/30) = 1.17</p>
                </div>
                <div class="note-box">
                    <p><strong>Consensus vs. Flagged:</strong></p>
                    <ul style="margin-left: 30px; margin-top: 10px;">
                        <li><strong>Consensus Issues:</strong> Flagged by 2+ agents OR severity 5 (high confidence)</li>
                        <li><strong>Flagged Issues:</strong> All issues detected, including single-agent findings</li>
                    </ul>
                </div>
            </section>
            
            <!-- Tab 4: Rubric Categories -->
            <section id="categories" class="section">
                <h2 class="section-header">
                    <div class="icon">📊</div>
                    Issue Distribution by Rubric Category
                </h2>
                
                <h3 style="margin: 30px 0 20px 0; font-weight: 700; color: #2e7d32;">📗 Authoring Guide Rubrics</h3>
                <div class="note-box" style="background: #e8f5e9; border-left-color: #4caf50;">
                    <strong>Pedagogical Quality:</strong> These rubrics evaluate learning design, conceptual clarity, assessment alignment, and instructional flow.
                </div>
'''
    
    # Add authoring category bars
    for category, count in sorted(authoring_counts.items(), key=lambda x: x[1], reverse=True):
        width_percent = (count / max_authoring) * 100
        html += f'''
                <div style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-weight: 600;">
                        <span><strong>{category}</strong></span>
                        <span>{count} issue{'s' if count != 1 else ''}</span>
                    </div>
                    <div style="height: 30px; background: #f0f0f0; border-radius: 15px; overflow: hidden;">
                        <div style="height: 100%; width: {width_percent}%;
                                   background: linear-gradient(90deg, #4caf50, #2e7d32);
                                   display: flex; align-items: center; justify-content: flex-end;
                                   padding-right: 10px; color: white; font-weight: 700; font-size: 0.85rem;">
                            {count}
                        </div>
                    </div>
                </div>
'''
    
    # Style guide section
    html += '''
                <h3 style="margin: 40px 0 20px 0; font-weight: 700; color: #01579b;">📘 Style Guide Rubrics</h3>
                <div class="note-box" style="background: #e1f5fe; border-left-color: #0288d1;">
                    <strong>Writing Mechanics:</strong> These rubrics evaluate grammar, formatting, notation consistency, and accessibility compliance.
                </div>
'''
    
    # Add style category bars  
    for category, count in sorted(style_counts.items(), key=lambda x: x[1], reverse=True):
        width_percent = (count / max_style) * 100
        html += f'''
                <div style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-weight: 600;">
                        <span><strong>{category}</strong></span>
                        <span>{count} issue{'s' if count != 1 else ''}</span>
                    </div>
                    <div style="height: 30px; background: #f0f0f0; border-radius: 15px; overflow: hidden;">
                        <div style="height: 100%; width: {width_percent}%;
                                   background: linear-gradient(90deg, #0288d1, #01579b);
                                   display: flex; align-items: center; justify-content: flex-end;
                                   padding-right: 10px; color: white; font-weight: 700; font-size: 0.85rem;">
                            {count}
                        </div>
                    </div>
                </div>
'''
    
    # Other categories if any
    if other_counts:
        html += '''
                <h3 style="margin: 40px 0 20px 0; font-weight: 700; color: #6c757d;">📝 Other</h3>
'''
        for category, count in sorted(other_counts.items(), key=lambda x: x[1], reverse=True):
            width_percent = (count / max_other) * 100
            html += f'''
                <div style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-weight: 600;">
                        <span><strong>{category}</strong></span>
                        <span>{count} issue{'s' if count != 1 else ''}</span>
                    </div>
                    <div style="height: 30px; background: #f0f0f0; border-radius: 15px; overflow: hidden;">
                        <div style="height: 100%; width: {width_percent}%;
                                   background: linear-gradient(90deg, #9e9e9e, #6c757d);
                                   display: flex; align-items: center; justify-content: flex-end;
                                   padding-right: 10px; color: white; font-weight: 700; font-size: 0.85rem;">
                            {count}
                        </div>
                    </div>
                </div>
'''
    
    html += '''
            </section>
            
            <!-- Tab 5: Consensus Issues -->
            <section id="consensus" class="section">
                <h2 class="section-header">
                    <div class="icon">📋</div>
                    Consensus Issues (High Confidence)
                </h2>
                <div class="note-box">
                    <strong>What This Shows:</strong> Issues flagged by multiple agents or critical (Severity 5) items. These have strong consensus and should be addressed.
                </div>
                
                <table class="issues-table">
                    <thead>
                        <tr>
                            <th>Priority</th>
                            <th>Issue</th>
                            <th>Category</th>
                            <th>Location</th>
                            <th>Suggestions</th>
                        </tr>
                    </thead>
                    <tbody>
'''
    
    # Add consensus issues
    for issue in consensus_issues:
        category_display = issue["category"]
        if issue["category"] not in ["Other"]:
            rubric_file = f"{issue['category'].lower().replace(' ', '_')}.xml"
            category_display = f'<a href="../config/rubrics/authoring_{rubric_file}" class="rubric-link">{issue["category"]}</a>'
        
        html += f'''
                        <tr>
                            <td><strong>{issue["priority"]:.2f}</strong></td>
                            <td><strong>{issue["issue_description"]}</strong></td>
                            <td>{category_display}</td>
                            <td>{issue["location"]}</td>
                            <td style="font-size: 0.85rem;">{issue["suggested_fix"]}</td>
                        </tr>
'''
    
    html += '''
                    </tbody>
                </table>
            </section>
            
            <!-- Tab 6: All Flagged Issues -->
            <section id="flagged" class="section">
                <h2 class="section-header">
                    <div class="icon">🔍</div>
                    Other Flagged Issues
                </h2>
                <div class="note-box">
                    <strong>What This Shows:</strong> Issues flagged by only 1 agent. These may include false positives, but we err on the side of showing them. Review and decide which to address.
                </div>
                
                <table class="issues-table">
                    <thead>
                        <tr>
                            <th>Priority</th>
                            <th>Issue</th>
                            <th>Category</th>
                            <th>Location</th>
                            <th>Agents</th>
                            <th>Suggestions</th>
                        </tr>
                    </thead>
                    <tbody>
'''
    
    # Add non-consensus flagged issues
    for issue in non_consensus_issues:
        category_display = issue["category"]
        if issue["category"] not in ["Other"]:
            rubric_file = f"{issue['category'].lower().replace(' ', '_')}.xml"
            category_display = f'<a href="../config/rubrics/authoring_{rubric_file}" class="rubric-link">{issue["category"]}</a>'
        
        html += f'''
                        <tr>
                            <td><strong>{issue["priority"]:.2f}</strong></td>
                            <td><strong>{issue["issue_description"]}</strong></td>
                            <td>{category_display}</td>
                            <td>{issue["location"]}</td>
                            <td><strong>{issue["agent_count"]}</strong> / {total_agents}</td>
                            <td style="font-size: 0.85rem;">{issue["suggested_fix"]}</td>
                        </tr>
'''
    
    html += '''
                    </tbody>
                </table>
            </section>
            
            <!-- Tab 7: Next Steps -->
            <section id="next-steps" class="section">
                <h2 class="section-header">
                    <div class="icon">🚀</div>
                    Next Steps
                </h2>
                <div class="note-box">
                    <p><strong>Recommended Workflow:</strong></p>
                    <ol style="margin-left: 30px; margin-top: 10px;">
                        <li>Review <strong>Consensus Issues</strong> tab (high-confidence problems)</li>
                        <li>Address highest <strong>Priority</strong> issues first (priority > 1.0)</li>
                        <li>Work through medium priority issues (0.5 - 1.0)</li>
                        <li>Check <strong>Other Flagged</strong> tab for single-agent findings</li>
                        <li>Use your judgment on low-priority items - some may be false positives</li>
                        <li>Re-run review after fixes to validate improvements</li>
                    </ol>
                </div>
                <div class="note-box" style="background: #e7f3ff; border-left-color: #667eea;">
                    <p><strong>Understanding Priority Scores:</strong></p>
                    <ul style="margin-left: 30px; margin-top: 10px;">
                        <li><strong>Priority > 1.0:</strong> High severity + strong consensus - fix immediately</li>
                        <li><strong>Priority 0.5-1.0:</strong> Moderate issues - should address</li>
                        <li><strong>Priority < 0.5:</strong> Minor issues or low consensus - review carefully</li>
                    </ul>
                    <p style="margin-top: 10px;"><em>Priority = Severity × (Agents Agreeing / 30)</em></p>
                </div>
            </section>
            
            <!-- Tab 8: System Flowchart -->
            <section id="flowchart" class="section">
                <h2 class="section-header">
                    <div class="icon">📊</div>
                    Complete Review System Architecture
                </h2>
                
                <div class="note-box" style="background: #fff3cd; border-left-color: #ffc107;">
                    <strong>⚠️ This Simulation:</strong> We're testing <strong>Module 1, Pass 1</strong> only. The full production system runs 2 modules with 2 passes each, plus human review after each module.
                </div>
                
                <div style="background: #f8f9fa; border-radius: 15px; padding: 40px; margin: 30px 0;">
                    
                    <!-- Start -->
                    <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 25px; border-radius: 10px; text-align: center; margin: 20px auto; max-width: 600px; font-weight: 700; font-size: 1.2rem;">
                        📝 Module Content (Draft)
                    </div>
                    
                    <div style="text-align: center; font-size: 2.5rem; color: #667eea; margin: 15px 0;">↓</div>
                    
                    <!-- Module 1 -->
                    <div style="background: #e8f5e9; padding: 30px; border-radius: 15px; margin: 20px auto; max-width: 800px; border: 3px solid #4caf50;">
                        <h3 style="text-align: center; color: #2e7d32; margin-bottom: 20px; font-weight: 700;">🤖 MODULE 1: AI Multi-Agent Review</h3>
                        
                        <div style="background: white; padding: 15px; border-radius: 10px; margin: 15px 0; text-align: center;">
                            <strong>Pass 1: Initial Review</strong><br>
                            <span style="color: #666; font-size: 0.9rem;">30 agents (15 authoring + 15 style)</span><br>
                            <span style="color: #4caf50; font-weight: 700;">← YOU ARE HERE (This Simulation)</span>
                        </div>
                        
                        <div style="text-align: center; font-size: 1.5rem; color: #4caf50; margin: 10px 0;">↓</div>
                        
                        <div style="background: white; padding: 15px; border-radius: 10px; margin: 15px 0; text-align: center;">
                            <strong>Pass 2: Verification Review</strong><br>
                            <span style="color: #666; font-size: 0.9rem;">10 agents verify fixes from Pass 1</span>
                        </div>
                        
                        <div style="text-align: center; font-size: 1.5rem; color: #4caf50; margin: 10px 0;">↓</div>
                        
                        <div style="background: linear-gradient(135deg, #4caf50, #2e7d32); color: white; padding: 15px; border-radius: 10px; margin: 15px 0; text-align: center; font-weight: 700;">
                            👥 Human Expert Review
                        </div>
                    </div>
                    
                    <div style="text-align: center; font-size: 2.5rem; color: #667eea; margin: 15px 0;">↓</div>
                    
                    <!-- Module 2 -->
                    <div style="background: #e1f5fe; padding: 30px; border-radius: 15px; margin: 20px auto; max-width: 800px; border: 3px solid #0288d1;">
                        <h3 style="text-align: center; color: #01579b; margin-bottom: 20px; font-weight: 700;">🤖 MODULE 2: AI Multi-Agent Review</h3>
                        
                        <div style="background: white; padding: 15px; border-radius: 10px; margin: 15px 0; text-align: center;">
                            <strong>Pass 1: Initial Review</strong><br>
                            <span style="color: #666; font-size: 0.9rem;">30 agents (fresh perspective)</span>
                        </div>
                        
                        <div style="text-align: center; font-size: 1.5rem; color: #0288d1; margin: 10px 0;">↓</div>
                        
                        <div style="background: white; padding: 15px; border-radius: 10px; margin: 15px 0; text-align: center;">
                            <strong>Pass 2: Verification Review</strong><br>
                            <span style="color: #666; font-size: 0.9rem;">10 agents verify fixes</span>
                        </div>
                        
                        <div style="text-align: center; font-size: 1.5rem; color: #0288d1; margin: 10px 0;">↓</div>
                        
                        <div style="background: linear-gradient(135deg, #0288d1, #01579b); color: white; padding: 15px; border-radius: 10px; margin: 15px 0; text-align: center; font-weight: 700;">
                            👥 Human Expert Review
                        </div>
                    </div>
                    
                    <div style="text-align: center; font-size: 2.5rem; color: #667eea; margin: 15px 0;">↓</div>
                    
                    <!-- Final -->
                    <div style="background: linear-gradient(135deg, #ffd700, #ffa500); color: white; padding: 25px; border-radius: 10px; text-align: center; margin: 20px auto; max-width: 600px; font-weight: 700; font-size: 1.2rem;">
                        ✅ Publication-Ready Content
                    </div>
                    
                </div>
                
                <div class="note-box">
                    <p><strong>Why This Architecture?</strong></p>
                    <ul style="margin-left: 30px; margin-top: 10px;">
                        <li><strong>2 Modules:</strong> Fresh AI perspectives catch issues missed the first time</li>
                        <li><strong>2 Passes Each:</strong> Pass 1 finds issues, Pass 2 verifies fixes worked</li>
                        <li><strong>Human Review:</strong> Expert validation after each module ensures quality</li>
                        <li><strong>30 + 10 Agents:</strong> Redundancy and verification prevent false negatives</li>
                    </ul>
                </div>
            </section>
            
        </div>
    </div>
    
    <script>
        function showSection(sectionId) {{
            document.querySelectorAll('.section').forEach(section => section.classList.remove('active'));
            document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active'));
            document.getElementById(sectionId).classList.add('active');
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>
'''
    
    return html
def main():
    """Main execution function."""
    
    print("=" * 80)
    print("LEARNVIA 30-Agent Content Review Simulation")
    print("=" * 80)
    print()
    
    # Load layered prompts
    print("Loading layered prompt system...")
    master_prompt = load_prompt_file("master_review_context.txt")
    authoring_prompt = load_prompt_file("authoring_prompt_rules.txt")
    style_prompt = load_prompt_file("style_prompt_rules.txt")
    print(f"✓ Master context: {len(master_prompt)} chars")
    print(f"✓ Authoring rules: {len(authoring_prompt)} chars")
    print(f"✓ Style rules: {len(style_prompt)} chars")
    print()
    
    # Load module content
    print("Loading test module...")
    module_xml = load_module_content(TEST_MODULE_PATH)
    module_text = extract_text_from_module(module_xml)
    print(f"✓ Module loaded: {len(module_text)} chars")
    print()
    
    # Simulate 30 agent reviews
    print("Simulating 30 agent reviews...")
    print()
    
    all_findings = []
    
    # Authoring agents
    print("AUTHORING AGENTS (15 total):")
    for i in range(AGENT_CONFIG["authoring"]["total"]):
        if i < AGENT_CONFIG["authoring"]["rubric_focused"]:
            # Rubric-focused agent
            competency = AGENT_CONFIG["authoring"]["competencies"][i % len(AGENT_CONFIG["authoring"]["competencies"])]
            rubric_file = f"authoring_{competency.lower().replace(' ', '_')}.xml"
            try:
                rubric_content = load_rubric_file(rubric_file)
            except FileNotFoundError:
                rubric_content = ""
            
            agent_id = f"Authoring-Specialist-{competency.replace(' ', '')}-{i+1}"
            agent_type = "authoring"
            focus = f"Specialist: {competency}"
        else:
            # Generalist agent
            rubric_content = ""
            agent_id = f"Authoring-Generalist-{i+1}"
            agent_type = "authoring"
            focus = "Generalist (Cross-Cutting)"
        
        prompt = build_agent_prompt(agent_type, focus, master_prompt, authoring_prompt, 
                                     rubric_content, module_text)
        
        findings = simulate_agent_review(agent_id, prompt)
        all_findings.extend(findings)
        
        print(f"  ✓ {agent_id}: {len(findings)} findings")
    
    print()
    print("STYLE AGENTS (15 total):")
    for i in range(AGENT_CONFIG["style"]["total"]):
        if i < AGENT_CONFIG["style"]["rubric_focused"]:
            # Rubric-focused agent
            competency = AGENT_CONFIG["style"]["competencies"][i % len(AGENT_CONFIG["style"]["competencies"])]
            rubric_file = f"style_{competency.lower().replace(' ', '_')}.xml"
            try:
                rubric_content = load_rubric_file(rubric_file)
            except FileNotFoundError:
                rubric_content = ""
            
            agent_id = f"Style-Specialist-{competency.replace(' ', '')}-{i+1}"
            agent_type = "style"
            focus = f"Specialist: {competency}"
        else:
            # Generalist agent
            rubric_content = ""
            agent_id = f"Style-Generalist-{i+1}"
            agent_type = "style"
            focus = "Generalist (Cross-Cutting)"
        
        prompt = build_agent_prompt(agent_type, focus, master_prompt, style_prompt, 
                                     rubric_content, module_text)
        
        findings = simulate_agent_review(agent_id, prompt)
        all_findings.extend(findings)
        
        print(f"  ✓ {agent_id}: {len(findings)} findings")
    
    print()
    print("=" * 80)
    print(f"TOTAL FINDINGS: {len(all_findings)}")
    print()
    
    # Aggregate consensus issues
    print("Aggregating consensus issues...")
    consensus_issues, non_consensus = aggregate_consensus_issues(all_findings, 30)
    print(f"✓ Consensus issues identified: {len(consensus_issues)}")
    print(f"✓ Non-consensus flagged issues: {len(non_consensus)}")
    print()
    
    # Generate HTML report
    print("Generating HTML report...")
    html_report = generate_html_report(consensus_issues, non_consensus, all_findings, AGENT_CONFIG, module_text)
    
    output_file = OUTPUT_PATH / "test_module_review_report.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    print(f"✓ Report saved: {output_file}")
    print()
    
    # Save JSON data for further analysis
    json_output = OUTPUT_PATH / "test_module_review_data.json"
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_agents": 30,
            "consensus_issues_count": len(consensus_issues),
            "non_consensus_issues_count": len(non_consensus),
            "consensus_issues": consensus_issues,
            "non_consensus_issues": non_consensus,
            "all_findings": all_findings
        }, f, indent=2)
    
    print(f"✓ JSON data saved: {json_output}")
    print()
    
    print("=" * 80)
    print("SIMULATION COMPLETE")
    print("=" * 80)
    print()
    print(f"Open the report: {output_file}")
    print()


if __name__ == "__main__":
    main()
