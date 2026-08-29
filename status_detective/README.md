API Status Detective

A Python diagnostic tool that sends requests to JSONPlaceholder and reports
each response's HTTP status code, category, and description.

Features

Tests six successful and unsuccessful API requests

Classifies success, client error, and server error responses

Describes returned resources and collections

Handles network errors

Includes a reusable request_report() function

Setup

Install the dependency in PowerShell:

py -m pip install -r requirements.txt

Run

py .\status_detective.py

Example Output

GET /posts/1
  Status: 200 (Success)
  Description: Request succeeded — resource returned

This project uses the free JSONPlaceholder API:
https://jsonplaceholder.typicode.com

