#!/bin/bash

# RSS Reader Alias Setup Script
# This script adds convenient aliases to your shell configuration

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Determine which shell configuration file to use
if [[ "$SHELL" == *"zsh"* ]]; then
    CONFIG_FILE="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [[ "$SHELL" == *"bash"* ]]; then
    CONFIG_FILE="$HOME/.bashrc"
    SHELL_NAME="bash"
else
    echo "❌ Unsupported shell: $SHELL"
    exit 1
fi

echo "🔧 Setting up RSS Reader aliases for $SHELL_NAME..."

# Create aliases
ALIASES=(
    "# RSS Reader Aliases"
    "alias rss-backend='$SCRIPT_DIR/start-backend.sh'"
    "alias rss-frontend='$SCRIPT_DIR/start-frontend.sh'"
    "alias rss-start='$SCRIPT_DIR/start-app.sh'"
    "alias rss-both='$SCRIPT_DIR/start-app.sh both'"
    "alias rss-b='$SCRIPT_DIR/start-app.sh backend'"
    "alias rss-f='$SCRIPT_DIR/start-app.sh frontend'"
)

# Check if aliases already exist
if grep -q "RSS Reader Aliases" "$CONFIG_FILE" 2>/dev/null; then
    echo "⚠️  RSS Reader aliases already exist in $CONFIG_FILE"
    echo "   Skipping alias setup..."
else
    # Add aliases to shell configuration
    echo "" >> "$CONFIG_FILE"
    for alias_line in "${ALIASES[@]}"; do
        echo "$alias_line" >> "$CONFIG_FILE"
    done
    
    echo "✅ Aliases added to $CONFIG_FILE"
    echo ""
    echo "🔄 To use the aliases immediately, run:"
    echo "   source $CONFIG_FILE"
    echo ""
fi

echo "📋 Available commands:"
echo "   rss-start    - Start both backend and frontend"
echo "   rss-backend  - Start only backend server"
echo "   rss-frontend - Start only frontend server"
echo "   rss-both     - Start both servers (same as rss-start)"
echo "   rss-b        - Short for backend only"
echo "   rss-f        - Short for frontend only"
echo ""
echo "🎯 Quick start:"
echo "   rss-start    # Start the full app"
echo ""
echo "💡 You can also run the scripts directly:"
echo "   ./start-app.sh"
echo "   ./start-backend.sh"
echo "   ./start-frontend.sh" 