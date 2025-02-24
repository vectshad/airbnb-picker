import streamlit as st
import pandas as pd

# Load the data
@st.cache_data
def load_data():
    df = pd.read_excel("airbnb.xlsx")
    df.columns = df.columns.str.strip()  # Remove spaces in column names
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Options")
min_bedroom, max_bedroom = int(df["bedroom"].min()), int(df["bedroom"].max())
bedroom_filter = st.sidebar.slider("Minimum Bedrooms", min_bedroom, max_bedroom, min_bedroom)
min_reviews = st.sidebar.slider("Minimum Reviews", 0, df["reviewer"].max(), 50)
max_price = st.sidebar.slider("Maximum Price (IDR)", df["price_in_IDR"].min(), df["price_in_IDR"].max(), df["price_in_IDR"].max())
max_distance = st.sidebar.slider("Max Distance to Pratunam (KM)", 0.0, df["distance_to_pratunam"].max(), df["distance_to_pratunam"].max())

# Apply Filters
filtered_df = df[
    (df["bedroom"] >= bedroom_filter) &
    (df["reviewer"] >= min_reviews) &
    (df["price_in_IDR"] <= max_price) &
    (df["distance_to_pratunam"] <= max_distance)
]

# Display Results
st.title("🏡 Airbnb Selection Dashboard")
st.write(f"Showing {len(filtered_df)} results")

for _, row in filtered_df.iterrows():
    st.subheader(row["airbnb_name"])
    st.write(f"**Pros:** {row['pros']}")
    st.write(f"🛏️ **Bedrooms:** {row['bedroom']}") 
    st.write(f"⭐ **Rating:** {row['review']} ({row['reviewer']} reviews)")
    st.write(f"📍 **Distance to Pratunam:** {row['distance_to_pratunam']} KM")
    st.write(f"💰 **Price:** Rp {row['price_in_IDR']:,}")
    st.markdown(f"[🔗 View on Airbnb]({row['link']})", unsafe_allow_html=True)
    
    if pd.notna(row["image_url"]):  
        st.image(row["image_url"], caption=row["airbnb_name"], use_container_width=True)

    st.markdown("---")  # Separator between listings
