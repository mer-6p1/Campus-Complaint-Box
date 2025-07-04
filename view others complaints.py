def update_vote(complaint_id, vote_type):
    complaints = load_complaints()
    if complaint_id in complaints:
        if vote_type == "up":
            complaints[complaint_id]["upvotes"] += 1
        elif vote_type == "down":
            complaints[complaint_id]["downvotes"] += 1
        with open(COMPLAINT_FILE, "w") as f:
            json.dump(complaints, f, indent=4)

# view others complaint

if menu == "View All Complaints":
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
