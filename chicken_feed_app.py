
import streamlit as st
import pycountry
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64

# Feed requirements based on type and age
feed_data = {
    "Broilers": {
        "Starter (0-4 weeks)": {"corn": 40, "soybean": 25, "rice": 5, "wheat": 5, "fishmeal": 10, "sunflower meal": 5, "limestone": 2, "premix": 5, "salt": 1, "dl_methionine": 1},
        "Grower (5-12 weeks)": {"corn": 35, "soybean": 20, "rice": 10, "wheat": 10, "fishmeal": 10, "sunflower meal": 10, "limestone": 3, "premix": 5, "salt": 1, "dl_methionine": 1},
        "Finisher (13+ weeks)": {"corn": 30, "soybean": 15, "rice": 15, "wheat": 15, "fishmeal": 5, "sunflower meal": 10, "limestone": 4, "premix": 5, "salt": 1, "dl_methionine": 1}
    },
    "Layers": {
        "Starter (0-4 weeks)": {"corn": 40, "soybean": 25, "rice": 5, "wheat": 5, "fishmeal": 10, "sunflower meal": 5, "limestone": 2, "premix": 5, "salt": 1, "dl_methionine": 1},
        "Grower (5-12 weeks)": {"corn": 35, "soybean": 20, "rice": 10, "wheat": 10, "fishmeal": 10, "sunflower meal": 10, "limestone": 3, "premix": 5, "salt": 1, "dl_methionine": 1},
        "Finisher (13+ weeks)": {"corn": 30, "soybean": 15, "rice": 15, "wheat": 15, "fishmeal": 5, "sunflower meal": 10, "limestone": 4, "premix": 5, "salt": 1, "dl_methionine": 1},
        "Laying (16+ weeks)": {"corn": 35, "soybean": 20, "rice": 10, "wheat": 10, "fishmeal": 5, "sunflower meal": 10, "limestone": 8, "premix": 5, "salt": 1, "dl_methionine": 1}
    },
    "Free-range": {
        "Starter (0-4 weeks)": {"corn": 40, "soybean": 25, "rice": 5, "wheat": 5, "fishmeal": 10, "sunflower meal": 5, "limestone": 2, "premix": 5, "salt": 1, "dl_methionine": 1},
        "Grower (5-12 weeks)": {"corn": 35, "soybean": 20, "rice": 10, "wheat": 10, "fishmeal": 10, "sunflower meal": 10, "limestone": 3, "premix": 5, "salt": 1, "dl_methionine": 1},
        "Finisher (13+ weeks)": {"corn": 30, "soybean": 15, "rice": 15, "wheat": 15, "fishmeal": 5, "sunflower meal": 10, "limestone": 4, "premix": 5, "salt": 1, "dl_methionine": 1},
        "Laying (16+ weeks)": {"corn": 35, "soybean": 20, "rice": 10, "wheat": 10, "fishmeal": 5, "sunflower meal": 10, "limestone": 8, "premix": 5, "salt": 1, "dl_methionine": 1}
    }
}

available_ingredients = list(next(iter(next(iter(feed_data.values())).values())).keys())
currencies = sorted([currency.alpha_3 for currency in pycountry.currencies])

# UI
st.title("🐔 Chicken Feed Calculator")
st.markdown("**Rosashi Farms** - Helping farmers feed smarter.")

currency = st.selectbox("Select your currency:", currencies)
chicken_type = st.selectbox("Select type of chickens:", list(feed_data.keys()))
age_group = st.selectbox("Select age group:", list(feed_data[chicken_type].keys()))
total_chickens = st.number_input("Number of chickens:", min_value=1, step=1)

ingredient_prices = {}
st.subheader("Ingredient Prices per 50KG Bag:")
for ing in available_ingredients:
    ingredient_prices[ing] = st.number_input(f"{ing.capitalize()} ({currency})", min_value=0.0, step=0.5)

st.subheader("Available Ingredients:")
selected_ingredients = st.multiselect("Select ingredients available to you:", available_ingredients, default=available_ingredients)

def calculate_feed():
    base = feed_data[chicken_type][age_group]
    adjusted = {k: v * total_chickens for k, v in base.items() if k in selected_ingredients}
    return adjusted

def generate_chart(feed_dict):
    fig, ax = plt.subplots()
    ax.pie(feed_dict.values(), labels=feed_dict.keys(), autopct='%1.1f%%')
    ax.set_title("Feed Composition")
    return fig

def generate_pdf(feed_dict):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, 750, "Rosashi Farms - Feed Recipe Report")
    c.setFont("Helvetica", 12)
    y = 720
    for k, v in feed_dict.items():
        c.drawString(40, y, f"{k.capitalize()}: {v} grams")
        y -= 20
    c.save()
    buffer.seek(0)
    return buffer

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

if st.button("Calculate Feed"):
    feed = calculate_feed()
    st.subheader("Feed Requirement (grams/day):")
    for k, v in feed.items():
        st.write(f"- {k}: {v:.1f}g")
    
    st.subheader("📊 Feed Composition Chart")
    st.pyplot(generate_chart(feed))

    total_cost = 0
    st.subheader("💰 Estimated Daily Cost:")
    for k, v in feed.items():
        price_per_kg = ingredient_prices[k] / 50 if ingredient_prices[k] else 0
        cost = (v / 1000) * price_per_kg
        total_cost += cost
        st.write(f"- {k}: {cost:.2f} {currency}")
    st.write(f"**Total:** {total_cost:.2f} {currency}")

    df = pd.DataFrame([feed])
    st.download_button("📥 Download as Excel", data=to_excel(df), file_name="rosashi_feed_plan.xlsx")
    pdf_file = generate_pdf(feed)
    st.download_button("📄 Download PDF Report", data=pdf_file, file_name="rosashi_feed_plan.pdf")

    st.subheader("🖨️ Print Feed Plan")
    st.markdown('<script>window.print()</script>', unsafe_allow_html=True)
