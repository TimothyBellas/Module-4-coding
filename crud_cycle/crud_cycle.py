import requests


# Every request in this exercise uses the JSONPlaceholder todos resource.
BASE_URL = "https://jsonplaceholder.typicode.com/todos"
# A timeout prevents the program from waiting forever if the API is unavailable.
TIMEOUT = 10


def print_result(step, response, description):
    """Print the required information for one CRUD step."""
    # requests stores the final HTTP method and URL on response.request.
    print(f"\n{step}")
    print(f"{response.request.method} {response.url}")
    print(f"Status: {response.status_code}")
    print(f"Result: {description}")


def main():
    # A Session reuses the same connection for all requests in the CRUD cycle.
    with requests.Session() as session:
        # CREATE: Send the new todo fields as a JSON request body.
        # The `json` argument also sets the correct Content-Type header.
        response = session.post(
            BASE_URL,
            json={
                "userId": 1,
                "title": "Complete Module 4",
                "completed": False,
            },
            timeout=TIMEOUT,
        )

        # Convert the JSON response into a Python dictionary. JSONPlaceholder
        # assigns the simulated todo an ID, which is needed for later requests.
        created_todo = response.json()
        todo_id = created_todo["id"]
        print_result("1. CREATE", response, f"Created simulated todo #{todo_id}.")

        # A single-resource URI is built by adding the new ID to /todos.
        todo_url = f"{BASE_URL}/{todo_id}"

        # READ: Attempt to retrieve the newly created todo using its ID.
        response = session.get(todo_url, timeout=TIMEOUT)

        # JSONPlaceholder fakes writes rather than saving them permanently.
        # Therefore, GET /todos/201 normally returns 404 after the POST.
        if response.status_code == 200:
            description = f"Retrieved todo #{todo_id}."
        else:
            description = (
                "Todo not found because JSONPlaceholder does not save POST data."
            )
        print_result("2. READ", response, description)

        # UPDATE: PATCH sends only the field that should change. PUT would
        # normally send a complete replacement for the todo resource.
        response = session.patch(
            todo_url, json={"completed": True}, timeout=TIMEOUT
        )

        # response.ok is True for successful status codes from 200 through 399.
        if response.ok:
            description = f"Marked simulated todo #{todo_id} as completed."
        else:
            description = "Update was not stored by the simulated API."
        print_result("3. UPDATE", response, description)

        # READ AGAIN: Try to confirm that `completed` is now true.
        response = session.get(todo_url, timeout=TIMEOUT)
        if response.status_code == 200:
            # .get() safely reads the completed field from the response JSON.
            completed = response.json().get("completed")
            description = f"Todo completed value is {completed}."
        else:
            description = "Cannot verify the update because the todo was not stored."
        print_result("4. READ AGAIN", response, description)

        # DELETE: Request removal of the resource at the same URI.
        response = session.delete(todo_url, timeout=TIMEOUT)
        description = (
            f"Delete request for simulated todo #{todo_id} was processed."
            if response.ok
            else "Delete request was not accepted."
        )
        print_result("5. DELETE", response, description)

        # VERIFY: A final GET checks whether the resource is still available.
        # A real API should return 404 after a successful deletion.
        response = session.get(todo_url, timeout=TIMEOUT)
        if response.status_code == 404:
            description = f"Todo #{todo_id} is not available (404 Not Found)."
        else:
            description = f"Todo #{todo_id} still returned a response."
        print_result("6. VERIFY", response, description)


if __name__ == "__main__":
    # Handle network problems and unexpected response data without displaying
    # a long traceback to the user.
    try:
        main()
    except (requests.RequestException, KeyError, ValueError) as error:
        print(f"CRUD cycle failed: {error}")
