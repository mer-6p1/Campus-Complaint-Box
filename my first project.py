

def main():
    st.set_page_config(page_title="Anonymous Complaint Box", layout="centered")
    st.title("📬 Anonymous Student Complaint Box")

    menu = st.sidebar.selectbox("Select Option", 
                                ["Submit Complaint", "My Complaints", "View All Complaints", "Admin"])

    # View my complaint
    if menu == "My Complaints":
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

