import streamlit as st
import requests
import os

st.set_page_config(page_title="🧳 Travel Itinerary AI", page_icon="🧳")

# Your backend URL
BACKEND_URL = os.getenv("BACKEND_URL", "https://travel-itinerary-ai.onrender.com")

st.title("🧳 Travel Itinerary AI")
st.write("Generate your travel itinerary from Gmail bookings powered by AI.")

st.header("📅 Enter your trip preferences:")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date")
with col2:
    end_date = st.date_input("End Date")

max_emails = st.number_input("Maximum Emails", min_value=0, value=5)
max_drive_files = st.number_input("Maximum Drive Files", min_value=0, value=0)

if st.button("🚀 Fetch Itinerary"):
    if not start_date or not end_date:
        st.error("Please select both start and end dates.")
    else:
        payload = {
            "after_date": start_date.strftime("%Y-%m-%d"),
            "before_date": end_date.strftime("%Y-%m-%d"),
            "max_emails": max_emails,
            "max_drive_files": max_drive_files,
        }

        st.write("Sending payload:", payload)

        try:
            response = requests.post(
                f"{BACKEND_URL}/trips/build",
                json=payload,
                timeout=60
            )
            if response.status_code == 200:
                itinerary = response.json().get("itinerary", "No itinerary found.")
                st.success("✅ Itinerary generated successfully!")
                st.text_area("📋 Your Itinerary", itinerary, height=300)
            else:
                st.error(f"❌ Error {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"❌ Request failed: {e}")
