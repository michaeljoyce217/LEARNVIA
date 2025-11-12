#!/usr/bin/env python3
"""
Example usage script for the Learnvia AI Revision System.
Demonstrates how to review educational modules using 60 AI reviewers.
"""

import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models import ModuleContent, ReviewPass
from src.orchestrator import RevisionOrchestrator, ModuleLoader
from src.reviewers import APIClient
from src.report_generator import ReportGenerator


def example_basic_review():
    """Basic example: Review a module with default settings."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Module Review")
    print("="*70)

    # Create sample module content
    sample_content = """
# Introduction to Linear Equations

## Framing Text
Linear equations are fundamental to algebra. They represent relationships
between variables that form straight lines when graphed. In this module,
we'll explore how to identify, write, and solve linear equations. This
knowledge is essential for understanding more complex mathematical concepts
and real-world applications like calculating costs, distances, and rates.

## Lesson Content
A linear equation is an equation where the highest power of the variable
is 1. The standard form is ax + b = c, where a, b, and c are constants.

Let's start with a simple example: 2x + 3 = 7

To solve this, we need to isolate x:
1. Subtract 3 from both sides: 2x = 4
2. Divide both sides by 2: x = 2

## Examples
Example 1: Solve 3x - 5 = 10
Solution: Add 5 to both sides to get 3x = 15, then divide by 3 to get x = 5.

Example 2: Find the equation of a line with slope 2 passing through (1, 3).
Solution: Using point-slope form, y - 3 = 2(x - 1), which simplifies to y = 2x + 1.

## Quiz Questions
1. What is the solution to 4x + 8 = 20?
   a) x = 3
   b) x = 4
   c) x = 5

2. Which equation represents a line with slope -1 and y-intercept 4?
   a) y = -x + 4
   b) y = x - 4
   c) y = 4x - 1

## Homework
Practice solving these equations:
1. 5x - 10 = 15
2. -2x + 6 = 0
3. 7x + 14 = 0
"""

    # Create module object
    module = ModuleContent(
        content=sample_content,
        module_id="example_linear_equations",
        title="Introduction to Linear Equations",
        author="Example Author"
    )

    # Initialize orchestrator (API key from environment)
    orchestrator = RevisionOrchestrator()

    # Run a single pass review (for demonstration)
    print("\nRunning Authoring Pass 1 with 20 AI reviewers...")
    print("(In production, this would make actual API calls)\n")

    # For demonstration, we'll show what would happen
    print("📋 What this review would do:")
    print("   • 20 AI reviewers analyze the content in parallel")
    print("   • Each focuses on different aspects (flow, examples, quiz, etc.)")
    print("   • Feedback is aggregated using consensus scoring")
    print("   • A friendly report is generated for the author")


def example_complete_review():
    """Complete example: Run the 2-pass review matching human process."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Complete 2-Pass Review Process (Matches Human Workflow)")
    print("="*70)

    # Load a more complex module
    module = ModuleContent(
        content=load_sample_module(),
        module_id="complex_module_001",
        title="Complex Mathematical Concepts"
    )

    print("\n🔄 Complete Review Process (Matching Human Workflow):")
    print("   ALPHA REVIEW: Mixed Content & Style (40 reviewers)")
    print("      • 25 primarily pedagogy-focused (but note style issues)")
    print("      • 15 primarily style-focused (but note content issues)")
    print("      • Matches how human alpha reviewers actually work")
    print("\n   COPY EDIT: Pure Mechanical/Style (20 reviewers)")
    print("      • NO pedagogical evaluation")
    print("      • Focus only on style guide compliance")
    print("      • Matches human copy editor role")
    print("\nTotal: 60 AI reviewers providing comprehensive feedback")

    # Show what the orchestrator would do
    print("\n📊 Process Flow:")
    print("   1. Each pass runs reviewers in parallel for efficiency")
    print("   2. Consensus aggregation identifies high-confidence issues")
    print("   3. Reports are generated in multiple formats (text, HTML, JSON)")
    print("   4. Author gets prioritized, actionable feedback")
    print("   5. System adapts based on author experience level")


def example_with_real_api():
    """Example with real API calls (requires OpenAI API key)."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Live API Integration")
    print("="*70)

    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n⚠️  No OpenAI API key found in environment.")
        print("To run with real API calls:")
        print("  1. Set your OpenAI API key: export OPENAI_API_KEY='your-key'")
        print("  2. Run this script again")
        return

    print("\n✅ API key found. Ready to make real API calls.")
    print("\n⚠️  WARNING: This will make 60 API calls (costs apply)")

    # Uncomment to run with real API:
    # module = ModuleContent(content="Your module content here", module_id="test_001")
    # orchestrator = RevisionOrchestrator(api_key=api_key)
    # session = orchestrator.run_complete_review(module, author_experience="new")


def example_report_formats():
    """Example showing different report formats."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Report Formats")
    print("="*70)

    print("\nThe system generates reports in multiple formats:")
    print("\n1. 📝 Text Report (Console/File):")
    print("   - Human-readable format")
    print("   - Priority matrix")
    print("   - Strengths and improvement areas")
    print("   - Student-success framing")

    print("\n2. 📄 Markdown Report:")
    print("   - Formatted for documentation")
    print("   - Easy to read in GitHub/GitLab")
    print("   - Includes emoji indicators")

    print("\n3. 🌐 HTML Report:")
    print("   - Beautiful web presentation")
    print("   - Color-coded severity")
    print("   - Interactive elements")

    print("\n4. 💾 JSON Report:")
    print("   - Machine-readable format")
    print("   - API integration")
    print("   - Data analysis")

    print("\n5. 📊 CSV Export:")
    print("   - Spreadsheet analysis")
    print("   - Issue tracking")
    print("   - Metrics reporting")


def load_sample_module():
    """Load a sample module with some intentional issues."""
    return """
# Understanding Quadratic Functions

Let's learn about quadratic functions. They're really important in math.

A quadratic function is when you have x squared. Find the vertex of the
parabola y = x^2 + 4x + 3.

The vertex is at (-2, -1).

Calculate the roots using the quadratic formula.

Example: y = 2x^2 + 3x + 1

Quiz:
1. Find the vertex of y = x^2 - 6x + 8
2. Determine if the parabola opens up or down
3. Calculate the y-intercept

Remember, quadratics are everywhere in real life!
"""


def show_configuration():
    """Show system configuration details."""
    print("\n" + "="*70)
    print("SYSTEM CONFIGURATION")
    print("="*70)

    print("\n📚 Guidelines Files:")
    print(f"   • Authoring: {os.path.exists('/Users/michaeljoyce/Desktop/LEARNVIA/authoring_prompt_rules.txt')}")
    print(f"   • Style: {os.path.exists('/Users/michaeljoyce/Desktop/LEARNVIA/style_prompt_rules.txt')}")
    print(f"   • Vision: {os.path.exists('/Users/michaeljoyce/Desktop/LEARNVIA/product_vision_context.txt')}")

    print("\n🤖 Reviewer Distribution (2-Pass System):")
    print("   • ALPHA REVIEW: 40 reviewers")
    print("     - 25 authoring-primary (pedagogy, examples, scaffolding)")
    print("     - 15 style-primary (contractions, imperatives, formatting)")
    print("     - All reviewers note both types of issues")
    print("   • COPY EDIT: 20 reviewers")
    print("     - Pure mechanical/style focus")
    print("     - No pedagogical evaluation")

    print("\n⚙️ Consensus Settings:")
    print("   • Similarity threshold: 75%")
    print("   • Confidence levels: very_low to very_high")
    print("   • Priority scoring: severity × confidence")

    print("\n📁 Output Directory:")
    print(f"   • Reports saved to: /Users/michaeljoyce/Desktop/LEARNVIA/reports/")


def main():
    """Main entry point."""
    print("\n" + "🎓"*35)
    print("LEARNVIA AI-POWERED CONTENT REVISION SYSTEM")
    print("60 AI Reviewers | 4-Pass Consensus | Student-Success Focus")
    print("🎓"*35)

    # Show configuration
    show_configuration()

    # Run examples
    example_basic_review()
    example_complete_review()
    example_report_formats()
    example_with_real_api()

    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("\nTo use this system:")
    print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key'")
    print("2. Create a ModuleContent object with your content")
    print("3. Initialize RevisionOrchestrator")
    print("4. Run review passes as needed")
    print("5. Review generated reports in /reports directory")

    print("\n📚 Example code:")
    print("""
from src.models import ModuleContent
from src.orchestrator import RevisionOrchestrator

# Load your module
module = ModuleContent(
    content=open('your_module.txt').read(),
    module_id='module_001'
)

# Run review
orchestrator = RevisionOrchestrator()
session = orchestrator.run_complete_review(module)
""")

    print("\n✨ Happy reviewing! Remember: We're here to support authors, not gatekeep!")


if __name__ == "__main__":
    main()