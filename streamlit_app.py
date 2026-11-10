import streamlit as st

st.set_page_config(page_title="Airbnb Co-Host", page_icon="🏡", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stTextInput > div > div > input, .stSelectbox > div > div > select {
        background-color: #ffffff;
        color: #1f2937;
        border-radius: 8px;
    }
    .stTextArea > div > div > textarea {
        background-color: #ffffff;
        color: #1f2937;
        border-radius: 8px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #FF385C 0%, #E61E4D 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1rem;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #E61E4D 0%, #D70466 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color: #FF385C; text-align: center;'>Your Personal Airbnb Co-Host</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280;'>Quick replies built straight from your property details.</p>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("### 📋 Step 1: Your Property Details")
col1, col2 = st.columns(2)
with col1:
    checkin_info = st.text_input("Check-in instructions", "3 PM using the front door keypad")
    wifi_info = st.text_input("Wi-Fi details", "Network: HomeWiFi, Password: welcome123")
with col2:
    parking_info = st.text_input("Parking rules", "Free parking right on the premises")
    pool_info = st.text_input("Pool / Extra info", "Pool is open 8 AM to 10 PM. No glass allowed.")

st.markdown("---")

st.markdown("### 💬 Step 2: Guest Message")

airbnb_url = st.text_input("Airbnb listing link", placeholder="https://www.airbnb.com/rooms/12345678")

guest_profile = st.selectbox(
    "Who is messaging you?",
    [
        "Regular guest",
        "Family with kids",
        "Remote worker or business traveler",
        "Couple taking a trip",
        "Someone bringing a pet",
        "First-time Airbnb guest"
    ]
)

guest_message = st.text_area(
    "What did they say in their message?", 
    placeholder="Type their message here, like 'Is there a baby changing station?' or 'Can food be delivered to the pool?'"
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Generate Custom Reply"):
    if not airbnb_url or not guest_message:
        st.error("Please fill out your listing link and the guest's message.")
    else:
        with st.spinner("Putting together a friendly reply..."):
            
            incoming = guest_message.lower()
            
            if "check" in incoming or "arrive" in incoming or "time" in incoming or "door" in incoming or "key" in incoming:
                core = f"Check-in is super easy: {checkin_info}."
            elif "wifi" in incoming or "internet" in incoming or "password" in incoming:
                core = f"Here are the internet details: {wifi_info}."
            elif "park" in incoming or "car" in incoming or "drive" in incoming:
                core = f"Regarding parking: {parking_info}."
            elif "pool" in incoming or "swim" in incoming or "water" in incoming or "food" in incoming:
                core = f"To answer your question about the pool area: {pool_info}."
            else:
                core = f"Thanks so much for asking about that! To answer your question about your message: everything is fully prepared for your stay."

            if guest_profile == "Family with kids":
                opener = "Hey there! We are super excited to host you and your family."
                ending = " We made sure everything is comfy and kid-friendly for your crew."
            elif guest_profile == "Remote worker or business traveler":
                opener = "Hi! Thanks for choosing our spot for your trip."
                ending = " We know having a smooth setup and a quiet space to focus is super important."
            elif guest_profile == "Couple taking a trip":
                opener = "Hi there! We are so thrilled to host your getaway."
                ending = " We hope you both have an amazing, relaxing time together."
            elif guest_profile == "Someone bringing a pet":
                opener = "Hello! We are super excited to welcome you and your furry friend."
                ending = " We love hosting pets and hope they love the space too."
            elif guest_profile == "First-time Airbnb guest":
                opener = "Hey! A huge welcome to Airbnb—we are honored to be your very first stay."
                ending = " If you need help with anything at all during your trip, just let us know."
            else:
                opener = "Hey there! Thanks so much for reaching out."
                ending = " We are looking forward to having you stay with us."

            final_reply = f"{opener} {core}{ending} Let me know if you need anything else before you head over!"

            st.markdown("---")
            st.markdown("### Ready to Copy and Send:")
            st.success(final_reply)
            st.info("You can copy this text and drop it right into your Airbnb chat.")
