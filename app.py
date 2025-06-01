import streamlit as st
import json
import uuid
from datetime import datetime

# ✅ MUST be the first Streamlit command
st.set_page_config(page_title="Anonymous Complaint Box", layout="centered")

# ✅ Secrets should be accessed after set_page_config
ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
st.sidebar.info("🔐 Admin password loaded.")  # Avoid printing actual password for security

# File to store complaints
COMPLAINT_FILE = "complaints.json"
CATEGORIES = ["Facilities", "Noise", "Cleanliness", "Cafeteria", "Other"]

# Load complaints
def load_complaints():
    try:
        with open(COMPLAINT_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save new complaint
def save_complaint(data):
    complaints = load_complaints()
    complaint_id = str(uuid.uuid4())
    complaints[complaint_id] = data
    with open(COMPLAINT_FILE, "w") as f:
        json.dump(complaints, f, indent=4)

# Update status
def update_status(complaint_id, new_status):
    complaints = load_complaints()
    if complaint_id in complaints:
        complaints[complaint_id]["status"] = new_status
        with open(COMPLAINT_FILE, "w") as f:
            json.dump(complaints, f, indent=4)

# Update votes
def update_vote(complaint_id, vote_type):
    complaints = load_complaints()
    if complaint_id in complaints:
        if vote_type == "up":
            complaints[complaint_id]["upvotes"] += 1
        elif vote_type == "down":
            complaints[complaint_id]["downvotes"] += 1
        with open(COMPLAINT_FILE, "w") as f:
            json.dump(complaints, f, indent=4)

# App
def main():
    st.title("📢 Anonymous Student Complaint Box")

    menu = st.sidebar.selectbox("Select Option", ["Submit Complaint", "My Complaints", "View All Complaints", "Admin"])

    if menu == "Submit Complaint":
        st.subheader("Submit a Complaint")
        complaint = st.text_area("Enter your complaint")
        category = st.selectbox("Select category", CATEGORIES)
        keyword = st.text_input("Create a secret keyword (used to view your complaints later)")

        if st.button("Submit"):
            if not complaint or not keyword:
                st.warning("Please complete all fields.")
            else:
                data = {
                    "complaint": complaint,
                    "category": category,
                    "keyword": keyword.strip().lower(),
                    "status": "Unsolved",
                    "timestamp": str(datetime.now()),
                    "upvotes": 0,
                    "downvotes": 0
                }
                save_complaint(data)
                st.success(f"✅ Complaint submitted anonymously under '{category}'.")

    elif menu == "My Complaints":
        st.subheader("View Your Complaints")
        keyword = st.text_input("Enter your secret keyword")

        if keyword:
            complaints = load_complaints()
            found = False
            for cid, info in complaints.items():
                if info["keyword"] == keyword.strip().lower():
                    found = True
                    st.write(f"📝 {info['complaint']}")
                    st.write(f"📂 Category: {info['category']}")
                    st.write(f"📅 Submitted on: {info['timestamp']}")
                    st.write(f"✅ Status: {info['status']}")
                    st.markdown("---")
            if not found:
                st.info("No complaints found for that keyword.")

    elif menu == "View All Complaints":
        st.subheader("📚 All Complaints")
        complaints = load_complaints()
        category_filter = st.selectbox("Filter by category", ["All"] + CATEGORIES)

        for cid, info in complaints.items():
            if category_filter == "All" or info["category"] == category_filter:
                st.write(f"📝 {info['complaint']}")
                st.write(f"📂 Category: {info['category']}")
                st.write(f"📅 {info['timestamp']}")
                st.write(f"✅ Status: {info['status']}")
                st.write(f"👍 {info.get('upvotes', 0)} | 👎 {info.get('downvotes', 0)}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍 Upvote", key=f"up_{cid}"):
                        update_vote(cid, "up")
                        st.success("You upvoted this complaint.")
                with col2:
                    if st.button("👎 Downvote", key=f"down_{cid}"):
                        update_vote(cid, "down")
                        st.success("You downvoted this complaint.")
                st.markdown("---")

    elif menu == "Admin":
        st.subheader("🔐 Admin Panel")
        password = st.text_input("Enter admin password", type="password")

        if password == ADMIN_PASSWORD:
            st.success("Admin login successful.")
            complaints = load_complaints()
            for cid, info in complaints.items():
                st.write(f"🆔 ID: {cid}")
                st.write(f"📝 {info['complaint']}")
                st.write(f"📂 {info['category']} | 📅 {info['timestamp']}")
                st.write(f"✅ Current Status: {info['status']}")

                new_status = st.selectbox(f"Change status", ["Unsolved", "Solved"], index=0 if info["status"] == "Unsolved" else 1, key=f"status_{cid}")
                if st.button(f"Update Status", key=f"btn_{cid}"):
                    update_status(cid, new_status)
                    st.success(f"Status for complaint {cid} updated.")
                st.markdown("---")
        else:
            if password:
                st.error("Incorrect admin password.")

if __name__ == "__main__":
    main()
