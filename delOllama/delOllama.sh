#!/bin/bash

# This script is used to uninstall Ollama on Linux.

set -eu

status() { echo ">>> $*" >&2; }
error() { echo "Error: $*"; exit 1; }
available() { command -v "$1" >/dev/null; }

# Get user confirmation
status "You are about to uninstall Ollama, which will completely remove Ollama and any data created by ollama."
status "Are you sure you want to continue? If you know what you're Doing, lease enter 'yes' to proceed, otherwise the uninstallation will be canceled."

read -r USER_CONFIRMATION

if [[ "$USER_CONFIRMATION" != "yes" ]]; then
    status "Uninstallation operation has been canceled."
    exit 1
fi

# Check if the user has root or sudo permissions
SUDO=""
if [ "$(id -u)" -ne 0 ]; then
    # If not root, check if sudo is available
    if ! available sudo; then
        error "This script requires superuser permissions. Please run as root or ensure sudo is installed."
    fi
    # Use sudo for subsequent commands
    SUDO="sudo"
fi

# Stop and disable ollama systemd service (if it exists)
if available systemctl; then
    if $SUDO systemctl list-unit-files | grep -q ollama.service; then
        status "Stopping ollama service..."
        $SUDO systemctl stop ollama || true
        status "Disabling ollama service..."
        $SUDO systemctl disable ollama || true

        # Delete ollama.service file (if it exists)
        # Get the service file path
        SERVICE_PATH=$(systemctl show ollama.service --property=Path)
        [ -n "$SERVICE_PATH" ] || SERVICE_PATH=$(systemctl show ollama.service --property=FragmentPath)
        if [ -n "$SERVICE_PATH" ]; then
            SERVICE_PATH=$(echo $SERVICE_PATH | grep -oP 'Path=(.*)' | grep -oP '(?<=Path=).*')
            status "Deleting ollama service file: $SERVICE_PATH..."
            $SUDO rm -f "$SERVICE_PATH"
            status "Reloading systemd service configuration..."
            $SUDO systemctl daemon-reload || true
        else
            status "Could not find the path to ollama service file."
        fi
    fi
fi

# Delete ollama user and group
if id ollama &>/dev/null; then
    status "Deleting ollama user and group..."
    # Remove users in group ollama
    for USER in $(cat /etc/group | grep ollama: | cut -d: -f4); do
        $SUDO gpasswd -d $USER ollama || true
    done
    $SUDO userdel -r ollama || true  # Use -r to delete home directory
fi

# Delete Ollama models and binary file
if which ollama &>/dev/null; then
    # Remove ollama models
    for MODEL in $(ollama list | tail +2 | cut -f1); do
        status "Deleting model: $MODEL..."
        $SUDO ollama rm "$MODEL" || true
    done

    OLLAMA_PATH=$(which ollama)
    status "Deleting ollama binary file: $OLLAMA_PATH..."
    $SUDO rm -f "$OLLAMA_PATH"
fi

status "Ollama uninstallation completed.
"
