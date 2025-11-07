"""
Mock API responses for CALCULUS CONTENT REVIEW
Detects calculus-specific pedagogical issues for Calc I-IV
Focuses on: multiple representations, misconceptions, conceptual understanding
"""

import asyncio
import random
import re
from typing import List, Dict, Any
from dataclasses import dataclass
import sys
from pathlib import Path

# Import models from real system
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))
from CODE.models import ReviewFeedback, ReviewerRole, SeverityLevel, ReviewPass


class ContentAnalyzer:
    """Analyzes calculus content for pedagogical issues"""

    def ensure_suggestions(self, issues: List[Dict]) -> List[Dict]:
        """Ensure all issues have suggestions and deferred flags"""
        for issue in issues:
            if 'deferred' not in issue:
                issue_type = issue.get('issue_type', '')
                issue_text = issue.get('issue', '').lower()
                is_deferred = any(keyword in issue_type or keyword in issue_text
                                 for keyword in ['accessibility', 'figure', 'animation', 'visual', 'alt text', 'image'])
                issue['deferred'] = is_deferred

            if 'solution' not in issue or not issue['solution']:
                severity = issue.get('severity', 3)
                issue_type = issue.get('issue_type', 'general')
                if severity >= 4:
                    issue['solution'] = f"Review the {issue_type.replace('_', ' ')} and ensure it meets calculus pedagogy standards for non-traditional learners."
                elif severity >= 3:
                    issue['solution'] = f"Improve the {issue_type.replace('_', ' ')} to support diverse learners."
                else:
                    issue['solution'] = f"Consider refining the {issue_type.replace('_', ' ')} for consistency."
        return issues

    def analyze_multiple_representations(self, content: str) -> List[Dict]:
        """Check if calculus concepts use graphical, numerical, and symbolic representations"""
        issues = []

        # Detect derivative without sufficient representations
        if "derivative" in content.lower():
            has_graph = any(word in content.lower() for word in ["graph", "slope", "tangent", "curve"])
            has_numeric = any(word in content.lower() for word in ["table", "difference quotient", "h→0", "approaches"])
            has_symbolic = any(notation in content for notation in ["d/dx", "f'", "dy/dx", "\\frac{d", "prime"])

            if not has_graph:
                issues.append({
                    "issue": "Derivative concept lacks graphical representation (tangent line, slope visualization)",
                    "severity": 4,
                    "location": "Derivative section",
                    "issue_type": "missing_representation",
                    "solution": "Add graph showing tangent line and connection between slope and derivative"
                })

            if not has_numeric:
                issues.append({
                    "issue": "Derivative concept lacks numerical approach (difference quotient table, rate calculation)",
                    "severity": 3,
                    "location": "Derivative section",
                    "issue_type": "missing_representation",
                    "solution": "Add table showing (f(x+h)-f(x))/h values as h approaches 0"
                })

        # Detect integral without sufficient representations
        if "integral" in content.lower() or "∫" in content:
            has_graph = any(word in content.lower() for word in ["area", "curve", "rectangle", "riemann"])
            has_numeric = any(word in content.lower() for word in ["sum", "Δx", "partition", "approximation"])
            has_symbolic = "∫" in content or "integral" in content.lower()

            if not has_graph:
                issues.append({
                    "issue": "Integral concept lacks graphical representation (area under curve, Riemann rectangles)",
                    "severity": 4,
                    "location": "Integral section",
                    "issue_type": "missing_representation",
                    "solution": "Add diagram showing area interpretation with rectangles approaching integral"
                })

            if not has_numeric:
                issues.append({
                    "issue": "Integral concept lacks numerical approach (Riemann sum calculation)",
                    "severity": 3,
                    "location": "Integral section",
                    "issue_type": "missing_representation",
                    "solution": "Add numerical example calculating Riemann sum with specific rectangles"
                })

        # Detect limit without sufficient representations
        if "limit" in content.lower():
            has_graph = any(word in content.lower() for word in ["graph", "approach", "hole", "asymptote"])
            has_numeric = "table" in content.lower() or "values" in content.lower()

            if not has_graph:
                issues.append({
                    "issue": "Limit concept lacks graphical representation (function approaching value)",
                    "severity": 3,
                    "location": "Limit section",
                    "issue_type": "missing_representation",
                    "solution": "Add graph showing function behavior as x approaches limit point"
                })

            if not has_numeric:
                issues.append({
                    "issue": "Limit concept lacks numerical approach (table of approaching values)",
                    "severity": 2,
                    "location": "Limit section",
                    "issue_type": "missing_representation",
                    "solution": "Add table showing x and f(x) values as x approaches the limit"
                })

        return issues

    def analyze_calculus_misconceptions(self, content: str) -> List[Dict]:
        """Detect when common calculus misconceptions are not addressed"""
        issues = []

        # Misconception 1: Derivative is just slope (not instantaneous rate)
        if "derivative" in content.lower():
            addresses_instantaneous = any(phrase in content.lower() for phrase in [
                "instantaneous rate", "instantaneous", "at a point", "at x =", "limit of slopes"
            ])
            if not addresses_instantaneous:
                issues.append({
                    "issue": "Derivative taught without emphasizing 'instantaneous rate' distinction from average rate",
                    "severity": 4,
                    "location": "Derivative introduction",
                    "issue_type": "misconception_not_addressed",
                    "solution": "Explicitly distinguish 'slope of secant line (average rate)' from 'slope of tangent line (instantaneous rate via limit)'"
                })

        # Misconception 2: Limit equals function value
        if "limit" in content.lower():
            addresses_discontinuity = any(phrase in content.lower() for phrase in [
                "continuous", "discontinuous", "undefined at", "hole", "does not exist"
            ])
            if not addresses_discontinuity:
                issues.append({
                    "issue": "Limit concept lacks clarification that lim f(x) ≠ f(a) at discontinuities",
                    "severity": 4,
                    "location": "Limit introduction",
                    "issue_type": "misconception_not_addressed",
                    "solution": "Show example where limit exists but function undefined (removable discontinuity)"
                })

        # Misconception 3: Integral is the antiderivative (not area)
        if "integral" in content.lower():
            addresses_area_definition = any(phrase in content.lower() for phrase in [
                "area under", "riemann", "sum", "accumulated"
            ])
            addresses_ftc = "fundamental theorem" in content.lower() or "ftc" in content.lower()

            if not addresses_area_definition and addresses_ftc:
                issues.append({
                    "issue": "Integral introduced via Fundamental Theorem without establishing area definition first",
                    "severity": 4,
                    "location": "Integral introduction",
                    "issue_type": "misconception_not_addressed",
                    "solution": "Teach integral as area (Riemann sums) BEFORE connecting to antiderivative via FTC"
                })

        # Misconception 4: Chain rule is simple multiplication
        if "chain rule" in content.lower():
            addresses_composition = any(phrase in content.lower() for phrase in [
                "composition", "composed", "inner function", "outer function", "f(g(x))", "nested"
            ])
            if not addresses_composition:
                issues.append({
                    "issue": "Chain rule taught without explicit function composition foundation",
                    "severity": 4,
                    "location": "Chain rule section",
                    "issue_type": "misconception_not_addressed",
                    "solution": "Review composition f(g(x)) before chain rule; identify inner/outer functions in examples"
                })

        # Misconception 5: Concavity means increasing
        if "concav" in content.lower():
            distinguishes_from_increasing = any(phrase in content.lower() for phrase in [
                "second derivative", "f''", "rate of change", "first derivative"
            ])
            if not distinguishes_from_increasing:
                issues.append({
                    "issue": "Concavity discussion may conflate f' (increasing) with f'' (concavity)",
                    "severity": 3,
                    "location": "Concavity section",
                    "issue_type": "misconception_not_addressed",
                    "solution": "Explicitly distinguish: f'>0 means increasing; f''>0 means concave up (rate increasing)"
                })

        # Misconception 6: Integral always positive
        if "integral" in content.lower() and "∫" in content:
            addresses_signed_area = any(phrase in content.lower() for phrase in [
                "signed area", "negative area", "below x-axis", "above and below"
            ])
            if not addresses_signed_area:
                issues.append({
                    "issue": "Integral taught as 'area' without emphasizing signed area (negative below x-axis)",
                    "severity": 3,
                    "location": "Integral section",
                    "issue_type": "misconception_not_addressed",
                    "solution": "Emphasize 'signed area': positive above x-axis, negative below"
                })

        return issues

    def analyze_conceptual_procedural_balance(self, content: str) -> List[Dict]:
        """Check if procedures are taught with conceptual understanding"""
        issues = []

        # Power rule without conceptual foundation
        if "power rule" in content.lower() or ("d/dx" in content and "x^" in content):
            has_why = any(phrase in content.lower() for phrase in [
                "why", "because", "reason", "concept", "meaning", "limit definition", "from the definition"
            ])
            has_formula_only = "=" in content and "x^" in content and not has_why

            if has_formula_only:
                issues.append({
                    "issue": "Power rule presented as formula without conceptual motivation or derivation",
                    "severity": 3,
                    "location": "Power rule section",
                    "issue_type": "procedural_only",
                    "solution": "Show where power rule comes from (limit of difference quotient) before just stating formula"
                })

        # Integration techniques without conceptual foundation
        if "u-substitution" in content.lower() or "substitution" in content.lower():
            mentions_chain_rule = "chain rule" in content.lower()
            if not mentions_chain_rule:
                issues.append({
                    "issue": "U-substitution taught without connecting to chain rule (reverse process)",
                    "severity": 3,
                    "location": "U-substitution section",
                    "issue_type": "procedural_only",
                    "solution": "Explain u-substitution as 'undoing the chain rule' before showing procedure"
                })

        # Critical points without conceptual understanding
        if "critical point" in content.lower():
            explains_why_derivative_zero = any(phrase in content.lower() for phrase in [
                "maximum", "minimum", "horizontal tangent", "slope is zero", "rate of change is zero"
            ])
            if not explains_why_derivative_zero:
                issues.append({
                    "issue": "Critical points defined without explaining WHY f'(x)=0 finds them",
                    "severity": 3,
                    "location": "Critical points section",
                    "issue_type": "procedural_only",
                    "solution": "Explain: at max/min, tangent line is horizontal (slope=0), so f'(x)=0"
                })

        return issues

    def analyze_assessment_alignment(self, content: str) -> List[Dict]:
        """Check if assessments test concepts, not just computation"""
        issues = []

        if "practice" in content.lower() or "question" in content.lower() or "problem" in content.lower():
            # Count computational vs conceptual indicators
            computational_words = ["find", "compute", "calculate", "evaluate", "solve for", "differentiate"]
            conceptual_words = ["explain", "why", "describe", "compare", "interpret", "what does", "meaning"]

            comp_count = sum(1 for word in computational_words if word in content.lower())
            concept_count = sum(1 for word in conceptual_words if word in content.lower())

            if comp_count > 5 and concept_count == 0:
                issues.append({
                    "issue": "Assessment appears purely computational without conceptual understanding questions",
                    "severity": 4,
                    "location": "Practice questions",
                    "issue_type": "assessment_imbalance",
                    "solution": "Add conceptual questions: 'Explain what f'(3)=5 means', 'Describe the connection between...'"
                })

            if comp_count > 0 and concept_count > 0 and comp_count / (comp_count + concept_count) > 0.8:
                issues.append({
                    "issue": "Assessment heavily weighted toward computation (>80%) vs conceptual understanding",
                    "severity": 3,
                    "location": "Practice questions",
                    "issue_type": "assessment_imbalance",
                    "solution": "Balance with more interpretation/explanation questions"
                })

        return issues

    def analyze_real_world_contexts(self, content: str) -> List[Dict]:
        """Check if real-world contexts are appropriate for non-traditional learners"""
        issues = []

        # Detect overly abstract contexts
        abstract_contexts = ["arbitrary function", "generic function", "function f", "given function"]
        for abstract in abstract_contexts:
            if abstract in content.lower() and "example" in content.lower():
                issues.append({
                    "issue": f"Abstract context '{abstract}' where concrete example would aid understanding",
                    "severity": 2,
                    "location": f"Near '{abstract}'",
                    "issue_type": "abstract_context",
                    "solution": "Use specific function (parabola, exponential) or real scenario (temperature, speed)"
                })

        # Detect disconnected advanced contexts
        disconnected_contexts = [
            "rocket", "spacecraft", "satellite", "orbital",
            "financial derivative", "option pricing", "portfolio",
            "epidemiology", "disease model", "infection rate",
            "quantum", "relativity", "electromagnetic"
        ]
        for context in disconnected_contexts:
            if context in content.lower():
                issues.append({
                    "issue": f"Context '{context}' requires domain knowledge beyond typical student experience",
                    "severity": 2,
                    "location": f"Near '{context}'",
                    "issue_type": "irrelevant_context",
                    "solution": "Use everyday contexts: phone battery, social media, driving, cooking, fitness"
                })

        return issues

    def analyze_pedagogical_flow(self, content: str) -> List[Dict]:
        """Check for pedagogical flow issues"""
        issues = []

        # Check for missing learning objectives
        if "learning objective" not in content.lower() and "you will learn" not in content.lower() and "students will" not in content.lower():
            issues.append({
                "issue": "Missing clear learning objectives at module start",
                "severity": 5,
                "location": "Module introduction",
                "issue_type": "missing_objectives",
                "solution": "Add explicit learning objectives: 'After this module, you will be able to...'",
                "deferred": False
            })

        # Check for transitions
        if len(content) > 5000:
            transition_words = ["however", "therefore", "moreover", "furthermore", "consequently", "next", "now", "then"]
            transition_count = sum(1 for word in transition_words if word in content.lower())
            if transition_count < 3:
                issues.append({
                    "issue": "Few transitional phrases detected - may affect flow between concepts",
                    "severity": 2,
                    "location": "Throughout module",
                    "issue_type": "pedagogical_flow",
                    "solution": "Add transitional phrases to connect concepts logically"
                })

        # Add multiple representations check
        issues.extend(self.analyze_multiple_representations(content))

        # Add misconceptions check
        issues.extend(self.analyze_calculus_misconceptions(content))

        # Add conceptual/procedural balance
        issues.extend(self.analyze_conceptual_procedural_balance(content))

        # Add assessment alignment
        issues.extend(self.analyze_assessment_alignment(content))

        # Add context quality
        issues.extend(self.analyze_real_world_contexts(content))

        return issues

    def analyze_structural_integrity(self, content: str) -> List[Dict]:
        """Check for structural issues"""
        issues = []

        # Check for missing title
        if not content.strip().startswith("#"):
            issues.append({
                "issue": "Module lacks proper title header",
                "severity": 3,
                "location": "Beginning of module",
                "issue_type": "structure"
            })

        # Check for missing summary
        if "summary" not in content.lower() and "conclusion" not in content.lower():
            issues.append({
                "issue": "Module lacks summary section reinforcing key concepts",
                "severity": 3,
                "location": "End of module",
                "issue_type": "structure",
                "solution": "Add summary listing key takeaways and formulas"
            })

        # Check for long paragraphs individually
        paragraphs = content.split('\n\n')
        long_paras = [(i, p) for i, p in enumerate(paragraphs) if len(p) > 800]
        if long_paras:
            for i, (para_num, para) in enumerate(long_paras[:3]):
                issues.append({
                    "issue": f"Paragraph {para_num} is very long ({len(para)} chars) - may overwhelm students",
                    "severity": 2,
                    "location": f"Paragraph {para_num}",
                    "issue_type": "structure",
                    "solution": "Break into smaller paragraphs, each focusing on one idea"
                })

        # Check for missing examples
        example_count = content.lower().count("example") + content.lower().count("ex:")
        if example_count < 3:
            issues.append({
                "issue": "Limited worked examples - students benefit from seeing multiple examples",
                "severity": 3,
                "location": "Throughout module",
                "issue_type": "pedagogical_flow",
                "solution": "Add 2-3 more worked examples with varying difficulty"
            })

        # Check for mentioned but missing visuals
        visual_triggers = ["diagram", "figure", "graph", "plot", "curve"]
        for trigger in visual_triggers:
            if trigger in content.lower() and "![" not in content:
                issues.append({
                    "issue": f"Content mentions '{trigger}' but no image embedded",
                    "severity": 3,
                    "location": f"Near '{trigger}'",
                    "issue_type": "missing_visual",
                    "solution": f"Add actual {trigger} or remove the reference"
                })

        return issues

    def analyze_conceptual_clarity(self, content: str) -> List[Dict]:
        """Check for clarity issues"""
        issues = []

        # Check for vague language - report each occurrence
        vague_phrases = ["various", "different", "several", "some", "many", "few"]
        for phrase in vague_phrases:
            if phrase in content.lower():
                issues.append({
                    "issue": f"Vague language: '{phrase}' - be more specific",
                    "severity": 2,
                    "location": f"Search for '{phrase}'",
                    "issue_type": "clarity",
                    "solution": f"Replace '{phrase}' with specific quantities or examples"
                })

        # Check for long sentences
        sentences = re.split(r'[.!?]\s+', content)
        long_sentences = [s for s in sentences if len(s) > 200]
        if long_sentences:
            issues.append({
                "issue": "Some sentences are very long - consider breaking them up for readability",
                "severity": 2,
                "location": "Throughout module",
                "issue_type": "style_grammar",
                "solution": "Break complex sentences into simpler, shorter sentences"
            })

        return issues

    def analyze_style_compliance(self, content: str) -> List[Dict]:
        """Check for style violations"""
        issues = []

        # Check for contractions
        contractions = ["don't", "won't", "can't", "we've", "they're", "it's"]
        for contraction in contractions:
            if contraction in content.lower():
                issues.append({
                    "issue": f"Contraction '{contraction}' found - expand to full form per style guide",
                    "severity": 2,
                    "location": f"Search for '{contraction}'",
                    "issue_type": "style_contraction",
                    "solution": f"Replace '{contraction}' with full form"
                })

        # Check for inconsistent spacing
        double_space_paras = content.count('\n\n\n')
        if double_space_paras > 3:
            issues.append({
                "issue": "Inconsistent paragraph spacing detected",
                "severity": 1,
                "location": "Throughout module",
                "issue_type": "style_consistency",
                "solution": "Standardize to double newlines between paragraphs"
            })

        return issues

    def analyze_assessment_quality(self, content: str) -> List[Dict]:
        """Check assessment quality"""
        issues = []

        # Check if practice problems have solutions
        if "practice" in content.lower() or "problem" in content.lower():
            if "solution" not in content.lower() and "answer" not in content.lower():
                issues.append({
                    "issue": "Practice problems lack solutions or hints for self-study",
                    "severity": 3,
                    "location": "Practice section",
                    "issue_type": "assessment",
                    "solution": "Add detailed solutions or progressive hints"
                })

        return issues


class MockAPIClient:
    """Mock API client that returns realistic calculus review responses"""

    def __init__(self):
        self.analyzer = ContentAnalyzer()
        self.response_delay = 0.1

    async def get_review(self, content: str, reviewer_config: Dict) -> Dict:
        """Generate realistic calculus review based on content"""
        await asyncio.sleep(self.response_delay)

        focus = reviewer_config.get("focus", "general")
        competency = reviewer_config.get("competency", None)

        issues = []

        if competency == "Pedagogical Flow" or focus == "general":
            issues.extend(self.analyzer.analyze_pedagogical_flow(content))

        if competency == "Structural Integrity" or focus == "general":
            issues.extend(self.analyzer.analyze_structural_integrity(content))

        if competency == "Conceptual Clarity" or focus == "general":
            issues.extend(self.analyzer.analyze_conceptual_clarity(content))

        if competency in ["Mechanical Compliance", "Consistency"] or focus == "style":
            issues.extend(self.analyzer.analyze_style_compliance(content))

        if competency == "Assessment Quality" or focus == "general":
            issues.extend(self.analyzer.analyze_assessment_quality(content))

        # Add variation between agents - keep most issues
        if len(issues) > 5 and random.random() > 0.6:
            drop_count = random.randint(1, 2)
            issues = random.sample(issues, len(issues) - drop_count)

        # Vary severity slightly
        for issue in issues:
            if random.random() < 0.2:
                issue["severity"] = max(1, min(5, issue["severity"] + random.choice([-1, 1])))

        issues = self.analyzer.ensure_suggestions(issues)

        return {"issues": issues}


class MockReviewerPool:
    """Mock reviewer pool for calculus content review"""

    def __init__(self, review_pass: ReviewPass, num_reviewers: int,
                 api_client: MockAPIClient, style_only: bool = False):
        self.review_pass = review_pass
        self.num_reviewers = num_reviewers
        self.api_client = api_client
        self.style_only = style_only
        self.reviewers = self._create_reviewers()

    def _create_reviewers(self) -> List[Dict]:
        """Create reviewer configurations"""
        reviewers = []

        if self.style_only:
            for i in range(self.num_reviewers):
                reviewers.append({
                    "id": f"style_reviewer_{i}",
                    "focus": "style",
                    "competency": random.choice(["Mechanical Compliance", "Consistency"])
                })
        else:
            # 60% specialists, 40% generalists
            specialist_count = int(self.num_reviewers * 0.6)
            competencies = [
                "Pedagogical Flow", "Structural Integrity", "Conceptual Clarity",
                "Assessment Quality"
            ]

            for i in range(specialist_count):
                reviewers.append({
                    "id": f"specialist_{i}",
                    "focus": "specialist",
                    "competency": competencies[i % len(competencies)]
                })

            for i in range(self.num_reviewers - specialist_count):
                reviewers.append({
                    "id": f"generalist_{i}",
                    "focus": "general",
                    "competency": None
                })

        return reviewers

    async def review_parallel(self, module) -> List[ReviewFeedback]:
        """Run reviews in parallel"""
        tasks = []
        for reviewer in self.reviewers:
            tasks.append(self._review_single(module, reviewer))

        nested_results = await asyncio.gather(*tasks)

        flat_results = []
        for items in nested_results:
            if isinstance(items, list):
                flat_results.extend(items)
            else:
                flat_results.append(items)

        return flat_results

    async def _review_single(self, module, reviewer_config) -> List[ReviewFeedback]:
        """Perform single review"""
        response = await self.api_client.get_review(module.content, reviewer_config)

        feedback_items = []
        for issue in response["issues"]:
            competency = reviewer_config.get("competency", "")
            if competency in ["Structural Integrity", "Pedagogical Flow", "Conceptual Clarity", "Assessment Quality"]:
                role = ReviewerRole.AUTHORING
            else:
                role = ReviewerRole.STYLE

            feedback = ReviewFeedback(
                reviewer_id=reviewer_config["id"],
                issue_type=issue.get("issue_type", "general"),
                severity=issue["severity"],
                location=issue.get("location", ""),
                issue=issue["issue"],
                suggestion=issue.get("solution", ""),
                confidence_contribution=random.uniform(0.7, 0.95)
            )
            feedback_items.append(feedback)

        return feedback_items
