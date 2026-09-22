# Learn it, demonstrate it, then describe it accurately

## A truthful introduction

“My background is Python and AI/ML. I built a personal Django companion to my browser-based spam checker with AI assistance to practice application security and CI. It has authenticated private scan history, authorization regression tests, static analysis and dependency auditing. I can walk through how the ownership tests catch a deliberate regression. I am still learning Docker and have not operated this application in production.”

Use this only after you can run and explain the project. The study asks for professional experience; this lab does not establish employment experience or guarantee eligibility.

## Five-minute walkthrough

1. **Feature (one minute):** sign in and submit a synthetic message. Explain frontend → Python view → analyzer → database → rendered response. Scores are uncalibrated rule points, not ML confidence.
2. **Security requirement (one minute):** a result belongs to one user. Show the owner filter in `scans/views.py`; explain why knowing an ID gives no permission.
3. **Verification (one minute):** show the Bob/Alice regression tests and positive owner tests. Run the mutation demonstration and explain the expected failures.
4. **Pipeline (one minute):** open a real Actions run. Explain why the container job depends on verification. Failed tests stop packaging; required branch checks must be configured separately to stop merging.
5. **Tradeoffs (one minute):** Django reduces custom authentication code; SQLite simplifies learning; storing less data reduces exposure. Public deployment still needs throttling, HTTPS and operational controls.

## Practice questions

**What is CI/CD?** CI automatically checks changes. Delivery makes checked changes ready to release; deployment actually releases them. This repository currently demonstrates CI and checked container packaging, not automatic Python production deployment.

**What is vulnerability verification?** Reproducing the prohibited behavior, fixing the cause, and proving with positive and negative tests that the behavior is corrected. Scanner output alone is a lead, not always a verified exploitable issue.

**Authentication versus authorization?** Authentication establishes who signed in. Authorization decides which records that identity may access.

**What blocks a release?** Here the verification job blocks container packaging on test, Bandit or dependency audit failure. In a real release process I would also define severity/exception policies, require approvals for documented exceptions, and verify rollback.

**How would you handle a false positive?** Reproduce and inspect the affected code or dependency, assess reachability and impact, document evidence, and narrowly suppress only a justified finding with an owner and expiry. Do not turn the whole scanner off.

**Can the model secure the application?** No. Spam detection is a product feature. Access control, sessions, safe rendering and deployment controls protect the application independently of detector accuracy.

**What production challenge did you face?** Do not invent one. Explain that this example is a personal lab and describe the ownership-verification challenge you actually reproduced. Discuss real work separately.

## Hands-on preparation

- Session 1: run the app without Docker and trace one submitted request through the Python code.
- Session 2: create Alice and Bob, run the tests, and explain each ownership assertion aloud.
- Session 3: build with Docker and explain image/container/volume/port using your running app.
- Session 4: read the Actions logs and make one small legitimate improvement with a test in a new pull request.

Be ready to show what you personally changed and how you verified it. Memorizing this guide is not a substitute for doing the exercises.
