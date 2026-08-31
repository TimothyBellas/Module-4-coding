# API Header Inspector

This project compares response headers from public API endpoints and demonstrates sending custom headers in a POST request.

## Features

For each GET response, the script displays:

- Content-Type
- Content-Length, or `Not specified`
- Whether caching headers are present
- Any rate-limiting headers
- Total number of response headers

The script also sends JSON data to HTTPBin with an `X-Student-Name: Tim` header. HTTPBin echoes the request so the custom header and body can be verified.

## Setup

Install the dependency:

```bash
python -m pip install -r requirements.txt
