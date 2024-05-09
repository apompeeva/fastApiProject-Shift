import httpx


def get_cookies(set_cookie_header: str) -> httpx.Cookies:
    cookies = httpx.Cookies()
    entries = set_cookie_header.split(", ")
    for entry in entries:
        chunks = entry.split("; ")
        chunk = next(c for c in chunks)
        k, v = chunk.split("=")
        cookies.set(k, v)
    return cookies
