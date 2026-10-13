from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check

print("--- Partea 1: build_url si is_https ---")
print("build_url fara slash:", build_url("example.com", "login"))
print("build_url cu slash:", build_url("example.com", "/login"))
print("is_https valid:", is_https("https://example.com"))
print("is_https invalid:", is_https("http://example.com"))
print()

print("--- Partea 2: show_response ---")
try:
    show_response("https://example.com")
except Exception as e:
    print("Eroare la conexiune.")
print()

print("--- Partea 3: check_site ---")
print("check_site valid:", check_site("https://example.com"))
print("check_site invalid:", check_site("http://this-site-does-not-exist.invalid"))
print()

print("--- Partea 4: scan_sites ---")
scan_sites()
print()

print("--- Partea 5: check_headers ---")
print("check_headers (prezente/lipsa):", check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print("check_headers (invalid):", check_headers("http://this-site-does-not-exist.invalid"))
print()

print("--- Partea 6: retry_check ---")
print("retry_check (status 200):", retry_check("https://httpbin.org/status/200"))
print("retry_check (status 404):", retry_check("https://httpbin.org/status/404"))
print("retry_check (status 500 - max attempts):", retry_check("https://httpbin.org/status/500"))
print("retry_check (status 500 - 2 attempts):", retry_check("https://httpbin.org/status/500", attempts=2))
print("retry_check (site invalid):", retry_check("http://this-site-does-not-exist.invalid"))
print()