"""
Mock API client for demonstration purposes.
Simulates OpenAI API responses without actual API calls.
"""

import json
import random
import asyncio
from typing import Dict, Any


class MockOpenAI:
    """Mock OpenAI module for testing without API key."""

    class ChatCompletion:
        @staticmethod
        def create(**kwargs):
            """Simulate API response."""
            # Generate mock issues based on review focus
            focus = kwargs.get('messages', [{}])[1].get('content', '')

            issues = []

            if 'authoring' in focus.lower() or 'pedagogical' in focus.lower():
                issues.extend([
                    {
                        "type": "concept_jump",
                        "severity": 4,
                        "location": "Between examples 2 and 3",
                        "issue": "Large conceptual jump without intermediate steps",
                        "suggestion": "Add an intermediate example to bridge the gap"
                    },
                    {
                        "type": "missing_concrete_examples",
                        "severity": 3,
                        "location": "Section 2",
                        "issue": "Abstract concept without student-relevant examples",
                        "suggestion": "Add real-world examples students can relate to"
                    }
                ])

            if 'style' in focus.lower() or 'contraction' in focus.lower():
                issues.extend([
                    {
                        "type": "contraction",
                        "severity": 2,
                        "location": "Line 15",
                        "issue": "Uses contraction 'don't'",
                        "suggestion": "Replace with 'do not'"
                    },
                    {
                        "type": "imperative",
                        "severity": 2,
                        "location": "Paragraph 3",
                        "issue": "Improper use of imperative 'Find the equation'",
                        "suggestion": "Rephrase as 'The equation is...'"
                    }
                ])

            if 'mathematical' in focus.lower():
                issues.append({
                    "type": "latex_formatting",
                    "severity": 2,
                    "location": "Example 1",
                    "issue": "Number not in LaTeX format",
                    "suggestion": "Use LaTeX for all mathematical expressions"
                })

            # Simulate response object
            class Message:
                def __init__(self, content):
                    self.content = content

            class Choice:
                def __init__(self, message):
                    self.message = message

            class Response:
                def __init__(self, choices):
                    self.choices = choices

            return Response([Choice(Message(json.dumps({"issues": issues})))])

    class error:
        """Mock error classes."""
        class RateLimitError(Exception):
            pass


# Replace openai import in reviewers.py with this mock
openai = MockOpenAI()