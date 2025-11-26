#!/bin/bash

# This script uninstalls the Telegram extension for the Gemini CLI.

# The Gemini CLI extensions directory.
GEMINI_EXTENSIONS_DIR="$HOME/.gemini/extensions"

# The name of the extension.
EXTENSION_NAME="telegram"

# The path to the extension's symbolic link.
EXTENSION_PATH="$GEMINI_EXTENSIONS_DIR/$EXTENSION_NAME"

# Check if the extension is installed.
if [ -L "$EXTENSION_PATH" ]; then
  # Remove the symbolic link.
  rm "$EXTENSION_PATH"
  echo "Telegram extension uninstalled successfully."
else
  echo "Telegram extension is not installed."
fi
