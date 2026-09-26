<div align="center">

# 📜 Daily Quote Generator

**A Python + GitHub Actions automation that generates and publishes a daily inspirational quote.**

[![Daily Quote](https://github.com/FROYD/daily_quotes/actions/workflows/daily_quote.yml/badge.svg)](https://github.com/FROYD/daily_quotes/actions/workflows/daily_quote.yml)

</div>

---

## 🔥 What is this?

Every day at **7:00 PM Philippine Time**, a GitHub Actions workflow automatically:

1. Fetches a random inspirational quote from [ZenQuotes API](https://zenquotes.io/)
2. Saves it as a dated Markdown file in the [`quotes/`](quotes/) folder
3. Updates this README with today's quote
4. Commits and pushes — earning a daily GitHub contribution ✅

---

<!-- QUOTE:START -->
<div align="center">

### 📜 Today's Quote — September 26, 2026

> *"The secret of perfect health lies in keeping the mind always cheerful - never worried, never hurried, never borne down by any fear, thought or anxiety."*

— **Sathya Sai Baba**

<sub>🗂️ <a href="quotes/2026-09-26.md">View today's quote file</a> · Powered by <a href="https://zenquotes.io/">ZenQuotes API</a></sub>

</div>
<!-- QUOTE:END -->

---

## 📂 Project Structure

```text
daily_quotes/
├── .github/workflows/
│   └── daily_quote.yml       # GitHub Actions cron workflow
├── data/
│   └── history.json          # Tracks used quotes to avoid duplicates
├── quotes/
│   └── 2026-09-27.md         # Dated quote archive
├── src/
│   └── generate_quote.py     # Main Python script
└── README.md                 # You are here!
```

## 🛠️ Tech Stack

- **Python 3.12+** — standard library only (`json`, `urllib`, `datetime`, `pathlib`)
- **GitHub Actions** — scheduled cron workflow
- **ZenQuotes API** — free, no auth required

## 🚀 Run Locally

```bash
python src/generate_quote.py
```

## 📜 Quote Archive

Browse all past quotes in the [`quotes/`](quotes/) directory.

---

<div align="center">
<sub>Built with ❤️ as a Python + DevOps learning project · Powered by <a href="https://zenquotes.io/">ZenQuotes API</a></sub>
</div>
