"""
AI Reviewer implementation for Learnvia content revision system.
Handles individual reviewers and their interaction with the OpenAI API.
Supports both XML-based configuration and legacy text-based prompts.
"""

import asyncio
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import time
import os
from dataclasses import dataclass
from enum import Enum


def get_project_root() -> Path:
    """Get the project root directory (LEARNVIA/).

    This works regardless of where the code is run from, making it
    portable for any git clone of the repository.

    Returns:
        Path to the LEARNVIA project root
    """
    # Start from this file's directory (CODE/)
    current_file = Path(__file__).resolve()
    code_dir = current_file.parent

    # Project root is parent of CODE/
    project_root = code_dir.parent

    # Verify we found the right directory
    if not (project_root / "NAVIGATION.md").exists():
        # Fallback: search upwards for NAVIGATION.md
        search_dir = code_dir
        for _ in range(5):  # Search up to 5 levels
            if (search_dir / "NAVIGATION.md").exists():
                return search_dir
            search_dir = search_dir.parent
        raise RuntimeError("Could not find LEARNVIA project root. Expected NAVIGATION.md to exist.")

    return project_root

# Try to import openai, fall back to mock if not available
try:
    import openai
except ImportError:
    from .mock_api import openai

from .models import (
    ReviewerConfig, ReviewerRole, ReviewPass,
    ReviewFeedback, ModuleContent, SeverityLevel
)


class ConfigMode(Enum):
    """Configuration mode for the reviewer system."""
    XML = "xml"  # Use XML-based configuration
    TEXT = "text"  # Use legacy text-based configuration
    AUTO = "auto"  # Automatically detect based on available files


@dataclass
class AgentType:
    """Configuration for agent type (rubric-focused or generalist)."""
    type: str  # "rubric_focused" or "generalist"
    competency: Optional[str] = None  # For rubric-focused agents
    focus_weight: float = 0.8  # Attention weight for rubric


class XMLConfigLoader:
    """Loads and parses XML configuration files for reviewers."""

    def __init__(self, config_dir: Optional[str] = None):
        """Initialize the XML configuration loader.

        Args:
            config_dir: Path to the configuration directory.
                       If None, uses ACTIVE_CONFIG/ in project root (recommended).
        """
        if config_dir is None:
            project_root = get_project_root()
            config_dir = str(project_root / "ACTIVE_CONFIG")

        self.config_dir = Path(config_dir)
        self.rubrics_dir = self.config_dir / "rubrics"
        self.templates_dir = self.config_dir / "templates"
        self._cache = {}

        # Map competency names to rubric files
        self.competency_to_file = {
            "Structural Integrity": "authoring_structural_integrity.xml",
            "Pedagogical Flow": "authoring_pedagogical_flow.xml",
            "Conceptual Clarity": "authoring_conceptual_clarity.xml",
            "Assessment Quality": "authoring_assessment_quality.xml",
            "Student Engagement": "authoring_student_engagement.xml",
            "Mechanical Compliance": "style_mechanical_compliance.xml",
            "Mathematical Formatting": "style_mathematical_formatting.xml",
            "Punctuation & Grammar": "style_punctuation_grammar.xml",
            "Accessibility": "style_accessibility.xml",
            "Consistency": "style_consistency.xml"
        }

    def load_rubric(self, competency_name: str) -> ET.Element:
        """Load a specific rubric XML file.

        Args:
            competency_name: Name of the competency to load

        Returns:
            Parsed XML element for the rubric

        Raises:
            FileNotFoundError: If the rubric file doesn't exist
            ET.ParseError: If the XML is malformed
        """
        cache_key = f"rubric_{competency_name}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        if competency_name not in self.competency_to_file:
            raise ValueError(f"Unknown competency: {competency_name}")

        file_name = self.competency_to_file[competency_name]
        file_path = self.rubrics_dir / file_name

        if not file_path.exists():
            raise FileNotFoundError(f"Rubric file not found: {file_path}")

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            self._cache[cache_key] = root
            return root
        except ET.ParseError as e:
            raise ET.ParseError(f"Error parsing XML file {file_path}: {e}")

    def load_template(self, template_name: str) -> str:
        """Load a prompt template XML file.

        Args:
            template_name: Name of the template file (without .xml)

        Returns:
            Template content as string

        Raises:
            FileNotFoundError: If the template file doesn't exist
        """
        cache_key = f"template_{template_name}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        file_path = self.templates_dir / f"{template_name}.xml"

        if not file_path.exists():
            raise FileNotFoundError(f"Template file not found: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self._cache[cache_key] = content
                return content
        except Exception as e:
            raise IOError(f"Error reading template file {file_path}: {e}")

    def load_agent_configuration(self) -> ET.Element:
        """Load the main agent configuration XML.

        Returns:
            Parsed XML element for agent configuration
        """
        cache_key = "agent_config"

        if cache_key in self._cache:
            return self._cache[cache_key]

        file_path = self.config_dir / "agent_configuration.xml"

        if not file_path.exists():
            raise FileNotFoundError(f"Agent configuration not found: {file_path}")

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            self._cache[cache_key] = root
            return root
        except ET.ParseError as e:
            raise ET.ParseError(f"Error parsing agent configuration: {e}")

    def substitute_variables(self, template: str, variables: Dict[str, str]) -> str:
        """Replace {{VARIABLES}} in template with actual values.

        Args:
            template: Template string with {{PLACEHOLDERS}}
            variables: Dictionary of variable names to values

        Returns:
            Template with variables substituted
        """
        result = template

        for var_name, var_value in variables.items():
            placeholder = f"{{{{{var_name}}}}}"
            result = result.replace(placeholder, var_value)

        return result

    def extract_rubric_content(self, rubric_element: ET.Element) -> str:
        """Extract rubric content as formatted text from XML element.

        Args:
            rubric_element: Parsed rubric XML element

        Returns:
            Formatted rubric content as string
        """
        content_parts = []

        # Extract metadata
        metadata = rubric_element.find('metadata')
        if metadata is not None:
            name = metadata.findtext('name', 'Unknown')
            category = metadata.findtext('category', 'Unknown')
            focus_weight = metadata.findtext('focus_weight', '0.8')
            content_parts.append(f"RUBRIC: {name} ({category})")
            content_parts.append(f"Focus Weight: {focus_weight}")

        # Extract purpose
        purpose = rubric_element.findtext('purpose', '')
        if purpose:
            content_parts.append(f"\nPurpose: {purpose.strip()}")

        # Extract evaluation criteria
        content_parts.append("\n\nEVALUATION CRITERIA:")

        criteria_section = rubric_element.find('evaluation_criteria')
        if criteria_section is not None:
            for severity in criteria_section.findall('severity'):
                level = severity.get('level', '')
                label = severity.get('label', '')
                content_parts.append(f"\n[Severity {level} - {label}]")

                criteria = severity.find('criteria')
                if criteria is not None:
                    for criterion in criteria.findall('criterion'):
                        if criterion.text:
                            content_parts.append(f"  - {criterion.text.strip()}")

                examples = severity.find('examples')
                if examples is not None:
                    for example in examples.findall('example'):
                        if example.text:
                            ex_type = example.get('type', 'example')
                            content_parts.append(f"    Example ({ex_type}): {example.text.strip()}")

        # Extract special focus areas if present
        focus_areas = rubric_element.find('focus_areas')
        if focus_areas is not None:
            content_parts.append("\n\nSPECIAL FOCUS AREAS:")
            for area in focus_areas.findall('area'):
                if area.text:
                    content_parts.append(f"  - {area.text.strip()}")

        return "\n".join(content_parts)


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

    def __init__(self, config: ReviewerConfig, api_client: Optional[APIClient] = None,
                 agent_type: Optional[AgentType] = None,
                 xml_loader: Optional[XMLConfigLoader] = None,
                 config_mode: ConfigMode = ConfigMode.AUTO):
        """Initialize reviewer with configuration.

        Args:
            config: Reviewer configuration
            api_client: API client for OpenAI calls
            agent_type: Agent type configuration (rubric-focused or generalist)
            xml_loader: XML configuration loader
            config_mode: Configuration mode (XML, TEXT, or AUTO)
        """
        self.config = config
        self.api_client = api_client or APIClient()
        self.agent_type = agent_type
        self.xml_loader = xml_loader
        self.config_mode = config_mode

        # Determine actual config mode if AUTO
        if self.config_mode == ConfigMode.AUTO:
            self.config_mode = self._detect_config_mode()

    def _detect_config_mode(self) -> ConfigMode:
        """Detect whether to use XML or text configuration.

        Returns:
            ConfigMode.XML if XML files exist, ConfigMode.TEXT otherwise
        """
        project_root = get_project_root()
        config_dir = project_root / "ACTIVE_CONFIG"

        # Check if XML configuration exists
        xml_exists = (
            (config_dir / "agent_configuration.xml").exists() and
            (config_dir / "rubrics").exists() and
            (config_dir / "templates").exists()
        )

        return ConfigMode.XML if xml_exists else ConfigMode.TEXT

    def generate_system_prompt(self) -> str:
        """Generate the system prompt for this reviewer.

        Returns:
            System prompt string, either from XML or text files
        """
        if self.config_mode == ConfigMode.XML and self.xml_loader and self.agent_type:
            return self._generate_xml_system_prompt()
        else:
            return self._generate_text_system_prompt()

    def _generate_xml_system_prompt(self) -> str:
        """Generate system prompt from XML configuration.

        Returns:
            System prompt generated from XML templates
        """
        try:
            # Determine template based on agent type
            if self.agent_type.type == "rubric_focused":
                template = self.xml_loader.load_template("rubric_focused_agent_template")

                # Load the specific rubric
                rubric_element = self.xml_loader.load_rubric(self.agent_type.competency)
                rubric_content = self.xml_loader.extract_rubric_content(rubric_element)

                # Load guidelines
                authoring_guidelines = self._load_guidelines_file("authoring_prompt_rules.txt")
                style_guidelines = self._load_guidelines_file("style_prompt_rules.txt")

                # Substitute variables
                variables = {
                    "COMPETENCY_NAME": self.agent_type.competency,
                    "RUBRIC_XML_CONTENT": rubric_content,
                    "FULL_AUTHORING_GUIDE": authoring_guidelines,
                    "FULL_STYLE_GUIDE": style_guidelines
                }

                return self.xml_loader.substitute_variables(template, variables)

            else:  # generalist
                template = self.xml_loader.load_template("generalist_agent_template")

                # Load guidelines
                authoring_guidelines = self._load_guidelines_file("authoring_prompt_rules.txt")
                style_guidelines = self._load_guidelines_file("style_prompt_rules.txt")

                # Substitute variables
                variables = {
                    "FULL_AUTHORING_GUIDE": authoring_guidelines,
                    "FULL_STYLE_GUIDE": style_guidelines
                }

                return self.xml_loader.substitute_variables(template, variables)

        except Exception as e:
            print(f"Warning: Error generating XML system prompt: {e}")
            print("Falling back to text-based prompt")
            return self._generate_text_system_prompt()

    def _load_guidelines_file(self, filename: str) -> str:
        """Load guidelines file content.

        Args:
            filename: Name of the guidelines file

        Returns:
            File content as string
        """
        project_root = get_project_root()

        # Try ACTIVE_CONFIG/prompts first (new structure)
        file_path = project_root / "ACTIVE_CONFIG" / "prompts" / filename

        # Try ACTIVE_CONFIG directly as fallback
        if not file_path.exists():
            file_path = project_root / "ACTIVE_CONFIG" / filename

        # Try root directory as final fallback (legacy)
        if not file_path.exists():
            file_path = project_root / filename

        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()

        return f"Guidelines file {filename} not found"

    def _generate_text_system_prompt(self) -> str:
        """Generate system prompt from text files (legacy mode).

        Returns:
            System prompt generated from text files
        """
        project_root = get_project_root()

        # Load the appropriate guidelines
        if self.config.role == ReviewerRole.AUTHORING:
            guidelines_filename = "authoring_prompt_rules.txt"
        else:
            guidelines_filename = "style_prompt_rules.txt"

        vision_filename = "product_vision_context.txt"

        # Use the _load_guidelines_file method which handles path resolution
        guidelines = self._load_guidelines_file(guidelines_filename)
        product_vision = self._load_guidelines_file(vision_filename)

        return self.config.get_system_prompt(product_vision, guidelines)

    def generate_prompt(self, module: ModuleContent) -> str:
        """Generate the review prompt for a module.

        Args:
            module: Module content to review

        Returns:
            Review prompt string
        """
        # Add agent type specific instructions if using XML mode
        agent_type_info = ""
        if self.config_mode == ConfigMode.XML and self.agent_type:
            if self.agent_type.type == "rubric_focused":
                agent_type_info = f"""
AGENT TYPE: Rubric-Focused Specialist
COMPETENCY: {self.agent_type.competency}
FOCUS WEIGHT: {self.agent_type.focus_weight}

You should dedicate {int(self.agent_type.focus_weight * 100)}% of your attention to evaluating against your specialized rubric.
The remaining {int((1 - self.agent_type.focus_weight) * 100)}% should consider general quality issues.
"""
            else:
                agent_type_info = """
AGENT TYPE: Generalist Reviewer

You should evaluate holistically across all competencies, identifying cross-cutting issues
and ensuring overall content quality and cohesion. Pay special attention to:
- Issues that span multiple competencies
- Overall flow and coherence
- Cumulative effect of multiple small issues
- Balance between different quality aspects
"""

        prompt = f"""Review the following educational module content:

MODULE CONTENT:
{module.content}

{agent_type_info}

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


class RubricFocusedReviewer(BaseReviewer):
    """Reviewer specialized in evaluating against a specific rubric."""

    def __init__(self, config: ReviewerConfig, competency: str,
                 api_client: Optional[APIClient] = None,
                 xml_loader: Optional[XMLConfigLoader] = None):
        """Initialize rubric-focused reviewer.

        Args:
            config: Reviewer configuration
            competency: Specific competency to focus on
            api_client: API client for OpenAI calls
            xml_loader: XML configuration loader
        """
        agent_type = AgentType(
            type="rubric_focused",
            competency=competency,
            focus_weight=0.8
        )
        super().__init__(config, api_client, agent_type, xml_loader, ConfigMode.XML)

    def generate_prompt(self, module: ModuleContent) -> str:
        """Generate rubric-focused review prompt."""
        base_prompt = super().generate_prompt(module)

        # Add rubric-specific emphasis
        rubric_emphasis = f"""

IMPORTANT: As a rubric-focused specialist in {self.agent_type.competency}:
- Dedicate 80% of your evaluation to your specialized rubric criteria
- Be especially thorough in identifying issues within your competency area
- Provide detailed, actionable feedback for issues in your specialty
- Still note general issues you observe, but prioritize your specialty
"""

        return base_prompt + rubric_emphasis


class GeneralistReviewer(BaseReviewer):
    """Reviewer providing holistic evaluation across all competencies."""

    def __init__(self, config: ReviewerConfig,
                 api_client: Optional[APIClient] = None,
                 xml_loader: Optional[XMLConfigLoader] = None):
        """Initialize generalist reviewer.

        Args:
            config: Reviewer configuration
            api_client: API client for OpenAI calls
            xml_loader: XML configuration loader
        """
        agent_type = AgentType(
            type="generalist",
            competency=None,
            focus_weight=1.0  # Full attention across all areas
        )
        super().__init__(config, api_client, agent_type, xml_loader, ConfigMode.XML)

    def generate_prompt(self, module: ModuleContent) -> str:
        """Generate generalist review prompt."""
        base_prompt = super().generate_prompt(module)

        # Add generalist emphasis
        generalist_emphasis = """

IMPORTANT: As a generalist reviewer:
- Evaluate the content holistically across ALL competencies
- Identify issues that cross multiple domains
- Consider the cumulative impact of multiple small issues
- Assess overall coherence and flow
- Look for gaps that specialists might miss due to their focus
- Ensure balance between different quality aspects
"""

        return base_prompt + generalist_emphasis


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
                 api_client: Optional[APIClient] = None,
                 config_mode: ConfigMode = ConfigMode.AUTO):
        """Initialize a pool of reviewers.

        Args:
            review_pass: The review pass type
            num_reviewers: Number of reviewers (ignored when using XML config)
            api_client: API client for OpenAI calls
            config_mode: Configuration mode (XML, TEXT, or AUTO)
        """
        self.review_pass = review_pass
        self.num_reviewers = num_reviewers
        self.api_client = api_client or APIClient()
        self.config_mode = config_mode

        # Initialize XML loader if using XML mode
        self.xml_loader = None
        if self.config_mode == ConfigMode.AUTO:
            # Check if XML configuration exists
            config_dir = Path("/Users/michaeljoyce/Desktop/LEARNVIA/config")
            if (config_dir / "agent_configuration.xml").exists():
                self.config_mode = ConfigMode.XML

        if self.config_mode == ConfigMode.XML:
            try:
                self.xml_loader = XMLConfigLoader()
            except Exception as e:
                print(f"Warning: Could not initialize XML loader: {e}")
                print("Falling back to text-based configuration")
                self.config_mode = ConfigMode.TEXT
                self.xml_loader = None

        self.reviewers = self._create_reviewers()

    def _create_reviewers_xml(self) -> List[BaseReviewer]:
        """Create reviewers based on XML configuration.

        Returns:
            List of configured reviewers
        """
        reviewers = []

        try:
            # Load agent configuration
            config_root = self.xml_loader.load_agent_configuration()

            # Determine pass number
            pass_num = None
            if self.review_pass == ReviewPass.CONTENT_PASS_1:
                pass_num = "1"
            elif self.review_pass == ReviewPass.CONTENT_PASS_2:
                pass_num = "2"
            elif self.review_pass == ReviewPass.COPY_PASS_1:
                pass_num = "3"
            elif self.review_pass == ReviewPass.COPY_PASS_2:
                pass_num = "4"

            # Find the configuration for this pass
            pass_config = None
            for pass_elem in config_root.findall('.//pass'):
                if pass_elem.get('number') == pass_num:
                    pass_config = pass_elem
                    break

            if not pass_config:
                print(f"Warning: No XML configuration found for pass {pass_num}")
                return self._create_reviewers_text()

            # Determine reviewer ID prefix
            pass_prefix = f"pass{pass_num}"

            # Create authoring agents
            authoring_section = pass_config.find('authoring_agents')
            if authoring_section is not None:
                # Create rubric-focused authoring agents
                rubric_focused = authoring_section.find('rubric_focused')
                if rubric_focused is not None:
                    for assignment in rubric_focused.findall('assignment'):
                        competency = assignment.get('competency')
                        agent_count = int(assignment.get('agents', '1'))

                        for i in range(agent_count):
                            config = ReviewerConfig(
                                reviewer_id=f"{pass_prefix}_auth_rubric_{competency.replace(' ', '_')}_{i:02d}",
                                role=ReviewerRole.AUTHORING,
                                review_pass=self.review_pass,
                                focus_area=competency,
                                prompt_variation=f"Rubric-focused specialist for {competency}",
                                temperature=0.6 + (i % 3) * 0.1,
                                max_tokens=2000
                            )
                            reviewer = RubricFocusedReviewer(
                                config=config,
                                competency=competency,
                                api_client=self.api_client,
                                xml_loader=self.xml_loader
                            )
                            reviewers.append(reviewer)

                # Create generalist authoring agents
                generalist_elem = authoring_section.find('generalist')
                if generalist_elem is not None:
                    generalist_count = int(generalist_elem.get('count', '0'))
                    for i in range(generalist_count):
                        config = ReviewerConfig(
                            reviewer_id=f"{pass_prefix}_auth_generalist_{i:02d}",
                            role=ReviewerRole.AUTHORING,
                            review_pass=self.review_pass,
                            focus_area="holistic_authoring",
                            prompt_variation="Generalist reviewer for overall authoring quality",
                            temperature=0.6 + (i % 3) * 0.1,
                            max_tokens=2000
                        )
                        reviewer = GeneralistReviewer(
                            config=config,
                            api_client=self.api_client,
                            xml_loader=self.xml_loader
                        )
                        reviewers.append(reviewer)

            # Create style agents
            style_section = pass_config.find('style_agents')
            if style_section is not None:
                # Create rubric-focused style agents
                rubric_focused = style_section.find('rubric_focused')
                if rubric_focused is not None:
                    for assignment in rubric_focused.findall('assignment'):
                        competency = assignment.get('competency')
                        agent_count = int(assignment.get('agents', '1'))

                        for i in range(agent_count):
                            config = ReviewerConfig(
                                reviewer_id=f"{pass_prefix}_style_rubric_{competency.replace(' ', '_').replace('&', 'and')}_{i:02d}",
                                role=ReviewerRole.STYLE,
                                review_pass=self.review_pass,
                                focus_area=competency,
                                prompt_variation=f"Rubric-focused specialist for {competency}",
                                temperature=0.6 + (i % 3) * 0.1,
                                max_tokens=2000
                            )
                            reviewer = RubricFocusedReviewer(
                                config=config,
                                competency=competency,
                                api_client=self.api_client,
                                xml_loader=self.xml_loader
                            )
                            reviewers.append(reviewer)

                # Create generalist style agents
                generalist_elem = style_section.find('generalist')
                if generalist_elem is not None:
                    generalist_count = int(generalist_elem.get('count', '0'))
                    for i in range(generalist_count):
                        config = ReviewerConfig(
                            reviewer_id=f"{pass_prefix}_style_generalist_{i:02d}",
                            role=ReviewerRole.STYLE,
                            review_pass=self.review_pass,
                            focus_area="holistic_style",
                            prompt_variation="Generalist reviewer for overall style quality",
                            temperature=0.6 + (i % 3) * 0.1,
                            max_tokens=2000
                        )
                        reviewer = GeneralistReviewer(
                            config=config,
                            api_client=self.api_client,
                            xml_loader=self.xml_loader
                        )
                        reviewers.append(reviewer)

            print(f"Created {len(reviewers)} reviewers from XML configuration for {self.review_pass.name}")
            return reviewers

        except Exception as e:
            print(f"Error creating reviewers from XML: {e}")
            print("Falling back to text-based configuration")
            return self._create_reviewers_text()

    def _create_reviewers_text(self) -> List[BaseReviewer]:
        """Create reviewers using legacy text-based configuration.

        Returns:
            List of configured reviewers
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

    def _create_reviewers(self) -> List[BaseReviewer]:
        """Create the configured set of reviewers.

        Supports both XML-based and text-based configuration.

        Returns:
            List of configured reviewers
        """
        if self.config_mode == ConfigMode.XML and self.xml_loader:
            return self._create_reviewers_xml()
        else:
            return self._create_reviewers_text()

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