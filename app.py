# Save new complaint
def save_complaint(data):
    complaints = load_complaints()
    complaint_id = str(uuid.uuid4())
    complaints[complaint_id] = data
    with open(COMPLAINT_FILE, "w") as f:
        json.dump(complaints, f, indent=4)


#submit complaint

if menu == "Submit Complaint":
    st.subheader("Submit a Complaint")
    complaint = st.text_area("Enter your complaint")
    category = st.selectbox("Select category", CATEGORIES)
    keyword = st.text_input("Create a secret keyword (used to view your complaints later)")
