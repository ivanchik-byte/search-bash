# search-cli

Terminal search, codebase inspection, and command-line AI assistant powered by Google Search Grounding.

Designed for Linux systems, remote SSH servers, and DevOps workflows. Returns concise answers, verified documentation links, executable shell commands, and codebase analysis directly inside your terminal.

---

## Features

- **Interactive Wizard**: Launch without arguments (`search`) to step through guided queries, domain targeting, and command execution.
- **Google Search Grounding**: Fetches up-to-date documentation and articles from live Google search, complete with clickable source links.
- **Command Generator (`-c`)**: Generates exact, copy-pasteable Linux commands with an interactive prompt to execute immediately.
- **Codebase & File Context (`-f`, `-d`)**: Reads individual files or scans repository trees (filtering noise like `.git`, `node_modules`, `venv`) to answer project-specific questions.
- **Domain Targeting (`-s`)**: Restricts search scope to specific documentation sites (e.g. `stackoverflow.com`, `docs.docker.com`, `github.com`).
- **Unix Pipeline Support**: Accepts piped logs, configs, or command outputs (`cat /var/log/syslog | search "find root cause"`).
- **Local Caching**: Repeated identical queries return within milliseconds from `~/.cache/search_cli/`, preserving API quotas.
- **Clean Terminal UI**: Formatted with clean ASCII blocks and syntax-highlighted Markdown. No emojis, no marketing chatter.

---

## Installation

### Option 1: Using pipx (Recommended)

```bash
git clone https://github.com/<your-username>/search-cli.git
cd search-cli
pipx install .
```

To install directly from GitHub:
```bash
pipx install git+https://github.com/<your-username>/search-cli.git
```

### Option 2: Local Install Script

```bash
git clone https://github.com/<your-username>/search-cli.git
cd search-cli
chmod +x install.sh
./install.sh
```

### Option 3: Standard pip

```bash
pip install .
```

Ensure `~/.local/bin` is in your `PATH`.

---

## Configuration

On your first run, `search` will automatically prompt you for your Gemini API key and validate it against the API:

```bash
search
```

Alternatively, configure the key directly:

```bash
# Save to ~/.config/search/config.json
search --set-key "AIzaSy..."

# Or set via environment variable:
export GEMINI_API_KEY="AIzaSy..."
```

A free API key can be obtained at [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## Usage Examples

### 1. Interactive Mode
Run without arguments to enter the interactive prompt:
```bash
search
```

### 2. General Technical Search
```bash
search "how to configure reverse proxy in nginx for websocket"
search "systemd service restart limit configuration"
```

### 3. Generate and Execute Shell Commands (`-c`)
```bash
search -c "find all files larger than 100MB and sort by size"
```
Output:
```
find / -type f -size +100M -exec ls -lh {} + 2>/dev/null | awk '{ print $5, $9 }' | sort -hr

Execute command? [y/N]: y
```
Use `-y` to execute automatically without prompting:
```bash
search -c -y "show free memory in human readable format"
```

### 4. Site-Scoped Search (`-s`)
```bash
search -s stackoverflow.com "python typeerror unhashable type list"
search -s docs.docker.com "healthcheck interval and retries"
```
To set a default domain for all future queries:
```bash
search --set-site "stackoverflow.com"
```

### 5. Inspect Files and Repositories (`-f`, `-d`)
```bash
# Analyze a configuration file:
search -f /etc/nginx/nginx.conf "identify potential performance bottlenecks"

# Analyze a repository structure:
search -d . "summarize project architecture and entry points"
```

### 6. Piped Input
```bash
# Analyze error log:
cat /var/log/nginx/error.log | search "what caused this error and how to fix it"

# Diagnose hardware / kernel messages:
dmesg | tail -n 50 | search
```

---

## Command-Line Options

```text
usage: search [-h] [-c] [-s DOMAIN] [-f PATH] [-d PATH] [-m NAME] [-i]
              [-w] [-r] [-y] [--no-cache] [--clear-cache]
              [--set-key KEY] [--set-model MODEL] [--set-site DOMAIN]
              [-v] [query ...]

positional arguments:
  query                 Query or prompt to process

options:
  -h, --help            Show this help message and exit
  -c, --cmd             Generate an executable shell command
  -s, --site DOMAIN     Scope search to a specific domain
  -f, --file PATH       Attach file content as context
  -d, --dir PATH        Attach directory tree and structure as context
  -m, --model NAME      Gemini model identifier (default: gemini-3.5-flash-lite)
  -i, --interactive     Launch interactive wizard
  -w, --no-web          Disable web search grounding (pure LLM)
  -r, --raw             Output plain unformatted text
  -y, --yes             Auto-execute generated command without confirmation
  --no-cache            Bypass local cache
  --clear-cache         Clear local cache
  --set-key KEY         Save API key to configuration
  --set-model MODEL     Save default model to configuration
  --set-site DOMAIN     Save default search domain to configuration
  -v, --version         Show program's version number and exit
```

---

## License

MIT
