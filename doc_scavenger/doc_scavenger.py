import requests


SEARCH_URL = "https://api.github.com/search/repositories"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2026-03-10",
    "User-Agent": "doc-scavenger-example",
}

PARAMS = {
    "q": "org:google",
    "sort": "stars",
    "order": "desc",
    "per_page": 3,
}


def main() -> None:
    response = requests.get(
        SEARCH_URL,
        headers=HEADERS,
        params=PARAMS,
        timeout=10,
    )

    # Raise an exception if GitHub returns an unsuccessful HTTP status.
    response.raise_for_status()

    data = response.json()

    print("Google's 3 most-starred repositories:")
    print()

    for repo in data["items"]:
        print(f"Name: {repo['name']}")
        print(f"Description: {repo['description'] or 'No description'}")
        print(f"Stars: {repo['stargazers_count']}")
        print(f"Primary language: {repo['language'] or 'Not specified'}")
        print()

    remaining = response.headers.get("X-RateLimit-Remaining", "Unknown")
    print(f"Remaining search rate limit: {remaining}")


if __name__ == "__main__":
    main()
