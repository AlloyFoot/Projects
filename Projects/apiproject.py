

import requests

def fetch_joke():
    url = "https://official-joke-api.appspot.com/random_joke"

    try:
        response = requests.get(url)

        # Check status code
        if response.status_code == 200:
            data = response.json()

            # Extract data
            setup = data.get("setup", "No setup found.")
            punchline = data.get("punchline", "No punchline found.")

            # Display nicely
            print("\nHere's a joke for you:\n")
            print(setup)
            print(punchline)

        else:
            print(f"Error: Received status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


def fetch_cat_fact():
    url = "https://catfact.ninja/fact"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            fact = data.get("fact", "No fact found.")

            print("\nRandom Cat Fact:\n")
            print(fact)

        else:
            print(f"Error: Received status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


if __name__ == "__main__":
    print("Choose an option:")
    print("1. Get a joke")
    print("2. Get a cat fact")

    choice = input("Enter 1 or 2: ")

    if choice == "1":
        fetch_joke()
    elif choice == "2":
        fetch_cat_fact()
    else:
        print("Invalid choice. Try again.")