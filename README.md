# search

A single-file terminal intelligence and search utility powered by Google Search Grounding.

Designed for Linux servers, remote SSH sessions, and DevOps workflows. Returns verified documentation, executable shell commands, and project-aware analysis directly inside your terminal.

Zero mandatory dependencies. Runs on standard Python 3.10+.

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

## Setup

Run `search` without arguments to launch the first-run configuration wizard:

```bash
search
```

It will prompt for your free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey), validate it, and store it in `~/.config/search/config.json`.

Alternatively, configure the key directly:
```bash
search --set-key "AIzaSy..."
# or
export GEMINI_API_KEY="AIzaSy..."
```

---

## Features

- **Single-File Architecture**: Everything lives in one self-contained script (`search`). No virtual environments, no package clutter.
- **Interactive Wizard**: Run `search` with no arguments to step through query formulation, target domain selection, and command execution.
- **Live Google Search Grounding**: Retrieves current web results with clickable source links.
- **Command Generator (`-c`)**: Generates exact, copy-pasteable Linux commands with an interactive prompt to execute them.
- **Codebase & File Context (`-f`, `-d`)**: Analyzes specific files or scans repository directory trees (filtering noise like `.git`, `node_modules`, `venv`).
- **Domain Targeting (`-s`)**: Restricts search scope to specific documentation sites (e.g. `stackoverflow.com`, `docs.docker.com`).
- **Unix Pipelines**: Reads stdin streams (`cat /var/log/syslog | search "explain root cause"`).
- **Local Caching**: Repeated identical queries return instantly from `~/.cache/search_cli/`, preserving API quotas.
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
search "systemd service restart limit configuration"
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
To auto-execute without confirmation:
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
  -s DOMAIN, --site DOMAIN
                        Scope search to a specific domain
  -f PATH, --file PATH  Attach file content as context
  -d PATH, --dir PATH   Attach directory tree and structure as context
  -m NAME, --model NAME
                        Gemini model identifier (default: gemini-3.5-flash-lite)
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
