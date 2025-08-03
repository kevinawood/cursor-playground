#!/bin/bash

# Quick permission fix script for RSS Reader
echo "🔧 Fixing file permissions..."

# Get current user's UID and GID
USER_UID=$(id -u)
USER_GID=$(id -g)

echo "Using UID: $USER_UID, GID: $USER_GID"

# Fix permissions for the entire project
sudo chown -R $USER_UID:$USER_GID .

# Make sure scripts are executable
chmod +x *.sh

echo "✅ Permissions fixed!"
echo "You should now be able to edit files without issues." 