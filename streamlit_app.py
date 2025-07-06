import streamlit as st
import requests
import os
from datetime import date

BACKEND_URL = os.getenv("BACKEND_URL", "https://travel-itinerary-ai.onrender.com")

st.set_page_config(page_title="🧳 Travel Itinerary AI", page_icon="🧳")

st.title("🧳 Travel Itinerary AI")
st.write("Generate your travel itinerary from Gmail bookings powered by AI.")

if "labels" not in st.session_state:
    st.session_state.labels = []
if "selected_label" not in st.session_state:
    st.session_state.selected_label = None

if st.button("🔄 Fetch Gmail Labels"):
    try:
        res = requests.get(f"{BACKEND_URL}/labels", timeout=60)
        res.raise_for_status()
        st.session_state.labels = res.json().get("labels", [])
        if st.session_state.labels:
            st.session_state.selected_label = st.session_state.labels[0]
            st.success("✅ Labels fetched successfully.")
        else:
            st.error("⚠️ No labels found.")
    except Exception as e:
        st.error(f"❌ Failed to fetch labels: {e}")

if st.session_state.labels:
    st.session_state.selected_label = st.selectbox(
        "📂 Select Gmail Label",
        st.session_state.labels,
        index=st.session_state.labels.index(st.session_state.selected_label)
        if st.session_state.selected_label in st.session_state.labels
        else 0,
    )

st.header("📅 Trip Preferences")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", date.today())
with col2:
    end_date = st.date_input("End Date", date.today())

max_emails = st.number_input("Maximum Emails", min_value=0, value=5)

if st.button("🚀 Build Itinerary"):
    if not st.session_state.selected_label:
        st.error("Please fetch and select a Gmail label first.")
    else:
        payload = {
            "after_date": start_date.strftime("%Y-%m-%d"),
            "before_date": end_date.strftime("%Y-%m-%d"),
            "max_emails": max_emails,
            "label_name": st.session_state.selected_label,
        }

        st.write("Payload:", payload)

        try:
            res = requests.post(f"{BACKEND_URL}/trips/build", json=payload, timeout=120)
            if res.ok:
                itinerary = res.json().get("itinerary", "No itinerary found.")
                st.success("✅ Itinerary generated successfully!")
                st.text_area("📋 Your Itinerary", itinerary, height=300)
            else:
                st.error(f"❌ Error {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"❌ Request failed: {e}")
