import streamlit as st

# Function to get feed requirements based on breed
def get_feed_requirements(breed):
    feed_data = {
        "Broilers": {"corn": 50, "soybean": 30, "fishmeal": 20},
        "Layers": {"corn": 40, "soybean": 35, "fishmeal": 25},
        "Free-range": {"corn": 35, "soybean": 25, "fishmeal": 20}
    }
    return feed_data.get(breed, None)

# Function to calculate feed per chicken
def calculate_feed(total_chickens, breed):
    feed = get_feed_requirements(breed)
    if not feed:
        return None
    return {ingredient: amount * total_chickens for ingredient, amount in feed.items()}

# Streamlit UI
st.title("🐔 Chicken Feed Calculator")

# Dropdown for breed selection
breed = st.selectbox("Select the breed of your chickens:", ["Broilers", "Layers", "Free-range"])

# Input for number of chickens
total_chickens = st.number_input("Enter the number of chickens:", min_value=1, step=1)

# Calculate and display results
if st.button("Calculate Feed"):
    feed_needed = calculate_feed(total_chickens, breed)

    if feed_needed:
        st.subheader(f"Feed requirement for {total_chickens} {breed} chickens:")
        for ingredient, amount in feed_needed.items():
            st.write(f"- {ingredient}: {amount} grams per day")
    else:
        st.error("Invalid breed selected.")
