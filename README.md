# daily_quotes

A small automation project that fetches a random quote every day and commits it to this repo using GitHub Actions.

The script runs on a schedule (7 PM PHT), pulls a quote from the [ZenQuotes API](https://zenquotes.io/), writes it to a markdown file, and pushes the commit — no manual work needed.

## Today's quote

<!-- QUOTE:START -->
> *"If your mind is empty, it is always ready for anything, it is open to everything."*
>
> — Shunryu Suzuki

`September 27, 2026` · [view file](quotes/2026-09-27.md)
<!-- QUOTE:END -->

## How it works

1. GitHub Actions triggers the workflow on a cron schedule
2. A Python script hits the ZenQuotes API for a random quote
3. The quote gets saved as `quotes/YYYY-MM-DD.md`
4. This README gets updated with the latest quote
5. Everything gets committed and pushed automatically

The script also keeps a simple history log (`data/history.json`) so it doesn't repeat the same quote twice.

## Project structure

```
daily_quotes/
├── .github/workflows/
│   └── daily_quote.yml       # cron workflow — runs daily at 11:00 UTC (7 PM PHT)
├── data/
│   └── history.json          # list of previously used quotes
├── quotes/                   # archive of all generated quotes
├── src/
│   └── generate_quote.py     # the actual script
└── README.md
```

## Run locally

```bash
python src/generate_quote.py
```

No dependencies outside the standard library.

## Quote archive

All past quotes are stored in the [`quotes/`](quotes/) directory, one file per day.

---

Quote data from [ZenQuotes API](https://zenquotes.io/).
