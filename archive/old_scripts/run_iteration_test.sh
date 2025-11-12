#!/bin/bash
# Run complete iteration test: review → compare → report

set -e  # Exit on error

MODULE_PATH="${1:-modules/module_5.6_exemplary.xml}"
REVIEW_LOG="${2:-modules/Chapter 5 Review Log - 5.6 Beta.csv}"
MODULE_NAME=$(basename "$MODULE_PATH" .xml)

echo "======================================"
echo "Iteration Test Workflow"
echo "======================================"
echo "Module: $MODULE_PATH"
echo "Review Log: $REVIEW_LOG"
echo ""

# Create outputs directory
mkdir -p outputs

echo "[1/3] Running AI review with Sonnet..."
python scripts/test_sonnet_review.py \
  --module "$MODULE_PATH" \
  --output "outputs/review_${MODULE_NAME}.json"

echo ""
echo "[2/3] Comparing with human review log..."
python scripts/compare_reviews.py \
  --ai "outputs/review_${MODULE_NAME}.json" \
  --human "$REVIEW_LOG" \
  --output "docs/comparison_${MODULE_NAME}.md"

echo ""
echo "[3/3] Generating summary..."

# Count results
TRUE_POS=$(grep -c "### Match" "docs/comparison_${MODULE_NAME}.md" || echo "0")
FALSE_POS=$(grep -c "### False Positive" "docs/comparison_${MODULE_NAME}.md" || echo "0")
FALSE_NEG=$(grep -c "### Missed Issue" "docs/comparison_${MODULE_NAME}.md" || echo "0")

echo ""
echo "======================================"
echo "Results Summary"
echo "======================================"
echo "True Positives: $TRUE_POS"
echo "False Positives: $FALSE_POS"
echo "False Negatives: $FALSE_NEG"
echo ""
echo "Full comparison: docs/comparison_${MODULE_NAME}.md"
echo "AI review output: outputs/review_${MODULE_NAME}.json"
echo "======================================"
