#!/bin/bash

# Run Black for auto-formatting
black .

# Run Flake8 for linting
flake8

# Check if any errors occurred
if [ $? -eq 0 ]; then
    echo "Pre-push checks passed. You can push your code."
else
    echo "Pre-push checks failed. Fix the errors before pushing."
    exit 1
fi
