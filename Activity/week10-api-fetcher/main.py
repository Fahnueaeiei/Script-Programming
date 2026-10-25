"""Week 10: Fetch and display JSONPlaceholder API data."""
from src.api_client import APIClient


def display_menu():
    print("\n" + "=" * 42)
    print("           API DATA FETCHER CLI")
    print("=" * 42)
    print("1. Fetch a Single TODO Item")
    print("2. Fetch All Posts")
    print("3. Fetch TODOs by User ID")
    print("4. Exit")
    print("=" * 42)


def read_positive_id(label):
    try:
        number = int(input(f"Enter {label}: ").strip())
        if number <= 0:
            print(f"{label} must be a positive number.")
            return None
        return number
    except ValueError:
        print(f"Invalid input. {label} must be a number.")
        return None


def handle_single_todo(client):
    todo_id = read_positive_id("TODO ID")
    if todo_id is None:
        return
    todo = client.fetch_single_todo(todo_id)
    if todo is None:
        print("Could not retrieve the TODO item.")
    elif not isinstance(todo, dict) or not todo:
        print("TODO item not found.")
    else:
        print("\n--- TODO Item Details ---")
        print(f"ID: {todo.get('id')}")
        print(f"User ID: {todo.get('userId')}")
        print(f"Title: {todo.get('title')}")
        print(f"Completed: {todo.get('completed')}")
        print("-------------------------")


def handle_all_posts(client):
    posts = client.fetch_all_posts()
    if posts is None:
        print("Could not retrieve posts.")
    elif not isinstance(posts, list) or not posts:
        print("No posts found.")
    else:
        print(f"\n--- First 5 Posts (of {len(posts)} total) ---")
        for index, post in enumerate(posts[:5], start=1):
            print(f"\n[{index}] Post ID: {post.get('id')} | User ID: {post.get('userId')}")
            print(f"Title: {post.get('title')}")
            body = str(post.get('body') or '').replace('\n', ' ')
            print(f"Body: {body[:60]}{'...' if len(body) > 60 else ''}")
        if len(posts) > 5:
            print(f"\n... and {len(posts) - 5} more posts not displayed.")
        print("----------------------------------")


def handle_user_todos(client):
    user_id = read_positive_id("User ID")
    if user_id is None:
        return
    todos = client.fetch_user_todos(user_id)
    if todos is None:
        print("Could not retrieve user TODOs.")
    elif not isinstance(todos, list) or not todos:
        print(f"No TODOs found for User ID {user_id}.")
    else:
        print(f"\n--- TODOs for User ID {user_id} ({len(todos)} total) ---")
        for todo in todos:
            status = "Completed" if todo.get('completed') else "Pending"
            print(f"ID: {todo.get('id')} | Title: {todo.get('title')} | Status: {status}")
        print("----------------------------------")


def main():
    client = APIClient()
    while True:
        display_menu()
        choice = input("Enter choice (1-4): ").strip()
        if choice == '1':
            handle_single_todo(client)
        elif choice == '2':
            handle_all_posts(client)
        elif choice == '3':
            handle_user_todos(client)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
