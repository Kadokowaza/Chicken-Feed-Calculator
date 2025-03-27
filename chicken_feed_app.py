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

# Available feed ingredients
available_ingredients = ["corn", "soybean", "fishmeal", "wheat", "sunflower meal", "rice bran"]

def calculate_feed(total_chickens, breed, age_group, selected_ingredients):
    base_feed = feed_data.get(breed, {}).get(age_group, {})
    if not base_feed:
        return None

    # Adjust feed based on available ingredients
    adjusted_feed = {}
    for ingredient, amount in base_feed.items():
        if ingredient in selected_ingredients:
            adjusted_feed[ingredient] = amount * total_chickens

    return adjusted_feed

# Streamlit UI
st.title("🐔 Chicken Feed Calculator")
st.write("Easily calculate the best feed mix for your chickens!")

# User input
breed = st.selectbox("Select the breed of your chickens:", list(feed_data.keys()))
age_group = st.selectbox("Select the age group of your chickens:", list(feed_data[breed].keys()))
total_chickens = st.number_input("Enter the number of chickens:", min_value=1, step=1)

# Tickable ingredient selection
st.subheader("Select available feed ingredients:")
selected_ingredients = st.multiselect("Choose from the list:", available_ingredients, default=["corn", "soybean", "fishmeal"])

# Calculate and display results
if st.button("Calculate Feed"):
    feed_needed = calculate_feed(total_chickens, breed, age_group, selected_ingredients)

    if feed_needed:
        st.subheader(f"Feed requirement for {total_chickens} {breed} chickens ({age_group}):")
        for ingredient, amount in feed_needed.items():
            st.write(f"- {ingredient}: {amount} grams per day")
        
        st.subheader("🐓 Recommended Feed Mixing Recipe:")
        total_weight = sum(feed_needed.values())
        for ingredient, amount in feed_needed.items():
            percentage = (amount / total_weight) * 100
            st.write(f"- {ingredient}: {percentage:.1f}% of total feed mix")
    else:
        st.error("No valid feed recipe found. Try selecting different ingredients.")
