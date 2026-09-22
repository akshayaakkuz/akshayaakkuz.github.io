# Signal Security Lab — Python companion

A personal DevSecOps learning project extending the idea behind the existing browser-only Signal spam checker. Django serves an HTML frontend, authenticates users, analyzes synthetic messages, and stores private scan metadata in SQLite. This is an English rule-based baseline, not a trained ML model or a claim of production experience.

## Start without Docker

Use Python 3.12. From this folder:

```sh
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser --username alice
python manage.py runserver 127.0.0.1:8000 --noreload
```

Open http://127.0.0.1:8000 and sign in. Choose a unique practice password; no credentials are included. `createsuperuser` is used for convenient local account creation; there is no admin route and staff accounts cannot bypass scan ownership. A fresh secret is generated per server process, so sessions expire on restart. A persistent `DJANGO_SECRET_KEY` can be supplied through the environment; never commit it.

## Start with Docker

Install and start Docker Desktop, then from this folder:

```sh
docker compose build
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py createsuperuser --username alice
docker compose up
```

Open http://127.0.0.1:8000. Stop with Ctrl+C and `docker compose down`. The named volume retains your data. The Dockerfile is the packaging recipe, the image is the built package, a container is a running instance, and the volume stores the database between runs. The host port is bound to loopback. The container runs as a non-root user. Its Django development server is for local learning only.

## What to demonstrate

1. Submit `URGENT: enter your password immediately.` and view the explanation.
2. Create a second local account (`python manage.py createsuperuser --username bob`). In a separate browser session, sign in as Bob and request Alice's `/scans/1/` URL (use the actual result ID). Expect 404.
3. Run `python manage.py test scans --verbosity 2`. Positive owner-access tests and negative cross-user tests pass.
4. Run `python scripts/verify_regression.py`. Two deliberate test failures appear, followed by a PASS message. The script removes ownership checks only in memory against a temporary test database. The script itself succeeds only when the regression is detected.
5. Inspect the GitHub Actions run: tests, regression proof, static analysis, dependency audit, then container build/test/smoke test.

## Data and security decisions

Browser → Django forms/CSRF/authentication → heuristic analyzer → owner-scoped SQLite metadata → escaped HTML response.

- Raw messages reach the Python server in this version, but are not stored in the model or logged by application code. Use synthetic examples only. Scores and rule labels can still be sensitive.
- Authenticated users create, read and delete only their own results. Ownership is assigned from the session, never a client-supplied owner field. UUIDs alone would not replace authorization.
- Django handles password hashing, sessions, CSRF checks and parameterized queries. Templates escape text. Deletion requires POST and CSRF.
- A 5,000-character form limit and 32 KiB request-data limit constrain input. The application does not fetch links, open attachments or call AI services.
- Responses use `no-store`, frame denial and a restrictive content security policy. Inline CSS is allowed for this small interface; scripts are not.
- The Python detector uses a smaller set of rules than the JavaScript detector; their scores are not promised to match.

## CI and release boundary

The workflow is `.github/workflows/security-ci.yml`. It runs on pushes and pull requests with a read-only token, pinned action commits and no deployment credentials. Tests and scanners must pass before the container job starts. Audit-service outages also fail the gate; do not silently suppress scanner errors.

This demonstrates CI and a gate before packaging. It does **not** deploy the Python service or automatically enforce merge protection. GitHub Pages still hosts only the original static app. To enforce merges, configure a repository ruleset requiring the `verify` and `container` checks. Dependabot configuration takes effect after merging to the default branch.

Before public deployment: add shared login throttling, a production WSGI/ASGI server, explicit public hosts, managed secrets, HTTPS with secure cookies and tested proxy settings, backups/retention, quotas, container scanning, secret scanning and a deployment/rollback process. The base image uses a moving patch tag, and dependencies are version-pinned without artifact hashes; digest/hash locking is a further supply-chain improvement. SQLite and unlimited result accumulation are acceptable only for this small local lab. There is no self-service registration or password reset.

## Checks

```sh
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test scans
python scripts/verify_regression.py
python -m pip install bandit==1.9.4 pip-audit==2.10.1
python -m bandit -r config scans -x tests.py
python -m pip_audit -r requirements.txt --no-deps --disable-pip
```

Scanners do not establish that an application is vulnerability-free. See [the interview practice guide](INTERVIEW.md) and [the security case study](SECURITY-CASE.md).
