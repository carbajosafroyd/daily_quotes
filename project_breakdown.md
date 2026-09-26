# How `daily_quotes` Works — Full Breakdown

This is a complete explanation of every part of the project so you actually understand what's going on, not just copy-paste it.

---

## The big picture

The whole idea is simple:

```
Every day at 7 PM → a script runs → it grabs a quote → saves it → commits it to your repo
```

Your computer doesn't need to be on. GitHub runs it for you on their servers.

The result: you get a **green contribution square** on your GitHub profile every day, and your repo gradually fills up with a nice archive of daily quotes.

---

## The files and what each one does

### `src/generate_quote.py`

This is the brain of the project. Here's what it does step by step when it runs:

```
1. What's today's date?  →  e.g. 2026-09-26
2. Did I already make a quote for today?  →  check if quotes/2026-09-26.md exists
3. If yes → stop, don't duplicate
4. If no → call the ZenQuotes API → get a random quote
5. Has this exact quote been used before?  →  check data/history.json
6. If duplicate → try again (up to 5 times)
7. Save the quote text to history.json
8. Create quotes/2026-09-26.md with the quote
9. Update README.md to show today's quote
```

#### Key Python concepts used:

| Concept | Where / Why |
|---|---|
| `pathlib.Path` | File path handling — `Path(__file__).parent.parent` goes from `src/` up to the project root |
| `urllib.request` | Makes an HTTP request to the API (like opening a URL in your browser, but in code) |
| `json.loads()` | Parses the API response from a JSON string into a Python list/dict |
| `datetime` + `timezone` | Gets the current date in Philippine Time (UTC+8) |
| `str.format()` / f-strings | Builds the markdown content with the quote text inserted |
| File I/O | `.read_text()` / `.write_text()` to read and write files |

#### The API call explained:

```python
req = urllib.request.Request(API_URL, headers={"User-Agent": "daily-quotes/1.0"})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode("utf-8"))
```

What this does:
- Creates an HTTP request to `https://zenquotes.io/api/random`
- Adds a `User-Agent` header (some APIs block requests without one)
- Opens the connection, waits up to 15 seconds for a response
- Reads the raw bytes, decodes them to a string, then parses the JSON

The API returns something like:
```json
[{"q": "Stay hungry, stay foolish.", "a": "Steve Jobs", "h": "..."}]
```

We grab `data[0]["q"]` for the quote text and `data[0]["a"]` for the author.

---

### `data/history.json`

Just a simple list of every quote text that has been used:

```json
[
  "Stay hungry, stay foolish.",
  "The secret of perfect health lies in keeping the mind always cheerful..."
]
```

Before saving a new quote, the script checks if the text is already in this list. If it is, it fetches another one. This prevents the repo from having the same quote twice.

---

### `quotes/YYYY-MM-DD.md`

Each day gets its own markdown file. The format is dead simple:

```markdown
# September 26, 2026

> "The secret of perfect health lies in keeping..."

— Sathya Sai Baba
```

Over time, this folder becomes a clean archive:
```
quotes/
├── 2026-09-26.md
├── 2026-09-27.md
├── 2026-09-28.md
└── ...
```

---

### `README.md`

The README has a special section between two HTML comments:

```html
<!-- QUOTE:START -->
...today's quote shows up here...
<!-- QUOTE:END -->
```

The script finds these two markers, deletes everything between them, and inserts the new quote. The rest of the README stays untouched.

This is a common pattern — a lot of GitHub profile READMEs use the same trick to auto-update sections.

---

### `.github/workflows/daily_quote.yml`

This is the **GitHub Actions workflow** — the thing that makes it all automatic.

```yaml
on:
  schedule:
    - cron: '0 11 * * *'
```

#### How cron works:

Cron is a scheduling format. The five fields are:

```
┌───────── minute (0-59)
│ ┌─────── hour (0-23)
│ │ ┌───── day of month (1-31)
│ │ │ ┌─── month (1-12)
│ │ │ │ ┌─ day of week (0-6, Sunday=0)
│ │ │ │ │
0 11 * * *
```

`0 11 * * *` means: **at minute 0, hour 11, every day, every month, every day of the week**.

GitHub Actions uses **UTC time**, so:
- 11:00 UTC = 11:00 + 8 hours = **7:00 PM Philippine Time**

That's how we schedule it for 7 PM your time.

#### What the workflow does step by step:

```yaml
steps:
  - name: checkout              # downloads your repo code onto the GitHub server
  - name: setup python          # installs Python 3.12 on that server
  - name: generate quote        # runs: python src/generate_quote.py
  - name: commit and push       # stages changes, commits, and pushes back to your repo
```

The commit step has a guard:
```bash
git diff --staged --quiet || git commit -m "add quote for 2026-09-27"
```

`git diff --staged --quiet` checks "are there any changes staged?" If there are NO changes (the `||` part), it skips the commit. This prevents empty commits if the script didn't generate anything.

#### Permissions:

```yaml
permissions:
  contents: write
```

This gives the workflow permission to push commits back to your repo. Without this, the `git push` would fail.

---

### `.gitignore`

Tells Git to ignore files that shouldn't be in the repo:

```
__pycache__/      # Python's compiled bytecode cache
*.py[cod]         # other compiled Python files
venv/             # virtual environment folder (if you ever make one)
.DS_Store         # macOS junk file
Thumbs.db         # Windows thumbnail cache
```

---

## The full flow visualized

```
 7:00 PM PHT
      │
      ▼
 GitHub Actions wakes up
      │
      ▼
 Checks out your repo code
      │
      ▼
 Installs Python 3.12
      │
      ▼
 Runs: python src/generate_quote.py
      │
      ├─► Calls https://zenquotes.io/api/random
      │         │
      │         ▼
      │   Gets back: {"q": "...", "a": "..."}
      │         │
      │         ▼
      │   Checks history.json → is it a duplicate?
      │         │
      │    No ──┤
      │         ▼
      │   Writes quotes/2026-09-27.md
      │         │
      │         ▼
      │   Updates README.md between the markers
      │         │
      │         ▼
      │   Saves quote text to history.json
      │
      ▼
 git add -A
      │
      ▼
 git commit -m "add quote for 2026-09-27"
      │
      ▼
 git push
      │
      ▼
 Green square on your profile ✓
```

---

## Things worth knowing

- **GitHub Actions cron isn't precise** — it says `0 11 * * *` but GitHub might run it a few minutes late (sometimes up to 15-20 min) because free-tier workflows are queued. It'll still run every day, just not at exactly 7:00:00 PM.

- **ZenQuotes has no auth** — you don't need an API key. But they ask for attribution (the link in the README footer handles that).

- **No external dependencies** — the script uses only Python's standard library (`json`, `urllib`, `datetime`, `pathlib`). No `pip install` needed. That's why there's no `requirements.txt`.

- **The history file grows forever** — this is fine. Even after years, it'll be a few hundred KB at most. If you wanted to, you could add logic to cap it at, say, 500 entries and start over.

- **You can always run it manually** — `python src/generate_quote.py` works on your PC. And on GitHub, you can click **Actions → daily quote → Run workflow** to trigger it anytime.
