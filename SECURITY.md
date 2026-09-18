# Security Policy

## Supported Versions

Security fixes are provided for the latest release on the `main` branch.

## Reporting a Vulnerability

If you discover a security vulnerability, please report it privately:

- **GitHub Advisory**: Open a report via GitHub Private Vulnerability Reporting
- **Telegram**: [@ivanchikbyte](https://t.me/ivanchikbyte)
- **Email**: `ivanchikbyte@gmail.com`

Please do not open public issues for security vulnerabilities.

I will acknowledge receipt within 48 hours and coordinate a fix before any public disclosure.

## Security Design

- API keys and provider configurations are stored locally in `~/.config/search/config.json` with strict `0600` permissions.
- Interactive key entry uses terminal masking to prevent exposure in shell history.
- API keys in request URLs are redacted before error output or local logging.
- No analytics, telemetry, or remote telemetry logging exist in this project.
