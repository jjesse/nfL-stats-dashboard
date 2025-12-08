#!/bin/bash

# NFL Stats Dashboard - Quick Test Script
# This script helps you quickly test the dashboard

echo "🏈 NFL Stats Dashboard - Quick Test"
echo "===================================="
echo ""

# Check if we're in the right directory
if [ ! -f "index.html" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "✅ Project files found"
echo ""

# Check for Python
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 detected"
    echo ""
    echo "🚀 Starting local web server on port 8000..."
    echo ""
    echo "📱 Open your browser and navigate to:"
    echo "   http://localhost:8000"
    echo ""
    echo "🧪 Test these pages:"
    echo "   - Home: http://localhost:8000/index.html"
    echo "   - Schedule: http://localhost:8000/schedule.html"
    echo "   - Team Stats: http://localhost:8000/team-stats.html"
    echo "   - QB Leaders: http://localhost:8000/qb-leaders.html"
    echo "   - Receiver Leaders: http://localhost:8000/receiver-leaders.html"
    echo "   - Rushing Leaders: http://localhost:8000/rushing-leaders.html"
    echo ""
    echo "💡 Tips:"
    echo "   - Open browser DevTools (F12) to see console logs"
    echo "   - Check Network tab to see API calls"
    echo "   - Type 'NFLAPI.clearCache()' in console to clear cache"
    echo ""
    echo "🛑 Press Ctrl+C to stop the server"
    echo ""
    echo "=================================="
    echo ""
    
    python3 -m http.server 8000
else
    echo "❌ Python 3 not found. Please install Python 3 or use another web server."
    echo ""
    echo "Alternative methods:"
    echo "  - Node.js: npx http-server -p 8000"
    echo "  - PHP: php -S localhost:8000"
    echo ""
    exit 1
fi
