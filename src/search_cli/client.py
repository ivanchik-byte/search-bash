import re
import requests
from .config import FALLBACK_MODEL


def validate_api_key(api_key: str) -> tuple[bool, str]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": "ping"}]}],
        "generationConfig": {"maxOutputTokens": 1},
    }
    try:
        resp = requests.post(url, json=payload, timeout=10.0)
        if resp.status_code == 200:
            return True, ""
        err_msg = f"HTTP {resp.status_code}"
        try:
            data = resp.json()
            if "error" in data and "message" in data["error"]:
                err_msg = data["error"]["message"]
        except Exception:
            pass
        return False, err_msg
    except Exception as e:
        return False, str(e)


def extract_shell_command(text: str) -> str | None:
    match = re.search(r"```(?:bash|sh|zsh)?\s*\n(.*?)\n```", text, re.DOTALL)
    if match:
        cmd = match.group(1).strip()
        if not cmd.startswith("#") and cmd:
            return cmd
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("$ "):
            return line[2:].strip()
    return None


def call_gemini(
    prompt: str,
    api_key: str,
    model: str,
    use_search: bool = True,
    cmd_mode: bool = False,
    site: str = None,
) -> dict:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}

    if cmd_mode:
        system_instruction = (
            "You are a precise Linux/Unix command-line assistant. "
            "Output the exact, production-ready shell command inside a single markdown code block: ```bash\n<command>\n```. "
            "Follow immediately with a concise 1-2 sentence explanation of arguments and flags used. "
            "Avoid introductory filler or disclaimers."
        )
    else:
        system_instruction = (
            "You are an expert systems engineer and developer CLI assistant. "
            "Provide concise, practical, technical responses. "
            "Use clear code blocks with language identifiers. "
            "Avoid conversational fluff, emojis, and unnecessary preambles."
        )

    augmented_prompt = prompt
    if site:
        augmented_prompt = f"Search specifically on site '{site}' if relevant.\n\nQuery: {prompt}"

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": augmented_prompt}],
            }
        ],
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        },
        "generationConfig": {
            "temperature": 0.2 if cmd_mode else 0.4,
            "maxOutputTokens": 3000,
        },
    }

    if use_search:
        payload["tools"] = [{"googleSearch": {}}]

    response = requests.post(url, headers=headers, json=payload, timeout=30.0)

    if response.status_code == 404 and model != FALLBACK_MODEL:
        return call_gemini(
            prompt=prompt,
            api_key=api_key,
            model=FALLBACK_MODEL,
            use_search=use_search,
            cmd_mode=cmd_mode,
            site=site,
        )

    if response.status_code != 200:
        error_msg = f"HTTP {response.status_code}"
        try:
            err_json = response.json()
            if "error" in err_json and "message" in err_json["error"]:
                error_msg = f"{error_msg}: {err_json['error']['message']}"
            else:
                error_msg = f"{error_msg}: {response.text}"
        except Exception:
            error_msg = f"{error_msg}: {response.text}"
        raise RuntimeError(error_msg)

    data = response.json()
    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError("No candidate responses returned by the API.")

    candidate = candidates[0]
    parts = candidate.get("content", {}).get("parts", [])
    text_parts = [p.get("text", "") for p in parts if "text" in p]
    answer_text = "".join(text_parts).strip()

    grounding_meta = candidate.get("groundingMetadata", {})
    queries = grounding_meta.get("webSearchQueries", [])
    chunks = grounding_meta.get("groundingChunks", [])

    sources = []
    seen_urls = set()
    for chunk in chunks:
        web = chunk.get("web", {})
        uri = web.get("uri")
        title = web.get("title", uri)
        if uri and uri not in seen_urls:
            seen_urls.add(uri)
            sources.append({"title": title, "url": uri})

    suggested_cmd = extract_shell_command(answer_text) if cmd_mode else None

    return {
        "text": answer_text,
        "suggested_cmd": suggested_cmd,
        "queries": queries,
        "sources": sources,
        "model_used": model,
    }
