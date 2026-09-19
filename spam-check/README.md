# Signal — simple spam message detector

A small, explainable JavaScript project that flags common patterns in English messages. This is an established rule-based baseline, not a novel research contribution or trained machine-learning model.

## Run
Open `index.html` in a browser. No setup or API key is needed. All analysis happens locally; messages are not stored, uploaded, or logged. The page uses no third-party dependencies.

## Test
With Node.js installed, run `node test.cjs` in this directory. The checks cover benign text, suspicious combinations, boundaries, normalization, and repeated signals. They do not establish real-world accuracy.

## Files
- `index.html`: responsive interface and styles
- `detector.js`: reusable detection function and weighted rules
- `app.js`: example messages and interface events
- `test.cjs`: functional regression checks

## Logic
Normalize Unicode and whitespace, remove common zero-width characters, match each rule once, and sum its weight. Scores 0–1 mean few spam signals, 2–4 need a closer look, and 5+ indicate likely spam. Stronger signals include credential requests, advance fees, prize claims, and unrealistic returns. Supporting signals include urgency, URLs, shortened links, repeated exclamation marks, and all caps.

The weights and thresholds are manually chosen and uncalibrated. Points are not probabilities. This tool cannot verify senders, check link destinations, detect malicious attachments, or understand context. It may flag educational discussions and legitimate warnings, and miss obfuscated or non-English spam. Do not use it to automatically delete or block messages.

## GitHub Pages
The app works as a static subfolder at `/spam-check/` on an existing GitHub Pages site. You can also upload these files to the root of a standalone repository and enable Pages from its main branch.

