from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import pycountry
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


st.set_page_config(
    page_title="Rosashi Farms Livestock Feed Planner",
    page_icon="🦆",
    layout="wide",
)


LIVESTOCK_DATA = {
    "Chickens": {
        "unit": "bird",
        "stages": {
            "Broiler starter (0-4 weeks)": {
                "daily_kg": 0.055,
                "feedings": 3,
                "ration": {
                    "corn": 40,
                    "soybean meal": 25,
                    "wheat bran": 8,
                    "fishmeal": 10,
                    "sunflower meal": 5,
                    "limestone": 2,
                    "premix": 5,
                    "salt": 1,
                    "dl methionine": 1,
                    "vegetable oil": 3,
                },
                "guidance": "Keep feed fresh and water available all day. Increase feeder space as birds grow.",
            },
            "Broiler grower (5-8 weeks)": {
                "daily_kg": 0.115,
                "feedings": 2,
                "ration": {
                    "corn": 42,
                    "soybean meal": 22,
                    "wheat bran": 10,
                    "fishmeal": 8,
                    "sunflower meal": 7,
                    "limestone": 3,
                    "premix": 4,
                    "salt": 1,
                    "dl methionine": 1,
                    "vegetable oil": 2,
                },
                "guidance": "Avoid sudden ration changes. Watch litter condition and remove wet feed quickly.",
            },
            "Layers laying (16+ weeks)": {
                "daily_kg": 0.12,
                "feedings": 2,
                "ration": {
                    "corn": 38,
                    "soybean meal": 20,
                    "wheat bran": 10,
                    "sunflower meal": 8,
                    "fishmeal": 5,
                    "limestone": 12,
                    "premix": 4,
                    "salt": 1,
                    "dl methionine": 1,
                    "vegetable oil": 1,
                },
                "guidance": "Calcium is important for laying birds. Provide clean water before morning feed.",
            },
        },
    },
    "Cattle": {
        "unit": "head",
        "stages": {
            "Calf starter": {
                "daily_kg": 2.5,
                "feedings": 2,
                "ration": {
                    "maize meal": 35,
                    "soybean meal": 18,
                    "wheat bran": 20,
                    "molasses": 8,
                    "hay": 12,
                    "mineral premix": 5,
                    "salt": 2,
                },
                "guidance": "Introduce starter gradually and keep roughage available. Milk plans should be managed separately.",
            },
            "Dairy cow in milk": {
                "daily_kg": 8.0,
                "feedings": 2,
                "ration": {
                    "hay": 35,
                    "silage": 30,
                    "maize meal": 16,
                    "soybean meal": 8,
                    "wheat bran": 6,
                    "molasses": 3,
                    "mineral premix": 1,
                    "salt": 1,
                },
                "guidance": "Split concentrate around milking and keep roughage available. Adjust for milk yield and body condition.",
            },
            "Beef grower/finisher": {
                "daily_kg": 7.0,
                "feedings": 2,
                "ration": {
                    "hay": 30,
                    "silage": 25,
                    "maize meal": 25,
                    "soybean meal": 8,
                    "wheat bran": 7,
                    "molasses": 3,
                    "mineral premix": 1,
                    "salt": 1,
                },
                "guidance": "Make grain increases slowly to reduce digestive upsets. Keep forage in the ration.",
            },
        },
    },
    "Goats": {
        "unit": "goat",
        "stages": {
            "Kid grower": {
                "daily_kg": 0.45,
                "feedings": 2,
                "ration": {
                    "hay": 45,
                    "maize meal": 18,
                    "soybean meal": 12,
                    "wheat bran": 15,
                    "molasses": 5,
                    "mineral premix": 3,
                    "salt": 2,
                },
                "guidance": "Offer clean forage daily and avoid abrupt grain increases.",
            },
            "Doe maintenance": {
                "daily_kg": 1.2,
                "feedings": 2,
                "ration": {
                    "hay": 65,
                    "maize meal": 10,
                    "wheat bran": 12,
                    "soybean meal": 5,
                    "molasses": 4,
                    "mineral premix": 3,
                    "salt": 1,
                },
                "guidance": "Forage should lead the diet. Increase feed for late pregnancy or milk production.",
            },
            "Dairy doe": {
                "daily_kg": 1.8,
                "feedings": 2,
                "ration": {
                    "hay": 50,
                    "maize meal": 16,
                    "wheat bran": 14,
                    "soybean meal": 10,
                    "molasses": 5,
                    "mineral premix": 4,
                    "salt": 1,
                },
                "guidance": "Feed after milking where possible and track body condition weekly.",
            },
        },
    },
    "Sheep": {
        "unit": "sheep",
        "stages": {
            "Lamb grower": {
                "daily_kg": 0.6,
                "feedings": 2,
                "ration": {
                    "hay": 45,
                    "maize meal": 22,
                    "soybean meal": 12,
                    "wheat bran": 13,
                    "molasses": 4,
                    "mineral premix": 3,
                    "salt": 1,
                },
                "guidance": "Keep forage available and introduce concentrate over several days.",
            },
            "Ewe maintenance": {
                "daily_kg": 1.4,
                "feedings": 2,
                "ration": {
                    "hay": 68,
                    "maize meal": 10,
                    "wheat bran": 12,
                    "soybean meal": 4,
                    "molasses": 3,
                    "mineral premix": 2,
                    "salt": 1,
                },
                "guidance": "Adjust upward in late pregnancy, cold weather, or poor pasture conditions.",
            },
        },
    },
    "Pigs": {
        "unit": "pig",
        "stages": {
            "Weaner": {
                "daily_kg": 1.0,
                "feedings": 3,
                "ration": {
                    "maize meal": 45,
                    "soybean meal": 24,
                    "wheat bran": 15,
                    "fishmeal": 6,
                    "vegetable oil": 3,
                    "limestone": 2,
                    "premix": 4,
                    "salt": 1,
                },
                "guidance": "Use smaller frequent meals and keep troughs clean to prevent stale feed.",
            },
            "Grower": {
                "daily_kg": 2.2,
                "feedings": 2,
                "ration": {
                    "maize meal": 50,
                    "soybean meal": 18,
                    "wheat bran": 20,
                    "fishmeal": 3,
                    "vegetable oil": 2,
                    "limestone": 2,
                    "premix": 4,
                    "salt": 1,
                },
                "guidance": "Keep water available at all times. Sort pigs by size if bullying affects intake.",
            },
            "Sow lactating": {
                "daily_kg": 5.5,
                "feedings": 3,
                "ration": {
                    "maize meal": 48,
                    "soybean meal": 22,
                    "wheat bran": 16,
                    "fishmeal": 4,
                    "vegetable oil": 3,
                    "limestone": 2,
                    "premix": 4,
                    "salt": 1,
                },
                "guidance": "Lactating sows need more feed and water. Increase meals if appetite is high.",
            },
        },
    },
    "Rabbits": {
        "unit": "rabbit",
        "stages": {
            "Grower": {
                "daily_kg": 0.12,
                "feedings": 2,
                "ration": {
                    "hay": 55,
                    "wheat bran": 18,
                    "maize meal": 10,
                    "soybean meal": 9,
                    "sunflower meal": 4,
                    "mineral premix": 3,
                    "salt": 1,
                },
                "guidance": "High fibre is important. Keep hay and clean water available.",
            },
            "Doe lactating": {
                "daily_kg": 0.25,
                "feedings": 2,
                "ration": {
                    "hay": 48,
                    "wheat bran": 18,
                    "maize meal": 13,
                    "soybean meal": 12,
                    "sunflower meal": 5,
                    "mineral premix": 3,
                    "salt": 1,
                },
                "guidance": "Increase feed gradually after kindling and watch kits for signs of poor milk supply.",
            },
        },
    },
    "Ducks": {
        "unit": "duck",
        "stages": {
            "Duckling starter (0-3 weeks)": {
                "daily_kg": 0.06,
                "feedings": 3,
                "ration": {
                    "village chicken feed": 70,
                    "maize bran": 25,
                    "fishmeal": 5,
                },
                "guidance": "Use village chicken feed as the main starter for ducklings, with a little maize bran. Provide shallow water near feed so ducklings can rinse their bills. Keep bedding dry.",
            },
            "Duck grower (4-8 weeks)": {
                "daily_kg": 0.14,
                "feedings": 2,
                "ration": {
                    "maize bran": 50,
                    "village chicken feed": 25,
                    "soybean meal": 12,
                    "fishmeal": 6,
                    "sunflower meal": 4,
                    "limestone": 2,
                    "salt": 1,
                },
                "guidance": "Shift more to maize bran as ducks grow. They forage well — use wide, shallow feeders with clean water nearby.",
            },
            "Layer duck (20+ weeks)": {
                "daily_kg": 0.17,
                "feedings": 2,
                "ration": {
                    "corn": 36,
                    "soybean meal": 22,
                    "wheat bran": 10,
                    "sunflower meal": 8,
                    "fishmeal": 5,
                    "limestone": 13,
                    "premix": 4,
                    "salt": 1,
                    "dl methionine": 1,
                },
                "guidance": "Laying ducks need extra calcium. Feed in the evening to support overnight egg formation.",
            },
        },
    },
    "Fish": {
        "unit": "fish",
        "stages": {
            "Tilapia fingerling": {
                "daily_kg": 0.003,
                "feedings": 4,
                "ration": {
                    "fishmeal": 28,
                    "soybean meal": 30,
                    "maize meal": 16,
                    "wheat bran": 12,
                    "vegetable oil": 4,
                    "premix": 8,
                    "salt": 2,
                },
                "guidance": "Feed small amounts several times daily and remove uneaten feed.",
            },
            "Tilapia grow-out": {
                "daily_kg": 0.02,
                "feedings": 3,
                "ration": {
                    "fishmeal": 18,
                    "soybean meal": 32,
                    "maize meal": 22,
                    "wheat bran": 14,
                    "vegetable oil": 4,
                    "premix": 8,
                    "salt": 2,
                },
                "guidance": "Adjust feeding to water temperature, fish size, and appetite.",
            },
        },
    },
}

# Lifecycle from young stock to sale (free-range farming)
# days_to_sale: typical days from start to market weight under free-range
# avg_daily_kg: average daily feed consumption across the lifecycle
# forage_offset_default: % reduction in purchased feed because animals forage
# typical_purchase_price_label: what you buy at the start
LIFECYCLE = {
    "Chickens": {
        "days_to_sale": 70,        # broiler raised free-range takes longer than 56d
        "avg_daily_kg": 0.085,
        "forage_offset_default": 30,
        "stock_label": "Day-old chick",
        "sale_label": "Live broiler at ~2.0 kg",
    },
    "Ducks": {
        "days_to_sale": 84,
        "avg_daily_kg": 0.110,
        "forage_offset_default": 40,   # ducks forage well, eat insects/greens
        "stock_label": "Duckling",
        "sale_label": "Live duck at ~2.5 kg",
    },
    "Cattle": {
        "days_to_sale": 540,           # 18 months for beef
        "avg_daily_kg": 6.0,
        "forage_offset_default": 60,   # mostly pasture
        "stock_label": "Weaner calf",
        "sale_label": "Finished beef ~400 kg liveweight",
    },
    "Goats": {
        "days_to_sale": 270,           # 9 months
        "avg_daily_kg": 0.9,
        "forage_offset_default": 55,
        "stock_label": "Weaned kid",
        "sale_label": "Live goat ~30 kg",
    },
    "Sheep": {
        "days_to_sale": 240,
        "avg_daily_kg": 1.0,
        "forage_offset_default": 55,
        "stock_label": "Weaned lamb",
        "sale_label": "Live sheep ~35 kg",
    },
    "Pigs": {
        "days_to_sale": 180,
        "avg_daily_kg": 1.8,
        "forage_offset_default": 25,   # pigs forage some but need feed
        "stock_label": "Weaner piglet",
        "sale_label": "Finished pig ~85 kg",
    },
    "Rabbits": {
        "days_to_sale": 90,
        "avg_daily_kg": 0.13,
        "forage_offset_default": 35,
        "stock_label": "Weaned kit",
        "sale_label": "Live rabbit ~2.0 kg",
    },
    "Fish": {
        "days_to_sale": 240,
        "avg_daily_kg": 0.012,
        "forage_offset_default": 15,   # pond fish get some natural food
        "stock_label": "Fingerling",
        "sale_label": "Tilapia ~400 g",
    },
}


CUSTOM_INGREDIENTS = [
    "village chicken feed",
    "maize bran",
    "corn",
    "maize meal",
    "soybean meal",
    "wheat bran",
    "fishmeal",
    "sunflower meal",
    "rice bran",
    "hay",
    "silage",
    "molasses",
    "limestone",
    "premix",
    "mineral premix",
    "salt",
    "dl methionine",
    "vegetable oil",
]

FEEDING_WINDOWS = {
    1: ["07:00"],
    2: ["07:00", "16:00"],
    3: ["06:30", "12:30", "17:30"],
    4: ["06:30", "10:30", "14:30", "17:30"],
}


def get_currencies():
    common = ["USD", "GBP", "EUR", "ZAR", "KES", "NGN", "GHS", "UGX", "TZS"]
    all_codes = sorted({currency.alpha_3 for currency in pycountry.currencies})
    return common + [code for code in all_codes if code not in common]


def profile_for(animal, stage):
    return LIVESTOCK_DATA[animal]["stages"][stage]


def normalize_ration(ration):
    total = sum(ration.values())
    if total <= 0:
        return {}
    return {ingredient: percentage / total for ingredient, percentage in ration.items()}


def calculate_group_plan(name, animal, stage, count, days, ration_override=None):
    profile = profile_for(animal, stage)
    ration = ration_override or profile["ration"]
    daily_total_kg = profile["daily_kg"] * count
    normalized = normalize_ration(ration)
    rows = []

    for ingredient, share in normalized.items():
        daily_kg = daily_total_kg * share
        rows.append(
            {
                "Group": name,
                "Animal": animal,
                "Stage": stage,
                "Ingredient": ingredient,
                "Daily kg": daily_kg,
                "Plan kg": daily_kg * days,
                "Ration %": share * 100,
            }
        )

    return pd.DataFrame(rows)


def build_schedule(name, animal, stage, count, days):
    profile = profile_for(animal, stage)
    feedings = profile["feedings"]
    daily_total_kg = profile["daily_kg"] * count
    times = FEEDING_WINDOWS.get(feedings, FEEDING_WINDOWS[2])
    amount_per_feeding = daily_total_kg / len(times)

    return pd.DataFrame(
        {
            "Group": name,
            "Animal": animal,
            "Stage": stage,
            "Feeding time": times,
            "Kg per feeding": [amount_per_feeding] * len(times),
            "Feedings per day": [len(times)] * len(times),
            "Plan days": [days] * len(times),
        }
    )


def add_costs(feed_df, prices, bag_size):
    priced = feed_df.copy()
    priced["Price per bag"] = priced["Ingredient"].map(prices).fillna(0.0)
    priced["Cost per kg"] = priced["Price per bag"] / bag_size
    priced["Plan cost"] = priced["Plan kg"] * priced["Cost per kg"]
    priced["Bags needed"] = priced["Plan kg"] / bag_size
    return priced


def dataframe_to_excel(sheets):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for sheet_name, dataframe in sheets.items():
            dataframe.to_excel(writer, sheet_name=sheet_name[:31], index=False)
    return output.getvalue()


def generate_pdf_report(feed_df, schedule_df, currency, total_cost):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 48

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(40, y, "Farm Feed Planner")
    y -= 22
    pdf.setFont("Helvetica", 10)
    pdf.drawString(40, y, "Planning guide only. Confirm final rations with a local livestock nutrition expert.")
    y -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, y, f"Total estimated plan cost: {total_cost:,.2f} {currency}")
    y -= 24

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(40, y, "Feed Requirements")
    y -= 16
    pdf.setFont("Helvetica", 9)

    summary = feed_df.groupby(["Group", "Ingredient"], as_index=False).agg({"Plan kg": "sum", "Plan cost": "sum"})
    for _, row in summary.head(28).iterrows():
        if y < 70:
            pdf.showPage()
            y = height - 48
            pdf.setFont("Helvetica", 9)
        pdf.drawString(
            40,
            y,
            f"{row['Group']} - {row['Ingredient']}: {row['Plan kg']:.1f} kg, {row['Plan cost']:.2f} {currency}",
        )
        y -= 14

    y -= 10
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(40, y, "Daily Feeding Times")
    y -= 16
    pdf.setFont("Helvetica", 9)

    for _, row in schedule_df.head(32).iterrows():
        if y < 70:
            pdf.showPage()
            y = height - 48
            pdf.setFont("Helvetica", 9)
        pdf.drawString(
            40,
            y,
            f"{row['Group']} - {row['Feeding time']}: {row['Kg per feeding']:.2f} kg",
        )
        y -= 14

    pdf.save()
    buffer.seek(0)
    return buffer


def plot_feed_mix(feed_df):
    ingredient_totals = feed_df.groupby("Ingredient", as_index=False)["Plan kg"].sum()
    ingredient_totals = ingredient_totals.sort_values("Plan kg", ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(ingredient_totals["Ingredient"], ingredient_totals["Plan kg"], color="#3f7d58")
    ax.set_ylabel("Kg for plan")
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return fig



ANIMAL_EMOJI = {
    "Chickens": "🐔",
    "Ducks": "🦆",
    "Cattle": "🐄",
    "Goats": "🐐",
    "Sheep": "🐑",
    "Pigs": "🐖",
    "Rabbits": "🐇",
    "Fish": "🐟",
}


def reset_custom_ration(animal, stage):
    profile = profile_for(animal, stage)
    st.session_state.custom_ration = dict(profile["ration"])


def go_to_step(step):
    st.session_state.step = step


# ---- Session state ----
if "farm_groups" not in st.session_state:
    st.session_state.farm_groups = []
if "step" not in st.session_state:
    st.session_state.step = 1
if "w_animal" not in st.session_state:
    st.session_state.w_animal = None
if "w_stage" not in st.session_state:
    st.session_state.w_stage = None
if "w_count" not in st.session_state:
    st.session_state.w_count = 25
if "w_days" not in st.session_state:
    st.session_state.w_days = 30
if "w_group_name" not in st.session_state:
    st.session_state.w_group_name = "My group"
if "s_currency" not in st.session_state:
    st.session_state.s_currency = "ZMW"
if "s_bag_size" not in st.session_state:
    st.session_state.s_bag_size = 50.0
if "s_default_days" not in st.session_state:
    st.session_state.s_default_days = 30
if "s_prices" not in st.session_state:
    st.session_state.s_prices = {ing: 0.0 for ing in CUSTOM_INGREDIENTS}
if "custom_ration" not in st.session_state:
    first_animal = next(iter(LIVESTOCK_DATA))
    first_stage = next(iter(LIVESTOCK_DATA[first_animal]["stages"]))
    st.session_state.custom_ration = dict(profile_for(first_animal, first_stage)["ration"])


# ---- Styles ----
st.markdown(
    """
    <style>
    html, body, [class*="css"] { font-size: 18px; }
    .stApp {
        background: linear-gradient(180deg, #f6fbf2 0%, #eef6e4 100%);
        color: #1f2d24;
    }
    .block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1100px; }
    .farm-hero {
        background: linear-gradient(135deg, #2c5e3f 0%, #3f7d58 100%);
        color: #ffffff;
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 6px 18px rgba(63, 125, 88, 0.18);
    }
    .farm-hero h1 { margin: 0; font-size: 2.2rem; font-weight: 800; }
    .farm-hero p { margin: 0.4rem 0 0 0; font-size: 1.1rem; opacity: 0.95; }

    /* Big readable text everywhere */
    .stMarkdown p, .stMarkdown li, .stMarkdown span { color: #1f2d24; }
    .stMarkdown p { font-size: 1.05rem; line-height: 1.55; }
    h1 { font-size: 2.1rem !important; }
    h2 { font-size: 1.6rem !important; color: #2c5e3f !important; }
    h3 { font-size: 1.3rem !important; color: #2c5e3f !important; }

    /* Step pill bar */
    .step-bar { display: flex; gap: 0.5rem; margin: 0.4rem 0 1.4rem 0; flex-wrap: wrap; }
    .step-pill {
        flex: 1; min-width: 140px;
        padding: 0.7rem 0.9rem;
        border-radius: 12px;
        background: #ffffff;
        border: 2px solid #d4e6c8;
        color: #6b7a6f;
        font-weight: 600; font-size: 1rem;
        text-align: center;
    }
    .step-pill.active { background: #3f7d58; color: white; border-color: #3f7d58; }
    .step-pill.done { background: #d4ecdc; color: #2c5e3f; border-color: #b6dcc4; }

    /* Buttons — ensure readable */
    .stButton > button {
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.8rem 1.2rem;
        min-height: 3.2rem;
        background: #ffffff !important;
        color: #1f2d24 !important;
        border: 2px solid #cfe1c2 !important;
        box-shadow: 0 1px 3px rgba(60,100,70,0.08);
    }
    .stButton > button:hover {
        background: #f1f7ea !important;
        border-color: #3f7d58 !important;
        color: #1f2d24 !important;
    }
    .stButton > button p, .stButton > button div, .stButton > button span {
        color: inherit !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    .stButton > button[kind="primary"] {
        background: #3f7d58 !important;
        color: #ffffff !important;
        border-color: #3f7d58 !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: #2c5e3f !important;
        border-color: #2c5e3f !important;
        color: #ffffff !important;
    }
    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] div,
    .stButton > button[kind="primary"] span {
        color: #ffffff !important;
    }
    /* Download buttons too */
    .stDownloadButton > button {
        background: #ffffff !important;
        color: #1f2d24 !important;
        border: 2px solid #cfe1c2 !important;
        font-weight: 700 !important;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        border: 1px solid #d4e6c8;
        border-radius: 12px;
        padding: 1rem 1.1rem;
        background: #ffffff;
        box-shadow: 0 1px 3px rgba(60,100,70,0.06);
    }
    div[data-testid="stMetricLabel"] { font-size: 1rem; color: #4a5a4f; font-weight: 600; }
    div[data-testid="stMetricValue"] { color: #2c5e3f; font-weight: 800; font-size: 1.7rem; }

    /* Inputs */
    input, .stNumberInput input, .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        font-size: 1.1rem !important;
    }
    label { font-size: 1.05rem !important; font-weight: 600 !important; color: #2c5e3f !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.4rem; background: rgba(255,255,255,0.6);
        padding: 0.3rem; border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px; padding: 0.6rem 1.2rem;
        font-weight: 700; font-size: 1.05rem;
        color: #2c5e3f !important;
    }
    .stTabs [data-baseweb="tab"] p {
        color: #2c5e3f !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    .stTabs [aria-selected="true"] { background: #3f7d58 !important; color: white !important; }
    .stTabs [aria-selected="true"] p { color: #ffffff !important; }

    /* Expander header readable */
    .stExpander summary, .stExpander summary p,
    details summary, details summary p {
        color: #2c5e3f !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary div {
        color: #2c5e3f !important;
        font-weight: 700 !important;
    }

    /* Note card */
    .small-note {
        color: #2f3d33; font-size: 1rem; line-height: 1.5;
        background: #f1f7ea; padding: 0.8rem 1rem;
        border-radius: 10px; border-left: 4px solid #5ea87a;
        margin: 0.6rem 0;
    }

    section[data-testid="stSidebar"] {
        background: #ffffff; border-right: 1px solid #d4e6c8;
    }

    /* Big numbers in results */
    .big-num { font-size: 2rem; font-weight: 800; color: #2c5e3f; }
    .big-label { color: #4a5a4f; font-size: 0.95rem; font-weight: 600; }

    /* Selected animal banner */
    .picked {
        background: #ffffff; border: 2px solid #3f7d58;
        border-radius: 12px; padding: 0.8rem 1rem;
        font-size: 1.1rem; font-weight: 600; color: #2c5e3f;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---- Hero ----
st.markdown(
    """
    <div class="farm-hero">
        <h1>🦆 Rosashi Farms Livestock Feed Planner</h1>
        <p>Make a feeding plan in 5 simple steps.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---- Sidebar: just reset ----
with st.sidebar:
    st.header("Menu")
    st.markdown(
        f"**Currency:** {st.session_state.s_currency}  \n"
        f"**Bag size:** {st.session_state.s_bag_size:.0f} kg  \n"
        f"**Default days:** {st.session_state.s_default_days}"
    )
    st.divider()
    if st.button("🔄 Start Over", use_container_width=True):
        st.session_state.step = 1
        st.session_state.w_animal = None
        st.session_state.w_stage = None
        st.rerun()
    if st.button("💰 Edit Finance / Costs", use_container_width=True):
        st.session_state.step = 2
        st.rerun()

# Active values used by all steps
currency = st.session_state.s_currency
bag_size = st.session_state.s_bag_size
default_days = st.session_state.s_default_days
prices = st.session_state.s_prices


# ---- Tabs ----
tab_plan, tab_farm, tab_reference = st.tabs(["📋 Quick Plan", "🚜 My Farm Plan", "📖 Feed Guide"])


def render_step_bar(current):
    labels = ["1. Animal", "2. Finance", "3. Age / Type", "4. How Many", "5. Your Plan"]
    pills = []
    for i, label in enumerate(labels, start=1):
        cls = "active" if i == current else ("done" if i < current else "")
        pills.append(f'<div class="step-pill {cls}">{label}</div>')
    st.markdown(f'<div class="step-bar">{"".join(pills)}</div>', unsafe_allow_html=True)


with tab_plan:
    render_step_bar(st.session_state.step)

    # ---- STEP 1: Animal ----
    if st.session_state.step == 1:
        st.subheader("Step 1 — Choose your animal")
        st.markdown("Tap the animal you want to feed.")
        animals = list(LIVESTOCK_DATA.keys())
        cols_per_row = 4
        for i in range(0, len(animals), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, animal in enumerate(animals[i:i + cols_per_row]):
                emoji = ANIMAL_EMOJI.get(animal, "🐾")
                if cols[j].button(f"{emoji}  {animal}", key=f"pick_{animal}", use_container_width=True):
                    st.session_state.w_animal = animal
                    st.session_state.w_stage = None
                    st.session_state.step = 2
                    st.rerun()

    # ---- STEP 2: Finance / Costs ----
    elif st.session_state.step == 2:
        animal = st.session_state.w_animal
        emoji = ANIMAL_EMOJI.get(animal, "🐾")
        if animal:
            st.markdown(
                f'<div class="picked">Selected: {emoji} {animal}</div>',
                unsafe_allow_html=True,
            )
        st.subheader("Step 2 — Finance / Costs")
        st.markdown(
            "<div class='small-note'>Set your money and bag details. "
            "Feed prices are optional — fill in only the ones you buy.</div>",
            unsafe_allow_html=True,
        )

        currency_options = ["ZMW", "USD", "GBP", "EUR", "ZAR", "KES", "TZS", "UGX"]
        other = [c for c in get_currencies() if c not in currency_options]
        all_currencies = currency_options + other
        current_currency_idx = all_currencies.index(st.session_state.s_currency) \
            if st.session_state.s_currency in all_currencies else 0

        f1, f2, f3 = st.columns(3)
        with f1:
            new_currency = st.selectbox("Currency", all_currencies, index=current_currency_idx)
        with f2:
            new_bag = st.number_input(
                "Bag size (kg)", min_value=1.0,
                value=float(st.session_state.s_bag_size), step=1.0,
            )
        with f3:
            new_default_days = st.number_input(
                "Default plan length (days)", min_value=1,
                value=int(st.session_state.s_default_days), step=1,
            )

        st.markdown("### 💰 Feed Prices (optional)")
        st.caption("Per bag price for each ingredient you buy. Leave at 0 to skip.")
        new_prices = {}
        cols = st.columns(2)
        for i, ingredient in enumerate(CUSTOM_INGREDIENTS):
            with cols[i % 2]:
                new_prices[ingredient] = st.number_input(
                    f"{ingredient.title()} per bag",
                    min_value=0.0, step=1.0,
                    value=float(st.session_state.s_prices.get(ingredient, 0.0)),
                    key=f"price_{ingredient}",
                )

        st.markdown("---")
        b1, b2 = st.columns([0.35, 0.65])
        if b1.button("⬅️  Back", key="back_to_1"):
            st.session_state.s_currency = new_currency
            st.session_state.s_bag_size = float(new_bag)
            st.session_state.s_default_days = int(new_default_days)
            st.session_state.s_prices = new_prices
            st.session_state.step = 1
            st.rerun()
        if b2.button("Continue  ➡️", key="to_step_3", type="primary", use_container_width=True):
            st.session_state.s_currency = new_currency
            st.session_state.s_bag_size = float(new_bag)
            st.session_state.s_default_days = int(new_default_days)
            st.session_state.s_prices = new_prices
            st.session_state.w_days = int(new_default_days)
            st.session_state.step = 3
            st.rerun()

    # ---- STEP 3: Stage ----
    elif st.session_state.step == 3:
        animal = st.session_state.w_animal
        emoji = ANIMAL_EMOJI.get(animal, "🐾")
        st.markdown(f'<div class="picked">Selected: {emoji} {animal}</div>', unsafe_allow_html=True)
        st.subheader("Step 3 — Choose age or type")
        st.markdown("Tap the option that matches your animals.")

        stages = list(LIVESTOCK_DATA[animal]["stages"].keys())
        for stage in stages:
            data = LIVESTOCK_DATA[animal]["stages"][stage]
            label = f"**{stage}**  —  {data['daily_kg']} kg per {LIVESTOCK_DATA[animal]['unit']} per day"
            if st.button(label, key=f"stage_{stage}", use_container_width=True):
                st.session_state.w_stage = stage
                st.session_state.step = 4
                st.rerun()

        st.markdown("---")
        if st.button("⬅️  Back", key="back_to_2"):
            st.session_state.step = 2
            st.rerun()

    # ---- STEP 4: Count + Days ----
    elif st.session_state.step == 4:
        animal = st.session_state.w_animal
        stage = st.session_state.w_stage
        emoji = ANIMAL_EMOJI.get(animal, "🐾")
        unit = LIVESTOCK_DATA[animal]["unit"]
        st.markdown(
            f'<div class="picked">Selected: {emoji} {animal} — {stage}</div>',
            unsafe_allow_html=True,
        )
        st.subheader("Step 4 — How many and how long?")

        c1, c2 = st.columns(2)
        with c1:
            count = st.number_input(
                f"Number of {unit}s",
                min_value=1,
                value=int(st.session_state.w_count),
                step=1,
            )
            st.session_state.w_count = int(count)
        with c2:
            days = st.number_input(
                "Plan length (days)",
                min_value=1,
                value=int(st.session_state.w_days),
                step=1,
            )
            st.session_state.w_days = int(days)

        group_name = st.text_input("Name this group (optional)", value=st.session_state.w_group_name)
        st.session_state.w_group_name = group_name

        st.markdown("---")
        b1, b2 = st.columns([0.4, 0.6])
        if b1.button("⬅️  Back", key="back_to_3"):
            st.session_state.step = 3
            st.rerun()
        if b2.button("See My Plan  ➡️", key="to_step_5", type="primary", use_container_width=True):
            st.session_state.step = 5
            st.rerun()

    # ---- STEP 5: Results ----
    elif st.session_state.step == 5:
        animal = st.session_state.w_animal
        stage = st.session_state.w_stage
        count = int(st.session_state.w_count)
        days = int(st.session_state.w_days)
        group_name = st.session_state.w_group_name or "My group"
        emoji = ANIMAL_EMOJI.get(animal, "🐾")

        st.markdown(
            f'<div class="picked">{emoji} {animal} — {stage} — {count} animals — {days} days</div>',
            unsafe_allow_html=True,
        )

        profile = profile_for(animal, stage)
        st.markdown(f"<div class='small-note'>💡 {profile['guidance']}</div>", unsafe_allow_html=True)

        ration = dict(profile["ration"])
        preview_df = calculate_group_plan(group_name, animal, stage, count, days, ration)
        preview_df = add_costs(preview_df, prices, bag_size)
        schedule_df = build_schedule(group_name, animal, stage, count, days)

        daily_kg = profile["daily_kg"] * count
        total_kg = daily_kg * days
        estimated_cost = preview_df["Plan cost"].sum()

        m = st.columns(3)
        m[0].metric("Feed per day", f"{daily_kg:,.2f} kg")
        m[1].metric(f"Feed for {days} days", f"{total_kg:,.1f} kg")
        m[2].metric("Estimated cost", f"{estimated_cost:,.2f} {currency}")

        st.subheader("🌾 Feed Mix")
        st.dataframe(
            preview_df[
                ["Ingredient", "Ration %", "Daily kg", "Plan kg", "Bags needed", "Plan cost"]
            ].style.format({
                "Ration %": "{:.1f}",
                "Daily kg": "{:.2f}",
                "Plan kg": "{:.1f}",
                "Bags needed": "{:.2f}",
                "Plan cost": "{:.2f}",
            }),
            use_container_width=True,
            hide_index=True,
        )

        # ---- Lifetime / sale cost (free-range) ----
        if animal in LIFECYCLE:
            lc = LIFECYCLE[animal]
            st.subheader("🌱 Lifetime Cost (free-range, to sale)")
            st.markdown(
                "<div class='small-note'>Free-range animals forage on grass, insects, "
                "and kitchen scraps, so they need <b>less purchased feed</b>. "
                "Adjust the forage saving below to match your farm.</div>",
                unsafe_allow_html=True,
            )

            lc1, lc2, lc3 = st.columns(3)
            with lc1:
                forage_pct = st.slider(
                    "Forage saving (%)",
                    min_value=0, max_value=80,
                    value=int(lc["forage_offset_default"]),
                    step=5,
                    help="How much purchased feed you save because animals forage freely.",
                )
            with lc2:
                days_to_sale = st.number_input(
                    "Days to sale",
                    min_value=30, max_value=1095,
                    value=int(lc["days_to_sale"]),
                    step=10,
                )
            with lc3:
                stock_price = st.number_input(
                    f"{lc['stock_label']} price each",
                    min_value=0.0, value=0.0, step=1.0,
                    help="What you pay per young animal at the start.",
                )

            # Cost per kg of feed (weighted by ration share)
            normalized = normalize_ration(ration)
            cost_per_kg_of_mix = sum(
                normalized.get(ing, 0) * (prices.get(ing, 0.0) / bag_size)
                for ing in normalized
            )

            forage_factor = 1 - (forage_pct / 100.0)
            lifetime_kg_per_animal = lc["avg_daily_kg"] * days_to_sale * forage_factor
            lifetime_kg_total = lifetime_kg_per_animal * count
            lifetime_feed_cost = lifetime_kg_total * cost_per_kg_of_mix
            lifetime_stock_cost = stock_price * count
            lifetime_total = lifetime_feed_cost + lifetime_stock_cost
            cost_per_animal = lifetime_total / count if count else 0

            lm = st.columns(4)
            lm[0].metric("Days to sale", f"{days_to_sale}")
            lm[1].metric("Feed kg total", f"{lifetime_kg_total:,.0f} kg")
            lm[2].metric("Total cost", f"{lifetime_total:,.0f} {currency}")
            lm[3].metric("Cost per animal", f"{cost_per_animal:,.0f} {currency}")

            st.markdown(
                f"<div class='small-note'>"
                f"<b>Plan:</b> Raise {count} {animal.lower()} from <i>{lc['stock_label'].lower()}</i> "
                f"to <i>{lc['sale_label'].lower()}</i> over {days_to_sale} days, free-range.<br>"
                f"<b>Feed cost:</b> {lifetime_feed_cost:,.0f} {currency} &nbsp;·&nbsp; "
                f"<b>Stock cost:</b> {lifetime_stock_cost:,.0f} {currency} &nbsp;·&nbsp; "
                f"<b>Forage saving applied:</b> {forage_pct}%"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.subheader("🕒 Daily Feeding Times")
        st.dataframe(
            schedule_df[["Feeding time", "Kg per feeding", "Feedings per day"]].style.format(
                {"Kg per feeding": "{:.2f}"}
            ),
            use_container_width=True,
            hide_index=True,
        )

        with st.expander("🔧 Advanced — adjust the ration mix"):
            if st.button("Reset to default ration"):
                reset_custom_ration(animal, stage)
                st.rerun()
            active_ingredients = st.multiselect(
                "Ingredients in this ration",
                CUSTOM_INGREDIENTS,
                default=list(ration.keys()),
            )
            custom_ration = {}
            for ingredient in active_ingredients:
                default_value = float(
                    st.session_state.custom_ration.get(ingredient, ration.get(ingredient, 0))
                )
                custom_ration[ingredient] = st.number_input(
                    f"{ingredient.title()} %",
                    min_value=0.0, max_value=100.0,
                    value=default_value, step=0.5,
                    key=f"ration_{animal}_{stage}_{ingredient}",
                )
            if custom_ration and st.button("Apply custom ration"):
                st.session_state.custom_ration = custom_ration
                st.rerun()

        st.markdown("---")
        b1, b2, b3 = st.columns([0.33, 0.34, 0.33])
        if b1.button("⬅️  Back", key="back_to_4"):
            st.session_state.step = 4
            st.rerun()
        if b2.button("➕ Add to My Farm Plan", type="primary", use_container_width=True):
            st.session_state.farm_groups.append({
                "name": group_name,
                "animal": animal,
                "stage": stage,
                "count": count,
                "days": days,
                "ration": ration,
            })
            st.success(f"Added {group_name} to your Farm Plan.")
        if b3.button("🔄 Plan Another Animal", use_container_width=True):
            st.session_state.step = 1
            st.session_state.w_animal = None
            st.session_state.w_stage = None
            st.rerun()


with tab_farm:
    st.subheader("🚜 My Farm Plan")
    if not st.session_state.farm_groups:
        st.info("No groups yet. Use the Quick Plan tab to add an animal group.")
    else:
        farm_feed_frames = []
        farm_schedule_frames = []
        group_rows = []

        for group in st.session_state.farm_groups:
            feed_df = calculate_group_plan(
                group["name"], group["animal"], group["stage"],
                group["count"], group["days"], group["ration"],
            )
            farm_feed_frames.append(feed_df)
            farm_schedule_frames.append(
                build_schedule(group["name"], group["animal"], group["stage"], group["count"], group["days"])
            )
            profile = profile_for(group["animal"], group["stage"])
            group_rows.append({
                "Group": group["name"],
                "Animal": group["animal"],
                "Stage": group["stage"],
                "Count": group["count"],
                "Days": group["days"],
                "Daily kg": profile["daily_kg"] * group["count"],
            })

        farm_feed = add_costs(pd.concat(farm_feed_frames, ignore_index=True), prices, bag_size)
        farm_schedule = pd.concat(farm_schedule_frames, ignore_index=True)
        groups_df = pd.DataFrame(group_rows)
        ingredient_summary = farm_feed.groupby("Ingredient", as_index=False).agg({
            "Daily kg": "sum", "Plan kg": "sum",
            "Bags needed": "sum", "Plan cost": "sum",
        })

        total_daily = farm_feed["Daily kg"].sum()
        total_plan = farm_feed["Plan kg"].sum()
        total_cost = farm_feed["Plan cost"].sum()

        m = st.columns(4)
        m[0].metric("Groups", len(st.session_state.farm_groups))
        m[1].metric("Daily feed", f"{total_daily:,.2f} kg")
        m[2].metric("Plan feed", f"{total_plan:,.1f} kg")
        m[3].metric("Plan cost", f"{total_cost:,.2f} {currency}")

        st.pyplot(plot_feed_mix(farm_feed), use_container_width=True)

        st.subheader("🐾 Groups")
        st.dataframe(
            groups_df.style.format({"Daily kg": "{:.2f}"}),
            use_container_width=True, hide_index=True,
        )

        st.subheader("🛒 Shopping List")
        st.dataframe(
            ingredient_summary.style.format({
                "Daily kg": "{:.2f}", "Plan kg": "{:.1f}",
                "Bags needed": "{:.2f}", "Plan cost": "{:.2f}",
            }),
            use_container_width=True, hide_index=True,
        )

        st.subheader("🕒 Feeding Schedule")
        st.dataframe(
            farm_schedule.style.format({"Kg per feeding": "{:.2f}"}),
            use_container_width=True, hide_index=True,
        )

        excel_file = dataframe_to_excel({
            "Groups": groups_df,
            "Shopping List": ingredient_summary,
            "Feed Details": farm_feed,
            "Schedule": farm_schedule,
        })
        pdf_file = generate_pdf_report(farm_feed, farm_schedule, currency, total_cost)

        d = st.columns([0.33, 0.33, 0.34])
        d[0].download_button(
            "📥 Download Excel", data=excel_file,
            file_name="farm_feed_plan.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
        d[1].download_button(
            "📄 Download PDF", data=pdf_file,
            file_name="farm_feed_plan.pdf", mime="application/pdf",
            use_container_width=True,
        )
        if d[2].button("🗑️ Clear Farm Plan", use_container_width=True):
            st.session_state.farm_groups = []
            st.rerun()


with tab_reference:
    st.subheader("📖 Feed Guide")
    st.markdown(
        "These rations are starting templates. Local forage, breed, age, weather, "
        "and ingredient availability can change the right answer."
    )

    for animal_name, animal_data in LIVESTOCK_DATA.items():
        emoji = ANIMAL_EMOJI.get(animal_name, "🐾")
        with st.expander(f"{emoji} {animal_name}"):
            for stage_name, stage_data in animal_data["stages"].items():
                ration_text = ", ".join(
                    f"{ingredient} {percentage}%"
                    for ingredient, percentage in stage_data["ration"].items()
                )
                st.markdown(f"**{stage_name}**")
                st.write(
                    f"{stage_data['daily_kg']} kg per {animal_data['unit']} per day, "
                    f"{stage_data['feedings']} feeding(s) daily."
                )
                st.caption(ration_text)
                st.write(stage_data["guidance"])

    st.warning(
        "Use this app for planning and budgeting, not as veterinary or nutrition diagnosis. "
        "Confirm final rations with a qualified local adviser before changing feed for vulnerable animals."
    )
