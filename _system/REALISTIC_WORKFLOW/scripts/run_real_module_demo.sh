#!/bin/bash

# Run Pass 1 review on real derivatives module

cd "$(dirname "$0")"

echo "============================================================"
echo "      PASS 1 CONTENT REVIEW - REAL MODULE DEMO"
echo "============================================================"
echo ""
echo "Starting review of Module 3.4: Basic Rules of Finding Derivatives"
echo ""

# Run the Pass 1 review
python run_pass1_only.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Review complete!"
    echo ""
    echo "📊 Opening visual report in browser..."

    # Check operating system and open report accordingly
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open ../outputs/PASS1_REAL_MODULE_REPORT.html
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        xdg-open ../outputs/PASS1_REAL_MODULE_REPORT.html 2>/dev/null
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        # Windows
        start ../outputs/PASS1_REAL_MODULE_REPORT.html
    else
        echo "Please open ../outputs/PASS1_REAL_MODULE_REPORT.html in your browser"
    fi

    echo ""
    echo "============================================================"
    echo "Report files generated:"
    echo "  • JSON: ../outputs/pass1_real_module_results.json"
    echo "  • HTML: ../outputs/PASS1_REAL_MODULE_REPORT.html"
    echo "============================================================"
else
    echo ""
    echo "❌ Error: Review process failed"
    echo "Please check the error messages above"
    exit 1
fi