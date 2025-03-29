import streamlit as st
import pycountry
import pandas as pd
from io import BytesIO

# Feed requirements based on type and age
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
    "fishmeal": ["sunflower meal", "rice"],
    "soybean": ["wheat", "sunflower meal"],
    "corn": ["wheat", "barley"]
}

# Full list of chicken breeds (optional)
chicken_breeds = [
    "Ancona", "Andalusian", "Appenzeller Barthuhner", "Appenzeller Spitzhauben", "Araucana", "Asil (Aseel)",
    "Australorp", "Barbu d'Anvers", "Barbu d'Everberg", "Barbu d'Uccle", "Barbu de Grubbe", "Barbu de Watermael",
    "Barnevelder", "Belgian Game", "Booted Bantam", "Brabanter", "Brahma", "Brakel", "Buckeye", "Campine",
    "Carlisle Old English Game", "Cochin", "Cream Legbar", "Crèvecoeur", "Croad Langshan", "Dandarawi",
    "Denizli", "Derbyshire Redcap", "Dominique", "Dorking", "Dutch Bantam", "Faverolles", "Fayoumi",
    "Friesian", "Frizzle", "German Langshan", "Hamburgh", "Houdan", "Indian Game", "Italiener", "Ixworth",
    "Japanese Bantam", "Jersey Giant", "Ko Shamo", "Kraienköppe", "La Bresse", "La Flèche", "Lakenvelder",
    "Legbar", "Leghorn", "Malay", "Malines", "Marans", "Marsh Daisy", "Minorca", "Modern Game",
    "Modern Langshan", "Nankin", "Nankin Shamo", "Neiderrheiner", "Netherlands Owlbeard", "New Hampshire Red",
    "Norfolk Grey", "North Holland Blue", "Ohiki", "Old English Game Bantam", "Old English Pheasant Fowl",
    "Orloff", "Orpington", "Oxford Old English Game", "Pekin", "Penedesenca", "Plymouth Rock", "Poland",
    "Rhode Island Red", "Rhodebar", "Rosecomb", "Rumpless Araucana", "Rumpless Game", "Scots Dumpy",
    "Scots Grey", "Sebright", "Serama", "Shamo", "Sicilian Buttercup", "Silkie", "Spanish", "Sulmtaler",
    "Sultan", "Sumatra", "Sussex", "Taiwan", "Thai Game", "Thüringian", "Transylvanian Naked Neck",
    "Tuzo", "Vorwerk", "Welbar", "Welsummer", "Wyandotte", "Wybar", "Yamato-Gunkei", "Yokohama"
]

# Get world currencies
currencies = sorted([currency.alpha_3 for currency in pycountry.currencies])

# Streamlit UI
st.title("🐔 Chicken Feed Calculator")
st.write("Easily calculate the best feed mix for your chickens!")

currency = st.selectbox("Select your currency:", currencies)
chicken_type = st.selectbox("Select type of chickens:", list(feed_data.keys()))
optional_breed = st.selectbox("Optional: Select specific breed (if known):", ["None"] + chicken_breeds)
age_group = st.selectbox("Select the age group of your chickens:", list(feed_data[chicken_type].keys()))
total_chickens = st.number_input("Enter the number of chickens:", min_value=1, step=1)

st.subheader("Enter price per 50KG bag (optional):")
ingredient_prices = {}
available_ingredients = ["corn", "soybean", "fishmeal", "wheat", "sunflower meal", "rice"]
for ingredient in available_ingredients:
    ingredient_prices[ingredient] = st.number_input(f"{ingredient.capitalize()} ({currency})", min_value=0.0, step=0.5, value=0.0)

st.subheader("Select available feed ingredients:")
selected_ingredients = st.multiselect("Choose from the list:", available_ingredients, default=["corn", "soybean", "fishmeal"])

# Feed calculation function
def calculate_feed(total_chickens, chicken_type, age_group, selected_ingredients):
    base_feed = feed_data.get(chicken_type, {}).get(age_group, {})
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

# Generate feeding schedule as DataFrame
def generate_feeding_schedule(chicken_type, feed_plan, days_to_maturity):
    data = []
    for day in range(1, days_to_maturity + 1):
        daily_feed = {"Day": day}
        for ingredient, total_grams in feed_plan.items():
            daily_feed[ingredient] = total_grams
        data.append(daily_feed)
    return pd.DataFrame(data)

# Download helper
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Feeding Schedule')
    return output.getvalue()

# Display results
if st.button("Calculate Feed"):
    feed_needed, missing_ingredients = calculate_feed(total_chickens, chicken_type, age_group, selected_ingredients)
    if feed_needed:
        st.subheader(f"Feed requirement for {total_chickens} {chicken_type} chickens ({age_group}):")
        for ingredient, amount in feed_needed.items():
            st.write(f"- {ingredient}: {amount} grams per day")

        total_weight = sum(feed_needed.values())
        st.subheader("🐓 Recommended Feed Mixing Recipe:")
        for ingredient, amount in feed_needed.items():
            percentage = (amount / total_weight) * 100
            st.write(f"- {ingredient}: {percentage:.1f}% of total feed mix")

        st.subheader("💰 Estimated Cost:")
        total_cost = 0
        for ingredient, amount in feed_needed.items():
            price_per_kg = ingredient_prices[ingredient] / 50 if ingredient_prices[ingredient] > 0 else 0
            kg_needed = amount / 1000
            cost = kg_needed * price_per_kg
            total_cost += cost
            st.write(f"- {ingredient}: {cost:.2f} {currency}")
        st.write(f"**Total Estimated Daily Cost:** {total_cost:.2f} {currency}")

        st.subheader("📦 Feed Duration:")
        for ingredient, amount in feed_needed.items():
            kg_total = 50
            kg_per_day = amount / 1000
            days = kg_total / kg_per_day if kg_per_day > 0 else 0
            st.write(f"- {ingredient}: {days:.1f} days (50KG bag)")

        st.subheader("📅 Total Feed Until Maturity:")
        days_to_maturity = 75 if chicken_type == "Broilers" else 140
        st.write(f"Estimated days to maturity: {days_to_maturity} days")
        for ingredient, amount in feed_needed.items():
            total_amount = (amount * days_to_maturity) / 1000
            st.write(f"- {ingredient}: {total_amount:.1f} KG total needed")

        st.subheader("📄 Download Feeding Schedule:")
        schedule_df = generate_feeding_schedule(chicken_type, feed_needed, days_to_maturity)
        csv = convert_df_to_csv(schedule_df)
        excel = convert_df_to_excel(schedule_df)
        st.download_button("Download as CSV", csv, "feeding_schedule.csv", "text/csv")
        st.download_button("Download as Excel", excel, "feeding_schedule.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    else:
        st.error("No valid feed recipe found. Try selecting different ingredients.")

    if missing_ingredients:
        st.subheader("⚠️ Missing Ingredients & Suggestions:")
        for missing, alternatives in missing_ingredients:
            alt_list = ", ".join(alternatives) if alternatives else "No suggestions available"
            st.write(f"- {missing}: Suggested alternatives: {alt_list}")
