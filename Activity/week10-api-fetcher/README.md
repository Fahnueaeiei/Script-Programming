# Week 10 — API Data Fetcher CLI

Python CLI project based on **Week 10: Interacting with Web APIs — Fetching and Processing JSON Data**. Uses [JSONPlaceholder](https://jsonplaceholder.typicode.com/) to demonstrate HTTP GET requests, JSON processing, and exception handling.

## Features

1. **Fetch a Single TODO Item** — enter a TODO ID, display ID, User ID, title, completed status.
2. **Fetch All Posts** — fetch `/posts` and show the first five posts, with a total count.
3. **Fetch TODOs by User ID** — enter a User ID and display that user's TODOs with status.
4. **Exit** — leave the CLI.

Handles invalid input, missing results, HTTP errors, connection errors, timeouts and malformed JSON.

## Structure

```text
week10-api-fetcher/
├── main.py
├── src/
│   ├── __init__.py
│   └── api_client.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Run

Requires Python 3.9+ and internet access.

```bash
cd week10-api-fetcher
python3 -m pip install -r requirements.txt
python3 main.py
```

## Screenshots to submit

Capture your own terminal screenshots for each of these options:

- **1. Fetch a Single TODO Item** — use TODO ID `1`.
- **2. Fetch All Posts** — show the first five posts.
- **3. Fetch TODOs by User ID** — use User ID `1`.

Submit the GitHub link and all three screenshots. API responses depend on live internet access.

## Add to existing Script-Programming repo

Copy this folder into `Script-Programming/Activity/` and from the repository root:

```bash
git status
git add Activity/week10-api-fetcher
git commit -m "Add Week 10 API Data Fetcher"
git push origin main
```

Do not run `git init` inside this folder if you are using the existing repository.
