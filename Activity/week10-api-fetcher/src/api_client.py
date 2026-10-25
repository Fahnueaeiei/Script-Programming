"""HTTP client for the JSONPlaceholder practice API."""
import requests


class APIClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def _make_request(self, endpoint):
        url = f"{self.BASE_URL}{endpoint}"
        print(f"[INFO] Fetching (GET) from {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as exc:
            print(f"[ERROR] HTTP error: {exc}")
        except requests.exceptions.ConnectionError as exc:
            print(f"[ERROR] Connection failed: {exc}")
        except requests.exceptions.Timeout:
            print("[ERROR] Request timed out.")
        except requests.exceptions.RequestException as exc:
            print(f"[ERROR] Request failed: {exc}")
        except ValueError:
            print("[ERROR] API returned invalid JSON.")
        return None

    def fetch_single_todo(self, todo_id):
        return self._make_request(f"/todos/{todo_id}")

    def fetch_all_posts(self):
        return self._make_request("/posts")

    def fetch_user_todos(self, user_id):
        return self._make_request(f"/todos?userId={user_id}")
