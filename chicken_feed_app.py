import streamlit as st

# Feed requirements based on breed and age
feed_data = {
    "Broilers": {
        "0-2 weeks": {"corn": 50, "soybean": 30, "fishmeal": 20},
        "3-6 weeks": {"corn": 55, "soybean": 25, "fishmeal": 20},
        "7+ weeks": {"corn": 60, "soybean": 20, "fishmeal": 20}
    },
    "Layers": {
        "0-6 weeks": {"corn": 40, "soybean": 35, "fishmeal": 25},
        "7-16 weeks": {"corn": 45, "soybean": 30, "fishmeal": 25},
        "17+ weeks": {"corn": 50, "soybean": 30, "fishmeal": 20}
    },
    "Free-range": {
        "0-6 weeks": {"corn": 35, "soybean": 25, "fishmeal": 20},
        "7-16 weeks": {"corn": 40, "soybean": 30, "fishmeal": 20},
        "17+ weeks": {"corn": 45, "soybean": 30, "fishmeal": 25}
    }
}

# Suggested alternative ingredients
alternative_ingredients = {
    "fishmeal": ["sunflower meal", "rice bran"],
    "soybean": ["wheat", "sunflower meal"],
    "corn": ["wheat", "barley"]
}

# Streamlit UI
st.title("🐔 Chicken Feed Calculator")
st.write("Easily calculate the best feed mix for your chickens!")

# User input
breed = st.selectbox("Select the breed of your chickens:", list(feed_data.keys()))
age_group = st.selectbox("Select the age group of your chickens:", list(feed_data[breed].keys()))
total_chickens = st.number_input("Enter the number of chickens:", min_value=1, step=1)

# Ingredient prices input (assume 50KG units)
st.subheader("Enter price per 50KG bag (optional):")
ingredient_prices = {}
available_ingredients = ["corn", "soybean", "fishmeal", "wheat", "sunflower meal", "rice bran"]
for ingredient in available_ingredients:
    ingredient_prices[ingredient] = st.number_input(f"{ingredient.capitalize()} (ZAR)", min_value=0.0, step=0.5, value=0.0)

# Tickable ingredient selection
st.subheader("Select available feed ingredients:")
selected_ingredients = st.multiselect("Choose from the list:", available_ingredients, default=["corn", "soybean", "fishmeal"])

# Feed calculation function
def calculate_feed(total_chickens, breed, age_group, selected_ingredients):
    base_feed = feed_data.get(breed, {}).get(age_group, {})
    if not base_feed:
        return None, []

    adjusted_feed = {}
    missing_ingredients = []

    for ingredient, amount in base_feed.items():
        if ingredient in selected_ingredients:
            adjusted_feed[ingredient] = amount * total_chickens
        else:
            missing_ingredients.append((ingredient, alternative_ingredients.get(ingredient, [])))

    return adjusted_feed, missing_ingredients

# Display results
if st.button("Calculate Feed"):
    feed_needed, missing_ingredients = calculate_feed(total_chickens, breed, age_group, selected_ingredients)

    if feed_needed:
        st.subheader(f"Feed requirement for {total_chickens} {breed} chickens ({age_group}):")
        for ingredient, amount in feed_needed.items():
            st.write(f"- {ingredient}: {amount} grams per day")

        total_weight = sum(feed_needed.values())
        st.subheader("🐓 Recommended Feed Mixing Recipe:")
        for ingredient, amount in feed_needed.items():
            percentage = (amount / total_weight) * 100
            st.write(f"- {ingredient}: {percentage:.1f}% of total feed mix")

        # Cost calculation
        st.subheader("💰 Estimated Cost:")
        total_cost = 0
        for ingredient, amount in feed_needed.items():
            price_per_kg = ingredient_prices[ingredient] / 50 if ingredient_prices[ingredient] > 0 else 0
            kg_needed = amount / 1000
            cost = kg_needed * price_per_kg
            total_cost += cost
            st.write(f"- {ingredient}: {cost:.2f} ZAR")
        st.write(f"**Total Estimated Daily Cost:** {total_cost:.2f} ZAR")

        # How long feed will last
        st.subheader("📦 Feed Duration:")
        feed_duration = {}
        for ingredient, amount in feed_needed.items():
            kg_total = 50  # Assuming 50KG bag per ingredient
            kg_per_day = amount / 1000
            days = kg_total / kg_per_day if kg_per_day > 0 else 0
            feed_duration[ingredient] = days
            st.write(f"- {ingredient}: {days:.1f} days (50KG bag)")

        # Feed requirement till maturity (assume standard days)
        st.subheader("📅 Total Feed Until Maturity:")
        days_to_maturity = 75 if breed == "Broilers" else 140
        st.write(f"Estimated days to maturity: {days_to_maturity} days")
        for ingredient, amount in feed_needed.items():
            total_amount = (amount * days_to_maturity) / 1000  # in KG
            st.write(f"- {ingredient}: {total_amount:.1f} KG total needed")

    else:
        st.error("No valid feed recipe found. Try selecting different ingredients.")

    if missing_ingredients:
        st.subheader("⚠️ Missing Ingredients & Suggestions:")
        for missing, alternatives in missing_ingredients:
            alt_list = ", ".join(alternatives) if alternatives else "No suggestions available"
            st.write(f"- {missing}: Suggested alternatives: {alt_list}")
