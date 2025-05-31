# Update status
def update_status(complaint_id, new_status):
    complaints = load_complaints()
    if complaint_id in complaints:
        complaints[complaint_id]["status"] = new_status
        with open(COMPLAINT_FILE, "w") as f:
            json.dump(complaints, f, indent=4)

# admin

if menu == "Admin":
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



