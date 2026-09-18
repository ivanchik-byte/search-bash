# search

A single-file terminal intelligence and search utility with multi-provider AI support (Google Gemini, OpenRouter, Nvidia NIM, and OpenAI-compatible endpoints).

Designed for Linux servers, remote SSH sessions, and DevOps workflows. Returns verified documentation, executable shell commands, and project-aware analysis directly inside your terminal.

Zero mandatory dependencies. Runs on standard Python 3.10+.

---

## Supported Providers

- **Google Gemini** (Google AI Studio) — Search Grounding with live Google results.
- **OpenRouter** (openrouter.ai) — 200+ models (Claude, Llama, DeepSeek, Mistral) with optional search grounding.
- **Nvidia NIM** (integrate.api.nvidia.com) — High-throughput inference for Nemotron, DeepSeek, Mistral.
- **Custom / Local** (Ollama, Groq, vLLM, LiteLLM) — Any OpenAI-compatible `/v1/chat/completions` endpoint.

---

## Installation (One Line)

Download the executable script directly into `~/.local/bin`:

```bash
curl -sSL https://raw.githubusercontent.com/<your-username>/search/main/search -o ~/.local/bin/search && chmod +x ~/.local/bin/search
```

Ensure `~/.local/bin` is in your `PATH`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

## Setup & Provider Configuration

Run the setup wizard to choose your provider and configure your API key:

```bash
search --setup
```

Or configure directly via CLI flags:

### Google Gemini:
```bash
search --set-provider gemini
search --set-key "AIzaSy..."
search --set-model "gemini-3.5-flash-lite"
```

### OpenRouter:
```bash
search --set-provider openrouter
search --set-key "sk-or-v1-..."
search --set-model "meta-llama/llama-3.3-70b-instruct"
```

### Nvidia NIM:
```bash
search --set-provider nvidia
search --set-key "nvapi-..."
search --set-model "nvidia/nemotron-3.5-lightning-30b-a3b"
```

### Local Ollama / Custom:
```bash
search --set-provider custom
search --set-url "http://localhost:11434/v1"
search --set-model "llama3.2"
```

---

## Features

- **Single-File Architecture**: Everything lives in one self-contained script (`search`).
- **Multi-Provider**: Switch between Gemini, OpenRouter, Nvidia, or local models anytime (`-p <provider>`).
- **Interactive Wizard**: Run `search` with no arguments to step through query formulation and command execution.
- **Command Generator (`-c`)**: Generates exact, copy-pasteable Linux commands with an interactive prompt to execute them.
- **Codebase & File Context (`-f`, `-d`)**: Analyzes specific files or scans repository directory trees (filtering noise like `.git`, `node_modules`, `venv`).
- **Domain Targeting (`-s`)**: Restricts search scope to specific documentation sites (e.g. `stackoverflow.com`, `docs.docker.com`).
- **Unix Pipelines**: Reads stdin streams (`cat /var/log/syslog | search "explain root cause"`).
- **Local Caching**: Repeated identical queries return instantly from `~/.cache/search_cli/`.
- **Clean Terminal UI**: Strict Unix style. No emojis, no marketing chatter.

---

## Usage Examples

### 1. Interactive Mode
```bash
search
```

### 2. General Technical Search
```bash
search "how to configure reverse proxy in nginx for websocket"
search -p openrouter -m meta-llama/llama-3.3-70b-instruct "explain b-trees"
```

### 3. Generate and Execute Shell Commands (`-c`)
```bash
search -c "find files larger than 100MB and sort by size"
```
Output:
```
find / -type f -size +100M -exec ls -lh {} + 2>/dev/null | awk '{ print $5, $9 }' | sort -hr

Execute command? [y/N]: y
```

### 4. Inspect Files and Repositories (`-f`, `-d`)
```bash
# Analyze a configuration file:
search -f /etc/nginx/nginx.conf "identify potential performance bottlenecks"

# Analyze a repository structure:
search -d . "summarize project architecture and entry points"
```

### 5. Piped Input
```bash
cat /var/log/nginx/error.log | search "what caused this error and how to fix it"
dmesg | tail -n 50 | search
```

---

## Command-Line Options

```text
usage: search [-h] [-c] [-p {gemini,openrouter,nvidia,custom}] [-m NAME]
              [-s DOMAIN] [-f PATH] [-d PATH] [-i] [-w] [-r] [-y] [--setup]
              [--no-cache] [--clear-cache] [--set-provider {gemini,openrouter,nvidia,custom}]
              [--set-key KEY] [--set-model MODEL] [--set-url URL] [--set-site DOMAIN]
              [--force] [-v] [query ...]

positional arguments:
  query                 Query or prompt to process

options:
  -h, --help            Show this help message and exit
  -c, --cmd             Generate an executable shell command
  -p, --provider        Switch provider (gemini, openrouter, nvidia, custom)
  -m, --model NAME      Model identifier
  -s, --site DOMAIN     Scope search to a specific domain
  -f, --file PATH       Attach file content as context
  -d, --dir PATH        Attach directory tree and structure as context
  -i, --interactive     Launch interactive wizard
  -w, --no-web          Disable web search grounding
  -r, --raw             Output plain unformatted text
  -y, --yes             Auto-execute generated command without confirmation
  --setup               Run provider and key configuration wizard
  --force               Force save settings even if validation warns
  --no-cache            Bypass local cache
  --clear-cache         Clear local cache
  --set-provider        Set default provider
  --set-key KEY         Save API key for active provider
  --set-model MODEL     Save default model for active provider
  --set-url URL         Save custom Base URL
  --set-site DOMAIN     Save default search domain
  -v, --version         Show program's version number and exit
```

---

## License

MIT
