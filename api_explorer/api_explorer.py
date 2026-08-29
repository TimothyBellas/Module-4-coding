import requests


BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT_SECONDS = 10


def get_list(endpoint, *, params=None):
    """GET a list endpoint and print basic response information."""
    response = requests.get(
        f"{BASE_URL}{endpoint}", params=params, timeout=TIMEOUT_SECONDS
    )
    print(f"Status code: {response.status_code}")
    response.raise_for_status()

    items = response.json()
    print(f"Items returned: {len(items)}")
    return items


def main():
    print("\n=== All Users ===")
    users = get_list("/users")
    for user in users:
        print(f"- {user['name']} <{user['email']}>")

    print("\n=== Posts by User #3 ===")
    posts = get_list("/posts", params={"userId": 3})
    for post in posts:
        print(f"- Post #{post['id']}: {post['title']}")

    print("\n=== Comments on Post #1 ===")
    comments = get_list("/posts/1/comments")
    for comment in comments:
        print(f"- {comment['name']} ({comment['email']})")

    print("\n=== Create a New Post (Simulated) ===")
    new_post = {
        "title": "Learning REST APIs with Python",
        "body": "This post was created using the requests library.",
        "userId": 3,
    }
    response = requests.post(
        f"{BASE_URL}/posts", json=new_post, timeout=TIMEOUT_SECONDS
    )
    print(f"Status code: {response.status_code}")
    response.raise_for_status()
    print("Response JSON:")
    print(response.json())


if __name__ == "__main__":
    try:
        main()
    except requests.RequestException as error:
        print(f"API request failed: {error}")

