# Save new complaint
def save_complaint(data):
    complaints = load_complaints()
    complaint_id = str(uuid.uuid4())
    complaints[complaint_id] = data
    with open(COMPLAINT_FILE, "w") as f:
        json.dump(complaints, f, indent=4)
