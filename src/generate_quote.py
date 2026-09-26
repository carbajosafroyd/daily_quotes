"""
Daily Quote Generator
Fetches a random inspirational quote from ZenQuotes API,
saves it as a dated Markdown file, and updates the README.
"""

import sys
import io
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

# Fix Windows console encoding for Unicode characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent
QUOTES_DIR = ROOT_DIR / "quotes"
README_PATH = ROOT_DIR / "README.md"
HISTORY_PATH = ROOT_DIR / "data" / "history.json"

# ── Timezone ───────────────────────────────────────────────────
PHT = timezone(timedelta(hours=8))  # Philippine Time (UTC+8)

# ── API ────────────────────────────────────────────────────────
ZENQUOTES_URL = "https://zenquotes.io/api/random"


def fetch_quote() -> dict:
    """Fetch a random quote from ZenQuotes API.

    Returns:
        dict with keys 'text' and 'author'
    """
    req = urllib.request.Request(
        ZENQUOTES_URL,
        headers={"User-Agent": "DailyQuoteBot/1.0"},
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"[ERROR] Failed to fetch quote: {e}")
        raise SystemExit(1)

    if not data or not isinstance(data, list):
        print("[ERROR] Unexpected API response format.")
        raise SystemExit(1)

    quote = data[0]
    return {"text": quote["q"], "author": quote["a"]}


def load_history() -> list[str]:
    """Load the list of previously used quotes."""
    if HISTORY_PATH.exists():
        return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
    return []


def save_history(history: list[str]) -> None:
    """Persist the history list to disk."""
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_PATH.write_text(
        json.dumps(history, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def fetch_unique_quote(max_retries: int = 5) -> dict:
    """Fetch a quote that hasn't been used before.

    Retries up to `max_retries` times to avoid duplicates.
    If all retries return duplicates, uses the last fetched quote.
    """
    history = load_history()

    for attempt in range(max_retries):
        quote = fetch_quote()
        if quote["text"] not in history:
            history.append(quote["text"])
            save_history(history)
            return quote
        print(f"  ↻ Duplicate quote on attempt {attempt + 1}, retrying...")

    # After all retries, just use the last one
    print("  ⚠ Could not find a unique quote, using last fetched.")
    history.append(quote["text"])
    save_history(history)
    return quote


def generate_quote_file(quote: dict, today: datetime) -> Path:
    """Create the dated Markdown quote file.

    Args:
        quote: dict with 'text' and 'author'
        today: datetime for today's date

    Returns:
        Path to the created file
    """
    QUOTES_DIR.mkdir(parents=True, exist_ok=True)

    date_str = today.strftime("%Y-%m-%d")
    date_display = today.strftime("%B %d, %Y")  # e.g. September 27, 2026
    filename = QUOTES_DIR / f"{date_str}.md"

    content = f"""# 📜 Daily Quote — {date_display}

> "{quote['text']}"

— **{quote['author']}**

---

*Generated automatically by [Daily Quote Generator](https://github.com/FROYD/daily_quotes)*
*Powered by [ZenQuotes API](https://zenquotes.io/)*
"""

    filename.write_text(content, encoding="utf-8")
    print(f"  ✔ Created {filename.relative_to(ROOT_DIR)}")
    return filename


def update_readme(quote: dict, today: datetime) -> None:
    """Update README.md with today's quote between marker comments."""
    date_display = today.strftime("%B %d, %Y")
    date_str = today.strftime("%Y-%m-%d")

    quote_section = f"""<!-- QUOTE:START -->
<div align="center">

### 📜 Today's Quote — {date_display}

> *"{quote['text']}"*

— **{quote['author']}**

<sub>🗂️ <a href="quotes/{date_str}.md">View today's quote file</a> · Powered by <a href="https://zenquotes.io/">ZenQuotes API</a></sub>

</div>
<!-- QUOTE:END -->"""

    if README_PATH.exists():
        readme = README_PATH.read_text(encoding="utf-8")

        # Replace content between markers
        start_marker = "<!-- QUOTE:START -->"
        end_marker = "<!-- QUOTE:END -->"

        if start_marker in readme and end_marker in readme:
            before = readme[: readme.index(start_marker)]
            after = readme[readme.index(end_marker) + len(end_marker) :]
            readme = before + quote_section + after
        else:
            # Markers not found — append to end
            readme += "\n\n" + quote_section
    else:
        # README doesn't exist yet — shouldn't happen, but handle it
        readme = quote_section

    README_PATH.write_text(readme, encoding="utf-8")
    print(f"  ✔ Updated README.md")


def main():
    today = datetime.now(PHT)
    date_str = today.strftime("%Y-%m-%d")

    print(f"╔══════════════════════════════════════╗")
    print(f"║     📜 Daily Quote Generator         ║")
    print(f"║     {date_str}                    ║")
    print(f"╚══════════════════════════════════════╝")
    print()

    # Check if today's quote already exists
    quote_file = QUOTES_DIR / f"{date_str}.md"
    if quote_file.exists():
        print(f"  ⚠ Quote for {date_str} already exists. Skipping.")
        return

    # Fetch a unique quote
    print("  ⏳ Fetching quote from ZenQuotes API...")
    quote = fetch_unique_quote()
    print(f'  💬 "{quote["text"]}"')
    print(f"     — {quote['author']}")
    print()

    # Generate files
    generate_quote_file(quote, today)
    update_readme(quote, today)

    print()
    print("  ✅ Done!")


if __name__ == "__main__":
    main()
