import streamlit as st
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="Travel Itinerary AI", page_icon="🧳", layout="centered")

st.title("🧳 Travel Itinerary AI")
st.markdown("Generate your travel itinerary from Gmail & Drive bookings with AI.")

st.header("📋 Enter your trip preferences:")

# Inputs
col1, col2 = st.columns(2)

with col1:
    after_date = st.date_input(
        "Start Date",
        value=datetime.today() - timedelta(days=30)
    )

with col2:
    before_date = st.date_input(
        "End Date",
        value=datetime.today()
    )

max_emails = st.number_input("Maximum Emails", min_value=1, max_value=20, value=5)
max_drive_files = st.number_input("Maximum Drive Files", min_value=1, max_value=20, value=5)

if st.button("🚀 Fetch Itinerary"):
    with st.spinner("Fetching your itinerary..."):
        url = "https://your-fastapi-backend.onrender.com/trips/build"  # ⬅️ replace with your real backend URL!

        payload = {
            "after_date": after_date.strftime("%Y-%m-%d"),
            "before_date": before_date.strftime("%Y-%m-%d"),
            "max_emails": max_emails,
            "max_drive_files": max_drive_files
        }

        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            trip = response.json()

            st.success("🎉 Itinerary generated!")

            st.header(f"🗺️ {trip['name']}")
            st.subheader(f"{trip['start_date']} → {trip['end_date']}")

            for item in trip["itinerary"]:
                st.write(f"**Day {item['day']}**: {item['activity']}")

        except Exception as e:
            st.error(f"❌ Failed to fetch itinerary: {e}")
