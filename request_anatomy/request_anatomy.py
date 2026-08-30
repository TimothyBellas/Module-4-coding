from __future__ import annotations

import json
import http.client
import time
from typing import Any, Mapping
from urllib.parse import urlsplit

BASE_URL = "https://jsonplaceholder.typicode.com"
SEPARATOR = "=" * 80


def format_body(body: Any) -> str:
    """Return a readable representation of an HTTP request or response body."""
    if body is None or body == b"" or body == "":
        return "(none)"

    if isinstance(body, bytes):
        body = body.decode("utf-8", errors="replace")

    if isinstance(body, str):
        try:
            return json.dumps(json.loads(body), indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            return body

    return str(body)


def print_headers(headers: Mapping[str, str]) -> None:
    """Print every header in a mapping."""
    if not headers:
        print("(none)")
        return

    for name, value in headers.items():
        print(f"{name}: {value}")


def perform_and_display(
    number: int,
    label: str,
    method: str,
    url: str,
    json_body: dict[str, Any] | None = None,
) -> None:
    """Build, send, and print one HTTP transaction."""
    parsed_url = urlsplit(url)
    path = parsed_url.path or "/"
    if parsed_url.query:
        path = f"{path}?{parsed_url.query}"

    body = None
    if json_body is not None:
        body = json.dumps(json_body).encode("utf-8")

    # Supplying these explicitly makes the displayed mapping match the headers
    # sent by http.client, rather than hiding automatically generated values.
    request_headers = {
        "Host": parsed_url.netloc,
        "User-Agent": "request-anatomy/1.0 (Python standard library)",
        "Accept": "application/json",
        "Accept-Encoding": "identity",
    }
    if body is not None:
        request_headers["Content-Type"] = "application/json; charset=utf-8"
        request_headers["Content-Length"] = str(len(body))

    print(f"\n{SEPARATOR}")
    print(f"TRANSACTION {number}: {label}")
    print(SEPARATOR)
    print(f"Method: {method}")
    print(f"URL:    {url}")

    print("\nREQUEST HEADERS")
    print("-" * 80)
    print_headers(request_headers)

    print("\nREQUEST BODY")
    print("-" * 80)
    print(format_body(body))

    connection_class = (
        http.client.HTTPSConnection
        if parsed_url.scheme == "https"
        else http.client.HTTPConnection
    )
    connection = connection_class(parsed_url.netloc, timeout=15)
    started_at = time.perf_counter()
    try:
        connection.request(method, path, body=body, headers=request_headers)
        response = connection.getresponse()
        response_body = response.read()
        elapsed_ms = (time.perf_counter() - started_at) * 1000
    except (OSError, http.client.HTTPException) as exc:
        print("\nRESPONSE")
        print("-" * 80)
        print(f"Request failed: {exc}")
        return
    finally:
        connection.close()

    print("\nRESPONSE STATUS")
    print("-" * 80)
    print(f"Status: {response.status} {response.reason}")

    print("\nKEY RESPONSE HEADERS")
    print("-" * 80)
    for header_name in ("Content-Type", "Content-Length"):
        value = response.getheader(header_name, "(not provided by server)")
        print(f"{header_name}: {value}")

    print("\nRESPONSE BODY")
    print("-" * 80)
    charset = response.headers.get_content_charset("utf-8")
    print(format_body(response_body.decode(charset, errors="replace")))

    print("\nTIMING")
    print("-" * 80)
    print(f"Elapsed: {elapsed_ms:.2f} ms")


def main() -> None:
    """Run the GET, POST, and PATCH transactions."""
    perform_and_display(
        1,
        "GET a specific user",
        "GET",
        f"{BASE_URL}/users/1",
    )

    perform_and_display(
        2,
        "POST a new post",
        "POST",
        f"{BASE_URL}/posts",
        json_body={
            "title": "Learning HTTP request anatomy",
            "body": "This post was created by request_anatomy.py.",
            "userId": 1,
        },
    )

    perform_and_display(
        3,
        "PATCH a post title",
        "PATCH",
        f"{BASE_URL}/posts/1",
        json_body={"title": "Updated title from request_anatomy.py"},
    )


if __name__ == "__main__":
    main()
