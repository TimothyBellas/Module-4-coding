from __future__ import annotations

import json

import requests


ENDPOINTS = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/users/1",
    "https://httpbin.org/get",
]

STUDENT_NAME = "Tim"


def matching_headers(headers: requests.structures.CaseInsensitiveDict, keyword: str) -> dict[str, str]:
    """Return headers whose names include *keyword*, ignoring case."""
    return {name: value for name, value in headers.items() if keyword in name.lower()}


def inspect_endpoint(url: str) -> None:
    """Request one URL and print a concise response-header summary."""
    print(f"\nGET {url}")
    print("-" * (len(url) + 4))

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"Request failed: {error}")
        return

    headers = response.headers
    caching_headers = {
        name: value
        for name, value in headers.items()
        if name.lower() in {"cache-control", "expires", "etag", "last-modified", "pragma", "age"}
    }
    rate_limit_headers = {
        name: value
        for name, value in headers.items()
        if "rate" in name.lower() or "limit" in name.lower()
    }

    print(f"Status: {response.status_code}")
    print(f"Content-Type: {headers.get('Content-Type', 'Not specified')}")
    print(f"Content-Length: {headers.get('Content-Length', 'Not specified')}")
    print(f"Caching headers present: {'Yes' if caching_headers else 'No'}")
    if caching_headers:
        print("  " + json.dumps(caching_headers))
    print(f"Rate-limiting headers: {json.dumps(rate_limit_headers) if rate_limit_headers else 'None'}")
    print(f"Total response headers: {len(headers)}")


def demonstrate_custom_headers() -> None:
    """POST JSON and custom headers to httpbin, which echoes the request."""
    url = "https://httpbin.org/post"
    payload = {"message": "Hello from the header inspector", "purpose": "header verification"}
    custom_headers = {
        "X-Student-Name": STUDENT_NAME,
        "X-Request-Purpose": "API header inspection exercise",
    }

    print(f"\nPOST {url}")
    print("-" * (len(url) + 5))
    try:
        response = requests.post(url, json=payload, headers=custom_headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"Request failed: {error}")
        return

    print("Echoed response:")
    print(json.dumps(response.json(), indent=2))


def main() -> None:
    for endpoint in ENDPOINTS:
        inspect_endpoint(endpoint)
    demonstrate_custom_headers()


if __name__ == "__main__":
    main()
