API Request Anatomy

request_anatomy.py demonstrates the complete anatomy of three HTTP API
transactions using JSONPlaceholder, a
public API intended for testing and examples.

Transactions

The script performs these requests:

GET /users/1 — retrieves a specific user.

POST /posts — creates a new post.

PATCH /posts/1 — updates the title of an existing post.

For every transaction, the output includes:

HTTP method and URL

All request headers

Request body, when present

Response status code and reason

Response Content-Type and Content-Length headers

Complete response body

Total elapsed time in milliseconds

Requirements

Python 3.10 or newer

An active internet connection

The program uses only Python's standard library. No third-party packages are
required.

Setup

Clone the repository and move into its directory:

git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
Set-Location YOUR-REPOSITORY

Optionally create and activate a virtual environment:

python -m venv .venv
.\.venv\Scripts\Activate.ps1

Install the listed requirements. This succeeds without downloading packages
because the project has no third-party dependencies:

python -m pip install -r requirements.txt

Run the Script

python request_anatomy.py

The output is divided into three clearly labeled sections. If an API request
cannot be completed, the script prints the error and continues to the next
transaction.

Project Files

.
|-- README.md
|-- request_anatomy.py
`-- requirements.txt

Notes

JSONPlaceholder simulates write operations. The POST and PATCH requests
return realistic responses, but they do not permanently change the service's
stored data.

