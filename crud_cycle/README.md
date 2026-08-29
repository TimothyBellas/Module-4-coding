Python REST API Exercises

Small Python exercises for learning REST APIs with JSONPlaceholder.

Files

api_explorer.py demonstrates GET and POST requests.

crud_cycle.py demonstrates CREATE, READ, UPDATE, DELETE, and verification.

API_DISCOVERY.md documents exploration of PokeAPI.

REST_API_DESIGN.md evaluates REST URIs and designs a recipe API.

Requirements

Python 3.9 or newer

Internet access

Install the dependency in PowerShell:

py -m pip install -r requirements.txt

Run

py .\api_explorer.py
py .\crud_cycle.py

Note

JSONPlaceholder simulates POST, PATCH, and DELETE requests. Changes are not
permanently saved, so a GET request for a newly created todo can return 404.

