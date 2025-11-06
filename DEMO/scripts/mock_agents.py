"""
Mock agent system for demo purposes.
Generates diverse individual agent feedback to be aggregated by consensus system.
"""

import re
import random
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

# Import the aggregator models
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.models import ReviewFeedback, SeverityLevel, ReviewPass


class AgentPersona:
    """Different agent personalities that affect what they catch."""
    STRICT = "strict"  # Catches everything
    MODERATE = "moderate"  # Catches most things
    LENIENT = "lenient"  # Misses some issues
    SPECIALIST = "specialist"  # Deep expertise in specific area
    GENERALIST = "generalist"  # Broad but shallow


class MockAgentSystem:
    """Simulates 60 individual AI reviewers with varying perspectives."""

    def __init__(self):
        # Pass 1: 20 content+style agents
        self.pass1_agents = self._create_agent_pool("content_p1", 20)
        # Pass 2: Different 20 content+style agents
        self.pass2_agents = self._create_agent_pool("content_p2", 20)
        # Pass 3: 10 copy edit agents
        self.pass3_agents = self._create_agent_pool("copy_p1", 10)
        # Pass 4: Different 10 copy edit agents
        self.pass4_agents = self._create_agent_pool("copy_p2", 10)

    def _create_agent_pool(self, prefix: str, count: int) -> List[Dict]:
        """Create a pool of agents with varying characteristics."""
        agents = []
        for i in range(1, count + 1):
            if "copy" in prefix:
                # Copy edit agents are more uniform but vary in strictness
                persona = random.choice([AgentPersona.STRICT, AgentPersona.STRICT,
                                       AgentPersona.MODERATE, AgentPersona.SPECIALIST])
            else:
                # Content agents have more variety
                persona = random.choice([AgentPersona.STRICT, AgentPersona.MODERATE,
                                       AgentPersona.LENIENT, AgentPersona.SPECIALIST,
                                       AgentPersona.GENERALIST])

            agents.append({
                "id": f"{prefix}_agent_{i:02d}",
                "persona": persona,
                "focus_areas": self._assign_focus_areas(persona, prefix),
                "detection_rate": self._get_detection_rate(persona)
            })
        return agents

    def _assign_focus_areas(self, persona: str, prefix: str) -> List[str]:
        """Assign focus areas based on agent persona."""
        if "copy" in prefix:
            return ["contractions", "voice", "formatting", "punctuation", "consistency"]

        if persona == AgentPersona.SPECIALIST:
            # Specialist focuses deeply on 1-2 areas
            return random.sample(["math_accuracy", "pedagogical_flow", "examples",
                                 "scaffolding", "framing", "quiz"], k=2)
        elif persona == AgentPersona.GENERALIST:
            # Generalist covers everything lightly
            return ["general", "clarity", "structure", "flow"]
        else:
            # Others have balanced coverage
            return ["math_accuracy", "pedagogical_flow", "examples", "style", "clarity"]

    def _get_detection_rate(self, persona: str) -> float:
        """Get the probability this agent will catch an issue."""
        rates = {
            AgentPersona.STRICT: 0.95,
            AgentPersona.MODERATE: 0.75,
            AgentPersona.LENIENT: 0.55,
            AgentPersona.SPECIALIST: 0.90,  # High in their area
            AgentPersona.GENERALIST: 0.65
        }
        return rates.get(persona, 0.70)

    def analyze_content(self, content: str, pass_number: int) -> List[ReviewFeedback]:
        """Generate individual agent feedback for aggregation."""
        all_feedback = []

        # Get the right agent pool
        if pass_number == 1:
            agents = self.pass1_agents
            review_pass = ReviewPass.CONTENT_PASS_1
        elif pass_number == 2:
            agents = self.pass2_agents
            review_pass = ReviewPass.CONTENT_PASS_2
        elif pass_number == 3:
            agents = self.pass3_agents
            review_pass = ReviewPass.COPY_PASS_1
        else:
            agents = self.pass4_agents
            review_pass = ReviewPass.COPY_PASS_2

        # Find all issues in the content
        if pass_number in [1, 2]:
            issues = self._find_content_issues(content, pass_number)
        else:
            issues = self._find_copy_edit_issues(content, pass_number)

        # Each agent independently reviews and may catch different issues
        for agent in agents:
            agent_feedback = self._agent_review(agent, issues, content)
            all_feedback.extend(agent_feedback)

        return all_feedback

    def _find_content_issues(self, content: str, pass_num: int) -> List[Dict]:
        """Find all potential content issues in the text."""
        issues = []
        lines = content.split('\n')

        # CRITICAL ISSUES (Severity 5)

        # Incorrect mathematical formula
        if "d/dx(x^n) = n * x^n-1" in content:
            issues.append({
                "type": "math_accuracy",
                "severity": SeverityLevel.CRITICAL,
                "location": "Line 13",
                "issue": "Incorrect mathematical notation: x^n-1 should be x^(n-1)",
                "suggestion": "Use proper notation: d/dx(x^n) = nx^(n-1)"
            })

        # Wrong formula given
        if "d/dx(x^n) = n * x^(n+1)" in content:
            issues.append({
                "type": "math_accuracy",
                "severity": SeverityLevel.CRITICAL,
                "location": "Line 16",
                "issue": "CRITICAL ERROR: Formula shows n*x^(n+1) instead of nx^(n-1)",
                "suggestion": "Correct to: d/dx(x^n) = nx^(n-1)"
            })

        # Incorrect calculation in example
        if "Multiply by 3: 3x^3" in content:
            issues.append({
                "type": "math_accuracy",
                "severity": SeverityLevel.CRITICAL,
                "location": "Line 34",
                "issue": "Incorrect step: should keep x^3 and change to x^2, not multiply to get 3x^3",
                "suggestion": "Step should be: 'Multiply by 3 and reduce exponent: 3x^2'"
            })

        # Wrong derivative examples
        if "If f(x) = x^6, then f'(x) = 6x^5" in content and "Then it'd be 5x^5" in content:
            issues.append({
                "type": "math_accuracy",
                "severity": SeverityLevel.CRITICAL,
                "location": "Line 46",
                "issue": "Confusing incorrect calculation shown before correction",
                "suggestion": "Remove the incorrect attempt or clearly mark it as a common error"
            })

        # HIGH SEVERITY ISSUES (Severity 4)

        # Framing too short
        framing_match = re.search(r'## Framing\n\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if framing_match:
            framing_text = framing_match.group(1)
            word_count = len(framing_text.split())
            if word_count < 100:
                issues.append({
                    "type": "framing_length",
                    "severity": SeverityLevel.HIGH,
                    "location": "Framing section",
                    "issue": f"Framing is only {word_count} words, should be 100-150",
                    "suggestion": "Expand framing to meet length requirements"
                })

        # Poor pedagogical explanation
        if "Trust me on this one" in content:
            issues.append({
                "type": "pedagogical_flow",
                "severity": SeverityLevel.HIGH,
                "location": "Line 22",
                "issue": "Dismissive explanation without proper justification",
                "suggestion": "Provide intuitive explanation or reference to where proof can be found"
            })

        # Missing homework section structure
        if "## Homework" not in content:
            issues.append({
                "type": "missing_component",
                "severity": SeverityLevel.HIGH,
                "location": "Document structure",
                "issue": "Missing proper Homework section heading",
                "suggestion": "Add ## Homework section"
            })

        # Quiz answers revealed
        if "(Answer should be b" in content or "The answer is obviously false" in content:
            issues.append({
                "type": "quiz_structure",
                "severity": SeverityLevel.HIGH,
                "location": "Quiz section",
                "issue": "Quiz answers or hints given in questions",
                "suggestion": "Remove answers and hints from quiz questions"
            })

        # MEDIUM SEVERITY ISSUES (Severity 3)

        # Missing LaTeX formatting
        for i, line in enumerate(lines, 1):
            # Check for unformatted math expressions
            if re.search(r'(?<![`$])x\d(?![`$])', line) and not line.strip().startswith('#'):
                issues.append({
                    "type": "formatting",
                    "severity": SeverityLevel.MEDIUM,
                    "location": f"Line {i}",
                    "issue": f"Mathematical variable not in LaTeX: {line[:50]}",
                    "suggestion": "Use LaTeX notation for all mathematical expressions"
                })

            if "x^n-1" in line and "$" not in line:
                issues.append({
                    "type": "formatting",
                    "severity": SeverityLevel.MEDIUM,
                    "location": f"Line {i}",
                    "issue": "Expression x^n-1 should be in LaTeX as $x^{n-1}$",
                    "suggestion": "Format as $x^{n-1}$ for clarity"
                })

        # Inconsistent terminology
        if "sqrt(x)" in content and "√x" in content:
            issues.append({
                "type": "consistency",
                "severity": SeverityLevel.MEDIUM,
                "location": "Throughout document",
                "issue": "Inconsistent notation: both sqrt(x) and √x used",
                "suggestion": "Choose one notation and use consistently"
            })

        # Unclear explanations
        if "kinda complicated" in content or "don't worry about that" in content:
            issues.append({
                "type": "clarity",
                "severity": SeverityLevel.MEDIUM,
                "location": "Explanation sections",
                "issue": "Informal language that may undermine content",
                "suggestion": "Use more professional language"
            })

        # LOW SEVERITY ISSUES (Severity 2)

        # Contractions (many!)
        contractions = ["don't", "doesn't", "won't", "can't", "let's", "it's",
                       "isn't", "aren't", "we'll", "you'll", "they'll", "we're",
                       "you're", "they're", "I'd", "we'd", "that's", "here's"]

        for i, line in enumerate(lines, 1):
            for contraction in contractions:
                if contraction in line.lower():
                    issues.append({
                        "type": "style_contractions",
                        "severity": SeverityLevel.LOW,
                        "location": f"Line {i}",
                        "issue": f"Contraction '{contraction}' found",
                        "suggestion": f"Replace with expanded form"
                    })

        # Imperative voice
        imperative_patterns = [
            (r'^(Find|Calculate|Try|Think|Look|Remember|Use)', "Direct command"),
            (r'(Remember to|Make sure|Be sure to)', "Directive phrase"),
            (r'^(Complete|Graph|Create|Derive|Explain)', "Assignment command")
        ]

        for i, line in enumerate(lines, 1):
            for pattern, desc in imperative_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        "type": "voice",
                        "severity": SeverityLevel.LOW,
                        "location": f"Line {i}",
                        "issue": f"Imperative voice: {desc}",
                        "suggestion": "Rephrase to avoid direct commands"
                    })

        # MINOR SEVERITY ISSUES (Severity 1)

        # Punctuation and style preferences
        if "!!" in content:
            issues.append({
                "type": "punctuation",
                "severity": SeverityLevel.MINOR,
                "location": "Multiple locations",
                "issue": "Multiple exclamation marks",
                "suggestion": "Use single exclamation mark"
            })

        if "..." in content:
            issues.append({
                "type": "punctuation",
                "severity": SeverityLevel.MINOR,
                "location": "Multiple locations",
                "issue": "Ellipsis usage",
                "suggestion": "Consider removing ellipsis for clarity"
            })

        return issues

    def _find_copy_edit_issues(self, content: str, pass_num: int) -> List[Dict]:
        """Find copy editing issues (style guide compliance)."""
        issues = []
        lines = content.split('\n')

        # Be EXTREMELY strict in copy edit passes

        # Every single contraction
        contractions_map = {
            "don't": "do not", "doesn't": "does not", "won't": "will not",
            "can't": "cannot", "let's": "let us", "it's": "it is",
            "isn't": "is not", "aren't": "are not", "we'll": "we will",
            "you'll": "you will", "they'll": "they will", "we're": "we are",
            "you're": "you are", "they're": "they are", "I'd": "I would",
            "we'd": "we would", "that's": "that is", "here's": "here is",
            "there's": "there is", "what's": "what is", "who's": "who is",
            "didn't": "did not", "hadn't": "had not", "hasn't": "has not",
            "haven't": "have not", "shouldn't": "should not", "wouldn't": "would not",
            "couldn't": "could not", "mustn't": "must not"
        }

        for i, line in enumerate(lines, 1):
            for contraction, replacement in contractions_map.items():
                # Check both lowercase and capitalized
                if contraction in line or contraction.capitalize() in line:
                    severity = SeverityLevel.HIGH if pass_num == 3 else SeverityLevel.CRITICAL
                    issues.append({
                        "type": "contraction",
                        "severity": severity,
                        "location": f"Line {i}",
                        "issue": f"Contraction '{contraction}' violates style guide",
                        "suggestion": f"Must replace with '{replacement}'"
                    })

        # Every instance of imperative voice
        for i, line in enumerate(lines, 1):
            # Check for imperatives at start of sentences
            if re.search(r'(?:^|\. )(Find|Calculate|Try|Think|Look|Remember|Use|Apply|Complete|Graph|Create|Derive|Explain|Show|Prove)\b', line):
                issues.append({
                    "type": "imperative_voice",
                    "severity": SeverityLevel.HIGH,
                    "location": f"Line {i}",
                    "issue": "Imperative voice violates style guide",
                    "suggestion": "Rephrase using passive voice or descriptive language"
                })

        # Check for informal language
        informal_terms = ["kinda", "gonna", "wanna", "gotta", "sorta", "yeah",
                         "okay", "ok", "cool", "awesome", "stuff", "things", "super"]
        for i, line in enumerate(lines, 1):
            for term in informal_terms:
                if term in line.lower():
                    issues.append({
                        "type": "informal_language",
                        "severity": SeverityLevel.MEDIUM,
                        "location": f"Line {i}",
                        "issue": f"Informal term '{term}' found",
                        "suggestion": "Use formal academic language"
                    })

        # LaTeX formatting compliance
        math_patterns = [
            (r'(?<![`$])\b[xymn]\^\d+(?![`$])', "Exponent not in LaTeX"),
            (r'(?<![`$])\bx\d+(?![`$])', "Variable with subscript not in LaTeX"),
            (r'(?<![`$])\d+/\d+(?![`$])', "Fraction not in LaTeX"),
        ]

        for i, line in enumerate(lines, 1):
            for pattern, issue_desc in math_patterns:
                if re.search(pattern, line):
                    issues.append({
                        "type": "latex_formatting",
                        "severity": SeverityLevel.HIGH,
                        "location": f"Line {i}",
                        "issue": issue_desc,
                        "suggestion": "All mathematical expressions must use LaTeX notation"
                    })

        # Consistency checks
        if "x^(n-1)" in content and "x^{n-1}" in content:
            issues.append({
                "type": "notation_consistency",
                "severity": SeverityLevel.MEDIUM,
                "location": "Throughout",
                "issue": "Inconsistent LaTeX notation style",
                "suggestion": "Use consistent LaTeX formatting"
            })

        return issues

    def _agent_review(self, agent: Dict, all_issues: List[Dict], content: str) -> List[ReviewFeedback]:
        """Simulate an individual agent's review."""
        feedback = []

        for issue in all_issues:
            # Check if this agent would catch this issue
            catch_probability = agent["detection_rate"]

            # Adjust probability based on agent's focus areas
            if issue["type"] in agent["focus_areas"]:
                catch_probability = min(1.0, catch_probability * 1.3)
            elif agent["persona"] == AgentPersona.SPECIALIST and issue["type"] not in agent["focus_areas"]:
                catch_probability *= 0.5

            # Randomly determine if agent catches this issue
            if random.random() < catch_probability:
                # Add some variation to the feedback
                suggestion = issue["suggestion"]
                if random.random() < 0.3:  # 30% chance of different wording
                    suggestion = self._vary_suggestion(suggestion)

                feedback.append(ReviewFeedback(
                    reviewer_id=agent["id"],
                    issue_type=issue["type"],
                    severity=issue["severity"],
                    location=issue["location"],
                    issue=issue["issue"],
                    suggestion=suggestion,
                    timestamp=datetime.now()
                ))

        # Occasionally add false positives (agent thinks there's an issue when there isn't)
        if agent["persona"] == AgentPersona.STRICT and random.random() < 0.1:
            feedback.append(self._generate_false_positive(agent["id"]))

        return feedback

    def _vary_suggestion(self, original: str) -> str:
        """Create variation in suggestion wording."""
        variations = {
            "Replace with": ["Change to", "Should be", "Correct to"],
            "Must": ["Should", "Need to", "Required to"],
            "Use": ["Apply", "Implement", "Utilize"],
            "Remove": ["Delete", "Eliminate", "Take out"]
        }

        result = original
        for key, alternatives in variations.items():
            if key in result and random.random() < 0.5:
                result = result.replace(key, random.choice(alternatives))

        return result

    def _generate_false_positive(self, agent_id: str) -> ReviewFeedback:
        """Generate a false positive (overly strict agent)."""
        false_positives = [
            {
                "type": "style_preference",
                "severity": SeverityLevel.MINOR,
                "location": "Line 24",
                "issue": "Sentence could be more concise",
                "suggestion": "Consider rewording for brevity"
            },
            {
                "type": "formatting",
                "severity": SeverityLevel.MINOR,
                "location": "Line 67",
                "issue": "Paragraph might be too long",
                "suggestion": "Consider breaking into smaller paragraphs"
            }
        ]

        fp = random.choice(false_positives)
        return ReviewFeedback(
            reviewer_id=agent_id,
            issue_type=fp["type"],
            severity=fp["severity"],
            location=fp["location"],
            issue=fp["issue"],
            suggestion=fp["suggestion"],
            timestamp=datetime.now()
        )

    def generate_statistics(self, feedback: List[ReviewFeedback]) -> Dict[str, Any]:
        """Generate statistics about the feedback."""
        stats = {
            "total_issues": len(feedback),
            "unique_issues": len(set((f.issue_type, f.location) for f in feedback)),
            "by_severity": {},
            "by_type": {},
            "agent_agreement": {}
        }

        # Count by severity
        for level in [SeverityLevel.CRITICAL, SeverityLevel.HIGH, SeverityLevel.MEDIUM,
                     SeverityLevel.LOW, SeverityLevel.MINOR]:
            count = len([f for f in feedback if f.severity == level])
            stats["by_severity"][level] = count

        # Count by type
        for f in feedback:
            stats["by_type"][f.issue_type] = stats["by_type"].get(f.issue_type, 0) + 1

        # Calculate agreement (how many agents found same issue)
        issue_counts = {}
        for f in feedback:
            key = (f.issue_type, f.location)
            issue_counts[key] = issue_counts.get(key, 0) + 1

        stats["agent_agreement"] = {
            "high_agreement": len([k for k, v in issue_counts.items() if v >= 15]),
            "medium_agreement": len([k for k, v in issue_counts.items() if 5 <= v < 15]),
            "low_agreement": len([k for k, v in issue_counts.items() if v < 5])
        }

        return stats