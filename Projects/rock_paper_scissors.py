import random

moves = ["Rock", "Paper", "Scissors"]
playAgain = True

while playAgain:
    q = input("Choose Rock, Paper, or Scissors: ")

    if q[0].lower() == "r":
        userChoice = "Rock"
    elif q[0].lower() == "p":
        userChoice = "Paper"
    elif q[0].lower() == "s":
        userChoice = "Scissors"
    else:
        continue

    computerChoice = random.choice(moves)

    print("You chose: ", q)
    print("Computer chose: ", computerChoice)

    if userChoice == computerChoice:
        print("tie")
    elif userChoice == "Rock" and computerChoice == "Scissors":
        print("you win")
    elif userChoice == "Paper" and computerChoice == "Rock":
        print("you win")
    elif userChoice == "Scissors" and computerChoice == "Paper":
        print("you win")
    else:
        print("i win")

    s = input("do you want to play again? (y/n): ")

    if s[0] == "y":
        playAgain = True
    else:
        playAgain = False

print("I hope you had fun!")
