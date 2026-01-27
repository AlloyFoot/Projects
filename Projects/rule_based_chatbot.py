import re, random
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)

destinations = { "beaches": ["Bali", "Maldives", "Phuket"], "mountains": ["Swiss Alps", "Rocky Mountains", "Himalayas"], "cities": ["Tokyo", "Paris", "New York"] }

jokes = [ "Why don't programmers like nature? Too many bugs!", "Why did the computer go to the doctor? Because it had a virus!", "Why do travelers always feel warm? Because of all their hot spots!" ]

weather_conditions = ["sunny", "cloudy", "rainy", "windy", "snowy"]

news_headlines = [
    "Global leaders meet to discuss climate action.",
    "New breakthrough announced in renewable energy.",
    "Major tech company unveils a new AI assistant.",
    "Scientists discover a potentially habitable exoplanet."
]

city_times = {
    "newyork": -5,
    "paris": 1,
    "tokyo": 9,
    "london": 0
}

conversation_history = []

def normalizeText(text):
    return re.sub(r"\s+", " ", text.strip().lower())

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

def getWeather():
    print(Fore.CYAN + "Travel Bot: Which city?")
    city = input(Fore.YELLOW + "You: ")
    condition = random.choice(weather_conditions)
    temp = random.randint(30, 95)
    print(Fore.GREEN + f"Travel Bot: The weather in {city} is {condition} and {temp}°F.")

def getNews():
    print(Fore.GREEN + "Travel Bot: Here is a news update:")
    print(Fore.CYAN + f"- {random.choice(news_headlines)}")

def getLocalTime():
    print(Fore.CYAN + "Travel Bot: Which city?")
    city = normalizeText(input(Fore.YELLOW + "You: "))
    if city in city_times:
        offset = city_times[city]
        utc = datetime.utcnow()
        local = utc.hour + offset
        local = local % 24
        print(Fore.GREEN + f"Travel Bot: The local time in {city.title()} is {local}:00.")
    else:
        print(Fore.RED + "Travel Bot: I don't know that city.")

def show_help():

    print(Fore.MAGENTA + "\nI can:")

    print(Fore.GREEN + "- Suggest travel spots (say 'recommendation')")

    print(Fore.GREEN + "- Offer packing tips (say 'packing')")

    print(Fore.GREEN + "- Tell a joke (say 'joke')")

    print(Fore.GREEN + "- Simulate weather info (say 'weather')")
    print(Fore.GREEN + "- Give news updates (say 'news')")
    print(Fore.GREEN + "- Show local time (say 'time')")

    print(Fore.CYAN + "Type 'exit' or 'bye' to end.\n")

def main():
    print(Fore.GREEN + "Hello, I am Travel Bot.")
    name = input(Fore.YELLOW + "What's your name?")

    print(Fore.GREEN + f"Nice to meet you, {name}! We will have a great time together!")

    show_help()

    while True:
            user_input = input(Fore.YELLOW + f"{name}: ")
            user_input = normalizeText(user_input)

            conversation_history.append(user_input)

            if re.search(r"\brecommend|\bsuggest", user_input):
                reccomend()
            elif re.search(r"\bpack", user_input):
                packingTips()
            elif re.search(r"\bjoke|\bfunny", user_input):
                tellJoke()
            elif re.search(r"\bweather", user_input):
                getWeather()
            elif re.search(r"\bnews", user_input):
                getNews()
            elif re.search(r"\btime", user_input):
                getLocalTime()
            elif re.search(r"\bhelp", user_input):
                show_help()
            elif re.search(r"\bexit|\bbye", user_input):
                print(Fore.CYAN + "TravelBot: Safe travels! Goodbye!")
                break
            else:
                print(Fore.RED + "TravelBot: Could you rephrase?")

    if __name__ == "__main__":
        main()