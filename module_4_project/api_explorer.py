"""Module 4 Project — Part 1: API Exploration.

Explore two public REST APIs and print useful, formatted response summaries.
Install the only third-party dependency with: pip install requests
"""

from collections.abc import Callable
from typing import Any

import requests


BASE_URLS = {
    "jsonplaceholder": "https://jsonplaceholder.typicode.com",
    "pokeapi": "https://pokeapi.co/api/v2",
}

TIMEOUT_SECONDS = 15

# Reusing one Session allows requests to share headers and HTTP connections.
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "module-4-api-explorer/1.0"})


def make_request(
    method: str,
    url: str,
    *,
    summary: Callable[[Any], None] | None = None,
    **kwargs: Any,
) -> requests.Response | None:
    """Send one HTTP request, report REST metadata, and handle failures safely."""

    # Preparing first reveals the complete URI, including encoded query parameters.
    prepared = requests.Request(method, url, **kwargs).prepare()
    print(f"\n{method.upper()} {prepared.url}")

    try:
        # A timeout prevents an unavailable API from making the program wait forever.
        response = SESSION.request(
            method, url, timeout=TIMEOUT_SECONDS, **kwargs
        )
    except requests.RequestException as error:
        # A network failure is different from an HTTP error: no response arrived.
        print(f"Request failed: {error}")
        return None

    # The status code reports the outcome; the reason supplies its readable label.
    print(f"Status: {response.status_code} {response.reason}")

    # Content-Type identifies the media type of the returned representation.
    print(f"Content-Type: {response.headers.get('Content-Type', 'not provided')}")

    # A 4xx/5xx status is handled as data so an HTTP error cannot crash the script.
    if not response.ok:
        try:
            error_data = response.json()
            print(f"Error summary: {error_data}")
        except requests.exceptions.JSONDecodeError:
            print(f"Error summary: {response.text[:160] or 'empty response body'}")
        return response

    if summary is not None:
        try:
            # Each callback extracts useful fields instead of dumping all JSON.
            summary(response.json())
        except (requests.exceptions.JSONDecodeError, KeyError, TypeError, IndexError) as error:
            print(f"Could not summarize the response: {error}")

    return response


# ============================================================
# API 1: JSONPlaceholder
# Documentation: https://jsonplaceholder.typicode.com/guide/
# ============================================================


def explore_jsonplaceholder() -> None:
    print("\n=== API 1: JSONPlaceholder ===")
    base_url = BASE_URLS["jsonplaceholder"]

    # GET /users addresses a collection resource: the complete user collection.
    make_request(
        "GET",
        f"{base_url}/users",
        summary=lambda users: print(
            "Users (name — email):\n  "
            + "\n  ".join(f"{user['name']} — {user['email']}" for user in users)
        ),
    )

    # A resource URI containing /1 identifies one specific user representation.
    make_request(
        "GET",
        f"{base_url}/users/1",
        summary=lambda user: print(
            f"User: {user['name']} | {user['email']} | {user['address']['city']}"
        ),
    )

    def summarize_posts(posts: list[dict[str, Any]]) -> None:
        # Collection responses are lists, so summarize their size and first item.
        first_title = posts[0]["title"] if posts else "No posts returned"
        print(f"Posts returned: {len(posts)} | First title: {first_title}")

    # Query parameters filter the posts collection without changing the endpoint.
    make_request(
        "GET",
        f"{base_url}/posts",
        params={"userId": 3},
        summary=summarize_posts,
    )

    # This nested resource represents posts belonging to user 1.
    make_request(
        "GET",
        f"{base_url}/users/1/posts",
        summary=summarize_posts,
    )

    def summarize_created_post(post: dict[str, Any]) -> None:
        print(
            f"Created representation: id={post['id']}, userId={post['userId']}, "
            f"title={post['title']!r}"
        )

    # POST supplies the project's required non-GET request. Status 201 means the
    # server accepted the representation as a newly created resource.
    make_request(
        "POST",
        f"{base_url}/posts",
        json={
            "title": "Learning REST APIs",
            "body": "Created by the Module 4 API Explorer.",
            "userId": 1,
        },
        summary=summarize_created_post,
    )

    # A nonexistent resource returns 404; make_request reports it and continues.
    make_request("GET", f"{base_url}/users/999999")


# ============================================================
# API 2: PokeAPI
# Documentation: https://pokeapi.co/docs/v2
# ============================================================


def explore_pokeapi() -> None:
    print("\n=== API 2: PokeAPI ===")
    base_url = BASE_URLS["pokeapi"]

    # PokeAPI is consumption-only: it supports GET but not POST, PUT, or DELETE.
    # Therefore, JSONPlaceholder's POST above fulfills the non-GET requirement.
    first_type_url: str | None = None
    first_ability_url: str | None = None
    first_move_url: str | None = None
    species_url: str | None = None

    def summarize_pokemon(pokemon: dict[str, Any]) -> None:
        nonlocal first_ability_url, first_move_url, first_type_url, species_url
        abilities = ", ".join(item["ability"]["name"] for item in pokemon["abilities"])
        types = ", ".join(item["type"]["name"] for item in pokemon["types"])

        # Save related-resource links from the response for the next four GETs.
        first_type_url = pokemon["types"][0]["type"]["url"]
        first_ability_url = pokemon["abilities"][0]["ability"]["url"]
        first_move_url = pokemon["moves"][0]["move"]["url"]
        species_url = pokemon["species"]["url"]
        print(
            f"Pokémon: {pokemon['name'].title()} | Height: {pokemon['height']} | "
            f"Weight: {pokemon['weight']} | Types: {types} | Abilities: {abilities}"
        )

    # Top-level keys include abilities, height, id, name, sprites, stats, types,
    # and weight; many values contain links to related REST resources.
    make_request("GET", f"{base_url}/pokemon/25", summary=summarize_pokemon)

    if first_type_url:
        # Following the URL supplied by the API demonstrates HATEOAS-style navigation.
        make_request(
            "GET",
            first_type_url,
            summary=lambda pokemon_type: print(
                f"Type: {pokemon_type['name']} | First five Pokémon: "
                + ", ".join(
                    entry["pokemon"]["name"]
                    for entry in pokemon_type["pokemon"][:5]
                )
            ),
        )
    else:
        # Dependent calls are skipped safely if the original Pokémon GET failed.
        print("\nSkipped the related type request because the Pokémon request failed.")

    if first_ability_url:
        make_request(
            "GET",
            first_ability_url,
            summary=lambda ability: print(
                f"Ability: {ability['name']} | Pokémon with this ability: "
                f"{len(ability['pokemon'])} | First five: "
                + ", ".join(
                    entry["pokemon"]["name"] for entry in ability["pokemon"][:5]
                )
            ),
        )
    else:
        print("\nSkipped the related ability request because the Pokémon request failed.")

    if species_url:
        make_request(
            "GET",
            species_url,
            summary=lambda species: print(
                f"Species: {species['name']} | Capture rate: {species['capture_rate']} | "
                f"Base happiness: {species['base_happiness']} | "
                f"Generation: {species['generation']['name']}"
            ),
        )
    else:
        print("\nSkipped the species request because the Pokémon request failed.")

    if first_move_url:
        # This linked resource describes the first move in Pikachu's move collection.
        make_request(
            "GET",
            first_move_url,
            summary=lambda move: print(
                f"Move: {move['name']} | Type: {move['type']['name']} | "
                f"Power: {move['power']} | Accuracy: {move['accuracy']} | "
                f"PP: {move['pp']}"
            ),
        )
    else:
        print("\nSkipped the move request because the Pokémon request failed.")


if __name__ == "__main__":
    # This guard runs the explorations only when this file is executed directly.
    explore_jsonplaceholder()
    explore_pokeapi()
    print("\n=== Exploration complete! ===")
