#!/bin/bash

# Run Black and Flake8 only on modified Python files outside the virtual environment
git diff --name-only --cached | grep '\.py$' | grep -v '/venv/' | xargs black
git diff --name-only --cached | grep '\.py$' | grep -v '/venv/' | xargs flake8

# Check if any errors occurred
if [ $? -eq 0 ]; then
    echo "Pre-push checks passed. You can push your code."
else
    echo "Pre-push checks failed. Fix the errors before pushing."
    exit 1
fi
