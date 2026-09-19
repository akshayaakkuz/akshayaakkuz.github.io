# Akshaya Suresh — portfolio & web projects

A personal portfolio and a practical spam-message detector, published with GitHub Pages.

**[Open portfolio](https://akshayaakkuz.github.io/)** · **[Try the spam checker](https://akshayaakkuz.github.io/spam-check/)**

## Projects

| Project | What it does | Source |
| --- | --- | --- |
| Personal portfolio | Responsive introduction and public GitHub repository feed | [index.html](index.html) |
| Signal | Checks English messages against explainable weighted spam rules, locally in the browser | [spam-check/](spam-check/) |

## Run locally

Open `index.html` or `spam-check/index.html` in a browser. No installation or build step is needed. The portfolio requests public repository information from GitHub; the spam checker needs no network requests for analysis.

## Validate the detector

With Node.js installed:

```sh
node spam-check/test.cjs
```

The functional checks cover normal messages, suspicious combinations, Unicode normalization, repeated signals, and input limits. They are regression checks, not a real-world accuracy benchmark.

## Design choices

- Plain HTML, CSS and JavaScript with no frontend dependencies.
- Relative asset paths work on GitHub Pages.
- Spam results explain the matched rules and their weights.
- Message content is not uploaded, stored or logged.
- The portfolio falls back to a GitHub link if the repository feed is unavailable.

## Limitations

Signal is a rule-based English-language baseline, not a trained model. It can miss spam and flag legitimate messages. It does not inspect URLs or authenticate senders. See the [detector documentation](spam-check/README.md) for scoring details.

## Deployment

GitHub Pages publishes the `main` branch from the repository root. The portfolio lives at `/` and Signal at `/spam-check/`.
