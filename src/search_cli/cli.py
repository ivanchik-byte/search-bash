import os
import sys
import subprocess
import argparse
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from . import __version__
from .config import load_config, save_config, prompt_api_key, DEFAULT_MODEL
from .cache import get_cache, set_cache, clear_cache
from .context import read_piped_stdin, read_file_context, scan_directory
from .client import call_gemini, validate_api_key

console = Console()
err_console = Console(stderr=True)


def ensure_key() -> str:
    config = load_config()
    api_key = config.get("api_key", "").strip()
    if not api_key:
        api_key = prompt_api_key(validate_func=validate_api_key)
    return api_key


def execute_shell_command(cmd: str):
    print(f"\n[+] Executing: {cmd}")
    try:
        res = subprocess.run(cmd, shell=True)
        if res.returncode != 0:
            print(f"[-] Command exited with code: {res.returncode}", file=sys.stderr)
    except Exception as e:
        print(f"[-] Execution error: {e}", file=sys.stderr)


def run_interactive():
    api_key = ensure_key()
    config = load_config()

    console.print(Panel(
        f"[bold white]Search CLI[/bold white] [dim]v{__version__}[/dim]\n"
        "[dim]Terminal Intelligence with Google Search Grounding[/dim]",
        border_style="cyan"
    ))

    while True:
        try:
            query = console.input("\n[bold cyan]Query[/bold cyan] (or 'q' to exit): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if not query or query.lower() in {"q", "exit", "quit"}:
            break

        default_site = config.get("default_site", "")
        site_prompt = f"Target site/domain (default: {default_site}): " if default_site else "Target site/domain (press Enter to skip, e.g. stackoverflow.com): "
        site_in = console.input(f"[dim]{site_prompt}[/dim]").strip()
        target_site = site_in if site_in else default_site

        ctx_in = console.input("[dim]File or dir context (optional, press Enter to skip): [/dim]").strip()
        context_data = ""
        if ctx_in:
            ctx_path = Path(ctx_in).expanduser()
            if ctx_path.is_file():
                try:
                    context_data = read_file_context(str(ctx_path))
                except Exception as e:
                    console.print(f"[red]Error reading file:[/red] {e}")
            elif ctx_path.is_dir():
                try:
                    context_data = scan_directory(str(ctx_path))
                except Exception as e:
                    console.print(f"[red]Error scanning directory:[/red] {e}")
            else:
                console.print(f"[yellow]Path not found: {ctx_in}[/yellow]")

        mode_in = console.input("[dim]Mode: [1] Search & Explain  [2] Shell Command Generator: [/dim]").strip()
        cmd_mode = mode_in == "2"

        full_prompt = query
        if context_data:
            full_prompt = f"Context:\n{context_data}\n\nTask:\n{query}"

        model = config.get("model", DEFAULT_MODEL)
        label = "Generating command..." if cmd_mode else f"Searching ({model})..."

        with console.status(f"[bold cyan]{label}[/bold cyan]", spinner="dots"):
            try:
                result = call_gemini(
                    prompt=full_prompt,
                    api_key=api_key,
                    model=model,
                    use_search=True,
                    cmd_mode=cmd_mode,
                    site=target_site or None,
                )
            except Exception as e:
                console.print(f"[bold red]API Error:[/bold red] {e}")
                continue

        console.print()
        title = f"Command Output" if cmd_mode else f"Results: {query}"
        console.print(Panel(Markdown(result["text"]), title=f"[bold]{title}[/bold]", border_style="cyan"))

        if result.get("sources"):
            console.print("[bold cyan]Sources:[/bold cyan]")
            for idx, s in enumerate(result["sources"][:5], 1):
                console.print(f"  [{idx}] {s['title']}\n      [blue underline]{s['url']}[/blue underline]")

        suggested_cmd = result.get("suggested_cmd")
        if suggested_cmd and sys.stdin.isatty():
            choice = console.input(f"\nExecute suggested command? [y/N/e(dit)]: ").strip().lower()
            if choice == "y":
                execute_shell_command(suggested_cmd)
            elif choice == "e":
                edited = console.input(f"Edit command: ")
                if edited.strip():
                    execute_shell_command(edited.strip())


def main():
    parser = argparse.ArgumentParser(
        prog="search",
        description="Terminal search, codebase inspection, and command-line AI assistant.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  search "how to configure reverse proxy in nginx"
  search -c "find files larger than 50MB and sort by size"
  search -s stackoverflow.com "python typeerror unhashable type"
  search -f ./nginx.conf "explain ssl configuration"
  search -d . "summarize project architecture"
  cat /var/log/syslog | search "identify root cause"
  search --set-key AIzaSy...
"""
    )
    parser.add_argument("query", nargs="*", help="Query or prompt to process")
    parser.add_argument("-c", "--cmd", action="store_true", help="Generate an executable shell command")
    parser.add_argument("-s", "--site", metavar="DOMAIN", help="Scope search to a specific domain (e.g. stackoverflow.com)")
    parser.add_argument("-f", "--file", metavar="PATH", help="Attach file content as context")
    parser.add_argument("-d", "--dir", metavar="PATH", help="Attach directory tree and structure as context")
    parser.add_argument("-m", "--model", metavar="NAME", help=f"Gemini model identifier (default: {DEFAULT_MODEL})")
    parser.add_argument("-i", "--interactive", action="store_true", help="Launch interactive wizard/prompt")
    parser.add_argument("-w", "--no-web", action="store_true", help="Disable web search grounding")
    parser.add_argument("-r", "--raw", action="store_true", help="Output plain unformatted text")
    parser.add_argument("-y", "--yes", action="store_true", help="Auto-execute generated command without confirmation")
    parser.add_argument("--no-cache", action="store_true", help="Bypass local cache")
    parser.add_argument("--clear-cache", action="store_true", help="Clear local cache")
    parser.add_argument("--set-key", metavar="KEY", help="Save API key to configuration")
    parser.add_argument("--set-model", metavar="MODEL", help="Save default model to configuration")
    parser.add_argument("--set-site", metavar="DOMAIN", help="Save default search domain to configuration")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    if args.clear_cache:
        cleared = clear_cache()
        print(f"[+] Cache cleared ({cleared} records removed).")
        return

    if args.set_key:
        valid, err = validate_api_key(args.set_key)
        if not valid:
            print(f"[-] Key validation failed: {err}", file=sys.stderr)
            sys.exit(1)
        save_config(api_key=args.set_key)
        print("[+] API key validated and saved successfully.")
        return

    if args.set_model:
        save_config(model=args.set_model)
        print(f"[+] Default model set to: {args.set_model}")
        return

    if args.set_site:
        save_config(default_site=args.set_site)
        print(f"[+] Default search domain set to: {args.set_site}")
        return

    piped_data = read_piped_stdin()
    query_str = " ".join(args.query).strip()

    # If no query and no piped data, or interactive flag is passed
    if args.interactive or (not query_str and not piped_data):
        if not sys.stdin.isatty():
            parser.print_help()
            sys.exit(0)
        run_interactive()
        return

    api_key = ensure_key()
    config = load_config()
    model = args.model or config.get("model", DEFAULT_MODEL)
    target_site = args.site or config.get("default_site", "")

    # Assemble context
    contexts = []
    if piped_data:
        contexts.append(f"Input Stream / Log:\n```\n{piped_data}\n```")

    if args.file:
        try:
            contexts.append(read_file_context(args.file))
        except Exception as e:
            err_console.print(f"[bold red]File error:[/bold red] {e}")
            sys.exit(1)

    if args.dir:
        try:
            contexts.append(scan_directory(args.dir))
        except Exception as e:
            err_console.print(f"[bold red]Directory error:[/bold red] {e}")
            sys.exit(1)

    if contexts and query_str:
        full_prompt = f"Context:\n" + "\n\n".join(contexts) + f"\n\nRequest:\n{query_str}"
    elif contexts and not query_str:
        full_prompt = (
            "Analyze the provided context data. Identify any errors, warnings, or anomalies, "
            "explain root causes, and provide actionable next steps and commands:\n\n" + "\n\n".join(contexts)
        )
    else:
        full_prompt = query_str

    # Cache lookup
    cache_key = f"{model}:{not args.no_web}:{args.cmd}:{target_site}:{full_prompt}"
    from_cache = False
    result = None

    if not args.no_cache:
        cached_result = get_cache(cache_key)
        if cached_result:
            result = cached_result
            from_cache = True

    if result is None:
        use_search = not args.no_web
        status_label = "Generating command..." if args.cmd else f"Querying ({model})..."
        status_spinner = console.status(f"[bold cyan]{status_label}[/bold cyan]", spinner="dots") if not args.raw else None

        try:
            if status_spinner:
                status_spinner.start()
            result = call_gemini(
                prompt=full_prompt,
                api_key=api_key,
                model=model,
                use_search=use_search,
                cmd_mode=args.cmd,
                site=target_site or None,
            )
            set_cache(cache_key, result)
        except Exception as e:
            if status_spinner:
                status_spinner.stop()
            err_console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)
        finally:
            if status_spinner:
                status_spinner.stop()

    # Raw output mode
    if args.raw:
        if args.cmd and result.get("suggested_cmd"):
            print(result["suggested_cmd"])
        else:
            print(result["text"])
        return

    # Rich formatting
    cache_notice = " [dim](cached)[/dim]" if from_cache else ""
    site_notice = f" [cyan]• site:{target_site}[/cyan]" if target_site else ""
    web_notice = " [green]• web[/green]" if not args.no_web else " [dim]• no-web[/dim]"
    
    panel_title = f"[bold white]{query_str or 'Context Analysis'}[/bold white]{site_notice}{web_notice}{cache_notice}"

    console.print()
    console.print(Panel(
        Markdown(result["text"]),
        title=panel_title,
        border_style="cyan",
        subtitle=f"[dim]model: {result.get('model_used', model)}[/dim]",
        subtitle_align="right",
    ))

    if result.get("sources"):
        console.print("[bold cyan]Sources:[/bold cyan]")
        for idx, s in enumerate(result["sources"][:5], 1):
            console.print(f"  [{idx}] {s['title']}\n      [blue underline]{s['url']}[/blue underline]")
    console.print()

    # Command execution handling
    suggested_cmd = result.get("suggested_cmd")
    if args.cmd and suggested_cmd:
        if args.yes:
            execute_shell_command(suggested_cmd)
        elif sys.stdin.isatty():
            try:
                choice = input("Execute command? [y/N]: ").strip().lower()
                if choice == "y":
                    execute_shell_command(suggested_cmd)
            except (KeyboardInterrupt, EOFError):
                pass


if __name__ == "__main__":
    main()
