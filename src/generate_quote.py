"""
generate_quote.py

Fetches a random quote from the ZenQuotes API, saves it as a
dated markdown file under quotes/, and updates the project README
with the latest quote. Keeps a history log to avoid repeats.
"""

import sys
import io
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Handle Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ── paths (relative to project root) ──────────────────────────
ROOT = Path(__file__).resolve().parent.parent
QUOTES_DIR = ROOT / "quotes"
README = ROOT / "README.md"
HISTORY = ROOT / "data" / "history.json"

# ── config ─────────────────────────────────────────────────────
PHT = timezone(timedelta(hours=8))
API_URL = "https://zenquotes.io/api/random"


# ── api ────────────────────────────────────────────────────────

def fetch_quote():
    """Hit the ZenQuotes API and return a (text, author) tuple."""
    req = urllib.request.Request(API_URL, headers={"User-Agent": "daily-quotes/1.0"})

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"error: couldn't reach ZenQuotes — {e}")
        raise SystemExit(1)

    if not data or not isinstance(data, list):
        print("error: unexpected response from API")
        raise SystemExit(1)

    return data[0]["q"], data[0]["a"]


# ── history (duplicate prevention) ─────────────────────────────

def load_history():
    if HISTORY.exists():
        return json.loads(HISTORY.read_text(encoding="utf-8"))
    return []


def save_history(history):
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    HISTORY.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")


def fetch_unique_quote(retries=5):
    """Try to get a quote we haven't used before."""
    history = load_history()

    for i in range(retries):
        text, author = fetch_quote()
        if text not in history:
            history.append(text)
            save_history(history)
            return text, author
        print(f"  duplicate (attempt {i + 1}), retrying...")

    # give up and use it anyway
    print("  couldn't avoid a duplicate, using last fetched quote")
    history.append(text)
    save_history(history)
    return text, author


# ── file generation ────────────────────────────────────────────

def write_quote_file(text, author, today):
    """Create quotes/YYYY-MM-DD.md, or quotes/YYYY-MM-DD_N.md if run multiple times."""
    QUOTES_DIR.mkdir(parents=True, exist_ok=True)

    date_str = today.strftime("%Y-%m-%d")
    date_display = today.strftime("%B %d, %Y")

    path = QUOTES_DIR / f"{date_str}.md"
    file_rel = f"{date_str}.md"
    if path.exists():
        counter = 2
        while (QUOTES_DIR / f"{date_str}_{counter}.md").exists():
            counter += 1
        file_rel = f"{date_str}_{counter}.md"
        path = QUOTES_DIR / file_rel

    content = f"""# {date_display}

> "{text}"

— {author}
"""
    path.write_text(content, encoding="utf-8")
    print(f"  saved quotes/{file_rel}")
    return path, file_rel


def update_readme(text, author, today, file_rel=None):
    """Swap the quote block between the QUOTE markers in README.md"""
    date_display = today.strftime("%B %d, %Y")

    new_block = (
        "<!-- QUOTE:START -->\n"
        f"> *\"{text}\"*\n"
        f">\n"
        f"> — **{author}**\n"
        f"\n"
        f"`{date_display}` · [archive](quotes/)\n"
        "<!-- QUOTE:END -->"
    )

    if not README.exists():
        README.write_text(f"# daily quote\n\n{new_block}\n", encoding="utf-8")
        print("  created README.md")
        return

    content = README.read_text(encoding="utf-8")
    start = "<!-- QUOTE:START -->"
    end = "<!-- QUOTE:END -->"

    if start in content and end in content:
        before = content[:content.index(start)]
        after = content[content.index(end) + len(end):]
        content = before + new_block + after
    else:
        content = f"# daily quote\n\n{new_block}\n"

    README.write_text(content, encoding="utf-8")
    print("  updated README.md")


# ── main ───────────────────────────────────────────────────────

def main():
    today = datetime.now(PHT)
    date_str = today.strftime("%Y-%m-%d")

    print(f"daily_quotes — {date_str}")
    print()

    # fetch
    print("  fetching quote...")
    text, author = fetch_unique_quote()
    print(f"  \"{text}\"")
    print(f"  — {author}")
    print()

    # write
    _, file_rel = write_quote_file(text, author, today)
    update_readme(text, author, today, file_rel)

    print()
    print("  done")


if __name__ == "__main__":
    main()
