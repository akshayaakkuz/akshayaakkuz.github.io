# Case study: verifying object-level authorization

This is an intentionally constructed learning exercise, not an incident from an employer or a discovered vulnerability in the original static Signal app.

## Threat

Alice has a private result. Bob is authenticated and changes a result ID in the URL. If the handler retrieves solely by primary key, Bob can read or delete Alice's result. Authentication alone does not establish ownership.

## Fix

Both detail and deletion lookups use `get_object_or_404(Scan, pk=pk, owner=request.user)`. History is also owner-filtered. Creation takes ownership from the authenticated session. Requests for someone else's records return the same 404 as nonexistent records.

## Verification evidence

`AccessTests.test_other_user_cannot_read` requests Alice's result as Bob and expects 404. `test_other_user_cannot_delete` also verifies the record survives. Positive controls prove Alice can read and delete her own record.

`scripts/verify_regression.py` temporarily removes the owner argument from lookups using an in-memory mock, runs these two tests against a disposable database, and expects two assertion failures. Nothing vulnerable is written to disk or served over the network. Running the normal suite tests the actual fixed implementation.

## Why both scanners and tests?

A dependency scanner finds known advisories for package versions. Static analysis identifies certain unsafe coding patterns. Neither understands this application's ownership policy reliably. The two-user HTTP tests directly express and check that policy. A passing result is evidence for these cases, not proof covering every route or attack.

## Review checklist

- Entry points: login, create/history, read and delete. No upload or external URL fetching.
- Trust boundaries: unauthenticated browser, authenticated identity, database records.
- Main risks: cross-user access, CSRF, HTML injection, stored message exposure, brute-force login and dependency vulnerabilities.
- Implemented: owner-scoped queries, CSRF middleware, escaped templates, metadata-only persistence, framework password hashing and regression tests.
- Open before public hosting: login throttling, HTTPS/secure-cookie deployment settings, operational limits and production server. This lab is deliberately loopback-only.
