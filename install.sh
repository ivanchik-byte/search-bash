#!/usr/bin/env bash
set -e

REPO="ivanchik-byte/search-bash"
BRANCH="main"
RAW_URL="https://raw.githubusercontent.com/${REPO}/${BRANCH}/search"
BIN_DIR="${HOME}/.local/bin"
TARGET="${BIN_DIR}/search"

if ! command -v python3 >/dev/null 2>&1; then
    echo -e "\033[31m[!] Python 3 is required but not found in PATH.\033[0m" >&2
    exit 1
fi

mkdir -p "${BIN_DIR}"
TMP_FILE="$(mktemp)"

echo -e "\033[36m[*] Downloading search-bash CLI...\033[0m"
if command -v curl >/dev/null 2>&1; then
    curl -fsSL "${RAW_URL}" -o "${TMP_FILE}"
elif command -v wget >/dev/null 2>&1; then
    wget -qO "${TMP_FILE}" "${RAW_URL}"
else
    echo -e "\033[31m[!] Neither curl nor wget was found.\033[0m" >&2
    rm -f "${TMP_FILE}"
    exit 1
fi

mv "${TMP_FILE}" "${TARGET}"
chmod +x "${TARGET}"

if [[ ":$PATH:" != *":${BIN_DIR}:"* ]]; then
    SHELL_NAME="$(basename "${SHELL:-bash}")"
    RC_FILE="${HOME}/.${SHELL_NAME}rc"
    [ -f "${RC_FILE}" ] || RC_FILE="${HOME}/.bashrc"
    echo ""
    echo -e "\033[33m[!] Note: ${BIN_DIR} is not in your current PATH.\033[0m"
    echo -e "Add it to your environment by running:"
    echo -e "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ${RC_FILE} && source ${RC_FILE}"
    echo ""
fi

echo -e "\033[32m[+] Successfully installed search to ${TARGET}\033[0m"
"${TARGET}" --version 2>/dev/null || true
