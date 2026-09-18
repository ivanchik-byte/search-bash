# Contributing

Thank you for your interest in improving `search-bash`.

## Core Principles

1. **Single file**: Everything lives in the standalone `search` script. Do not introduce mandatory third-party pip dependencies. Standard library only.
2. **Discuss features first**: Open an issue to discuss new features before writing code. Keeping the CLI lean and focused is a priority.
3. **Focused bug fixes**: Bug fixes and reliability improvements are welcome. Please include reproduction steps.
4. **No emojis**: Do not add emojis to code, terminal output, comments, or documentation.

## Local Testing

Verify Python syntax before opening a pull request:

```bash
python3 -m py_compile search
./search --help
```

Use clear, descriptive commit messages following the Conventional Commits format (`fix:`, `feat:`, `docs:`).
