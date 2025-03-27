def get_feed_requirements(breed):
    # Feed recommendations (grams per day per chicken)
    feed_data = {
        "Broilers": {"corn": 50, "soybean": 30, "fishmeal": 20},
        "Layers": {"corn": 40, "soybean": 35, "fishmeal": 25},
        "Free-range": {"corn": 35, "soybean": 25, "fishmeal": 20}
    }
    
    if breed in feed_data:
        return feed_data[breed]
    else:
        return None

def calculate_feed(total_chickens, breed):
    feed = get_feed_requirements(breed)
    
    if not feed:
        return "Invalid breed selected."

    total_feed = {ingredient: amount * total_chickens for ingredient, amount in feed.items()}
    
    return total_feed

# Ask the user for input
print("Welcome to the Chicken Feed Calculator! 🐔")
print("Choose the breed of your chickens: Broilers, Layers, Free-range")

breed = input("Enter chicken breed: ").strip().capitalize()
try:
    total_chickens = int(input("Enter the number of chickens: "))
except ValueError:
    print("Invalid number entered. Please enter a valid number.")
    exit()

# Calculate feed
feed_needed = calculate_feed(total_chickens, breed)

# Display results
if isinstance(feed_needed, dict):
    print(f"\nFeed requirement for {total_chickens} {breed} chickens:")
    for ingredient, amount in feed_needed.items():
        print(f"- {ingredient}: {amount} grams per day")
else:
    print(feed_needed)

