# Django HTTPS & Security Review

## Settings Applied
- **SECURE_SSL_REDIRECT = True** → forces all traffic over HTTPS.
- **SECURE_HSTS_SECONDS = 31536000** → enables HSTS for 1 year.
- **SECURE_HSTS_INCLUDE_SUBDOMAINS = True** → protects subdomains.
- **SECURE_HSTS_PRELOAD = True** → allows inclusion in browser preload lists.
- **SESSION_COOKIE_SECURE = True** → cookies only over HTTPS.
- **CSRF_COOKIE_SECURE = True** → CSRF cookies only over HTTPS.
- **X_FRAME_OPTIONS = "DENY"** → prevents clickjacking.
- **SECURE_CONTENT_TYPE_NOSNIFF = True** → stops MIME-sniffing.
- **SECURE_BROWSER_XSS_FILTER = True** → enables browser XSS filter.

## Deployment
- Configured **Nginx** to serve HTTPS with Let’s Encrypt SSL certificates.
- Redirects HTTP traffic to HTTPS.
- HSTS headers added at the web server level for redundancy.

## Potential Improvements
- Enable Content Security Policy (CSP) for stricter XSS defense.
- Rotate SSL certificates automatically with certbot renew.
- Add monitoring for HTTPS misconfigurations.
