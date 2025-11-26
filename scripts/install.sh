#!/bin/bash

# This script installs the Telegram extension for the Gemini CLI.

# Get the directory of this script.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# The Gemini CLI extensions directory.
GEMINI_EXTENSIONS_DIR="$HOME/.gemini/extensions"

# The name of the extension.
EXTENSION_NAME="telegram"

# Create the Gemini CLI extensions directory if it doesn't exist.
mkdir -p "$GEMINI_EXTENSIONS_DIR"

# Create a symbolic link to the extension's directory.
ln -s "$SCRIPT_DIR" "$GEMINI_EXTENSIONS_DIR/$EXTENSION_NAME"

echo "Telegram extension installed successfully."
echo "Please restart the Gemini CLI to use the extension."
