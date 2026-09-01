API Explorer Documentation

This project uses two public REST APIs that require no authentication. The
companion script is api_explorer.py; it sends eleven requests and summarizes each response instead of
printing full JSON payloads.

1. JSONPlaceholder

Base URL: https://jsonplaceholder.typicode.com

Authentication: None

Method

Path

Description

Example response shape

GET

/users

Retrieve the user collection

[{"id": 1, "name": "...", "email": "...", "address": {...}}, ...]

GET

/users/1

Retrieve one specific user

{"id": 1, "name": "...", "email": "...", "address": {...}}

GET

/posts?userId=3

Filter the posts collection by user ID

[{"userId": 3, "id": 21, "title": "...", "body": "..."}, ...]

GET

/users/1/posts

Retrieve user 1's nested posts collection

[{"userId": 1, "id": 1, "title": "...", "body": "..."}, ...]

POST

/posts

Simulate creation of a post

{"title": "...", "body": "...", "userId": 1, "id": 101}

The script also requests GET /users/999999 to verify that a 404 Not Found
response is handled without stopping the program.

Rate limits observed: No rate-limit headers were returned during this small
test. JSONPlaceholder's public guide does not publish a numeric quota for these
example requests, so clients should still avoid rapid or excessive traffic.

Surprise / limitation: The write endpoints are simulated. A successful POST
returns 201 Created and an ID, but JSONPlaceholder does not permanently save
the new resource.

2. PokeAPI

Base URL: https://pokeapi.co/api/v2

Authentication: None

Supported method: GET only; PokeAPI is consumption-only

Method

Path

Description

Example response shape

GET

/pokemon/25

Retrieve Pikachu by numeric ID

{"id": 25, "name": "pikachu", "height": 4, "weight": 60, "abilities": [...], "types": [...]}

GET

/type/13/

Follow Pikachu's first type link and retrieve Electric-type details

{"id": 13, "name": "electric", "pokemon": [{"pokemon": {"name": "...", "url": "..."}}, ...]}

GET

/ability/9/

Follow Pikachu's first ability link and retrieve Static ability details

{"id": 9, "name": "static", "pokemon": [{"pokemon": {"name": "...", "url": "..."}}, ...]}

GET

/pokemon-species/25/

Follow Pikachu's species link and retrieve species metadata

{"id": 25, "name": "pikachu", "capture_rate": 190, "base_happiness": 70, "generation": {...}}

GET

/move/5/

Follow Pikachu's first move link and retrieve move details

{"id": 5, "name": "mega-punch", "accuracy": 85, "power": 80, "pp": 20, "type": {...}}

Rate limits observed: No numeric rate-limit headers were returned during the
test. PokeAPI describes its service as open and states that caching is used;
responsible clients should cache repeated requests and avoid abusive traffic.

Surprise / limitation: PokeAPI does not support POST, PUT, or DELETE. The
project's required non-GET request is therefore the successful JSONPlaceholder
POST /posts call. Height and weight also use decimetres and hectograms, and
related objects are represented as names plus URLs rather than being fully
embedded.

Error-handling behavior

Every request uses a 15-second timeout. Connection failures, timeouts, and other
requests exceptions are caught and reported without stopping the remaining
exploration. HTTP error responses such as the deliberate 404 are printed as a
short error summary and returned to the caller without raising an exception.
Successful responses are parsed as JSON; malformed or unexpectedly structured
data produces a concise summary error rather than a crash.

Running the project

python -m pip install requests
python api_explorer.py
