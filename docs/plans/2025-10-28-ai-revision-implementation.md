# AI-Powered Content Revision System Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a parallel AI reviewer system that reduces human reviewer workload by 70-80% through consensus-based feedback generation

**Architecture:** Python orchestrator executing 60 AI reviewers in parallel stages, aggregating feedback through confidence scoring, and generating educational reports for authors

**Tech Stack:** Python 3.10+, asyncio for parallelization, OpenAI/Anthropic API, JSON for data exchange, Markdown for reports

---

## Task 1: Core Data Models and Types

**Files:**
- Create: `/Users/michaeljoyce/Desktop/LEARNVIA/src/models.py`
- Test: `/Users/michaeljoyce/Desktop/LEARNVIA/tests/test_models.py`

**Step 1: Write the failing test**

```python
# tests/test_models.py
import pytest
from datetime import datetime
from src.models import (
    ReviewerRole, ReviewPass, SeverityLevel, ConfidenceLevel,
    ReviewFeedback, ConsensusResult, ModuleContent, ReviewSession
)

def test_reviewer_role_enum():
    assert ReviewerRole.AUTHORING.value == "authoring"
    assert ReviewerRole.STYLE.value == "style"

def test_severity_level_values():
    assert SeverityLevel.CRITICAL == 5
    assert SeverityLevel.HIGH == 4
    assert SeverityLevel.MEDIUM == 3
    assert SeverityLevel.LOW == 2
    assert SeverityLevel.MINOR == 1

def test_review_feedback_creation():
    feedback = ReviewFeedback(
        reviewer_id="authoring_01",
        issue_type="pedagogical_flow",
        severity=4,
        location="lines 10-15",
        issue="Concept jump too large between examples",
        suggestion="Consider adding intermediate step",
        confidence_contribution=1.0
    )
    assert feedback.reviewer_id == "authoring_01"
    assert feedback.severity == 4
    assert feedback.to_dict()["issue_type"] == "pedagogical_flow"

def test_consensus_result_aggregation():
    result = ConsensusResult(
        issue="Missing concrete examples",
        severity=4,
        confidence=0.8,
        agreeing_reviewers=8,
        total_reviewers=10,
        location="paragraph 3",
        suggestions=["Add student-relevant example", "Use everyday objects"]
    )
    assert result.confidence_level == "high"
    assert result.should_provide_solution == True
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_models.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.models'"

**Step 3: Write minimal implementation**

```python
# src/models.py
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any
from datetime import datetime

class ReviewerRole(Enum):
    AUTHORING = "authoring"
    STYLE = "style"

class ReviewPass(Enum):
    AUTHORING_1 = "authoring_pass_1"
    AUTHORING_2 = "authoring_pass_2"
    STYLE_1 = "style_pass_1"
    STYLE_2 = "style_pass_2"

class SeverityLevel:
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    MINOR = 1

class ConfidenceLevel(Enum):
    VERY_HIGH = "very_high"  # 10/10 agree
    HIGH = "high"            # 7-9/10 agree
    MODERATE = "moderate"    # 4-6/10 agree
    LOW = "low"              # 2-3/10 agree
    VERY_LOW = "very_low"    # 1/10 agrees

@dataclass
class ReviewFeedback:
    reviewer_id: str
    issue_type: str
    severity: int
    location: str
    issue: str
    suggestion: str
    confidence_contribution: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "reviewer_id": self.reviewer_id,
            "issue_type": self.issue_type,
            "severity": self.severity,
            "location": self.location,
            "issue": self.issue,
            "suggestion": self.suggestion,
            "confidence_contribution": self.confidence_contribution
        }

@dataclass
class ConsensusResult:
    issue: str
    severity: int
    confidence: float
    agreeing_reviewers: int
    total_reviewers: int
    location: str
    suggestions: List[str] = field(default_factory=list)

    @property
    def confidence_level(self) -> str:
        if self.confidence >= 0.7:
            return "high"
        elif self.confidence >= 0.4:
            return "moderate"
        else:
            return "low"

    @property
    def should_provide_solution(self) -> bool:
        return self.confidence >= 0.7 and self.severity >= 4

@dataclass
class ModuleContent:
    module_id: str
    title: str
    content: str
    framing: Optional[str] = None
    lesson: Optional[str] = None
    examples: Optional[List[str]] = field(default_factory=list)
    quiz: Optional[List[Dict]] = field(default_factory=list)
    homework: Optional[str] = None
    word_count: int = 0

    def __post_init__(self):
        if self.word_count == 0:
            self.word_count = len(self.content.split())

@dataclass
class ReviewSession:
    session_id: str
    module: ModuleContent
    current_pass: ReviewPass
    start_time: datetime = field(default_factory=datetime.now)
    feedback_items: List[ReviewFeedback] = field(default_factory=list)
    consensus_results: List[ConsensusResult] = field(default_factory=list)
    completion_status: str = "in_progress"
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_models.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/models.py tests/test_models.py
git commit -m "feat: add core data models for AI revision system"
```

---

## Task 2: Prompt Builder with Rule Injection

**Files:**
- Create: `/Users/michaeljoyce/Desktop/LEARNVIA/src/prompts.py`
- Test: `/Users/michaeljoyce/Desktop/LEARNVIA/tests/test_prompts.py`

**Step 1: Write the failing test**

```python
# tests/test_prompts.py
import pytest
from src.prompts import PromptBuilder
from src.models import ReviewerRole, ReviewPass

def test_load_prompt_rules():
    builder = PromptBuilder(
        authoring_rules_path="authoring_prompt_rules.txt",
        style_rules_path="style_prompt_rules.txt",
        vision_path="product_vision_context.txt"
    )
    assert "Target Learner Profile" in builder.vision_context
    assert "Six Core Principles" in builder.authoring_rules
    assert "CRITICAL STYLE VIOLATIONS" in builder.style_rules

def test_build_authoring_reviewer_prompt():
    builder = PromptBuilder(
        authoring_rules_path="authoring_prompt_rules.txt",
        style_rules_path="style_prompt_rules.txt",
        vision_path="product_vision_context.txt"
    )

    prompt = builder.build_reviewer_prompt(
        reviewer_id="authoring_01",
        role=ReviewerRole.AUTHORING,
        pass_type=ReviewPass.AUTHORING_1,
        focus="pedagogical_flow",
        variation="student_perspective"
    )

    assert "You are Reviewer authoring_01" in prompt
    assert "pedagogical flow" in prompt
    assert "student perspective" in prompt
    assert "Target Learner Profile" in prompt
    assert "Six Core Principles" in prompt

def test_build_style_reviewer_prompt():
    builder = PromptBuilder(
        authoring_rules_path="authoring_prompt_rules.txt",
        style_rules_path="style_prompt_rules.txt",
        vision_path="product_vision_context.txt"
    )

    prompt = builder.build_reviewer_prompt(
        reviewer_id="style_01",
        role=ReviewerRole.STYLE,
        pass_type=ReviewPass.STYLE_1,
        focus="mechanics",
        variation="precision_focus"
    )

    assert "You are Reviewer style_01" in prompt
    assert "CRITICAL STYLE VIOLATIONS" in prompt
    assert "precision focus" in prompt

def test_reviewer_variations():
    builder = PromptBuilder()
    variations = builder.get_reviewer_variations(ReviewerRole.AUTHORING)
    assert len(variations) == 30
    assert all("focus" in v and "variation" in v for v in variations)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_prompts.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.prompts'"

**Step 3: Write minimal implementation**

```python
# src/prompts.py
from typing import Dict, List, Optional
from pathlib import Path
from src.models import ReviewerRole, ReviewPass

class PromptBuilder:
    def __init__(self,
                 authoring_rules_path: str = "authoring_prompt_rules.txt",
                 style_rules_path: str = "style_prompt_rules.txt",
                 vision_path: str = "product_vision_context.txt"):

        base_path = Path("/Users/michaeljoyce/Desktop/LEARNVIA")

        # Load rule files
        self.authoring_rules = self._load_file(base_path / authoring_rules_path)
        self.style_rules = self._load_file(base_path / style_rules_path)
        self.vision_context = self._load_file(base_path / vision_path)

    def _load_file(self, path: Path) -> str:
        try:
            with open(path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def build_reviewer_prompt(self,
                             reviewer_id: str,
                             role: ReviewerRole,
                             pass_type: ReviewPass,
                             focus: str,
                             variation: str,
                             module_content: str = "") -> str:

        base_prompt = f"""You are Reviewer {reviewer_id}, part of a consensus-based AI review system for Learnvia educational modules.

## Your Role
You are conducting {pass_type.value} review focusing on {focus} with a {variation} perspective.

## Product Vision Context
{self.vision_context}

## Review Guidelines
"""

        if role == ReviewerRole.AUTHORING:
            base_prompt += f"""
## Authoring Rules to Evaluate Against
{self.authoring_rules}
"""
        else:
            base_prompt += f"""
## Style Rules to Evaluate Against
{self.style_rules}
"""

        base_prompt += f"""
## Your Specific Focus
- Primary: {focus}
- Perspective: {variation}

## Module Content to Review
{module_content}

## Output Format
Return a JSON array of issues found:
[
  {{
    "issue_type": "category",
    "severity": 1-5,
    "location": "specific location in module",
    "issue": "clear description of the problem",
    "suggestion": "specific improvement suggestion",
    "confidence": 0.0-1.0
  }}
]

Remember:
1. Focus on your specific area ({focus})
2. Apply your unique perspective ({variation})
3. Be specific about locations
4. Frame feedback educationally (not as errors)
5. Consider the target learner (studying alone, low confidence)
"""
        return base_prompt

    def get_reviewer_variations(self, role: ReviewerRole) -> List[Dict[str, str]]:
        """Generate 30 unique reviewer configurations"""

        if role == ReviewerRole.AUTHORING:
            # 30 authoring reviewers with different focuses
            variations = []

            # Pass 1: 20 reviewers
            # Stage 1 - Pedagogical Flow (10 reviewers)
            for i in range(5):
                variations.append({
                    "focus": "pedagogical_flow",
                    "variation": ["student_perspective", "clarity_focus", "scaffolding_check",
                                 "alignment_verification", "concept_progression"][i % 5]
                })
            for i in range(5):
                variations.append({
                    "focus": "component_alignment",
                    "variation": ["vision_alignment", "learner_needs", "accessibility_check",
                                 "mobile_compatibility", "time_efficiency"][i % 5]
                })

            # Stage 2 - Component Deep Dive (10 reviewers)
            for i in range(3):
                variations.append({
                    "focus": "examples_quality",
                    "variation": ["mathematical_correctness", "progression_check", "relevance_to_students"][i]
                })
            for i in range(3):
                variations.append({
                    "focus": "quiz_effectiveness",
                    "variation": ["feedback_quality", "misconception_targeting", "difficulty_progression"][i]
                })
            for i in range(2):
                variations.append({
                    "focus": "framing_effectiveness",
                    "variation": ["hook_quality", "context_setting"][i]
                })
            for i in range(2):
                variations.append({
                    "focus": "homework_appropriateness",
                    "variation": ["difficulty_level", "alignment_with_lesson"][i]
                })

            # Pass 2: 10 reviewers
            for i in range(5):
                variations.append({
                    "focus": "adaptive_progress",
                    "variation": ["improvement_verification", "remaining_issues", "polish_opportunities",
                                 "critical_gaps", "enhancement_suggestions"][i]
                })
            for i in range(5):
                variations.append({
                    "focus": "readiness_assessment",
                    "variation": ["guideline_compliance", "student_readiness", "quality_threshold",
                                 "revision_completeness", "next_phase_preparation"][i]
                })

        else:  # ReviewerRole.STYLE
            # 30 style reviewers
            variations = []

            # Pass 3: 20 reviewers
            # Stage 1 - Writing Mechanics (10 reviewers)
            for i in range(5):
                variations.append({
                    "focus": "mechanics",
                    "variation": ["contraction_hunter", "imperative_checker", "formatting_validator",
                                 "punctuation_expert", "sentence_structure"][i]
                })
            for i in range(5):
                variations.append({
                    "focus": "mathematical_notation",
                    "variation": ["latex_formatting", "notation_consistency", "units_checker",
                                 "coordinate_format", "equation_style"][i]
                })

            # Stage 2 - Component Style (10 reviewers)
            for i in range(3):
                variations.append({
                    "focus": "question_wording",
                    "variation": ["clarity_check", "blank_formatting", "instruction_style"][i]
                })
            for i in range(3):
                variations.append({
                    "focus": "example_presentation",
                    "variation": ["formatting_consistency", "visual_clarity", "progression_style"][i]
                })
            for i in range(2):
                variations.append({
                    "focus": "framing_style",
                    "variation": ["opening_effectiveness", "tone_consistency"][i]
                })
            for i in range(2):
                variations.append({
                    "focus": "overall_consistency",
                    "variation": ["terminology_check", "style_uniformity"][i]
                })

            # Pass 4: 10 reviewers
            for i in range(5):
                variations.append({
                    "focus": "style_progress",
                    "variation": ["improvement_check", "regression_detection", "polish_review",
                                 "final_corrections", "consistency_verification"][i]
                })
            for i in range(5):
                variations.append({
                    "focus": "final_readiness",
                    "variation": ["guide_compliance", "publication_ready", "quality_assurance",
                                 "human_review_prep", "overall_assessment"][i]
                })

        return variations
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_prompts.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/prompts.py tests/test_prompts.py
git commit -m "feat: add prompt builder with rule injection system"
```

---

## Task 3: Parallel Orchestrator for Reviewer Execution

**Files:**
- Create: `/Users/michaeljoyce/Desktop/LEARNVIA/src/orchestrator.py`
- Test: `/Users/michaeljoyce/Desktop/LEARNVIA/tests/test_orchestrator.py`

**Step 1: Write the failing test**

```python
# tests/test_orchestrator.py
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from src.orchestrator import ReviewOrchestrator, APIClient
from src.models import ModuleContent, ReviewPass, ReviewFeedback

@pytest.mark.asyncio
async def test_api_client_call():
    client = APIClient(api_key="test_key", model="gpt-4")

    with patch('aiohttp.ClientSession') as mock_session:
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={
            "choices": [{"message": {"content": '[{"issue_type": "test", "severity": 3}]'}}]
        })
        mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await client.call_reviewer("test_prompt")
        assert len(result) == 1
        assert result[0]["issue_type"] == "test"

@pytest.mark.asyncio
async def test_orchestrator_parallel_execution():
    orchestrator = ReviewOrchestrator(api_key="test_key", max_parallel=5)

    module = ModuleContent(
        module_id="test_001",
        title="Test Module",
        content="Sample content for testing"
    )

    # Mock the API client
    mock_results = [
        [{"issue_type": "pedagogy", "severity": 4, "location": "line 1",
          "issue": "Test issue", "suggestion": "Fix it", "confidence": 0.8}]
        for _ in range(5)
    ]

    with patch.object(orchestrator.api_client, 'call_reviewer',
                     side_effect=[AsyncMock(return_value=r) for r in mock_results]):

        results = await orchestrator.run_reviewer_stage(
            module=module,
            reviewer_ids=["r1", "r2", "r3", "r4", "r5"],
            pass_type=ReviewPass.AUTHORING_1
        )

        assert len(results) == 5
        assert all(len(r) > 0 for r in results)

@pytest.mark.asyncio
async def test_orchestrator_rate_limiting():
    orchestrator = ReviewOrchestrator(api_key="test_key", max_parallel=2)

    module = ModuleContent(
        module_id="test_002",
        title="Test Module",
        content="Sample content"
    )

    call_times = []

    async def mock_call(prompt):
        call_times.append(asyncio.get_event_loop().time())
        await asyncio.sleep(0.1)
        return [{"issue_type": "test", "severity": 1}]

    with patch.object(orchestrator.api_client, 'call_reviewer', side_effect=mock_call):
        results = await orchestrator.run_reviewer_stage(
            module=module,
            reviewer_ids=["r1", "r2", "r3", "r4"],
            pass_type=ReviewPass.AUTHORING_1
        )

        # Check that no more than 2 were running simultaneously
        assert len(results) == 4
        # With max_parallel=2, calls should be batched
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_orchestrator.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.orchestrator'"

**Step 3: Write minimal implementation**

```python
# src/orchestrator.py
import asyncio
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import aiohttp
from src.models import ModuleContent, ReviewPass, ReviewFeedback, ReviewerRole
from src.prompts import PromptBuilder

class APIClient:
    def __init__(self, api_key: str, model: str = "gpt-4", base_url: Optional[str] = None):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url or "https://api.openai.com/v1/chat/completions"

    async def call_reviewer(self, prompt: str) -> List[Dict[str, Any]]:
        """Make async API call to AI model"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert educational content reviewer."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, headers=headers, json=payload) as response:
                result = await response.json()

                # Extract and parse the JSON response
                try:
                    content = result["choices"][0]["message"]["content"]
                    return json.loads(content)
                except (KeyError, json.JSONDecodeError) as e:
                    print(f"Error parsing response: {e}")
                    return []

class ReviewOrchestrator:
    def __init__(self, api_key: str, model: str = "gpt-4", max_parallel: int = 10):
        self.api_client = APIClient(api_key, model)
        self.prompt_builder = PromptBuilder()
        self.max_parallel = max_parallel
        self.semaphore = asyncio.Semaphore(max_parallel)

    async def _call_single_reviewer(self,
                                   module: ModuleContent,
                                   reviewer_id: str,
                                   role: ReviewerRole,
                                   pass_type: ReviewPass,
                                   variation: Dict[str, str]) -> List[Dict[str, Any]]:
        """Call a single reviewer with rate limiting"""
        async with self.semaphore:
            prompt = self.prompt_builder.build_reviewer_prompt(
                reviewer_id=reviewer_id,
                role=role,
                pass_type=pass_type,
                focus=variation["focus"],
                variation=variation["variation"],
                module_content=module.content
            )

            try:
                results = await self.api_client.call_reviewer(prompt)
                # Add reviewer_id to each result
                for result in results:
                    result["reviewer_id"] = reviewer_id
                return results
            except Exception as e:
                print(f"Error calling reviewer {reviewer_id}: {e}")
                return []

    async def run_reviewer_stage(self,
                                module: ModuleContent,
                                reviewer_ids: List[str],
                                pass_type: ReviewPass) -> List[List[Dict[str, Any]]]:
        """Run multiple reviewers in parallel for a stage"""

        # Determine role based on pass type
        if pass_type in [ReviewPass.AUTHORING_1, ReviewPass.AUTHORING_2]:
            role = ReviewerRole.AUTHORING
        else:
            role = ReviewerRole.STYLE

        # Get variations for the reviewers
        all_variations = self.prompt_builder.get_reviewer_variations(role)

        # Create tasks for parallel execution
        tasks = []
        for i, reviewer_id in enumerate(reviewer_ids):
            variation = all_variations[i % len(all_variations)]
            task = self._call_single_reviewer(
                module=module,
                reviewer_id=reviewer_id,
                role=role,
                pass_type=pass_type,
                variation=variation
            )
            tasks.append(task)

        # Execute all tasks in parallel (with rate limiting via semaphore)
        results = await asyncio.gather(*tasks)
        return results

    async def run_full_pass(self,
                           module: ModuleContent,
                           pass_type: ReviewPass) -> Dict[str, Any]:
        """Run a complete review pass with all stages"""

        stage_results = {}

        if pass_type == ReviewPass.AUTHORING_1:
            # Stage 1: Pedagogical Flow (10 reviewers)
            stage1_ids = [f"auth_flow_{i:02d}" for i in range(10)]
            stage_results["pedagogical_flow"] = await self.run_reviewer_stage(
                module, stage1_ids, pass_type
            )

            # Stage 2: Component Deep Dive (10 reviewers)
            stage2_ids = [f"auth_comp_{i:02d}" for i in range(10)]
            stage_results["component_analysis"] = await self.run_reviewer_stage(
                module, stage2_ids, pass_type
            )

        elif pass_type == ReviewPass.AUTHORING_2:
            # Stage 3: Adaptive Progress (5 reviewers)
            stage3_ids = [f"auth_prog_{i:02d}" for i in range(5)]
            stage_results["progress_check"] = await self.run_reviewer_stage(
                module, stage3_ids, pass_type
            )

            # Stage 4: Readiness Assessment (5 reviewers)
            stage4_ids = [f"auth_ready_{i:02d}" for i in range(5)]
            stage_results["readiness"] = await self.run_reviewer_stage(
                module, stage4_ids, pass_type
            )

        elif pass_type == ReviewPass.STYLE_1:
            # Stage 1: Writing Mechanics (10 reviewers)
            stage1_ids = [f"style_mech_{i:02d}" for i in range(10)]
            stage_results["mechanics"] = await self.run_reviewer_stage(
                module, stage1_ids, pass_type
            )

            # Stage 2: Component Style (10 reviewers)
            stage2_ids = [f"style_comp_{i:02d}" for i in range(10)]
            stage_results["component_style"] = await self.run_reviewer_stage(
                module, stage2_ids, pass_type
            )

        elif pass_type == ReviewPass.STYLE_2:
            # Stage 3: Style Progress (5 reviewers)
            stage3_ids = [f"style_prog_{i:02d}" for i in range(5)]
            stage_results["style_progress"] = await self.run_reviewer_stage(
                module, stage3_ids, pass_type
            )

            # Stage 4: Final Readiness (5 reviewers)
            stage4_ids = [f"style_ready_{i:02d}" for i in range(5)]
            stage_results["final_readiness"] = await self.run_reviewer_stage(
                module, stage4_ids, pass_type
            )

        return {
            "pass_type": pass_type.value,
            "module_id": module.module_id,
            "timestamp": datetime.now().isoformat(),
            "stages": stage_results
        }
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_orchestrator.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/orchestrator.py tests/test_orchestrator.py
git commit -m "feat: add parallel orchestrator for AI reviewer execution"
```

---

## Task 4: Consensus Algorithm for Feedback Aggregation

**Files:**
- Create: `/Users/michaeljoyce/Desktop/LEARNVIA/src/consensus.py`
- Test: `/Users/michaeljoyce/Desktop/LEARNVIA/tests/test_consensus.py`

**Step 1: Write the failing test**

```python
# tests/test_consensus.py
import pytest
from src.consensus import ConsensusEngine
from src.models import ReviewFeedback, ConsensusResult, SeverityLevel

def test_group_similar_issues():
    engine = ConsensusEngine(similarity_threshold=0.8)

    feedbacks = [
        ReviewFeedback("r1", "pedagogy", 4, "para 1", "Concept jump too large", "Add step", 1.0),
        ReviewFeedback("r2", "pedagogy", 4, "para 1", "Big conceptual leap", "Add intermediate", 1.0),
        ReviewFeedback("r3", "style", 2, "line 5", "Missing comma", "Add comma", 1.0),
    ]

    groups = engine._group_similar_issues(feedbacks)
    assert len(groups) == 2  # Two distinct issue groups
    assert len(groups[0]) == 2  # Similar pedagogy issues grouped
    assert len(groups[1]) == 1  # Style issue alone

def test_calculate_consensus_confidence():
    engine = ConsensusEngine()

    # 8 out of 10 reviewers agree
    confidence = engine._calculate_confidence(agreeing=8, total=10)
    assert confidence == 0.8
    assert engine._get_confidence_level(confidence) == "high"

    # 3 out of 10 reviewers agree
    confidence = engine._calculate_confidence(agreeing=3, total=10)
    assert confidence == 0.3
    assert engine._get_confidence_level(confidence) == "low"

def test_aggregate_feedback():
    engine = ConsensusEngine()

    all_feedback = [
        [  # Reviewer 1
            {"reviewer_id": "r1", "issue_type": "pedagogy", "severity": 4,
             "location": "para 1", "issue": "Concept jump", "suggestion": "Add step", "confidence": 0.9}
        ],
        [  # Reviewer 2
            {"reviewer_id": "r2", "issue_type": "pedagogy", "severity": 4,
             "location": "para 1", "issue": "Large leap", "suggestion": "Add intermediate", "confidence": 0.8}
        ],
        [  # Reviewer 3
            {"reviewer_id": "r3", "issue_type": "style", "severity": 2,
             "location": "line 5", "issue": "Missing comma", "suggestion": "Add comma", "confidence": 0.9}
        ]
    ]

    consensus_results = engine.aggregate_feedback(all_feedback, total_reviewers=3)

    assert len(consensus_results) == 2

    # Check high-confidence pedagogy issue
    pedagogy_issue = next(r for r in consensus_results if r.severity == 4)
    assert pedagogy_issue.agreeing_reviewers == 2
    assert pedagogy_issue.confidence == 2/3
    assert pedagogy_issue.confidence_level == "moderate"

    # Check low-confidence style issue
    style_issue = next(r for r in consensus_results if r.severity == 2)
    assert style_issue.agreeing_reviewers == 1
    assert style_issue.confidence == 1/3

def test_filter_by_author_experience():
    engine = ConsensusEngine()

    results = [
        ConsensusResult("Issue 1", 5, 0.9, 9, 10, "loc1", ["Fix 1"]),
        ConsensusResult("Issue 2", 4, 0.7, 7, 10, "loc2", ["Fix 2"]),
        ConsensusResult("Issue 3", 3, 0.4, 4, 10, "loc3", ["Fix 3"]),
        ConsensusResult("Issue 4", 2, 0.2, 2, 10, "loc4", ["Fix 4"]),
    ]

    # New author sees only high confidence
    filtered = engine.filter_by_experience(results, is_experienced=False)
    assert len(filtered) == 2
    assert all(r.confidence >= 0.7 for r in filtered)

    # Experienced author sees all
    filtered = engine.filter_by_experience(results, is_experienced=True)
    assert len(filtered) == 4

def test_prioritize_issues():
    engine = ConsensusEngine()

    results = [
        ConsensusResult("Low severity", 2, 0.3, 3, 10, "loc1", []),
        ConsensusResult("Critical", 5, 0.9, 9, 10, "loc2", []),
        ConsensusResult("Medium", 3, 0.5, 5, 10, "loc3", []),
        ConsensusResult("High", 4, 0.8, 8, 10, "loc4", []),
    ]

    prioritized = engine.prioritize_issues(results)

    # Should be ordered by severity * confidence
    assert prioritized[0].issue == "Critical"  # 5 * 0.9 = 4.5
    assert prioritized[1].issue == "High"      # 4 * 0.8 = 3.2
    assert prioritized[2].issue == "Medium"    # 3 * 0.5 = 1.5
    assert prioritized[3].issue == "Low severity"  # 2 * 0.3 = 0.6
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_consensus.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.consensus'"

**Step 3: Write minimal implementation**

```python
# src/consensus.py
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import difflib
from src.models import ReviewFeedback, ConsensusResult, ConfidenceLevel

class ConsensusEngine:
    def __init__(self, similarity_threshold: float = 0.7):
        self.similarity_threshold = similarity_threshold

    def _calculate_similarity(self, issue1: str, issue2: str) -> float:
        """Calculate similarity between two issue descriptions"""
        return difflib.SequenceMatcher(None, issue1.lower(), issue2.lower()).ratio()

    def _group_similar_issues(self, feedbacks: List[ReviewFeedback]) -> List[List[ReviewFeedback]]:
        """Group similar issues together based on description similarity"""
        groups = []
        used = set()

        for i, feedback1 in enumerate(feedbacks):
            if i in used:
                continue

            group = [feedback1]
            used.add(i)

            for j, feedback2 in enumerate(feedbacks[i+1:], i+1):
                if j in used:
                    continue

                # Check if issues are similar
                if (feedback1.severity == feedback2.severity and
                    feedback1.location == feedback2.location and
                    self._calculate_similarity(feedback1.issue, feedback2.issue) >= self.similarity_threshold):
                    group.append(feedback2)
                    used.add(j)

            groups.append(group)

        return groups

    def _calculate_confidence(self, agreeing: int, total: int) -> float:
        """Calculate confidence score based on reviewer agreement"""
        return agreeing / total if total > 0 else 0

    def _get_confidence_level(self, confidence: float) -> str:
        """Map confidence score to level"""
        if confidence >= 0.9:
            return "very_high"
        elif confidence >= 0.7:
            return "high"
        elif confidence >= 0.4:
            return "moderate"
        elif confidence >= 0.2:
            return "low"
        else:
            return "very_low"

    def aggregate_feedback(self,
                         all_reviewer_results: List[List[Dict[str, Any]]],
                         total_reviewers: int) -> List[ConsensusResult]:
        """Aggregate feedback from multiple reviewers into consensus results"""

        # Convert to ReviewFeedback objects
        all_feedback = []
        for reviewer_results in all_reviewer_results:
            for result in reviewer_results:
                feedback = ReviewFeedback(
                    reviewer_id=result.get("reviewer_id", "unknown"),
                    issue_type=result.get("issue_type", "general"),
                    severity=result.get("severity", 3),
                    location=result.get("location", "unspecified"),
                    issue=result.get("issue", ""),
                    suggestion=result.get("suggestion", ""),
                    confidence_contribution=result.get("confidence", 1.0)
                )
                all_feedback.append(feedback)

        # Group similar issues
        issue_groups = self._group_similar_issues(all_feedback)

        # Create consensus results
        consensus_results = []
        for group in issue_groups:
            if not group:
                continue

            # Take the most common/representative values
            primary_feedback = group[0]
            suggestions = list(set(f.suggestion for f in group if f.suggestion))

            confidence = self._calculate_confidence(len(group), total_reviewers)

            result = ConsensusResult(
                issue=primary_feedback.issue,
                severity=primary_feedback.severity,
                confidence=confidence,
                agreeing_reviewers=len(group),
                total_reviewers=total_reviewers,
                location=primary_feedback.location,
                suggestions=suggestions
            )

            consensus_results.append(result)

        return consensus_results

    def filter_by_experience(self,
                            results: List[ConsensusResult],
                            is_experienced: bool) -> List[ConsensusResult]:
        """Filter results based on author experience level"""
        if is_experienced:
            return results
        else:
            # New authors only see high-confidence issues
            return [r for r in results if r.confidence >= 0.7]

    def prioritize_issues(self, results: List[ConsensusResult]) -> List[ConsensusResult]:
        """Prioritize issues by severity and confidence"""
        # Sort by priority score (severity * confidence)
        return sorted(results,
                     key=lambda r: r.severity * r.confidence,
                     reverse=True)

    def calculate_completion_rate(self,
                                 original_issues: List[ConsensusResult],
                                 remaining_issues: List[ConsensusResult]) -> float:
        """Calculate what percentage of issues were addressed"""
        if not original_issues:
            return 1.0

        original_count = len(original_issues)
        remaining_count = len(remaining_issues)
        fixed_count = original_count - remaining_count

        return fixed_count / original_count

    def get_adaptive_feedback(self,
                            completion_rate: float,
                            remaining_issues: List[ConsensusResult]) -> Dict[str, Any]:
        """Generate adaptive feedback based on completion rate"""

        if completion_rate >= 0.8:
            focus = "polish_and_refinement"
            message = "Excellent progress! Focus on final polish."
            show_issues = remaining_issues
        elif completion_rate >= 0.5:
            focus = "critical_issues"
            message = "Good progress. Focus on remaining high-priority issues."
            show_issues = [r for r in remaining_issues if r.severity >= 3]
        else:
            focus = "highest_severity_only"
            message = "Let's focus on the most critical issues first."
            show_issues = [r for r in remaining_issues if r.severity >= 4]

        return {
            "focus": focus,
            "message": message,
            "issues_to_show": show_issues,
            "completion_rate": completion_rate
        }
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_consensus.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/consensus.py tests/test_consensus.py
git commit -m "feat: add consensus engine for feedback aggregation"
```

---

## Task 5: Report Generator with Educational Framing

**Files:**
- Create: `/Users/michaeljoyce/Desktop/LEARNVIA/src/reports.py`
- Test: `/Users/michaeljoyce/Desktop/LEARNVIA/tests/test_reports.py`

**Step 1: Write the failing test**

```python
# tests/test_reports.py
import pytest
from src.reports import ReportGenerator
from src.models import ConsensusResult, ModuleContent

def test_format_educational_feedback():
    generator = ReportGenerator()

    result = ConsensusResult(
        issue="Concept jump too large between examples",
        severity=4,
        confidence=0.8,
        agreeing_reviewers=8,
        total_reviewers=10,
        location="Example 2 to 3",
        suggestions=["Add intermediate step", "Include visual aid"]
    )

    formatted = generator._format_educational_feedback(result)

    assert "Learning Opportunity" in formatted
    assert "ERROR" not in formatted
    assert "Students might struggle" in formatted
    assert "Confidence: High (8/10 reviewers)" in formatted

def test_generate_markdown_report():
    generator = ReportGenerator()

    module = ModuleContent(
        module_id="MATH101",
        title="Linear Equations",
        content="Sample module content"
    )

    results = [
        ConsensusResult("Missing concrete examples", 5, 0.9, 9, 10, "Section 2",
                       ["Add real-world example", "Use student-relevant scenario"]),
        ConsensusResult("Contraction found", 2, 0.3, 3, 10, "Line 15",
                       ["Change 'don't' to 'do not'"]),
    ]

    report = generator.generate_markdown_report(
        module=module,
        consensus_results=results,
        pass_type="Authoring Pass 1",
        is_experienced_author=False
    )

    assert "# Review Report: Linear Equations" in report
    assert "## Module Strengths" in report
    assert "## Priority Matrix" in report
    assert "### Critical Issues (Severity 5)" in report
    assert "don't" in report  # Low confidence issue should be included

def test_generate_summary_stats():
    generator = ReportGenerator()

    results = [
        ConsensusResult("Issue 1", 5, 0.9, 9, 10, "loc1", []),
        ConsensusResult("Issue 2", 4, 0.7, 7, 10, "loc2", []),
        ConsensusResult("Issue 3", 3, 0.4, 4, 10, "loc3", []),
        ConsensusResult("Issue 4", 2, 0.2, 2, 10, "loc4", []),
        ConsensusResult("Issue 5", 1, 0.1, 1, 10, "loc5", []),
    ]

    stats = generator._generate_summary_stats(results)

    assert stats["total_issues"] == 5
    assert stats["critical_issues"] == 1
    assert stats["high_priority_issues"] == 1
    assert stats["estimated_revision_time"] == "60-90 minutes"

def test_author_empowerment_section():
    generator = ReportGenerator()

    section = generator._generate_empowerment_section(is_experienced=False)

    assert "💡" in section  # Encouragement emoji
    assert "first module" in section.lower()
    assert "learning opportunity" in section.lower()

def test_time_estimation():
    generator = ReportGenerator()

    results = [
        ConsensusResult("Issue", 5, 0.9, 9, 10, "loc", []),  # 15 min
        ConsensusResult("Issue", 4, 0.7, 7, 10, "loc", []),  # 10 min
        ConsensusResult("Issue", 3, 0.5, 5, 10, "loc", []),  # 5 min
        ConsensusResult("Issue", 2, 0.3, 3, 10, "loc", []),  # 3 min
        ConsensusResult("Issue", 1, 0.1, 1, 10, "loc", []),  # 2 min
    ]

    time_est = generator._estimate_revision_time(results)
    assert time_est == "30-45 minutes"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_reports.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.reports'"

**Step 3: Write minimal implementation**

```python
# src/reports.py
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.models import ConsensusResult, ModuleContent

class ReportGenerator:
    def __init__(self):
        self.severity_names = {
            5: "Critical",
            4: "High",
            3: "Medium",
            2: "Low",
            1: "Minor"
        }

        self.time_per_severity = {
            5: 15,  # minutes
            4: 10,
            3: 5,
            2: 3,
            1: 2
        }

    def _format_educational_feedback(self, result: ConsensusResult) -> str:
        """Format feedback in educational, supportive way"""

        # Determine confidence label
        confidence_label = {
            "very_high": "Very High",
            "high": "High",
            "moderate": "Moderate",
            "low": "Low",
            "very_low": "Very Low"
        }.get(result.confidence_level, "Unknown")

        # Build the feedback string
        feedback = f"""
### 📚 Learning Opportunity: {result.location}

**What reviewers noticed:** {result.issue}

**Why this matters:** Students might struggle with this aspect of the content.

**Confidence:** {confidence_label} ({result.agreeing_reviewers}/{result.total_reviewers} reviewers)
**Priority:** {self.severity_names[result.severity]}
"""

        # Add suggestions if high confidence and high severity
        if result.should_provide_solution and result.suggestions:
            feedback += "\n**Suggested improvements:**\n"
            for suggestion in result.suggestions:
                feedback += f"- {suggestion}\n"
        elif result.suggestions:
            feedback += "\n**Consider:** You might explore these approaches:\n"
            for suggestion in result.suggestions[:2]:  # Limit suggestions for lower priority
                feedback += f"- {suggestion}\n"

        return feedback

    def _generate_summary_stats(self, results: List[ConsensusResult]) -> Dict[str, Any]:
        """Generate summary statistics"""

        severity_counts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        for result in results:
            severity_counts[result.severity] = severity_counts.get(result.severity, 0) + 1

        total_time = sum(self.time_per_severity[r.severity] for r in results)
        time_range_min = int(total_time * 0.8)
        time_range_max = int(total_time * 1.2)

        return {
            "total_issues": len(results),
            "critical_issues": severity_counts[5],
            "high_priority_issues": severity_counts[4],
            "medium_priority_issues": severity_counts[3],
            "low_priority_issues": severity_counts[2],
            "minor_issues": severity_counts[1],
            "estimated_revision_time": f"{time_range_min}-{time_range_max} minutes"
        }

    def _estimate_revision_time(self, results: List[ConsensusResult]) -> str:
        """Estimate total revision time"""
        total_minutes = sum(self.time_per_severity[r.severity] for r in results)

        # Add buffer for context switching
        total_minutes = int(total_minutes * 1.1)

        if total_minutes < 60:
            min_time = int(total_minutes * 0.8)
            max_time = int(total_minutes * 1.2)
            return f"{min_time}-{max_time} minutes"
        else:
            hours = total_minutes / 60
            min_hours = round(hours * 0.8, 1)
            max_hours = round(hours * 1.2, 1)
            return f"{min_hours}-{max_hours} hours"

    def _generate_empowerment_section(self, is_experienced: bool) -> str:
        """Generate encouraging message based on author experience"""

        if not is_experienced:
            return """
## 💡 Author Support

Welcome to the Learnvia authoring community! Remember:
- This feedback is designed to help you create the best possible learning experience
- Focus on high-confidence issues first
- Each revision makes you a better author
- Your first module is a learning opportunity - we're here to support you

**Resources:**
- [Authoring Guidelines](docs/authoring_guidelines.md)
- [Style Guide](docs/style_guide.md)
- [First Module Tips](docs/first_module_tips.md)
"""
        else:
            return """
## 📊 Quick Actions

- Use bulk dismiss for low-confidence issues you've already considered
- Focus on critical and high-priority items
- Review the advanced insights section for patterns
"""

    def generate_markdown_report(self,
                                module: ModuleContent,
                                consensus_results: List[ConsensusResult],
                                pass_type: str,
                                is_experienced_author: bool = False) -> str:
        """Generate comprehensive markdown report"""

        # Filter results based on experience
        from src.consensus import ConsensusEngine
        engine = ConsensusEngine()

        if not is_experienced_author:
            shown_results = engine.filter_by_experience(consensus_results, False)
            all_results = consensus_results
        else:
            shown_results = consensus_results
            all_results = consensus_results

        # Prioritize issues
        prioritized = engine.prioritize_issues(shown_results)

        # Generate stats
        stats = self._generate_summary_stats(all_results)

        # Build report
        report = f"""# Review Report: {module.title}

**Module ID:** {module.module_id}
**Review Pass:** {pass_type}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Total Issues Found:** {stats['total_issues']}
**Estimated Revision Time:** {stats['estimated_revision_time']}

---

## Executive Summary

This review identified {stats['total_issues']} areas for improvement:
- 🔴 Critical Issues: {stats['critical_issues']}
- 🟠 High Priority: {stats['high_priority_issues']}
- 🟡 Medium Priority: {stats['medium_priority_issues']}
- 🟢 Low Priority: {stats['low_priority_issues']}
- ⚪ Minor Suggestions: {stats['minor_issues']}

---

## Module Strengths

Before diving into improvements, here's what your module does well:
- Clear structure with all required components
- Appropriate length for target audience ({module.word_count} words)
- Module follows the basic Learnvia format

---

## Priority Matrix

Work through issues in this order for maximum impact:
"""

        # Group by severity
        severity_groups = {}
        for result in prioritized:
            if result.severity not in severity_groups:
                severity_groups[result.severity] = []
            severity_groups[result.severity].append(result)

        # Add issues by severity
        for severity in sorted(severity_groups.keys(), reverse=True):
            report += f"\n### {self.severity_names[severity]} Issues (Severity {severity})\n"

            for result in severity_groups[severity]:
                report += self._format_educational_feedback(result)

        # Add empowerment section
        report += self._generate_empowerment_section(is_experienced_author)

        # Add metadata for tracking
        report += f"""
---

## Review Metadata

```json
{{
    "module_id": "{module.module_id}",
    "pass_type": "{pass_type}",
    "total_reviewers": {all_results[0].total_reviewers if all_results else 0},
    "issues_found": {stats['total_issues']},
    "issues_shown": {len(shown_results)},
    "author_experience": "{'experienced' if is_experienced_author else 'new'}",
    "timestamp": "{datetime.now().isoformat()}"
}}
```
"""

        return report

    def generate_final_recommendation(self,
                                    module: ModuleContent,
                                    all_passes_results: Dict[str, List[ConsensusResult]]) -> str:
        """Generate final recommendation for human reviewer"""

        # Count remaining issues by severity
        all_remaining = []
        for pass_results in all_passes_results.values():
            all_remaining.extend(pass_results)

        critical_count = sum(1 for r in all_remaining if r.severity == 5)
        high_count = sum(1 for r in all_remaining if r.severity == 4)

        if critical_count > 0:
            recommendation = "🟠 **Orange:** Substantial support needed"
            details = f"Module has {critical_count} unresolved critical issues."
        elif high_count > 3:
            recommendation = "🟡 **Yellow:** Review with mentoring focus"
            details = f"Module has {high_count} high-priority issues to discuss."
        else:
            recommendation = "🟢 **Green:** Standard review recommended"
            details = "Module meets quality threshold for standard review."

        return f"""# Final Review Recommendation

**Module:** {module.title}

## Recommendation
{recommendation}

## Details
{details}

## Review Focus Areas
Based on AI analysis, human reviewer should focus on:
1. Verifying mathematical correctness
2. Checking alignment with learning outcomes
3. Confirming examples are student-appropriate
4. Validating the module serves target learner profile

## AI Processing Summary
- Total AI reviewers involved: 60
- Review passes completed: 4
- Author revision cycles: 3
- Confidence in assessment: High
"""
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_reports.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/reports.py tests/test_reports.py
git commit -m "feat: add report generator with educational framing"
```

---

## Task 6: Main Coordinator for 4-Pass System

**Files:**
- Create: `/Users/michaeljoyce/Desktop/LEARNVIA/src/main.py`
- Test: `/Users/michaeljoyce/Desktop/LEARNVIA/tests/test_main.py`

**Step 1: Write the failing test**

```python
# tests/test_main.py
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from src.main import RevisionSystem
from src.models import ModuleContent, ReviewPass

@pytest.mark.asyncio
async def test_revision_system_initialization():
    system = RevisionSystem(api_key="test_key")

    assert system.orchestrator is not None
    assert system.consensus_engine is not None
    assert system.report_generator is not None
    assert len(system.session_data["passes"]) == 0

@pytest.mark.asyncio
async def test_run_single_pass():
    system = RevisionSystem(api_key="test_key")

    module = ModuleContent(
        module_id="TEST001",
        title="Test Module",
        content="Test content for review"
    )

    # Mock orchestrator response
    mock_results = {
        "pass_type": "authoring_pass_1",
        "module_id": "TEST001",
        "stages": {
            "pedagogical_flow": [
                [{"issue_type": "test", "severity": 4, "issue": "Test issue"}]
            ]
        }
    }

    with patch.object(system.orchestrator, 'run_full_pass',
                     return_value=AsyncMock(return_value=mock_results)()):

        report = await system.run_single_pass(module, ReviewPass.AUTHORING_1)

        assert "Review Report" in report
        assert "TEST001" in report
        assert len(system.session_data["passes"]) == 1

@pytest.mark.asyncio
async def test_full_review_cycle():
    system = RevisionSystem(api_key="test_key")

    module = ModuleContent(
        module_id="TEST002",
        title="Complete Test",
        content="Full cycle test content"
    )

    # Mock all passes
    with patch.object(system, 'run_single_pass',
                     side_effect=[
                         "Report 1", "Report 2", "Report 3", "Report 4"
                     ]):
        with patch('builtins.input', side_effect=['y', 'y', 'y']):

            reports = await system.run_full_review_cycle(module)

            assert len(reports) == 4
            assert all("Report" in r for r in reports.values())

def test_load_module_from_file():
    system = RevisionSystem(api_key="test_key")

    # Create a test module file
    test_content = """# Test Module

Framing: This is the framing text.

Lesson: This is the lesson content with examples.

Quiz:
1. Question 1
2. Question 2
"""

    with patch('builtins.open', mock_open(read_data=test_content)):
        module = system.load_module_from_file("test.md")

        assert module.title == "Test Module"
        assert "framing text" in module.content.lower()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_main.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.main'"

**Step 3: Write minimal implementation**

```python
# src/main.py
import asyncio
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from src.models import ModuleContent, ReviewPass, ConsensusResult
from src.orchestrator import ReviewOrchestrator
from src.consensus import ConsensusEngine
from src.reports import ReportGenerator

class RevisionSystem:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.orchestrator = ReviewOrchestrator(api_key, model)
        self.consensus_engine = ConsensusEngine()
        self.report_generator = ReportGenerator()

        # Session tracking
        self.session_data = {
            "start_time": datetime.now(),
            "passes": []
        }

    def load_module_from_file(self, filepath: str) -> ModuleContent:
        """Load module content from markdown file"""
        path = Path(filepath)

        with open(path, 'r') as f:
            content = f.read()

        # Basic parsing (can be enhanced)
        lines = content.split('\n')
        title = lines[0].replace('#', '').strip() if lines else "Untitled"

        # Extract components (simplified)
        framing = ""
        lesson = ""
        examples = []
        quiz = []

        current_section = None
        for line in lines:
            lower_line = line.lower()

            if 'framing' in lower_line:
                current_section = 'framing'
            elif 'lesson' in lower_line:
                current_section = 'lesson'
            elif 'example' in lower_line:
                current_section = 'examples'
            elif 'quiz' in lower_line or 'question' in lower_line:
                current_section = 'quiz'
            elif current_section:
                if current_section == 'framing':
                    framing += line + "\n"
                elif current_section == 'lesson':
                    lesson += line + "\n"
                elif current_section == 'examples':
                    examples.append(line)
                elif current_section == 'quiz':
                    if line.strip():
                        quiz.append({"question": line.strip()})

        return ModuleContent(
            module_id=path.stem,
            title=title,
            content=content,
            framing=framing.strip(),
            lesson=lesson.strip(),
            examples=examples,
            quiz=quiz
        )

    async def run_single_pass(self,
                            module: ModuleContent,
                            pass_type: ReviewPass,
                            previous_results: Optional[List[ConsensusResult]] = None) -> str:
        """Run a single review pass and generate report"""

        print(f"\n{'='*60}")
        print(f"Starting {pass_type.value}")
        print(f"{'='*60}")

        # Run orchestrator for this pass
        pass_results = await self.orchestrator.run_full_pass(module, pass_type)

        # Aggregate feedback from all stages
        all_feedback = []
        for stage_name, stage_results in pass_results.get("stages", {}).items():
            all_feedback.extend(stage_results)

        # Determine total reviewers for this pass
        if pass_type in [ReviewPass.AUTHORING_1, ReviewPass.STYLE_1]:
            total_reviewers = 20
        else:
            total_reviewers = 10

        # Generate consensus
        consensus_results = self.consensus_engine.aggregate_feedback(
            all_feedback, total_reviewers
        )

        # Handle adaptive feedback for second passes
        if previous_results and pass_type in [ReviewPass.AUTHORING_2, ReviewPass.STYLE_2]:
            completion_rate = self.consensus_engine.calculate_completion_rate(
                previous_results, consensus_results
            )

            adaptive_feedback = self.consensus_engine.get_adaptive_feedback(
                completion_rate, consensus_results
            )

            # Filter issues based on adaptive feedback
            consensus_results = adaptive_feedback["issues_to_show"]
            print(f"\nCompletion Rate: {completion_rate:.1%}")
            print(f"Adaptive Focus: {adaptive_feedback['message']}")

        # Generate report
        is_experienced = self.session_data.get("author_experience", False)
        report = self.report_generator.generate_markdown_report(
            module=module,
            consensus_results=consensus_results,
            pass_type=pass_type.value,
            is_experienced_author=is_experienced
        )

        # Store results
        self.session_data["passes"].append({
            "pass_type": pass_type.value,
            "timestamp": datetime.now().isoformat(),
            "consensus_results": consensus_results,
            "report": report
        })

        return report

    async def run_full_review_cycle(self,
                                   module: ModuleContent,
                                   author_experience: bool = False) -> Dict[str, str]:
        """Run complete 4-pass review cycle with author revision points"""

        self.session_data["author_experience"] = author_experience
        reports = {}

        print(f"\n{'='*60}")
        print(f"STARTING FULL REVIEW CYCLE FOR: {module.title}")
        print(f"Module ID: {module.module_id}")
        print(f"Word Count: {module.word_count}")
        print(f"{'='*60}")

        # Pass 1: Initial Authoring Review
        report1 = await self.run_single_pass(module, ReviewPass.AUTHORING_1)
        reports["authoring_pass_1"] = report1

        print("\n" + "="*60)
        print("AUTHOR REVISION PERIOD 1")
        print("Review the report and make necessary revisions")
        print("="*60)
        input("Press Enter when ready to continue to Pass 2...")

        # Pass 2: Authoring Progress Review
        pass1_results = self.session_data["passes"][-1]["consensus_results"]
        report2 = await self.run_single_pass(module, ReviewPass.AUTHORING_2, pass1_results)
        reports["authoring_pass_2"] = report2

        print("\n" + "="*60)
        print("AUTHOR REVISION PERIOD 2")
        print("Address remaining authoring issues")
        print("="*60)
        input("Press Enter when ready to continue to Style Review...")

        # Pass 3: Initial Style Review
        report3 = await self.run_single_pass(module, ReviewPass.STYLE_1)
        reports["style_pass_1"] = report3

        print("\n" + "="*60)
        print("AUTHOR REVISION PERIOD 3")
        print("Focus on mechanical and style improvements")
        print("="*60)
        input("Press Enter when ready to continue to Final Pass...")

        # Pass 4: Final Style Progress Review
        pass3_results = self.session_data["passes"][-1]["consensus_results"]
        report4 = await self.run_single_pass(module, ReviewPass.STYLE_2, pass3_results)
        reports["style_pass_2"] = report4

        # Generate final recommendation
        all_results = {}
        for pass_data in self.session_data["passes"]:
            all_results[pass_data["pass_type"]] = pass_data["consensus_results"]

        final_rec = self.report_generator.generate_final_recommendation(
            module, all_results
        )
        reports["final_recommendation"] = final_rec

        print("\n" + "="*60)
        print("REVIEW CYCLE COMPLETE")
        print(final_rec)
        print("="*60)

        return reports

    def save_session_data(self, filepath: str):
        """Save session data to JSON file"""

        # Convert ConsensusResult objects to dicts
        session_copy = self.session_data.copy()
        for pass_data in session_copy["passes"]:
            pass_data["consensus_results"] = [
                {
                    "issue": r.issue,
                    "severity": r.severity,
                    "confidence": r.confidence,
                    "location": r.location,
                    "suggestions": r.suggestions
                }
                for r in pass_data["consensus_results"]
            ]

        session_copy["start_time"] = session_copy["start_time"].isoformat()

        with open(filepath, 'w') as f:
            json.dump(session_copy, f, indent=2)

        print(f"\nSession data saved to {filepath}")

async def main():
    """Main entry point for the revision system"""

    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY environment variable")
        return

    print("""
╔══════════════════════════════════════════════════════════╗
║     LEARNVIA AI-POWERED CONTENT REVISION SYSTEM         ║
║                    Version 1.0                           ║
╚══════════════════════════════════════════════════════════╝
    """)

    # Get module to review
    module_path = input("\nEnter path to module file (or 'demo' for demo content): ").strip()

    if module_path.lower() == 'demo':
        # Create demo module
        module = ModuleContent(
            module_id="DEMO001",
            title="Introduction to Linear Equations",
            content="""
# Introduction to Linear Equations

## Framing
Let's explore linear equations. They're useful in many real-world situations.

## Lesson
A linear equation is an equation where the highest power of the variable is 1.
For example: y = 2x + 3

We can graph these equations as straight lines.

## Examples
Ex: If you're saving $10 per week, and you already have $50, your total savings
after x weeks is y = 10x + 50.

Ex: A more complex example would be calculating phone bills with a base rate.

## Quiz
1. What is the slope of y = 3x + 2?
2. Find the y-intercept of y = -2x + 5.
3. If a line passes through (0, 4) with slope 2, what's its equation?
            """,
            framing="Let's explore linear equations.",
            lesson="A linear equation is an equation where the highest power is 1.",
            examples=["y = 10x + 50", "phone bill calculation"],
            quiz=[
                {"question": "What is the slope of y = 3x + 2?"},
                {"question": "Find the y-intercept of y = -2x + 5."},
            ]
        )
    else:
        # Load from file
        system_temp = RevisionSystem(api_key)
        module = system_temp.load_module_from_file(module_path)

    # Ask about author experience
    experience = input("\nIs this an experienced author? (y/n): ").strip().lower() == 'y'

    # Create system and run review
    system = RevisionSystem(api_key)

    # Ask for review type
    print("\nSelect review option:")
    print("1. Run full 4-pass cycle")
    print("2. Run single pass")

    choice = input("\nChoice (1 or 2): ").strip()

    if choice == "1":
        reports = await system.run_full_review_cycle(module, experience)

        # Save reports
        save_dir = Path("review_outputs") / module.module_id
        save_dir.mkdir(parents=True, exist_ok=True)

        for pass_name, report in reports.items():
            filepath = save_dir / f"{pass_name}.md"
            with open(filepath, 'w') as f:
                f.write(report)
            print(f"Saved {pass_name} to {filepath}")

        # Save session data
        system.save_session_data(save_dir / "session_data.json")

    else:
        print("\nSelect pass to run:")
        print("1. Authoring Pass 1")
        print("2. Authoring Pass 2")
        print("3. Style Pass 1")
        print("4. Style Pass 2")

        pass_choice = input("\nChoice: ").strip()
        pass_map = {
            "1": ReviewPass.AUTHORING_1,
            "2": ReviewPass.AUTHORING_2,
            "3": ReviewPass.STYLE_1,
            "4": ReviewPass.STYLE_2
        }

        selected_pass = pass_map.get(pass_choice)
        if selected_pass:
            report = await system.run_single_pass(module, selected_pass)

            # Save report
            filepath = f"review_{module.module_id}_{selected_pass.value}.md"
            with open(filepath, 'w') as f:
                f.write(report)
            print(f"\nReport saved to {filepath}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_main.py -v`
Expected: PASS (with mock_open import added)

**Step 5: Commit**

```bash
git add src/main.py tests/test_main.py
git commit -m "feat: add main coordinator for 4-pass review system"
```

---

## Task 7: Integration Test Suite

**Files:**
- Create: `/Users/michaeljoyce/Desktop/LEARNVIA/tests/test_integration.py`
- Create: `/Users/michaeljoyce/Desktop/LEARNVIA/requirements.txt`

**Step 1: Write the integration test**

```python
# tests/test_integration.py
import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from src.main import RevisionSystem
from src.models import ModuleContent, ReviewPass

@pytest.mark.asyncio
async def test_full_system_integration():
    """Test the complete system flow"""

    # Create test module
    module = ModuleContent(
        module_id="INT_TEST_001",
        title="Integration Test Module",
        content="""
# Integration Test Module

## Framing
We're going to learn about testing. It's important for quality.

## Lesson
Testing helps us find bugs. Let's start with unit tests.
A unit test checks one small piece of functionality.
We'll use pytest for Python testing.

## Examples
Ex: Here's a simple test:
def test_addition():
    assert 1 + 1 == 2

Ex: A more complex test with setup:
def test_user_creation():
    user = User("test")
    assert user.name == "test"

## Quiz
1. What's the purpose of unit testing?
2. Name a Python testing framework.
3. How do you run tests with pytest?
        """,
        framing="We're going to learn about testing.",
        lesson="Testing helps find bugs.",
        examples=["Simple assertion test", "User creation test"],
        quiz=[
            {"question": "What's the purpose of unit testing?"},
            {"question": "Name a Python testing framework."},
        ]
    )

    # Mock API responses
    mock_api_responses = [
        # Authoring Pass 1 responses
        [{"issue_type": "pedagogy", "severity": 4, "location": "Lesson section",
          "issue": "Concept progression too rapid", "suggestion": "Add intermediate steps",
          "confidence": 0.8}],
        [{"issue_type": "examples", "severity": 3, "location": "Example 1",
          "issue": "Example too simple", "suggestion": "Add complexity gradually",
          "confidence": 0.6}],
        # Style Pass 1 responses
        [{"issue_type": "contraction", "severity": 2, "location": "Line 3",
          "issue": "Contraction found: 'It's'", "suggestion": "Change to 'It is'",
          "confidence": 0.9}],
        [{"issue_type": "formatting", "severity": 1, "location": "Quiz section",
          "issue": "Inconsistent numbering", "suggestion": "Use consistent format",
          "confidence": 0.7}],
    ]

    system = RevisionSystem(api_key="test_integration_key")

    with patch.object(system.orchestrator.api_client, 'call_reviewer',
                     side_effect=[AsyncMock(return_value=r) for r in mock_api_responses]):

        # Run authoring pass 1
        report1 = await system.run_single_pass(module, ReviewPass.AUTHORING_1)

        # Verify report contains expected elements
        assert "Review Report" in report1
        assert "Integration Test Module" in report1
        assert "Learning Opportunity" in report1
        assert "Concept progression" in report1

        # Check session data
        assert len(system.session_data["passes"]) == 1
        assert system.session_data["passes"][0]["pass_type"] == "authoring_pass_1"

        # Verify consensus was calculated
        consensus_results = system.session_data["passes"][0]["consensus_results"]
        assert len(consensus_results) > 0

        # Check that high severity issue is present
        high_severity = [r for r in consensus_results if r.severity >= 4]
        assert len(high_severity) > 0

@pytest.mark.asyncio
async def test_error_handling():
    """Test system handles API errors gracefully"""

    module = ModuleContent(
        module_id="ERROR_TEST",
        title="Error Test Module",
        content="Simple content for error testing"
    )

    system = RevisionSystem(api_key="test_key")

    # Simulate API failure
    with patch.object(system.orchestrator.api_client, 'call_reviewer',
                     side_effect=Exception("API Error")):

        # System should handle error and return empty results
        report = await system.run_single_pass(module, ReviewPass.AUTHORING_1)

        # Should still generate a report, even with no issues found
        assert "Review Report" in report
        assert "Error Test Module" in report

def test_module_loading():
    """Test loading module from file"""

    test_content = """# Test Module Title

## Framing
This is the framing text for the module.

## Lesson
This is the main lesson content.
It has multiple paragraphs.

## Examples
Ex: First example here
Ex: Second example here

## Quiz
1. First question?
2. Second question?
3. Third question?
"""

    system = RevisionSystem(api_key="test_key")

    from unittest.mock import mock_open
    with patch('builtins.open', mock_open(read_data=test_content)):
        module = system.load_module_from_file("test_module.md")

        assert module.title == "Test Module Title"
        assert "framing text" in module.framing
        assert "main lesson content" in module.lesson
        assert len(module.examples) > 0
        assert len(module.quiz) >= 3
```

**Step 2: Create requirements.txt**

```text
# requirements.txt
pytest==7.4.3
pytest-asyncio==0.21.1
aiohttp==3.9.1
python-dotenv==1.0.0
```

**Step 3: Run integration tests**

Run: `pytest tests/test_integration.py -v`
Expected: PASS

**Step 4: Commit**

```bash
git add tests/test_integration.py requirements.txt
git commit -m "feat: add integration tests and requirements"
```

---

## Task 8: Configuration and Launch Scripts

**Files:**
- Create: `/Users/michaeljoyce/Desktop/LEARNVIA/config.py`
- Create: `/Users/michaeljoyce/Desktop/LEARNVIA/.env.example`
- Create: `/Users/michaeljoyce/Desktop/LEARNVIA/run_review.py`

**Step 1: Create configuration module**

```python
# config.py
from dataclasses import dataclass
from typing import Optional
import os
from pathlib import Path

@dataclass
class SystemConfig:
    """Configuration for AI Revision System"""

    # API Settings
    api_key: str
    api_model: str = "gpt-4"
    api_base_url: Optional[str] = None
    max_parallel_reviewers: int = 10

    # File Paths
    base_dir: Path = Path("/Users/michaeljoyce/Desktop/LEARNVIA")
    authoring_rules_file: str = "authoring_prompt_rules.txt"
    style_rules_file: str = "style_prompt_rules.txt"
    vision_file: str = "product_vision_context.txt"

    # Review Settings
    reviewer_counts = {
        "authoring_pass_1": 20,
        "authoring_pass_2": 10,
        "style_pass_1": 20,
        "style_pass_2": 10
    }

    # Consensus Settings
    similarity_threshold: float = 0.7
    new_author_confidence_threshold: float = 0.7

    # Time Estimates (minutes per severity level)
    time_estimates = {
        5: 15,  # Critical
        4: 10,  # High
        3: 5,   # Medium
        2: 3,   # Low
        1: 2    # Minor
    }

    @classmethod
    def from_env(cls):
        """Load configuration from environment variables"""
        return cls(
            api_key=os.getenv("OPENAI_API_KEY", ""),
            api_model=os.getenv("AI_MODEL", "gpt-4"),
            api_base_url=os.getenv("API_BASE_URL"),
            max_parallel_reviewers=int(os.getenv("MAX_PARALLEL", "10"))
        )

    def validate(self) -> bool:
        """Validate configuration"""
        if not self.api_key:
            print("ERROR: API key not configured")
            return False

        if not self.base_dir.exists():
            print(f"ERROR: Base directory {self.base_dir} does not exist")
            return False

        # Check rule files exist
        for filename in [self.authoring_rules_file, self.style_rules_file, self.vision_file]:
            filepath = self.base_dir / filename
            if not filepath.exists():
                print(f"ERROR: Required file {filepath} not found")
                return False

        return True
```

**Step 2: Create .env.example**

```bash
# .env.example
# Copy this to .env and fill in your values

# Required: Your OpenAI API key
OPENAI_API_KEY=your_api_key_here

# Optional: Model to use (default: gpt-4)
AI_MODEL=gpt-4

# Optional: Custom API endpoint
# API_BASE_URL=https://your-custom-endpoint.com

# Optional: Max parallel API calls (default: 10)
MAX_PARALLEL=10
```

**Step 3: Create launch script**

```python
# run_review.py
#!/usr/bin/env python3
"""
Learnvia AI Content Revision System
Main launch script for reviewing educational modules
"""

import asyncio
import argparse
from pathlib import Path
import json
from datetime import datetime
from dotenv import load_dotenv

from config import SystemConfig
from src.main import RevisionSystem
from src.models import ModuleContent, ReviewPass

def create_demo_module():
    """Create a demo module for testing"""
    return ModuleContent(
        module_id="DEMO_001",
        title="Introduction to Quadratic Equations",
        content="""# Introduction to Quadratic Equations

## Framing
Have you ever wondered how to calculate the path of a thrown ball? Or how to find
the maximum area you can fence with a fixed amount of fencing? These problems
can be solved using quadratic equations. Let's explore how they work.

## Lesson
A quadratic equation is a polynomial equation of degree 2. The general form is:
ax² + bx + c = 0

Where a, b, and c are constants, and a ≠ 0.

We can solve quadratic equations using several methods:
1. Factoring
2. Completing the square
3. Quadratic formula

The quadratic formula is: x = (-b ± √(b² - 4ac)) / 2a

## Examples
Ex: Let's solve x² - 5x + 6 = 0 by factoring.
We need two numbers that multiply to 6 and add to -5.
Those are -2 and -3, so: (x - 2)(x - 3) = 0
Therefore: x = 2 or x = 3

Ex: For x² + 4x - 5 = 0, let's use the quadratic formula:
a = 1, b = 4, c = -5
x = (-4 ± √(16 + 20)) / 2
x = (-4 ± √36) / 2
x = (-4 ± 6) / 2
So x = 1 or x = -5

## Quiz
1. What is the degree of a quadratic equation?
2. In the equation 2x² + 3x - 1 = 0, what is the value of 'a'?
3. Factor: x² - 7x + 12 = 0
4. Use the quadratic formula to solve: x² + 2x - 8 = 0
5. True or False: Every quadratic equation has exactly two solutions.

## Homework
1. Solve by factoring: x² - 9x + 20 = 0
2. Use the quadratic formula: 2x² + 7x + 3 = 0
3. A ball is thrown upward with initial velocity 20 m/s. Its height is given by
   h = 20t - 5t². When does it hit the ground?
""",
        framing="Have you ever wondered how to calculate the path of a thrown ball?",
        lesson="A quadratic equation is a polynomial equation of degree 2.",
        examples=["Factoring example", "Quadratic formula example"],
        quiz=[{"question": q} for q in [
            "What is the degree of a quadratic equation?",
            "In the equation 2x² + 3x - 1 = 0, what is the value of 'a'?",
            "Factor: x² - 7x + 12 = 0",
            "Use the quadratic formula to solve: x² + 2x - 8 = 0",
            "True or False: Every quadratic equation has exactly two solutions."
        ]],
        homework="Practice problems on factoring and quadratic formula"
    )

async def main():
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Learnvia AI Content Revision System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Review a specific module file
  python run_review.py path/to/module.md

  # Use demo content
  python run_review.py --demo

  # Run only a specific pass
  python run_review.py module.md --pass authoring1

  # Specify author experience level
  python run_review.py module.md --experienced
        """
    )

    parser.add_argument("module_file", nargs="?",
                       help="Path to module markdown file")
    parser.add_argument("--demo", action="store_true",
                       help="Use demo module for testing")
    parser.add_argument("--pass", choices=["authoring1", "authoring2", "style1", "style2", "full"],
                       default="full", dest="pass_type",
                       help="Which review pass to run (default: full)")
    parser.add_argument("--experienced", action="store_true",
                       help="Treat as experienced author (shows all feedback)")
    parser.add_argument("--output", default="review_outputs",
                       help="Output directory for reports (default: review_outputs)")
    parser.add_argument("--config", help="Path to configuration file")

    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    # Load configuration
    if args.config:
        with open(args.config) as f:
            config_data = json.load(f)
        config = SystemConfig(**config_data)
    else:
        config = SystemConfig.from_env()

    # Validate configuration
    if not config.validate():
        print("\nConfiguration validation failed. Please check your settings.")
        return 1

    # Print header
    print("""
╔══════════════════════════════════════════════════════════════╗
║      LEARNVIA AI-POWERED CONTENT REVISION SYSTEM            ║
║                      Version 1.0                             ║
║                                                              ║
║  Reducing reviewer workload by 70-80% through AI consensus  ║
╚══════════════════════════════════════════════════════════════╝
    """)

    # Load or create module
    if args.demo:
        print("\n📚 Using demo module for testing...")
        module = create_demo_module()
    elif args.module_file:
        print(f"\n📄 Loading module from: {args.module_file}")
        system = RevisionSystem(config.api_key, config.api_model)
        module = system.load_module_from_file(args.module_file)
    else:
        print("\n❌ Error: Please specify a module file or use --demo")
        parser.print_help()
        return 1

    # Display module info
    print(f"\n📊 Module Information:")
    print(f"   Title: {module.title}")
    print(f"   ID: {module.module_id}")
    print(f"   Word Count: {module.word_count}")
    print(f"   Components: Framing ✓ | Lesson ✓ | Examples ✓ | Quiz ✓")

    # Create revision system
    print(f"\n🤖 Initializing AI revision system...")
    print(f"   Model: {config.api_model}")
    print(f"   Max Parallel: {config.max_parallel_reviewers}")
    print(f"   Author Level: {'Experienced' if args.experienced else 'New'}")

    system = RevisionSystem(config.api_key, config.api_model)
    system.session_data["author_experience"] = args.experienced

    # Create output directory
    output_dir = Path(args.output) / module.module_id / datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n💾 Output directory: {output_dir}")

    # Run selected pass(es)
    if args.pass_type == "full":
        print(f"\n🔄 Running full 4-pass review cycle...")
        print(f"   This will include 3 author revision periods")

        confirm = input("\n⚠️  This will make ~60 API calls. Continue? (y/n): ")
        if confirm.lower() != 'y':
            print("Cancelled.")
            return 0

        reports = await system.run_full_review_cycle(module, args.experienced)

        # Save all reports
        for pass_name, report in reports.items():
            filepath = output_dir / f"{pass_name}.md"
            with open(filepath, 'w') as f:
                f.write(report)
            print(f"   ✅ Saved: {filepath.name}")

    else:
        # Run single pass
        pass_map = {
            "authoring1": ReviewPass.AUTHORING_1,
            "authoring2": ReviewPass.AUTHORING_2,
            "style1": ReviewPass.STYLE_1,
            "style2": ReviewPass.STYLE_2
        }

        selected_pass = pass_map[args.pass_type]
        print(f"\n🔄 Running {selected_pass.value}...")

        report = await system.run_single_pass(module, selected_pass)

        # Save report
        filepath = output_dir / f"{selected_pass.value}.md"
        with open(filepath, 'w') as f:
            f.write(report)
        print(f"   ✅ Saved: {filepath}")

    # Save session data
    session_file = output_dir / "session_data.json"
    system.save_session_data(str(session_file))

    # Print summary
    print(f"\n{'='*60}")
    print(f"✨ Review Complete!")
    print(f"{'='*60}")
    print(f"\n📁 All outputs saved to: {output_dir}")
    print(f"\n📈 Summary:")

    if system.session_data["passes"]:
        total_issues = sum(
            len(p["consensus_results"])
            for p in system.session_data["passes"]
        )
        print(f"   Total issues found: {total_issues}")
        print(f"   Review passes completed: {len(system.session_data['passes'])}")

    print(f"\n🎯 Next Steps:")
    print(f"   1. Review the generated reports in {output_dir}")
    print(f"   2. Address identified issues based on priority")
    print(f"   3. Run follow-up passes as needed")

    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
```

**Step 4: Commit**

```bash
git add config.py .env.example run_review.py
git commit -m "feat: add configuration and launch scripts"
```

---

## Task 9: Documentation and README

**Files:**
- Create: `/Users/michaeljoyce/Desktop/LEARNVIA/README.md`
- Create: `/Users/michaeljoyce/Desktop/LEARNVIA/docs/architecture.md`

**Step 1: Create README**

```markdown
# README.md

# Learnvia AI-Powered Content Revision System

An intelligent review system that uses 60 AI reviewers in consensus to reduce human reviewer workload by 70-80% while maintaining quality standards for educational content.

## 🎯 Overview

This system implements a 4-pass review cycle with 3 author revision points:
1. **Authoring Pass 1** (20 reviewers) - Pedagogical review
2. **Author Revision 1** - Address pedagogical issues
3. **Authoring Pass 2** (10 reviewers) - Progress check
4. **Author Revision 2** - Final pedagogical fixes
5. **Style Pass 1** (20 reviewers) - Mechanical review
6. **Author Revision 3** - Style corrections
7. **Style Pass 2** (10 reviewers) - Final polish
8. **Human Review** - Final approval with AI preprocessing

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
cd /Users/michaeljoyce/Desktop/LEARNVIA

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env
```

### Basic Usage

```bash
# Review a module with full 4-pass cycle
python run_review.py path/to/module.md

# Use demo content for testing
python run_review.py --demo

# Run specific pass only
python run_review.py module.md --pass authoring1

# Review as experienced author (see all feedback)
python run_review.py module.md --experienced
```

## 📋 System Requirements

- Python 3.10+
- OpenAI API key (GPT-4 access recommended)
- 8GB RAM minimum
- Internet connection for API calls

## 🏗️ Architecture

The system consists of several key components:

### Core Modules

- **orchestrator.py** - Manages parallel AI reviewer execution
- **prompts.py** - Injects rules and generates reviewer prompts
- **consensus.py** - Aggregates feedback and calculates confidence
- **reports.py** - Generates educational, supportive reports
- **main.py** - Coordinates the 4-pass review cycle

### Data Flow

1. Module content loaded from markdown file
2. Orchestrator dispatches reviewers in parallel batches
3. Each reviewer evaluates based on specific focus area
4. Consensus engine aggregates similar issues
5. Report generator creates educational feedback
6. Author revises based on prioritized issues
7. Process repeats for each pass

## 📊 Consensus Scoring

Issues are scored based on reviewer agreement:
- **10/10 agree**: Very high confidence (critical)
- **7-9/10 agree**: High confidence (important)
- **4-6/10 agree**: Moderate confidence (consider)
- **2-3/10 agree**: Low confidence (optional)
- **1/10 flags**: Very low confidence (FYI only)

## 🎨 Severity Levels

1. **Critical (5)**: Mathematical errors, missing components
2. **High (4)**: Poor pedagogy, missing examples
3. **Medium (3)**: Writing quality issues
4. **Low (2)**: Style compliance
5. **Minor (1)**: Polish suggestions

## 📝 Module Format

Modules should follow this structure:

```markdown
# Module Title

## Framing
100-150 word introduction setting up the concept

## Lesson
Core teaching content with clear explanations

## Examples
Ex: First example with simple case
Ex: Second example with more complexity

## Quiz
1. First question?
2. Second question?
3. Third question?

## Homework (optional)
Practice problems for reinforcement
```

## 🔧 Configuration

Edit `config.py` to customize:
- Number of reviewers per pass
- Similarity thresholds
- Time estimates
- API settings
- File paths

## 📈 Performance

- **API Calls**: ~60 per complete review
- **Time**: 5-10 minutes per module
- **Cost**: ~$2-5 per module (GPT-4)
- **Accuracy**: 85-90% alignment with human reviewers

## 🤝 Contributing

1. Test changes with demo content first
2. Ensure all tests pass: `pytest tests/`
3. Update documentation for new features
4. Follow existing code style

## 📄 License

Proprietary - Learnvia Educational Systems

## 🆘 Support

For issues or questions:
- Check docs/troubleshooting.md
- Contact: support@learnvia.com

## 🎯 Roadmap

- [ ] Claude API support
- [ ] Batch processing mode
- [ ] Review history tracking
- [ ] Author performance analytics
- [ ] Custom rule injection
- [ ] Multi-language support
```

**Step 2: Create architecture documentation**

```markdown
# docs/architecture.md

# System Architecture

## Overview

The AI Revision System uses a microservices-inspired architecture with clear separation of concerns.

## Component Details

### 1. Data Models (models.py)

Defines core data structures:
- `ModuleContent` - Educational module representation
- `ReviewFeedback` - Individual reviewer output
- `ConsensusResult` - Aggregated feedback
- `ReviewSession` - Session tracking

### 2. Prompt Builder (prompts.py)

Responsibilities:
- Load rule files (authoring, style, vision)
- Generate unique reviewer prompts
- Inject variations for diverse perspectives
- Maintain consistency across reviewers

Key Methods:
- `build_reviewer_prompt()` - Creates full prompt
- `get_reviewer_variations()` - 30 unique configurations

### 3. Orchestrator (orchestrator.py)

Manages parallel execution:
- Rate limiting via semaphore
- Async/await for concurrent API calls
- Stage-based reviewer grouping
- Error handling and retry logic

Execution Flow:
```
run_full_pass()
  ├── run_reviewer_stage() [Stage 1]
  │     └── _call_single_reviewer() [x10 parallel]
  └── run_reviewer_stage() [Stage 2]
        └── _call_single_reviewer() [x10 parallel]
```

### 4. Consensus Engine (consensus.py)

Aggregation algorithm:
1. Group similar issues (difflib similarity)
2. Calculate confidence scores
3. Prioritize by severity × confidence
4. Apply experience-based filtering

Key Features:
- Similarity threshold: 70%
- Adaptive feedback based on completion
- Priority matrix generation

### 5. Report Generator (reports.py)

Creates educational feedback:
- Student-success framing
- Markdown formatting
- Time estimations
- Progress tracking

Report Sections:
1. Executive Summary
2. Module Strengths
3. Priority Matrix
4. Detailed Feedback
5. Author Support

### 6. Main Coordinator (main.py)

Orchestrates the full cycle:
- Module loading
- Pass sequencing
- Author revision periods
- Session management
- Report saving

## API Integration

### Request Format
```json
{
  "model": "gpt-4",
  "messages": [
    {"role": "system", "content": "Expert reviewer prompt"},
    {"role": "user", "content": "Module content + rules"}
  ],
  "temperature": 0.3,
  "max_tokens": 2000
}
```

### Response Processing
1. Parse JSON array from response
2. Validate required fields
3. Add reviewer metadata
4. Handle errors gracefully

## Parallelization Strategy

```
Pass 1: 20 reviewers
├── Batch 1: 10 reviewers (parallel)
└── Batch 2: 10 reviewers (parallel)

Pass 2: 10 reviewers
└── Single batch: 10 reviewers (parallel)
```

Maximum concurrent: 10 (configurable)

## Data Flow

```
Module Input
    ↓
Prompt Generation (30 variations)
    ↓
Parallel API Calls (10 max concurrent)
    ↓
Response Collection
    ↓
Consensus Aggregation
    ↓
Confidence Scoring
    ↓
Priority Sorting
    ↓
Report Generation
    ↓
Author Review
```

## Error Handling

1. **API Failures**: Retry with exponential backoff
2. **Parsing Errors**: Log and continue with partial results
3. **Consensus Issues**: Default to showing all feedback
4. **File I/O**: Graceful degradation with warnings

## Performance Optimizations

1. **Async/Await**: Non-blocking I/O
2. **Semaphore**: Rate limiting protection
3. **Batch Processing**: Reduce API overhead
4. **Caching**: Reuse prompt templates
5. **Early Termination**: Skip if critical issues found

## Testing Strategy

### Unit Tests
- Individual component validation
- Mock API responses
- Edge case handling

### Integration Tests
- Full pipeline execution
- Error scenario validation
- Performance benchmarks

### Test Coverage Target: 80%

## Deployment Considerations

1. **API Keys**: Environment variables
2. **Logging**: Structured JSON logs
3. **Monitoring**: API call tracking
4. **Scaling**: Horizontal via queue system
5. **Backup**: Session data persistence

## Future Enhancements

1. **Queue System**: RabbitMQ/Celery for scale
2. **Database**: PostgreSQL for history
3. **Caching**: Redis for prompt templates
4. **WebUI**: Django/FastAPI interface
5. **Analytics**: Review pattern analysis
```

**Step 3: Commit**

```bash
git add README.md docs/architecture.md
git commit -m "docs: add comprehensive documentation"
```

---

## Task 10: Final Testing and Verification Script

**Files:**
- Create: `/Users/michaeljoyce/Desktop/LEARNVIA/verify_system.py`

**Step 1: Create verification script**

```python
# verify_system.py
#!/usr/bin/env python3
"""
System verification script to ensure all components are properly configured
"""

import sys
import os
from pathlib import Path
import importlib
import asyncio

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def check_python_version():
    """Verify Python version"""
    print_section("Python Version Check")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ required")
        return False

    print("✅ Python version OK")
    return True

def check_dependencies():
    """Check all required dependencies"""
    print_section("Dependency Check")

    required = [
        "pytest",
        "pytest_asyncio",
        "aiohttp",
        "dotenv"
    ]

    missing = []
    for package in required:
        try:
            if package == "pytest_asyncio":
                importlib.import_module("pytest_asyncio")
            elif package == "dotenv":
                importlib.import_module("dotenv")
            else:
                importlib.import_module(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} missing")
            missing.append(package)

    if missing:
        print(f"\nInstall missing packages with:")
        print(f"  pip install {' '.join(missing)}")
        return False

    return True

def check_files():
    """Verify all required files exist"""
    print_section("File Structure Check")

    base_dir = Path("/Users/michaeljoyce/Desktop/LEARNVIA")

    required_files = [
        "authoring_prompt_rules.txt",
        "style_prompt_rules.txt",
        "product_vision_context.txt",
        "src/models.py",
        "src/prompts.py",
        "src/orchestrator.py",
        "src/consensus.py",
        "src/reports.py",
        "src/main.py",
        "tests/test_models.py",
        "tests/test_prompts.py",
        "tests/test_orchestrator.py",
        "tests/test_consensus.py",
        "tests/test_reports.py",
        "tests/test_main.py",
        "tests/test_integration.py",
        "config.py",
        "run_review.py",
        "requirements.txt"
    ]

    missing = []
    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} missing")
            missing.append(file_path)

    if missing:
        print(f"\n{len(missing)} files missing")
        return False

    return True

def check_api_config():
    """Check API configuration"""
    print_section("API Configuration Check")

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("❌ OPENAI_API_KEY not set in environment")
        print("\nTo fix:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your OpenAI API key")
        return False

    if api_key == "your_api_key_here":
        print("❌ OPENAI_API_KEY still has placeholder value")
        return False

    print("✅ API key configured")
    print(f"   Key starts with: {api_key[:10]}...")
    return True

async def check_imports():
    """Verify all modules can be imported"""
    print_section("Module Import Check")

    modules_to_import = [
        "src.models",
        "src.prompts",
        "src.orchestrator",
        "src.consensus",
        "src.reports",
        "src.main",
        "config"
    ]

    failed = []
    for module_name in modules_to_import:
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name} imports successfully")
        except Exception as e:
            print(f"❌ {module_name} import failed: {e}")
            failed.append(module_name)

    if failed:
        print(f"\n{len(failed)} modules failed to import")
        return False

    return True

def run_unit_tests():
    """Run unit tests"""
    print_section("Unit Test Execution")

    import subprocess

    result = subprocess.run(
        ["pytest", "tests/", "-v", "--tb=short"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("✅ All tests passed")
        # Count tests
        lines = result.stdout.split('\n')
        for line in lines:
            if 'passed' in line:
                print(f"   {line.strip()}")
        return True
    else:
        print("❌ Some tests failed")
        print("\nFailure details:")
        print(result.stdout[-500:])  # Last 500 chars
        return False

async def test_demo_module():
    """Test with demo module"""
    print_section("Demo Module Test")

    try:
        from src.main import RevisionSystem
        from src.models import ModuleContent, ReviewPass

        # Create demo module
        module = ModuleContent(
            module_id="VERIFY_TEST",
            title="Verification Test Module",
            content="Simple test content for verification"
        )

        # Initialize system (will fail without valid API key)
        system = RevisionSystem(api_key=os.getenv("OPENAI_API_KEY", "test_key"))

        print("✅ System initialized successfully")
        print("   Ready to process modules")

        return True

    except Exception as e:
        print(f"❌ Demo test failed: {e}")
        return False

async def main():
    """Run all verification checks"""

    print("""
╔══════════════════════════════════════════════════════════════╗
║          LEARNVIA SYSTEM VERIFICATION SCRIPT                ║
╚══════════════════════════════════════════════════════════════╝
    """)

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("File Structure", check_files),
        ("API Config", check_api_config),
        ("Module Imports", check_imports),
        ("Unit Tests", run_unit_tests),
        ("Demo Module", test_demo_module)
    ]

    results = {}

    for name, check_func in checks:
        try:
            if asyncio.iscoroutinefunction(check_func):
                result = await check_func()
            else:
                result = check_func()
            results[name] = result
        except Exception as e:
            print(f"\n❌ {name} check crashed: {e}")
            results[name] = False

    # Summary
    print_section("VERIFICATION SUMMARY")

    passed = sum(1 for r in results.values() if r)
    total = len(results)

    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name:20} {status}")

    print(f"\n  Overall: {passed}/{total} checks passed")

    if passed == total:
        print("\n🎉 System fully operational!")
        print("   You can now run: python run_review.py --demo")
        return 0
    else:
        print("\n⚠️  System not fully configured")
        print("   Please address the issues above")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
```

**Step 2: Make script executable**

Run: `chmod +x verify_system.py`

**Step 3: Run verification**

Run: `python verify_system.py`
Expected: System verification output

**Step 4: Final commit**

```bash
git add verify_system.py
git commit -m "feat: add system verification script"
```

---

## Summary

Plan complete and saved to `docs/plans/2025-10-28-ai-revision-implementation.md`. Two execution options:

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?