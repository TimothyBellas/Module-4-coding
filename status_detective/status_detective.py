import requests


BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 10


def status_category(status_code):
    """Return a readable category based on the HTTP status-code range."""
    if 200 <= status_code < 300:
        return "Success"
    if 400 <= status_code < 500:
        return "Client Error"
    if 500 <= status_code < 600:
        return "Server Error"
    if 300 <= status_code < 400:
        return "Redirection"
    return "Informational"


def describe_response(method, response):
    """Create a short description using the method, status, and response data."""
    status = response.status_code

    if status == 404:
        return "Request failed — resource or endpoint not found"
    if 400 <= status < 500:
        return "Request failed — check the URI or request data"
    if 500 <= status < 600:
        return "Request failed — the server encountered an error"

    if 200 <= status < 300:
        if method == "POST":
            return "Request succeeded — resource created"
        if method == "DELETE":
            return "Request succeeded — resource deleted"

        # A successful GET may return either one object or a list of objects.
        try:
            data = response.json()
            if isinstance(data, list):
                return f"Request succeeded — collection returned ({len(data)} items)"
        except ValueError:
            # If the body is not JSON, give a general success description.
            pass
        return "Request succeeded — resource returned"

    return "Request completed — inspect the response for details"


def request_report(method, url, json_data=None):
    """Make any HTTP request and return a formatted status report.

    The URL may be a complete URL or a path such as ``/posts/1``.
    ``json_data`` is used as the request body for methods such as POST.
    """
    method = method.upper()

    # Add the JSONPlaceholder base URL when only an endpoint path is provided.
    full_url = url if url.startswith(("http://", "https://")) else f"{BASE_URL}{url}"

    try:
        response = requests.request(
            method,
            full_url,
            json=json_data,
            timeout=TIMEOUT,
        )
    except requests.RequestException as error:
        # Network errors do not have an HTTP status code.
        return (
            f"{method} {url}\n"
            "  Status: N/A (Request Error)\n"
            f"  Description: Request could not be completed — {error}"
        )

    category = status_category(response.status_code)
    description = describe_response(method, response)

    return (
        f"{method} {url}\n"
        f"  Status: {response.status_code} ({category})\n"
        f"  Description: {description}"
    )


def main():
    """Run all six required API diagnostics in order."""
    tests = [
        ("GET", "/posts/1", None),
        ("GET", "/posts/99999", None),
        (
            "POST",
            "/posts",
            {
                "title": "Status Detective Test",
                "body": "Testing a valid POST request.",
                "userId": 1,
            },
        ),
        ("DELETE", "/posts/1", None),
        ("GET", "/invalidendpoint", None),
        ("GET", "/users/1/todos", None),
    ]

    # Unpack each test and print a blank line between reports.
    for method, url, json_data in tests:
        print(request_report(method, url, json_data))
        print()


if __name__ == "__main__":
    main()

