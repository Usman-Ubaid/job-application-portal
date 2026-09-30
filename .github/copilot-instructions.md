# Copilot Instructions for Job Application Portal

## Project Overview
Full-stack job portal. Backend: Django + Django REST Framework (`backend/`).
Frontend: Next.js App Router + TypeScript (`frontend/`).
Two user roles: `SK` (seeker) and `EP` (employer).

## Backend Conventions (`backend/`)

### Environment & Tooling
- Dependency management: Poetry, not pip. Add packages with `poetry add <package>` (or `--group dev` for dev-only tools). Never suggest editing `requirements.txt` — it doesn't exist.
- Formatting: Black. Assume format-on-save is configured; don't manually reformat code to a different style.
- Run commands via the `Makefile` where a target exists (`make run`, `make migrate`, `make test`) instead of raw `python manage.py` commands.

### Django Structure
- One app per domain: `users`, `jobs`, `applications`, `companies`, `common`.
- Shared permission classes (`IsEmployer`, `IsOwner`, `IsSeeker`) live in `common/permissions.py` and are imported from there — never duplicate permission logic inside an individual app.
- Custom user model at `users.User` with `role` field (`SEEKER`/`EMPLOYER` constants, not raw strings).
- Views are class-based (`APIView`), not function-based. Permission checks go through `get_permissions()`, not manual `if` checks inside methods.
- Serializers: `ModelSerializer` when directly backed by a model, plain `Serializer` only for non-model input (e.g. login credentials).
- Ownership/role logic belongs in permission classes and `has_object_permission`, not scattered in views.

### Auth
- JWT via `djangorestframework-simplejwt`, but tokens are delivered in **HTTP-only cookies**, not the response body. Never suggest returning tokens in JSON or storing them in localStorage.
- Authentication class: `users.authentication.CookieJWTAuthentication` (reads `access_token` cookie).
- Refresh tokens rotate and are blacklisted on use (`ROTATE_REFRESH_TOKENS`, `BLACKLIST_AFTER_ROTATION`). Logout blacklists the current refresh token and clears both cookies.

### Migrations
- When adding a required field to a table with existing rows, do NOT delete existing data to make the migration pass. Either make the field nullable and enforce the constraint at the serializer level, or write a proper data migration (`RunPython`) with a reverse function.
- Prefer nullable-at-DB-level + validation-at-serializer-level for new required fields on existing models, unless explicitly told to backfill.

### Testing
- `pytest-django`, not Django's built-in `TestCase`/`unittest` style.
- Test files live in `<app>/tests/` (a package with `__init__.py`), never a single `tests.py`.
- Use `pytestmark = pytest.mark.django_db` at module level instead of decorating every test function individually.
- Use fixtures (`create_user`, `create_job`, etc.) that return a factory function with sensible defaults, overridable via `**kwargs`. Follow the existing fixture pattern in each app's test folder rather than inventing a new one.
- Use `APIClient` + `force_authenticate` for permission/logic tests where the cookie mechanism itself isn't under test. Use the real `/api/auth/login/` flow only when the cookie/token behavior itself is being tested.
- File upload tests use `SimpleUploadedFile`; `MEDIA_ROOT` is overridden to a temp dir via `conftest.py` — don't let test-generated files land in the real `media/` folder.

## Frontend Conventions (`frontend/`)

### Environment & Tooling
- Next.js **App Router** (`src/app/`), not Pages Router. Never create or suggest a `pages/` directory.
- TypeScript strict — always type function params, especially event handlers (e.g. `React.FormEvent<HTMLFormElement>`).
- Formatting: Prettier (`semi: true`). Don't hand-format differently.
- Styling: Tailwind CSS utility classes directly in JSX. No CSS Modules, styled-components, or inline `style={}` unless there's a specific reason.
- Path alias `@/*` maps to `src/*`.

### Component Rules
- Server Components are the default. Only add `"use client"` when a component actually needs hooks (`useState`, `useEffect`, `useContext`), event handlers, or browser-only APIs.
- JSX attributes are camelCase: `className` not `class`, `htmlFor` not `for`, `onClick` not `onclick`.
- Don't extract a shared component (`Button`, `Input`, etc.) until a second place actually needs it — avoid speculative abstraction.

### API Communication
- All backend calls go through the shared `axiosInstance` in `src/lib/axios.ts` (`baseURL: http://localhost:8000/api`, `withCredentials: true`). Never call `fetch` or a fresh `axios.create()` directly in a component.
- Use `localhost` consistently (not `127.0.0.1`) on both frontend and backend URLs — required for cookies to be treated as same-site in development.
- Auth state is read via the `useAuth()` hook (`src/context/AuthContext.tsx`), not by calling `/api/auth/user/` directly from components.
- Server state (jobs, applications, companies) should go through TanStack Query, not raw `useEffect` + `useState` fetching, once those features are built.

### Auth Flow
- `login()`/`logout()` in `AuthContext` do NOT catch their own errors — the calling component (e.g. the login page) is responsible for try/catch, loading state, and displaying errors.
- Session check on mount treats a `401` from `/api/auth/user/` as "no user logged in", not an error to surface to the user.

## General
- Never hardcode secrets, API keys, or credentials — they belong in `.env` (backend) or `.env.local` (frontend), both gitignored.
- Prefer explaining trade-offs and asking before introducing a new dependency, rather than silently adding one.