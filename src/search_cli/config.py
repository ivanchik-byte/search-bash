import os
import sys
import json
from pathlib import Path

DEFAULT_MODEL = "gemini-3.5-flash-lite"
FALLBACK_MODEL = "gemini-2.0-flash"

CONFIG_DIR = Path.home() / ".config" / "search"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config() -> dict:
    config = {
        "api_key": os.environ.get("GEMINI_API_KEY", "").strip(),
        "model": os.environ.get("SEARCH_MODEL", DEFAULT_MODEL).strip(),
        "default_site": "",
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                if not config["api_key"] and saved.get("api_key"):
                    config["api_key"] = saved["api_key"].strip()
                if "model" in saved and not os.environ.get("SEARCH_MODEL"):
                    config["model"] = saved["model"].strip()
                if "default_site" in saved:
                    config["default_site"] = saved["default_site"].strip()
        except Exception:
            pass
    return config


def save_config(api_key: str = None, model: str = None, default_site: str = None):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    current = {}
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                current = json.load(f)
        except Exception:
            current = {}

    if api_key is not None:
        current["api_key"] = api_key.strip()
    if model is not None:
        current["model"] = model.strip()
    if default_site is not None:
        current["default_site"] = default_site.strip()

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(current, f, indent=2, ensure_ascii=False)


def prompt_api_key(validate_func=None) -> str:
    print("[*] Gemini API key is not configured.")
    print("    Get your free key at: https://aistudio.google.com/app/apikey")
    
    if not sys.stdin.isatty():
        print("[-] Interactive prompt unavailable in non-interactive environment.", file=sys.stderr)
        print("    Set the GEMINI_API_KEY environment variable or run 'search --set-key <KEY>'.", file=sys.stderr)
        sys.exit(1)

    while True:
        try:
            raw_key = input("\nEnter API key (or 'q' to quit): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            sys.exit(1)

        if not raw_key or raw_key.lower() == "q":
            print("Aborted.")
            sys.exit(1)

        if validate_func:
            print("[*] Validating API key...")
            valid, err = validate_func(raw_key)
            if not valid:
                print(f"[-] Key validation failed: {err}")
                print("    Please verify the key and try again.")
                continue

        save_config(api_key=raw_key)
        print("[+] API key saved to ~/.config/search/config.json")
        return raw_key
