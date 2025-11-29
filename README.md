# GitHub Connector

A Python client for interacting with the GitHub API, featuring automatic retries for rate-limiting, server errors, and connection issues.

---

## Features

* Makes authenticated API requests to GitHub.
* Handles rate-limiting (HTTP 429 and 403) automatically with retries.
* Implements exponential backoff for server errors (HTTP 5xx).
* Raises custom exceptions for specific errors:

  * `ResourceNotFound` (404)
  * `MaxRetriesExceeded` (exceeded retry limit)

---

## Installation

```bash
git clone <repo-url>
cd github_connector
poetry install
```

> Requires Python 3.9+ and `requests`.

---

## Testing

This project uses **pytest** and **pytest-mock** for testing.

```bash
poetry run pytest
```

---

## Exceptions

* **ResourceNotFound** – Raised when a 404 response is returned.
* **MaxRetriesExceeded** – Raised when the client exceeds the maximum retry attempts.

---

## License

MIT License

