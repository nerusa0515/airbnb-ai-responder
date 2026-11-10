import streamlit as st

st.set_page_config(page_title="Airbnb Co-Host Dashboard", page_icon="🏡", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton > button {
        background: linear-gradient(135deg, #FF385C 0%, #E61E4D 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #E61E4D 0%, #D70466 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Top Bar / Account Connection Status
col_top1, col_top2 = st.columns([3, 1])
with col_top1:
    st.markdown("<h2 style='color: #FF385C; margin: 0;'>🏡 Co-Host Command Center</h2>", unsafe_allow_html=True)
with col_top2:
    st.success("🔗 Connected to Airbnb")

st.markdown("---")

# Sidebar settings for operation mode
st.sidebar.header("⚙️ Co-Host Settings")
listing_linked = st.sidebar.selectbox("Active Listing", ["Seaside Sunset Villa (#849201)", "Downtown Loft (#392810)"])
operation_mode = st.sidebar.radio(
    "Messaging Mode",
    ["Approval Mode (Review & Click to Send)", "Auto-Pilot Mode (Fully Automated)"]
)

st.sidebar.markdown("---")
st.sidebar.info("When linked via official API/PMS, incoming guest messages automatically land here based on your chosen mode.")

# Main Dashboard Layout
if "Approval Mode" in operation_mode:
    st.markdown("### 📥 Pending Message Approval Queue")
    st.markdown("The following guest messages just came in from Airbnb and need your review:")

    # Mock pending message item
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("**Guest:** Sarah Jenkins (Family with Kids)")
        st.markdown("**Listing:** Seaside Sunset Villa")
        st.markdown("**Incoming Message:** *'Hi! Is there a baby changing station or pack-and-play available at the property?'*")
        st.markdown("*Received 2 mins ago*")

    with col2:
        st.markdown("**AI Drafted Response:**")
        draft_response = "Hey there! We are super excited to host you and your family. We have a portable baby changing station and pack-and-play set up and ready for your little one to use. We made sure everything is comfy and kid-friendly for your crew. Let me know if you need anything else before you head over!"
        
        st.info(draft_response)
        
        if st.button("✨ Approve & Send to Airbnb"):
            st.success("🚀 Message successfully approved and sent straight to Sarah's Airbnb chat!")
            st.balloons()

    st.markdown("---")
    st.markdown("### ➕ Simulate a New Incoming Guest Message")
    with st.form("simulate_form"):
        sim_guest = st.text_input("Guest Name", "Alex Rodriguez")
        sim_msg = st.text_area("Guest Message", "What time is check-in and how do we access the keys?")
        submitted = st.form_submit_button("Simulate Incoming Message")
        if submitted:
            st.warning(f"New message simulated from {sim_guest}! It has been added to your approval queue above.")

else:
    st.markdown("### ⚡ Auto-Pilot Active Feed")
    st.markdown("Your co-host app is running automatically in the background. Incoming messages are answered and sent to guests instantly.")
    
    # Live activity log simulation
    st.success("✅ **[Auto-Sent 5m ago]** Replied to *David M.* regarding Wi-Fi details.")
    st.success("✅ **[Auto-Sent 42m ago]** Replied to *Jessica L.* regarding parking instructions.")
    st.success("✅ **[Auto-Sent 2h ago]** Replied to *Mark T.* regarding check-in time.")

    st.markdown("---")
    st.markdown("### 🧪 Test Auto-Pilot Response")
    test_msg = st.text_input("Test a guest question", "Can we bring our dog?")
    if st.button("Simulate Auto-Reply"):
        st.info(f"**Incoming:** {test_msg}")
        st.success("**Auto-Pilot Response Sent Instantly:** Hello! We are super excited to welcome you and your furry friend. We love hosting pets and hope they love the space too. Free parking is available right on the premises during your entire stay. Let me know if you need anything else before you head over!")
