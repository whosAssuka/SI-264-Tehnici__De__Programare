import requests
SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    if path.startswith("/"):
        return f"https://{host}{path}"
    return f"https://{host}/{path}"


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        r = requests.get(url, timeout=5)
        return {
            "status": r.status_code,
            "content_type": r.headers.get("Content-Type", "unknown"),
            "length": len(r.content),
            "server": r.headers.get("Server", "unknown")
        }
    except Exception as e:
        return {"status": None, "error": str(e)}


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results = []
    success = 0
    failed = 0
    
    for site in SITES:
        res = check_site(site)
        if res["status"] == 200:
            results.append((site, res))
            success += 1
        else:
            failed += 1
            
    for site, info in results:
        print(f"{site} -> {info['status']}, {info['length']} octeți")
        
    print(f"Reușite: {success} Eșuate: {failed}")


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        r = requests.get(url, timeout=5)
        response_headers = {k.lower(): v for k, v in r.headers.items()}
        
        present = []
        missing = []
        
        for h in SECURITY_HEADERS:
            if h.lower() in response_headers:
                present.append(h)
            else:
                missing.append(h)
                
        score = int((len(present) / len(SECURITY_HEADERS)) * 100)
        
        return {
            "present": present,
            "missing": missing,
            "score": score
        }
    except:
        return {"status": None}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    last_status = None
    for i in range(1, attempts + 1):
        try:
            r = requests.get(url, timeout=5)
            last_status = r.status_code
            if r.status_code < 500:
                return {"status": r.status_code, "attempts": i}
        except:
            last_status = None
            
    return {"status": last_status, "attempts": attempts}