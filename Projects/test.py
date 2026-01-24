import colorama
from colorama import Fore, Style
from textblob import TextBlob

# Initialize colorama for colored output
colorama.init()

def show_processing_animation():
    print(f"{Fore.CYAN}Analyzing...{Style.RESET_ALL}")

def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.25:
        return polarity, "Positive"
    elif polarity < -0.25:
        return polarity, "Negative"
    else:
        return polarity, "Neutral"

def execute_command(command):
    global positive_count, negative_count, neutral_count

    if command == "help":
        print(f"{Fore.CYAN}Available commands:{Style.RESET_ALL}")
        print("history - view conversation history")
        print("summary - view sentiment summary")
        print("reset - clear all data")
        print("exit - quit the program")
        return True

    if command == "summary":
        print(f"{Fore.CYAN}Sentiment Summary:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Positive: {positive_count}{Style.RESET_ALL}")
        print(f"{Fore.RED}Negative: {negative_count}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Neutral: {neutral_count}{Style.RESET_ALL}")
        return True

    if command == "reset":
        conversation_history.clear()
        positive_count = negative_count = neutral_count = 0
        print(f"{Fore.CYAN}🧹 All data has been reset!{Style.RESET_ALL}")
        return True

    if command == "history":
        if not conversation_history:
            print(f"{Fore.YELLOW}No conversation history yet.{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}📜 Conversation History:{Style.RESET_ALL}")
            for idx, (text, polarity, sentiment_type) in enumerate(conversation_history, start=1):
                if sentiment_type == "Positive":
                    color = Fore.GREEN
                elif sentiment_type == "Negative":
                    color = Fore.RED
                else:
                    color = Fore.YELLOW

                print(f"{idx}. {color}{text} (Polarity: {polarity:.2f}, {sentiment_type}){Style.RESET_ALL}")
        return True

    return False

def get_valid_name():
    while True:
        name = input(f"{Fore.MAGENTA}Please enter your name: {Style.RESET_ALL}").strip()
        if name.isalpha():
            return name
        print(f"{Fore.RED}Name must contain only letters.{Style.RESET_ALL}")

# Emojis for the start of the program
print(f"{Fore.CYAN}🕵️‍♂️ Welcome to Sentiment Spy! 🕵️‍♀️{Style.RESET_ALL}")

user_name = get_valid_name()

# Store conversation as a list of tuples: (text, polarity, sentiment_type)
conversation_history = []

positive_count = 0
negative_count = 0
neutral_count = 0

print(f"\n{Fore.CYAN}Hello, Agent {user_name}!")
print("Type a sentence and I will analyze your sentence with TextBlob and show you the sentiment. 🔍")
print(f"Type {Fore.YELLOW}'reset'{Fore.CYAN}, {Fore.YELLOW}'history'{Fore.CYAN}, "
      f"{Fore.YELLOW}'summary'{Fore.CYAN}, {Fore.YELLOW}'help'{Fore.CYAN}, or {Fore.YELLOW}'exit'{Fore.CYAN} to quit.{Style.RESET_ALL}\n")

while True:
    user_input = input(f"{Fore.GREEN}>> {Style.RESET_ALL}").strip()

    if not user_input:
        print(f"{Fore.RED}Please enter some text or a valid command.{Style.RESET_ALL}")
        continue

    # Check for commands
    if execute_command(user_input.lower()):
        if user_input.lower() == "exit":
            print(f"\n{Fore.BLUE}👋 Exiting Sentiment Spy. Farewell, Agent {user_name}! 👋{Style.RESET_ALL}")
            break
        continue

    show_processing_animation()

    # Analyze sentiment
    polarity, sentiment_type = analyze_sentiment(user_input)

    # Store in history
    conversation_history.append((user_input, polarity, sentiment_type))

    # Update counts
    if sentiment_type == "Positive":
        positive_count += 1
        color = Fore.GREEN
        emoji = "😊"
    elif sentiment_type == "Negative":
        negative_count += 1
        color = Fore.RED
        emoji = "😠"
    else:
        neutral_count += 1
        color = Fore.YELLOW
        emoji = "😐"

    # Print result with color, emojis, and polarity
    print(f"{color}{emoji} {sentiment_type} sentiment detected! "
          f"(Polarity: {polarity:.2f}){Style.RESET_ALL}")
