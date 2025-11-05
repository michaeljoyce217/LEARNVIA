"""
Test suite for the AI reviewer functionality.
Tests individual reviewers and their interaction with the OpenAI API.
"""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio
from datetime import datetime

# Will be imported once implemented
from src.reviewers import (
    BaseReviewer, AuthoringReviewer, StyleReviewer,
    ReviewerPool, APIClient
)
from src.models import (
    ReviewerRole, ReviewPass, SeverityLevel,
    ReviewFeedback, ModuleContent, ReviewerConfig
)


class TestBaseReviewer:
    """Tests for the BaseReviewer class."""

    def test_reviewer_initialization(self):
        """Test creating a reviewer with configuration."""
        config = ReviewerConfig(
            reviewer_id="test_01",
            role=ReviewerRole.AUTHORING,
            review_pass=ReviewPass.CONTENT_PASS_1,
            focus_area="pedagogical_flow"
        )

        reviewer = BaseReviewer(config)
        assert reviewer.config.reviewer_id == "test_01"
        assert reviewer.config.role == ReviewerRole.AUTHORING

    @pytest.mark.asyncio
    @patch('src.reviewers.APIClient')
    async def test_review_module_async(self, mock_api_client):
        """Test async review of a module."""
        config = ReviewerConfig(
            reviewer_id="test_01",
            role=ReviewerRole.AUTHORING,
            review_pass=ReviewPass.CONTENT_PASS_1,
            focus_area="pedagogical_flow"
        )

        # Mock API response (use AsyncMock for async methods)
        mock_instance = mock_api_client.return_value
        mock_instance.call_api_async = AsyncMock(return_value={
            "issues": [{
                "type": "concept_jump",
                "severity": 4,
                "location": "paragraph 3",
                "issue": "Large conceptual jump between examples",
                "suggestion": "Add intermediate step"
            }]
        })
        mock_instance.validate_response = MagicMock(return_value=True)

        reviewer = BaseReviewer(config, api_client=mock_instance)
        module = ModuleContent(content="Test module content")

        feedback = await reviewer.review_async(module)

        assert len(feedback) == 1
        assert feedback[0].severity == 4
        assert feedback[0].issue_type == "concept_jump"

    def test_parse_api_response(self):
        """Test parsing API response into feedback objects."""
        config = ReviewerConfig(
            reviewer_id="test_01",
            role=ReviewerRole.AUTHORING,
            review_pass=ReviewPass.CONTENT_PASS_1,
            focus_area="pedagogical_flow"
        )

        reviewer = BaseReviewer(config)

        api_response = {
            "issues": [
                {
                    "type": "missing_examples",
                    "severity": 4,
                    "location": "section 2",
                    "issue": "No concrete examples provided",
                    "suggestion": "Add student-relevant examples"
                },
                {
                    "type": "vague_reference",
                    "severity": 3,
                    "location": "line 10",
                    "issue": "Uses 'it' without clear antecedent",
                    "suggestion": "Replace with specific noun"
                }
            ]
        }

        feedback_list = reviewer.parse_response(api_response)

        assert len(feedback_list) == 2
        assert feedback_list[0].issue_type == "missing_examples"
        assert feedback_list[1].severity == 3


class TestAuthoringReviewer:
    """Tests for the AuthoringReviewer specialized class."""

    def test_authoring_reviewer_prompt_generation(self):
        """Test that authoring reviewer generates correct prompts."""
        config = ReviewerConfig(
            reviewer_id="authoring_01",
            role=ReviewerRole.AUTHORING,
            review_pass=ReviewPass.CONTENT_PASS_1,
            focus_area="pedagogical_flow",
            prompt_variation="Focus on student engagement"
        )

        reviewer = AuthoringReviewer(config)
        module = ModuleContent(content="Test content")

        prompt = reviewer.generate_prompt(module)

        # Check that focus area is included
        assert "pedagogical" in prompt.lower()
        # Check that prompt variation is included
        assert "student engagement" in prompt.lower()
        # Check that pedagogical-specific guidance is included
        assert "chunking" in prompt.lower() or "scaffolding" in prompt.lower()

    def test_authoring_specific_validations(self):
        """Test authoring-specific validation rules."""
        config = ReviewerConfig(
            reviewer_id="authoring_01",
            role=ReviewerRole.AUTHORING,
            review_pass=ReviewPass.CONTENT_PASS_1,
            focus_area="examples"
        )

        reviewer = AuthoringReviewer(config)

        # Test with module missing examples
        module = ModuleContent(
            content="This is a lesson without any examples.",
            components={"lesson": "content", "examples": ""}
        )

        issues = reviewer.check_structural_requirements(module)

        assert any("example" in issue.lower() for issue in issues)


class TestStyleReviewer:
    """Tests for the StyleReviewer specialized class."""

    def test_style_reviewer_prompt_generation(self):
        """Test that style reviewer generates correct prompts."""
        config = ReviewerConfig(
            reviewer_id="style_01",
            role=ReviewerRole.STYLE,
            review_pass=ReviewPass.COPY_PASS_1,
            focus_area="contractions_imperatives"
        )

        reviewer = StyleReviewer(config)
        module = ModuleContent(content="Let's find the equation.")

        prompt = reviewer.generate_prompt(module)

        # Check that focus area is included
        assert "contraction" in prompt.lower() or "imperative" in prompt.lower()
        # Check that automatic detection worked
        assert "let's" in prompt.lower()
        # Check that guidance is included
        assert "possessive" in prompt.lower() or "allowed" in prompt.lower()

    def test_contraction_detection(self):
        """Test detection of contractions in content."""
        config = ReviewerConfig(
            reviewer_id="style_01",
            role=ReviewerRole.STYLE,
            review_pass=ReviewPass.COPY_PASS_1,
            focus_area="contractions"
        )

        reviewer = StyleReviewer(config)

        content_with_contractions = "Let's solve this. It's important that we don't use contractions."
        issues = reviewer.detect_contractions(content_with_contractions)

        assert len(issues) >= 3  # Let's, It's, don't

    def test_imperative_detection(self):
        """Test detection of improper imperative use."""
        config = ReviewerConfig(
            reviewer_id="style_02",
            role=ReviewerRole.STYLE,
            review_pass=ReviewPass.COPY_PASS_1,
            focus_area="imperatives"
        )

        reviewer = StyleReviewer(config)

        content_with_imperatives = "Find the equation. Calculate the slope. State your answer."
        issues = reviewer.detect_imperatives(content_with_imperatives)

        assert len(issues) >= 3  # Find, Calculate, State


class TestReviewerPool:
    """Tests for the ReviewerPool that manages multiple reviewers."""

    def test_pool_initialization(self):
        """Test creating a pool of reviewers."""
        pool = ReviewerPool(ReviewPass.CONTENT_PASS_1, num_reviewers=20)

        assert len(pool.reviewers) == 20
        assert all(r.config.review_pass == ReviewPass.CONTENT_PASS_1 for r in pool.reviewers)

    def test_pool_reviewer_distribution(self):
        """Test that reviewer focus areas are properly distributed."""
        pool = ReviewerPool(ReviewPass.CONTENT_PASS_1, num_reviewers=20)

        focus_areas = [r.config.focus_area for r in pool.reviewers]

        # Check that we have diverse focus areas
        assert "pedagogical_flow" in focus_areas
        assert "examples" in focus_areas
        assert "quiz_questions" in focus_areas

    @pytest.mark.asyncio
    @patch('src.reviewers.APIClient')
    async def test_pool_parallel_review(self, mock_api_client):
        """Test parallel execution of multiple reviewers."""
        # Mock the API client instance
        mock_instance = mock_api_client.return_value
        mock_instance.call_api_async = AsyncMock(return_value={
            "issues": [{
                "type": "test_issue",
                "severity": 3,
                "location": "test",
                "issue": "Test issue",
                "suggestion": "Test suggestion"
            }]
        })
        mock_instance.validate_response = MagicMock(return_value=True)

        pool = ReviewerPool(ReviewPass.CONTENT_PASS_1, num_reviewers=20, api_client=mock_instance)
        module = ModuleContent(content="Test content")

        start_time = datetime.now()
        all_feedback = await pool.review_parallel(module)
        end_time = datetime.now()

        # Check that we got feedback from all reviewers (20 for content pass: 10 authoring + 10 style)
        assert len(all_feedback) == 20

        # Check that execution was parallel (should be fast)
        duration = (end_time - start_time).total_seconds()
        assert duration < 2  # Parallel execution should be under 2 seconds

    @pytest.mark.asyncio
    @patch('src.reviewers.APIClient')
    async def test_pool_error_handling(self, mock_api_client):
        """Test that pool handles individual reviewer errors gracefully."""
        # Create mock API client
        mock_instance = mock_api_client.return_value
        mock_instance.validate_response = MagicMock(return_value=True)

        pool = ReviewerPool(ReviewPass.CONTENT_PASS_1, num_reviewers=20, api_client=mock_instance)

        # Mock one reviewer to fail
        pool.reviewers[1].review_async = AsyncMock(side_effect=Exception("API Error"))

        # Mock others to succeed
        successful_feedback = [ReviewFeedback(
            reviewer_id="test_reviewer",
            issue_type="test",
            severity=2,
            location="test",
            issue="test",
            suggestion="test"
        )]

        # Mock all other reviewers to succeed
        for i in range(len(pool.reviewers)):
            if i != 1:  # Skip the failing reviewer
                pool.reviewers[i].review_async = AsyncMock(return_value=successful_feedback)

        module = ModuleContent(content="Test content")
        all_feedback = await pool.review_parallel(module)

        # Should still get feedback from 19 working reviewers (1 failed out of 20)
        assert len(all_feedback) == 19


class TestAPIClient:
    """Tests for the API client that interfaces with OpenAI."""

    def test_api_client_initialization(self):
        """Test API client setup."""
        client = APIClient(api_key="test_key")
        assert client.api_key == "test_key"

    @patch('openai.ChatCompletion.create')
    def test_api_call_success(self, mock_openai):
        """Test successful API call."""
        mock_openai.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content='{"issues": []}'))]
        )

        client = APIClient(api_key="test_key")
        response = client.call_api("Test prompt", "Test system prompt")

        assert response == {"issues": []}
        mock_openai.assert_called_once()

    @patch('openai.ChatCompletion.create')
    def test_api_call_retry_on_rate_limit(self, mock_openai):
        """Test that API client retries on rate limit errors."""
        # First call fails with rate limit, second succeeds
        mock_openai.side_effect = [
            Exception("Rate limit exceeded"),
            MagicMock(choices=[MagicMock(message=MagicMock(content='{"issues": []}'))])
        ]

        client = APIClient(api_key="test_key", max_retries=2)
        response = client.call_api("Test prompt", "Test system prompt")

        assert response == {"issues": []}
        assert mock_openai.call_count == 2

    def test_api_response_validation(self):
        """Test that API responses are validated."""
        client = APIClient(api_key="test_key")

        # Valid response
        valid = client.validate_response({"issues": []})
        assert valid is True

        # Invalid response
        invalid = client.validate_response({"wrong_key": []})
        assert invalid is False


# Integration test
class TestReviewSystemIntegration:
    """Integration tests for the complete review system."""

    @pytest.mark.asyncio
    @patch('src.reviewers.APIClient')
    async def test_complete_review_pass(self, mock_api_client):
        """Test a complete review pass with all components."""
        # Setup mock responses
        mock_instance = mock_api_client.return_value
        mock_instance.call_api_async = AsyncMock(return_value={
            "issues": [{
                "type": "test_issue",
                "severity": 4,
                "location": "test location",
                "issue": "Test issue found",
                "suggestion": "Test suggestion provided"
            }]
        })
        mock_instance.validate_response = MagicMock(return_value=True)

        # Create module
        module = ModuleContent(
            content="This is test content for the module.",
            module_id="test_module_001",
            title="Test Module"
        )

        # Create reviewer pool for first pass
        pool = ReviewerPool(ReviewPass.CONTENT_PASS_1, num_reviewers=20, api_client=mock_instance)

        # Execute review
        feedback = await pool.review_parallel(module)

        # Verify results
        assert len(feedback) == 20  # 20 reviewers for content pass (10 authoring + 10 style)
        assert all(f.severity == 4 for f in feedback)
        assert all(f.issue_type == "test_issue" for f in feedback)