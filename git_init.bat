@echo off
REM GitHub Upload Helper Script for Windows
REM This script helps you upload your project to GitHub

echo ==========================================
echo GitHub Upload Helper
echo ==========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Git is installed ✓
echo.

REM Initialize git if not already done
if not exist ".git" (
    echo Initializing Git repository...
    git init
    echo Git initialized ✓
) else (
    echo Git repository already exists ✓
)
echo.

REM Show current status
echo Current status:
git status
echo.

REM Prompt for GitHub username
set /p GITHUB_USER="Enter your GitHub username: "
if "%GITHUB_USER%"=="" (
    echo ERROR: GitHub username is required!
    pause
    exit /b 1
)

REM Prompt for repository name
set /p REPO_NAME="Enter repository name (default: placement-portal): "
if "%REPO_NAME%"=="" set REPO_NAME=placement-portal

echo.
echo ==========================================
echo Configuration:
echo Username: %GITHUB_USER%
echo Repository: %REPO_NAME%
echo URL: https://github.com/%GITHUB_USER%/%REPO_NAME%.git
echo ==========================================
echo.

set /p CONFIRM="Is this correct? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo Adding files to Git...
git add .
echo Files added ✓
echo.

echo Creating initial commit...
git commit -m "Initial commit: Placement Portal with AI features"
echo Commit created ✓
echo.

echo Setting up remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git
echo Remote configured ✓
echo.

echo Renaming branch to main...
git branch -M main
echo Branch renamed ✓
echo.

echo ==========================================
echo Ready to push to GitHub!
echo ==========================================
echo.
echo IMPORTANT: Make sure you have created the repository on GitHub first!
echo Go to: https://github.com/new
echo.
echo Repository name: %REPO_NAME%
echo Description: AI-powered placement management system
echo Public or Private: Your choice
echo DO NOT initialize with README
echo.

set /p PUSH="Ready to push? (Y/N): "
if /i not "%PUSH%"=="Y" (
    echo.
    echo Cancelled. You can push later with: git push -u origin main
    pause
    exit /b 0
)

echo.
echo Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo ==========================================
    echo Push failed!
    echo ==========================================
    echo.
    echo Possible reasons:
    echo 1. Repository doesn't exist on GitHub
    echo 2. Authentication failed
    echo 3. Network issues
    echo.
    echo Please:
    echo 1. Create repository on GitHub: https://github.com/new
    echo 2. Try again with: git push -u origin main
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo SUCCESS! ✓
echo ==========================================
echo.
echo Your project is now on GitHub!
echo URL: https://github.com/%GITHUB_USER%/%REPO_NAME%
echo.
echo Next steps:
echo 1. Visit your repository on GitHub
echo 2. Add topics: django, react, machine-learning
echo 3. Add description
echo 4. Update README.md with your info
echo.
pause
