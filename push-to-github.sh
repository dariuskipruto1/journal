#!/bin/bash
# Push to GitHub and Deploy
# This script will help you push your Journal Desk project to GitHub

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🚀 Journal Desk - Push to GitHub & Deploy               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Your project is ready but not on GitHub yet."
echo "Let me help you get it there!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 1: Create GitHub Repository"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Go to: https://github.com/new"
echo ""
echo "Fill in:"
echo "  • Repository name: journal-desk"
echo "  • Description: Personal journal and task management app"
echo "  • Visibility: Public (for deployment)"
echo "  • DO NOT initialize with README (we have one)"
echo ""
echo "Click 'Create repository'"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 2: Run This Command"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Replace USERNAME with your GitHub username, then run:"
echo ""
echo "  git remote add origin https://github.com/USERNAME/journal-desk.git"
echo "  git branch -M main"
echo "  git push -u origin main"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 3: Deploy to Railway"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Once on GitHub:"
echo "  1. Go to https://railway.app/"
echo "  2. Click 'Create Project' → 'Deploy from GitHub'"
echo "  3. Select 'journal-desk' repository"
echo "  4. Wait 2-3 minutes for deployment"
echo "  5. Your app is LIVE! 🎉"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Prompt for GitHub username
read -p "Enter your GitHub username (or press Enter to skip): " github_username

if [ -z "$github_username" ]; then
    echo "⏭️  Skipped. You can run the commands manually later."
    echo ""
    exit 0
fi

echo ""
echo "📝 Setting up GitHub remote..."
echo ""

git remote add origin "https://github.com/${github_username}/journal-desk.git"
echo "✅ Remote added"

git branch -M main
echo "✅ Branch renamed to main"

echo ""
echo "🚀 Pushing to GitHub..."
echo ""
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║             ✅ Code pushed to GitHub!                      ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🎯 Next: Deploy to Railway"
    echo ""
    echo "1. Go to: https://railway.app/"
    echo "2. Click 'Create Project'"
    echo "3. Select 'Deploy from GitHub'"
    echo "4. Choose 'journal-desk' repository"
    echo "5. Railway deploys automatically!"
    echo ""
    echo "Your app URL: https://journal-desk.railway.app"
    echo "Admin panel:  https://journal-desk.railway.app/admin/"
    echo ""
else
    echo ""
    echo "⚠️  Git push failed. Make sure:"
    echo "  • GitHub username is correct"
    echo "  • Repository exists on GitHub"
    echo "  • You have push permission"
    echo ""
fi
