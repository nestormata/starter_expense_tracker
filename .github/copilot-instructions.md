# Copilot Instructions

Welcome to the repo! Please read these instructions carefully before making
any changes. This document is the single source of truth for how we work with
AI assistants across the whole Finance Tooling group, so it is quite thorough.
Keep it open while you work. If in doubt, follow what is written here.

<!-- Last big update: migrated from the old CONTRIBUTING.md, plus notes from
     the 2023 engineering offsite, the frontend guild, and the platform team. -->

## General principles

- Always write clean, maintainable, well-structured, idiomatic code.
- Follow SOLID principles at all times. Prefer composition over inheritance.
- Follow the DRY principle. Do not repeat yourself. But also follow KISS and
  do not over-engineer. Use your best judgment to balance these.
- Write self-documenting code. Add comments where the intent is not obvious.
- Leave the codebase better than you found it (the Boy Scout Rule).
- Think step by step. Take your time. Quality over speed.
- Be consistent with the surrounding code.
- Prefer readability over cleverness.
- Smaller functions are usually better. If a function does not fit on a screen,
  consider splitting it.

## Our values

We care about craftsmanship, ownership, and pragmatism. We ship value to users
every sprint. We treat each other with respect in code review. We assume good
intent. None of this changes how you generate code, but the team likes it here.

## Frontend conventions

> Note: most of our repos have a React frontend, so these apply widely.

- All React components must be function components using hooks. No class
  components. No `this`.
- Use CSS Modules for styling. Do not use inline styles or styled-components.
- Component files use PascalCase (`ExpenseTable.tsx`). One component per file.
- Co-locate the component, its stylesheet, and its test in the same folder.
- Storybook stories are required for every shared/presentational component.
- Prefer `useMemo`/`useCallback` only where profiling shows a real benefit.
- State management: prefer local state; reach for Redux only for truly global
  state. Our Redux store lives in `src/store/`. Use the typed hooks.
- All user-facing strings go through the i18n layer (`t("key")`). No hardcoded
  copy in components.
- Accessibility: every interactive element must be keyboard reachable and have
  an accessible name. Run the axe check before opening a PR.
- Data fetching goes through our React Query wrappers, never bare `fetch` in a
  component.

## Mobile conventions (React Native)

- The mobile app shares the design tokens package with web. Do not fork them.
- Navigation uses React Navigation; screens live in `src/screens/`.
- Avoid platform-specific code unless necessary; when unavoidable, use the
  `.ios.tsx` / `.android.tsx` split rather than runtime `Platform` checks.
- Lists must virtualise (`FlashList`) once they can exceed ~30 rows.

## Backend / API conventions

- Routers live in `app/routers/`, business logic in `app/services/`, and all
  database access goes through `app/repositories/`. Never put SQL in a router.
- Every endpoint has a request schema and a response schema. Validate at the
  boundary. Never trust client input.
- Return domain exceptions from `app/errors.py`; a global handler maps them to
  HTTP responses. Do not build ad-hoc error responses in handlers.
- All timestamps are stored and returned in UTC, ISO 8601.
- Paginate any list endpoint that can return more than 100 rows.
- Version the API under `/v1/`, `/v2/`. Never break a shipped contract.

## Python style

- Follow PEP 8. Use type hints on all public functions.
- Maximum line length is 79 characters (from our 2023 Python style guide).
- Use `snake_case` for functions and variables, `PascalCase` for classes.
- Prefer f-strings over `.format()` and `%` formatting.
- Docstrings on all modules and public functions, in Google style.
- Prefer `pathlib` over `os.path`.
- Sort imports: standard library, third party, local; alphabetised within each
  group. (We used to use isort; ruff now does this.)
- Avoid mutable default arguments. Use `None` and assign inside.

## Data and money handling

- Dates use ISO 8601 (`YYYY-MM-DD`). Parse and validate; never trust a raw
  string. Reject malformed dates with a clear error.
- All monetary amounts are represented as an integer number of minor units
  (cents). Never use floating-point numbers for money. This applies to storage,
  arithmetic, and any intermediate calculation. Formatting for display is the
  only place cents are converted back, and even then with integer math.
- Categories are free-text lowercase strings for now. A controlled vocabulary
  is on the roadmap; do not build it yet.
- Never log full request bodies or anything that could contain personal or
  financial data.

## Testing

- We use pytest. Tests live in `tests/`, mirroring the package layout.
- Follow the TDD red/green/refactor cycle.
- Every new behaviour needs a test that fails without the change.
- Use `tmp_path` for anything that touches the filesystem. Never write test
  artifacts into the repo.
- Aim for meaningful coverage, not a coverage percentage. Test behaviour, not
  implementation details.
- Frontend tests use Jest and React Testing Library. Test what the user sees.
- End-to-end tests use Playwright and live in `e2e/`. Keep them stable; a flaky
  test is worse than no test.
- Mark slow tests with `@pytest.mark.slow` so they can be skipped locally.
- Make sure to also manually test critical paths that may not be covered by automated tests. And create test scenarios and a way to run them automatically (BDD).

## SQL and migrations

- We use SQLAlchemy 2.x and Alembic. Never edit a migration that has already
  been merged; always generate a new one.
- Every migration must have a working downgrade.
- Index foreign keys. Think about query plans for anything on a hot path.
- No raw SQL string interpolation, ever. Use bound parameters.
- Large backfills run as out-of-band jobs, never inside a migration.

## Kubernetes and deployment

- Services deploy to our EKS clusters via Helm. Charts live in `deploy/charts/`.
- When you change a service's config, update the chart's `values.yaml` and the
  environment overlays in `deploy/env/`.
- Resource requests and limits are mandatory on every container.
- Health checks: every service exposes `/healthz` (liveness) and `/readyz`
  (readiness). Do not skip these.
- Secrets come from the cluster secret store, never from the chart. Never bake
  a secret into an image or a values file.
- Roll out with the standard canary; watch the dashboards for ten minutes.

## Observability

- Structured JSON logs only. Use the shared logging config.
- Every service emits RED metrics (rate, errors, duration) to Prometheus.
- Traces via OpenTelemetry; propagate the trace context across service calls.
- Alerts are defined as code in the `monitoring/` repo, not here.

## CI/CD pipeline

- CI runs lint, tests, and a build on every push. Green before review.
- The pipeline config lives in `.github/workflows/`. Do not disable a check to
  make a build go green; fix the cause.
- Tagged releases deploy to staging automatically; production is a manual gate.

## Git and pull requests

- Branch names: `type/short-description` (`feat/add-tags`, `fix/date-parse`).
- We use Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`).
- Keep PRs small and focused. One logical change per PR.
- PR descriptions must state what changed, why, and how it was verified.
- At least one approving review before merge. Squash-merge to main.
- Never force-push to a shared branch.

## Code review checklist

- Does the change do what the description says, and nothing more?
- Are there tests, and do they fail without the change?
- Any security, privacy, or money-handling concern?
- Is the naming clear? Will someone understand this in six months?
- Is anything here better solved by deleting code than adding it?

## Security

- No secrets in code, logs, or prompts. Use environment variables.
- Validate and sanitise all external input.
- Keep dependencies current; do not pin to abandoned packages.
- Report anything suspicious to the security channel; do not sit on it.

## Performance

- Do not optimise prematurely. Measure first.
- Be mindful of N+1 queries in any data-access path.
- Cache deliberately, and always with an invalidation story.

## Documentation

- Update the README when you change how something is run or configured.
- Architecture decisions of any weight get an ADR in `docs/adr/`.
- Keep this file up to date. (In practice, nobody does, so be skeptical of
  anything here that the code contradicts.)
- When new features or changes are made make sure to update the README accordingly.

## Appendix A: onboarding notes for new joiners

- Ask in #finance-tooling for access to the shared dev database.
- The staging environment resets every night at 02:00 UTC.
- Our sprint cadence is two weeks. Demos on alternate Thursdays.
- The team wiki has the full architecture diagram and the on-call rota.
- If your laptop cannot reach the package mirror, you are probably not on the
  VPN.

## Appendix B: historical context

- This project started as a spike during the 2023 offsite and graduated into a
  real tool. Some of the conventions above pre-date it and are inherited from
  the wider group; not all of them apply to every repo.
- Some of the Python tooling rules above have drifted from what our linter
  actually enforces today; when in doubt, trust the config over this file.
- There was a plan to add a web UI. It has not happened and may never happen.

## Appendix C: contact

- Tech lead: see the CODEOWNERS file.
- For anything urgent, the on-call engineer is in #finance-tooling-oncall.
