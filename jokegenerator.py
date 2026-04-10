import requests
def generate_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)

    if response.status_code == 200:
        print(f"Response Sequence: {response.json()}")
    
        joke_data = response.json()
        return f"{joke_data['setup']} - {joke_data['punchline']}"
    else:
        print("Failed to retrive joke")

def main():
    print("welcome to the random joke generator!")

    while True:
        inputx = input("Press Enter to get a joke, or press q/exit to leave.: ").strip().lower()
        if inputx in ("q", "exit"):
            print("Exiting...")
            break
    
        joke = generate_joke()
        print(joke)
if __name__ == "__main__":
    main()