#!/bin/bash
# Production Readiness Verification Script

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     Journal Desk - Production Readiness Verification       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

CHECKS_PASSED=0
CHECKS_FAILED=0

check_file() {
    if [ -f "$1" ]; then
        echo "✅ $2"
        ((CHECKS_PASSED++))
    else
        echo "❌ $2"
        ((CHECKS_FAILED++))
    fi
}

check_dir() {
    if [ -d "$1" ] && [ "$(ls -A $1)" ]; then
        echo "✅ $2"
        ((CHECKS_PASSED++))
    else
        echo "❌ $2"
        ((CHECKS_FAILED++))
    fi
}

# 1. Check Python and dependencies
echo "📋 Checking Python environment..."
python3 --version > /dev/null 2>&1 && echo "✅ Python 3 installed" && ((CHECKS_PASSED++)) || (echo "❌ Python 3 not found" && ((CHECKS_FAILED++)))

# 2. Check static files
echo ""
echo "📦 Checking static files..."
check_dir "staticfiles" "Static files collected"

# 3. Check deployment files
echo ""
echo "📄 Checking deployment files..."
check_file "Dockerfile" "Dockerfile exists"
check_file "docker-compose.yml" "docker-compose.yml exists"
check_file "Procfile" "Procfile exists"
check_file "runtime.txt" "runtime.txt exists"
check_file "deploy.sh" "deploy.sh exists"
check_file "DEPLOYMENT_GUIDE.md" "DEPLOYMENT_GUIDE.md exists"
check_file "DEPLOYMENT_READY.md" "DEPLOYMENT_READY.md exists"

# 4. Check git
echo ""
echo "🔧 Checking git repository..."
check_dir ".git" "Git repository initialized"
check_file "requirements.txt" "requirements.txt exists"

# 5. Check environment
echo ""
echo "🌍 Checking environment configuration..."
check_file ".env" ".env file exists"
check_file ".env.production" ".env.production file exists"

# 6. Check key files
echo ""
echo "✨ Checking application files..."
check_file "manage.py" "manage.py exists"
check_file "journal_project/settings.py" "Django settings exists"
check_file "journal_project/urls.py" "Django urls exists"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                   VERIFICATION RESULTS                     ║"
echo "╠════════════════════════════════════════════════════════════╣"
printf "✅ Checks Passed: %d\n" $CHECKS_PASSED
printf "❌ Checks Failed: %d\n" $CHECKS_FAILED
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo "🎉 All checks passed! Your application is ready for deployment."
    echo ""
    echo "Next steps:"
    echo "1. Read DEPLOYMENT_READY.md for quick deployment options"
    echo "2. For Heroku (easiest): ./deploy.sh journal-desk-yourname"
    echo "3. For Docker: docker-compose up -d"
    echo "4. For AWS/DigitalOcean: See DEPLOYMENT_GUIDE.md"
    echo ""
    exit 0
else
    echo "⚠️  Some checks failed. Please fix the issues above before deploying."
    exit 1
fi
