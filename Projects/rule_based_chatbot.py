import re, random
from colorama import Fore, init

init(autoreset=True)

destinations = { "beaches": ["Bali", "Maldives", "Phuket"], "mountains": ["Swiss Alps", "Rocky Mountains", "Himalayas"], "cities": ["Tokyo", "Paris", "New York"] }

jokes = [ "Why don't programmers like nature? Too many bugs!", "Why did the computer go to the doctor? Because it had a virus!", "Why do travelers always feel warm? Because of all their hot spots!" ]

def normalizeText(text):
    return re.sub(r"\s+", "", text.strip().lower())

def reccomend():
    print(Fore.CYAN + "Travel Bot: Beacher, mountains or cities?")
    preference = input(Fore.YELLOW + "You: ")
    preference = normalizeText(preference)

    if preference in destinations:
        sugg = random.choice(destinations[preference])
        print(Fore.GREEN + f"Travel Bot: How about {sugg}?")
        print(Fore.CYAN + "Travel Bot: Do you like it? (yes/no)")
        ans = input(Fore.YELLOW + "You: ").lower()

        if ans == "yes":
            print(Fore.GREEN + f"Travel Bot: Awesome! Enjoy visiting {sugg}!")
        elif ans == "no":
            print(Fore.RED + "Travel Bot: Let's try another.")
            reccomend()
        else:
            print(Fore.RED + "Travel Bot: I'll suggest again.")
            reccomend()
    else:
        print(Fore.RED + "I don't have that suggestion, sorry.")
        reccomend()

def packingTips():
    print(Fore.CYAN + "Travel Bot: Where do you want to go?")
    loc = normalizeText(input(Fore.YELLOW + "You: "))



    while True:
        try:
            print(Fore.CYAN + "Travel Bot: How many days?")
            days = int(input(Fore.YELLOW + "You: "))
            break
        except ValueError:
            print(Fore.RED + "Please enter a valid integer.")
    
    print(Fore.GREEN + f"TravelBot: Packing tips for {days} days in {loc}:")

    print(Fore.GREEN + "- Pack versatile clothes.")

    print(Fore.GREEN + "- Bring chargers/adapters.")

    print(Fore.GREEN + "- Check the weather forecast.")


def tellJoke():
    print(Fore.YELLOW + f"Travel Bot: {random.choice(jokes)}")


def show_help():

    print(Fore.MAGENTA + "\nI can:")

    print(Fore.GREEN + "- Suggest travel spots (say 'recommendation')")

    print(Fore.GREEN + "- Offer packing tips (say 'packing')")

    print(Fore.GREEN + "- Tell a joke (say 'joke')")

    print(Fore.CYAN + "Type 'exit' or 'bye' to end.\n")

def main():
    print(Fore.GREEN + "Hello, I am Travel Bot.")
    name = input(Fore.YELLOW + "What's your name?")

    print(Fore.GREEN + f"Nice to meet you, {name}! We will have a great time together!")

    show_help()

    while True:
            user_input = input(Fore.YELLOW + f"{name}: ")
            user_input = normalizeText(user_input)

            if "recommend" in user_input or "suggest" in user_input:
                reccomend()
            elif "pack" in user_input or "packing" in user_input:
                packingTips()
            elif "joke" in user_input or "funny" in user_input:
                tellJoke()
            elif "help" in user_input:
                show_help()
            elif "exit" in user_input or "bye" in user_input:
                print(Fore.CYAN + "TravelBot: Safe travels! Goodbye!")
                break
            else:
                print(Fore.RED + "TravelBot: Could you rephrase?")

    if __name__ == "__main__":
        main()