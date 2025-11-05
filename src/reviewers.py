"""
AI Reviewer implementation for Learnvia content revision system.
Handles individual reviewers and their interaction with the OpenAI API.
"""

import asyncio
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import time
import os
from dataclasses import dataclass

# Try to import openai, fall back to mock if not available
try:
    import openai
except ImportError:
    from .mock_api import openai

from .models import (
    ReviewerConfig, ReviewerRole, ReviewPass,
    ReviewFeedback, ModuleContent, SeverityLevel
)


class APIClient:
    """Handles communication with the OpenAI API."""

    def __init__(self, api_key: Optional[str] = None, max_retries: int = 3,
                 retry_delay: float = 1.0):
        """Initialize API client with key and retry settings."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or "mock_api_key"

        # Only require real API key if not using mock
        if hasattr(openai, 'api_key'):
            if not self.api_key or self.api_key == "mock_api_key":
                print("⚠️  No OpenAI API key found. Using mock API for demonstration.")
            openai.api_key = self.api_key

        self.max_retries = max_retries
        self.retry_delay = retry_delay

    async def call_api_async(self, prompt: str, system_prompt: str,
                             temperature: float = 0.7,
                             max_tokens: int = 2000) -> Dict[str, Any]:
        """Make an async API call with retry logic."""
        for attempt in range(self.max_retries):
            try:
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=temperature,
                        max_tokens=max_tokens,
                        response_format={"type": "json_object"}
                    )
                )

                content = response.choices[0].message.content
                return json.loads(content)

            except openai.error.RateLimitError:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
                else:
                    raise

            except json.JSONDecodeError as e:
                # Try to extract JSON from the response
                if 'content' in locals():
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                raise e

            except Exception as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                else:
                    raise e

    def call_api(self, prompt: str, system_prompt: str,
                 temperature: float = 0.7,
                 max_tokens: int = 2000) -> Dict[str, Any]:
        """Synchronous API call wrapper."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                self.call_api_async(prompt, system_prompt, temperature, max_tokens)
            )
        finally:
            loop.close()

    def validate_response(self, response: Dict[str, Any]) -> bool:
        """Validate that the API response has the expected structure."""
        return "issues" in response and isinstance(response["issues"], list)


class BaseReviewer:
    """Base class for all AI reviewers."""

    def __init__(self, config: ReviewerConfig, api_client: Optional[APIClient] = None):
        """Initialize reviewer with configuration."""
        self.config = config
        self.api_client = api_client or APIClient()

    def generate_system_prompt(self) -> str:
        """Generate the system prompt for this reviewer."""
        # Load the appropriate guidelines
        if self.config.role == ReviewerRole.AUTHORING:
            guidelines_path = "/Users/michaeljoyce/Desktop/LEARNVIA/authoring_prompt_rules.txt"
        else:
            guidelines_path = "/Users/michaeljoyce/Desktop/LEARNVIA/style_prompt_rules.txt"

        vision_path = "/Users/michaeljoyce/Desktop/LEARNVIA/product_vision_context.txt"

        try:
            with open(guidelines_path, 'r') as f:
                guidelines = f.read()
            with open(vision_path, 'r') as f:
                product_vision = f.read()
        except FileNotFoundError:
            guidelines = "Guidelines not found"
            product_vision = "Product vision not found"

        return self.config.get_system_prompt(product_vision, guidelines)

    def generate_prompt(self, module: ModuleContent) -> str:
        """Generate the review prompt for a module."""
        prompt = f"""Review the following educational module content:

MODULE CONTENT:
{module.content}

FOCUS AREA: {self.config.focus_area}

Please identify issues related to your focus area. For each issue found, provide:
1. Issue type (specific category)
2. Severity (1-5, where 5 is critical)
3. Location (paragraph, line, or section reference)
4. Specific issue description
5. Actionable suggestion for improvement

Format your response as JSON with the following structure:
{{
    "issues": [
        {{
            "type": "issue_type",
            "severity": <1-5>,
            "location": "specific location",
            "issue": "description of the issue",
            "suggestion": "how to fix it"
        }}
    ]
}}

Remember to evaluate from the perspective of a student studying home alone with low confidence and limited time.
"""
        # Add prompt variation if specified
        if self.config.prompt_variation:
            prompt += f"\n\nAdditional focus: {self.config.prompt_variation}\n"

        return prompt

    async def review_async(self, module: ModuleContent) -> List[ReviewFeedback]:
        """Perform async review of a module."""
        system_prompt = self.generate_system_prompt()
        prompt = self.generate_prompt(module)

        try:
            response = await self.api_client.call_api_async(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )

            if self.api_client.validate_response(response):
                return self.parse_response(response)
            else:
                return []

        except Exception as e:
            print(f"Error in reviewer {self.config.reviewer_id}: {str(e)}")
            return []

    def parse_response(self, response: Dict[str, Any]) -> List[ReviewFeedback]:
        """Parse API response into ReviewFeedback objects."""
        feedback_list = []

        for issue in response.get("issues", []):
            feedback = ReviewFeedback(
                reviewer_id=self.config.reviewer_id,
                issue_type=issue.get("type", "unknown"),
                severity=issue.get("severity", 1),
                location=issue.get("location", "unspecified"),
                issue=issue.get("issue", ""),
                suggestion=issue.get("suggestion", "")
            )
            feedback_list.append(feedback)

        return feedback_list


class AuthoringReviewer(BaseReviewer):
    """Specialized reviewer for authoring guidelines."""

    def check_structural_requirements(self, module: ModuleContent) -> List[str]:
        """Check if module has required structural components."""
        issues = []

        required_components = ["framing", "lesson", "examples", "quiz"]

        for component in required_components:
            if component not in module.components or not module.components[component]:
                issues.append(f"Missing required component: {component}")

        # Check framing word count
        if "framing" in module.components:
            framing_words = len(module.components["framing"].split())
            if framing_words < 100 or framing_words > 150:
                issues.append(f"Framing text should be 100-150 words (found {framing_words})")

        return issues

    def generate_prompt(self, module: ModuleContent) -> str:
        """Generate authoring-specific review prompt."""
        base_prompt = super().generate_prompt(module)

        # Add structural checks
        structural_issues = self.check_structural_requirements(module)
        if structural_issues:
            base_prompt += f"\n\nStructural issues detected:\n" + "\n".join(structural_issues)

        # Add focus-specific instructions
        if "pedagogical" in self.config.focus_area.lower():
            base_prompt += """
Focus specifically on:
- Chunking: Are concepts broken down into digestible pieces?
- Scaffolding: Does complexity build gradually?
- Alignment: Does content align with learning objectives?
- Engagement: Are there interactive elements every few minutes?
"""
        elif "example" in self.config.focus_area.lower():
            base_prompt += """
Focus specifically on:
- Mathematical correctness of examples
- Progression from simple to complex
- Student relevance of examples
- Clarity of explanations
"""
        elif "quiz" in self.config.focus_area.lower():
            base_prompt += """
Focus specifically on:
- Question clarity and brevity
- Feedback quality for each answer choice
- Progression of difficulty
- Targeting of common misconceptions
"""

        return base_prompt


class StyleReviewer(BaseReviewer):
    """Specialized reviewer for style guide compliance."""

    def detect_contractions(self, content: str) -> List[str]:
        """Detect contractions in content."""
        # Common contractions to check for
        contractions_pattern = r"\b(don't|doesn't|didn't|won't|wouldn't|can't|couldn't|shouldn't|isn't|aren't|wasn't|weren't|haven't|hasn't|hadn't|let's|that's|what's|it's|he's|she's|they're|we're|you're|I'm|they've|we've|you've|I've|they'd|we'd|you'd|I'd|they'll|we'll|you'll|I'll)\b"

        matches = re.finditer(contractions_pattern, content, re.IGNORECASE)
        return [match.group() for match in matches]

    def detect_imperatives(self, content: str) -> List[str]:
        """Detect improper use of imperative voice."""
        # Common imperative verbs at the start of sentences
        imperative_pattern = r"(?:^|\. )([A-Z][a-z]*) (?:the |a |an )"

        imperatives = []
        common_imperatives = [
            "Find", "Calculate", "Determine", "Solve", "Compute",
            "State", "Write", "Draw", "Plot", "Graph", "Show",
            "Prove", "Derive", "Simplify", "Factor", "Expand"
        ]

        sentences = content.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            for verb in common_imperatives:
                if sentence.startswith(verb + " "):
                    imperatives.append(verb)

        return imperatives

    def generate_prompt(self, module: ModuleContent) -> str:
        """Generate style-specific review prompt."""
        base_prompt = super().generate_prompt(module)

        # Add automatic detection results
        contractions = self.detect_contractions(module.content)
        if contractions:
            base_prompt += f"\n\nContractions detected: {', '.join(set(contractions))}"

        imperatives = self.detect_imperatives(module.content)
        if imperatives:
            base_prompt += f"\n\nPossible imperatives detected: {', '.join(set(imperatives))}"

        # Add focus-specific instructions
        if "contraction" in self.config.focus_area.lower():
            base_prompt += """
Focus specifically on:
- Identifying ALL contractions (don't, won't, let's, etc.)
- Suggesting replacements without contractions
- Note: Possessives (square's area) are allowed
"""
        elif "imperative" in self.config.focus_area.lower():
            base_prompt += """
Focus specifically on:
- Improper use of imperative voice in general instruction
- Remember: Imperatives ARE allowed in questions and procedures
- Suggest rephrasing to avoid commands
"""
        elif "mathematical" in self.config.focus_area.lower():
            base_prompt += """
Focus specifically on:
- LaTeX formatting for all math and numbers
- Proper spacing in coordinates (14, 20)
- Units formatting (5\\text{ cm})
- Punctuation inside LaTeX
"""

        return base_prompt


class ReviewerPool:
    """Manages a pool of reviewers for a specific review pass."""

    def __init__(self, review_pass: ReviewPass, num_reviewers: int,
                 api_client: Optional[APIClient] = None):
        """Initialize a pool of reviewers."""
        self.review_pass = review_pass
        self.num_reviewers = num_reviewers
        self.api_client = api_client or APIClient()
        self.reviewers = self._create_reviewers()

    def _create_reviewers(self) -> List[BaseReviewer]:
        """Create the configured set of reviewers for 4-pass system.

        PASS 1 & 2: 20 agents each - Mixed content + style review
        PASS 3 & 4: 10 agents each - Pure copy edit (style only)

        Each pass uses DIFFERENT reviewers (no information transfer).
        """
        reviewers = []

        if self.review_pass in [ReviewPass.CONTENT_PASS_1, ReviewPass.CONTENT_PASS_2]:
            # CONTENT REVIEW PASSES: 20 reviewers with STRICT separation
            # 10 agents use ONLY authoring guidelines
            # 10 agents use ONLY style guidelines
            # NO mixed reviewing - each agent has single focus

            # Determine reviewer ID prefix based on pass
            pass_prefix = "content_p1" if self.review_pass == ReviewPass.CONTENT_PASS_1 else "content_p2"

            # 10 STRICTLY authoring-focused (ONLY pedagogical guidelines)
            authoring_areas = (
                ["pedagogical_flow"] * 3 +
                ["component_alignment"] * 2 +
                ["examples"] * 2 +
                ["quiz_questions"] * 2 +
                ["scaffolding"] * 1
            )

            # 10 STRICTLY style-focused (ONLY style guidelines)
            style_areas = (
                ["style_compliance"] * 2 +
                ["contractions_imperatives"] * 2 +
                ["mathematical_notation"] * 2 +
                ["clarity"] * 2 +
                ["punctuation"] * 1 +
                ["formatting"] * 1
            )

            # Create STRICTLY authoring-only reviewers
            for i, area in enumerate(authoring_areas[:10]):
                config = ReviewerConfig(
                    reviewer_id=f"{pass_prefix}_auth_{i:02d}",
                    role=ReviewerRole.AUTHORING,
                    review_pass=self.review_pass,
                    focus_area=area,
                    prompt_variation="Focus ONLY on pedagogical quality. Do NOT evaluate style or mechanics. Focus on content quality, not author evaluation.",
                    temperature=0.6 + (i % 3) * 0.1,
                    max_tokens=2000
                )
                reviewers.append(AuthoringReviewer(config, self.api_client))

            # Create STRICTLY style-only reviewers
            for i, area in enumerate(style_areas[:10]):
                config = ReviewerConfig(
                    reviewer_id=f"{pass_prefix}_style_{i:02d}",
                    role=ReviewerRole.STYLE,
                    review_pass=self.review_pass,
                    focus_area=area,
                    prompt_variation="Focus ONLY on style and mechanical issues. Do NOT evaluate pedagogical content. Focus on content quality, not author evaluation.",
                    temperature=0.6 + (i % 3) * 0.1,
                    max_tokens=2000
                )
                reviewers.append(StyleReviewer(config, self.api_client))

        else:  # ReviewPass.COPY_PASS_1 or ReviewPass.COPY_PASS_2
            # COPY EDIT PASSES: 10 reviewers doing PURE style/mechanical
            # Apply ONLY style_prompt_rules.txt (NO authoring evaluation)

            # Determine reviewer ID prefix based on pass
            pass_prefix = "copy_p1" if self.review_pass == ReviewPass.COPY_PASS_1 else "copy_p2"

            focus_areas = (
                ["contractions"] * 2 +
                ["imperatives"] * 2 +
                ["mathematical_notation"] * 2 +
                ["punctuation"] * 1 +
                ["formatting"] * 2 +
                ["consistency"] * 1
            )

            for i, area in enumerate(focus_areas[:10]):
                config = ReviewerConfig(
                    reviewer_id=f"{pass_prefix}_{i:02d}",
                    role=ReviewerRole.STYLE,
                    review_pass=self.review_pass,
                    focus_area=area,
                    prompt_variation="Focus ONLY on mechanical/style issues. Do NOT evaluate pedagogical content. Focus on content quality, not author evaluation.",
                    temperature=0.6 + (i % 3) * 0.1,
                    max_tokens=2000
                )
                reviewers.append(StyleReviewer(config, self.api_client))

        return reviewers

    async def review_parallel(self, module: ModuleContent) -> List[ReviewFeedback]:
        """Execute all reviewers in parallel and collect feedback."""
        tasks = [reviewer.review_async(module) for reviewer in self.reviewers]

        # Execute all reviews in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Flatten results and handle errors
        all_feedback = []
        for result in results:
            if isinstance(result, Exception):
                print(f"Reviewer error: {result}")
            elif isinstance(result, list):
                all_feedback.extend(result)

        return all_feedback

    def review(self, module: ModuleContent) -> List[ReviewFeedback]:
        """Synchronous wrapper for parallel review."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.review_parallel(module))
        finally:
            loop.close()