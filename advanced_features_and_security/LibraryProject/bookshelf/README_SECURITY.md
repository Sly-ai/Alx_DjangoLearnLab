# Security measures implemented — LibraryProject (bookshelf)

This document explains applied security hardening and how to test it.

## settings.py changes
- `DEBUG = False` (production). Never run production with DEBUG=True.
- `ALLOWED_HOSTS` must be populated for production.
- `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True` — cookies only over HTTPS.
- `SESSION_COOKIE_HTTPONLY = True` — reduces JS access to session cookie.
- `SECURE_CONTENT_TYPE_NOSNIFF = True` and `SECURE_BROWSER_XSS_FILTER = True` — browser-side protections.
- `X_FRAME_OPTIONS = "DENY"` — prevents clickjacking.
- `SECURE_HSTS_*` and `SECURE_SSL_REDIRECT` — enable strict transport rules (activate with caution during rollout).

## CSRF protection
- All forms include `{% csrf_token %}` (`form_example.html` and `book_list.html`).
- Deletion endpoints are POST-only and protected by CSRF middleware.

## Input validation & SQL injection prevention
- All user inputs are validated through `bookshelf/forms.py` using Django forms (`BookForm`, `BookSearchForm`).
- Database operations use the Django ORM (e.g. `filter(title__icontains=q)`), which parameterizes queries automatically and prevents SQL injection.

## Content Security Policy (CSP)
- A small middleware `LibraryProject/middleware.py` sets `Content-Security-Policy` header from `CSP_POLICY` in settings.
- Start with a strict policy (`'self'`) and only allow external domains explicitly when needed.

## Views
- Protected by `@login_required` and `@permission_required(...)`.
- Use `@require_http_methods` to restrict allowed HTTP methods.
- Use `transaction.atomic()` for writes to ensure consistency.

## Testing
Manual tests to perform:
1. Verify forms reject invalid inputs (empty title, future published date, excessively long fields).
2. Log in as a user without `can_create` and confirm you cannot access `book_create`.
3. Attempt CSRF attack: submit a POST with a missing/invalid CSRF token — should be blocked.
4. Attempt XSS: create a book with `<script>alert(1)</script>` in description; confirm page escapes output (no script execution).
5. Check CSP header is present and matches `CSP_POLICY`.
6. Confirm cookies have `Secure` and (for session) `HttpOnly` flags (check via browser devtools under Application → Cookies).

## Notes & deployment
- SSL/TLS is mandatory in production when `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` are True. Ensure HTTPS and reverse proxy correctly set `X-Forwarded-Proto` if used.
- Start with smaller `SECURE_HSTS_SECONDS` values during rollout; only increase after verifying HTTPS works for all hosts.
