<div align="center">

**English** | [Русский](READMEru.md)

# search-bash

A fast, standalone terminal search and AI assistant for Linux and macOS.  
Zero external dependencies. Pure Python 3.10+.

[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS-lightgrey?style=flat-square)]()
[![Telegram](https://img.shields.io/badge/Telegram-@ivanchikbyte-2CA5E0?style=flat-square&logo=telegram&logoColor=white)](https://t.me/ivanchikbyte)

<br />

![search-bash demo](demo.gif)

</div>

---

## Quick Install

One command downloads the standalone script to `~/.local/bin/search` and makes it executable:

```bash
curl -fsSL https://raw.githubusercontent.com/ivanchik-byte/search-bash/main/install.sh | bash
```

<details>
<summary>Other install options (pipx, npm, manual)</summary>

### pipx (Python isolated environment)
```bash
pipx install git+https://github.com/ivanchik-byte/search-bash.git
```

### npm / npx (Node.js)
Install globally via npm:
```bash
npm install -g github:ivanchik-byte/search-bash
```
Or run directly with npx without installing:
```bash
npx github:ivanchik-byte/search-bash "how to configure nginx websocket"
```

### Direct download
```bash
mkdir -p ~/.local/bin
curl -fsSL https://raw.githubusercontent.com/ivanchik-byte/search-bash/main/search -o ~/.local/bin/search
chmod +x ~/.local/bin/search
```

### Git clone
```bash
git clone https://github.com/ivanchik-byte/search-bash.git ~/.search-bash
mkdir -p ~/.local/bin
ln -sf ~/.search-bash/search ~/.local/bin/search
```

Make sure `~/.local/bin` is in your `$PATH`:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

</details>

---

## Quick Setup

Run the setup wizard on your first run:

```bash
search --setup
```

It walks you through selecting a provider and prompts for your API key securely (input is hidden without terminal echo).

Settings and keys are saved locally in `~/.config/search/config.json` with strict `0600` file permissions.

### Supported Providers

| Provider | Default Model | Live Web Search | Best For |
| :--- | :--- | :--- | :--- |
| **Google Gemini** | `gemini-3.5-flash-lite` | Yes (Google Search Grounding) | Fast lookups, current docs, free tier |
| **Nvidia NIM** | `nvidia/nemotron-3.5-lightning-30b-a3b` | No | Deep reasoning and fast coding inference |
| **OpenRouter** | `meta-llama/llama-3.3-70b-instruct` | Optional | Access to 200+ models (Claude, Llama, DeepSeek) |
| **Custom / Local** | User specified | No | Local Ollama, Groq, vLLM, private endpoints |

---

## What You Can Do

### 1. Fast terminal lookups with real web results

Ask technical questions right from your shell. With Gemini, responses come grounded with real Google Search results:

```bash
search "how to configure nginx reverse proxy for websockets"
```

### 2. Generate and run shell commands

Use `-c` when you know what you want to do, but forget the syntax. It outputs the command and asks if you want to execute it:

```bash
search -c "find all files over 500MB modified in the last 7 days"
```

```text
find . -type f -size +500M -mtime -7 -exec ls -lh {} +

Execute command? [y/N]:
```

### 3. Analyze directories and clean disk space

Use `-a` (or `-d <path>`) to inspect folders. It groups files, highlights the largest disk consumers, collapses clutter like `node_modules` or `.git`, and suggests what is safe to delete:

```bash
search -a
```

After the overview is displayed, you can inspect candidate files directly by rank number or file path:

```text
Inspect file content? [1-10 or file path, Enter to finish]: 1
... [AI checks file purpose and safety] ...
Delete 'dump_2026.sql'? [y/N]: y
```

### 4. Pipe logs and diagnostics

Pipe stdout or log files directly into `search` to diagnose errors and stack traces:

```bash
cat /var/log/nginx/error.log | search "explain why this connection dropped"
```

### 5. Attach files and logs

Pass files or glob patterns with `-f`. It handles large files with intelligent tail sampling:

```bash
search -f "*.log" "summarize errors from the last 24 hours"
```

---

## Command Reference

| Option | Description |
| :--- | :--- |
| `-c, --cmd` | Generate an executable shell command with confirmation prompt |
| `-a, --all-files` | Scan current directory and highlight cleanup candidates |
| `-d, --dir PATH` | Scan a specific folder structure |
| `-f, --file PATH` | Attach file or glob pattern (`-f "*.log"`, `-f file.txt:tail:100`) |
| `-p, --provider NAME` | Override provider for one query (`gemini`, `nvidia`, `openrouter`, `custom`) |
| `-m, --model NAME` | Override model identifier for one query |
| `-s, --site DOMAIN` | Scope web search to a specific domain (e.g. `docs.docker.com`) |
| `-i, --interactive` | Launch interactive wizard session |
| `-w, --no-web` | Disable web search grounding |
| `-r, --raw` | Output plain text without borders or boxes |
| `-y, --yes` | Auto-execute generated command without confirmation |
| `--setup` | Run interactive provider and key setup |
| `--clear-cache` | Clear cached query responses in `~/.cache/search_cli/` |

---

## Why I wrote this

I wrote search-bash because I needed to turn on my PC and log into a VM. But before doing that, I had to check something in the browser. Since I use Firefox, I just didn't want to open the browser, wait for all my tabs to restore, open a new tab, google what I needed, close that tab, kill the process via pkill (so that my previous tabs wouldn't get wiped out and force me to hit Ctrl+Shift+T later), and only then start logging into the VM. So, I built this simple and fun little CLI tool instead.

---

## Community & Security

- **Contributing**: Read [CONTRIBUTING.md](CONTRIBUTING.md) for local development guidelines.
- **Code of Conduct**: See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- **Security**: For private vulnerability reporting, see [SECURITY.md](SECURITY.md).

---

## License

MIT
