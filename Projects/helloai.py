print("Hello! I am AI Bot. Whats your name?: ")
name = input()

print(f"Nice to meet you, {name}!")

print()

print("How are you feeling today? (good/bad): ")
mood = input().lower()

print()

if mood == "good":
    print("I'm glad to hear that.")
elif mood == "bad":
    print("I hope things get better for you soon.")
else:
    print("Sometimes it's hard to put feelings into words.")

print()

print(f"It was nice chatting with you, {name}! Goodbye!")