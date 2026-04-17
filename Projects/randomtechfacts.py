import requests
import html
import random

url = "https://uselessfacts.jsph.pl/random.json?language=en"

def get_fact():
    response = requests.get(url)
    if response.status_code == 200:
        fact_data = response.json()
        print(fact_data['text'])
    else:
        print("Failed to retrieve fact")

while True:
    userInput = input("enter for a fact, or q to quit: ")
    if userInput.lower() == "q":
        break
    get_fact()

