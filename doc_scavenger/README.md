itHub API Documentation Scavenger

This project demonstrates how to use the GitHub REST API's repository search endpoint without an API key.

What it does

doc_scavenger.py:

Searches repositories in the google organization

Sorts results by star count in descending order

Fetches the top 3 repositories

Prints each repository's:

Name

Description

Star count

Primary language

Prints the remaining GitHub search rate limit from the response headers

Authentication

This script does not use an API key or access token.

It makes an unauthenticated request to GitHub's public REST API. GitHub applies a lower rate limit to unauthenticated search requests.

Requirements

Python 3.9+

requests

Install dependencies with:

pip install -r requirements.txt

Run

python doc_scavenger.py

API Endpoint

The script uses:

GET https://api.github.com/search/repositories

with these query parameters:

q=org:google
sort=stars
order=desc
per_page=3

It also sends GitHub's recommended JSON Accept header:

Accept: application/vnd.github+json
