# daily_quotes

A small automation project that fetches a random quote every day and commits it to this repo using GitHub Actions.

The script runs on a schedule (3:15 AM PHT), pulls a quote from the [ZenQuotes API](https://zenquotes.io/), writes it to a markdown file, and pushes the commit — no manual work needed.

## Today's quote

<!-- QUOTE:START -->
> *"Walk slowly but never walk backward."*
>
> — Unknown

`September 30, 2026` · [view file](quotes/2026-09-30.md)
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
│   └── daily_quote.yml       # cron workflow — runs daily at 19:15 UTC (3:15 AM PHT)
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
