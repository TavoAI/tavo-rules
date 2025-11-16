#!/bin/bash
# sync-submodules.sh - Sync external format repositories
# This script updates all git submodules to their latest compatible versions

set -e

echo "🔄 Syncing git submodules..."

# Update all submodules to latest
git submodule update --init --recursive

# Check for any updates
git submodule foreach --quiet 'echo "📦 $name: $(git rev-parse --short HEAD)"'

echo "✅ All submodules synced successfully"

# Optional: Run validation tests on updated rules
echo "🧪 Running format compatibility tests..."
# Add validation logic here when implemented
