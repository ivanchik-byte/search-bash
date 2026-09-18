#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_BIN="$HOME/.local/bin/search"

echo "[*] Installing search-cli..."

mkdir -p "$HOME/.local/bin"
mkdir -p "$HOME/.config/search"
mkdir -p "$HOME/.cache/search_cli"

# Check for pipx first
if command -v pipx >/dev/null 2>&1; then
    echo "[*] Found pipx. Installing package..."
    pipx install "$SCRIPT_DIR" --force
    echo "[+] Successfully installed via pipx."
    exit 0
fi

# Fallback: create launcher wrapper
WRAPPER="$HOME/.local/bin/search"
cat << 'EOF' > "$WRAPPER"
#!/usr/bin/env bash
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PYTHONPATH="$SCRIPT_DIR/../programs/search-cli/src:$PYTHONPATH" exec python3 -m search_cli.cli "$@"
EOF

# Direct launcher fallback
cat << EOF > "$WRAPPER"
#!/usr/bin/env bash
PYTHONPATH="$SCRIPT_DIR/src:\$PYTHONPATH" exec python3 -m search_cli.cli "\$@"
EOF
chmod +x "$WRAPPER"

echo "[+] Successfully installed launcher to: $WRAPPER"

if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "[-] Warning: $HOME/.local/bin is not in your PATH."
    echo "    Add this line to ~/.bashrc or ~/.zshrc:"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo ""
echo "Quick Start:"
echo "1. Run 'search' to start the interactive wizard and configure your API key."
echo "2. Or set it directly: search --set-key <API_KEY>"
