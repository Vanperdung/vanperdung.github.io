#!/usr/bin/env bash
set -euo pipefail

HUGO_VERSION="0.146.0"
HUGO_BINARY_DIR="$HOME/.local/bin"

log() { echo "[setup] $*"; }

# ---------------------------------------------------------------------------
# System packages
# ---------------------------------------------------------------------------
log "Installing system packages..."
sudo apt-get update -qq
sudo apt-get install -y \
    git \
    curl \
    wget \
    build-essential

# ---------------------------------------------------------------------------
# Hugo Extended
# ---------------------------------------------------------------------------
if command -v hugo &>/dev/null && hugo version | grep -q "v${HUGO_VERSION}"; then
    log "Hugo ${HUGO_VERSION} already installed, skipping."
else
    log "Installing Hugo Extended ${HUGO_VERSION}..."
    TMP=$(mktemp -d)
    curl -fsSL -o "$TMP/hugo.tar.gz" \
        "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
    tar -xzf "$TMP/hugo.tar.gz" -C "$TMP"
    mkdir -p "$HUGO_BINARY_DIR"
    mv "$TMP/hugo" "$HUGO_BINARY_DIR/hugo"
    chmod +x "$HUGO_BINARY_DIR/hugo"
    rm -rf "$TMP"
    log "Hugo installed to $HUGO_BINARY_DIR/hugo"
fi

# ---------------------------------------------------------------------------
# Ensure ~/.local/bin is on PATH
# ---------------------------------------------------------------------------
SHELL_RC=""
case "$SHELL" in
    */zsh)  SHELL_RC="$HOME/.zshrc" ;;
    */bash) SHELL_RC="$HOME/.bashrc" ;;
esac

if [[ -n "$SHELL_RC" ]] && ! grep -q '\.local/bin' "$SHELL_RC" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
    log "Added ~/.local/bin to PATH in $SHELL_RC"
fi

export PATH="$HUGO_BINARY_DIR:$PATH"

# ---------------------------------------------------------------------------
# Verify
# ---------------------------------------------------------------------------
log "Versions:"
hugo version
git  --version

log "Setup complete. Run 'source ~/.zshrc' (or ~/.bashrc) to reload your PATH."
