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

print("Did you learn something today? (yes/no): ")
learn = input().lower()

print()

if learn == "yes":
    print("I hope that it was helpful!")
else:
    print("Everyone learns something, whether they realize it or not.\nIt could be as small as learning what you wanted to wear today, or learning that it was going to rain!")

print()

print(f"It was nice chatting with you, {name}! Goodbye!")

# https://github.com/AlloyFoot/Projects.git