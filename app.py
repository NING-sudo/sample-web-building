# app.py
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, abort

app = Flask(__name__)

# ------------------------------------------------------------------
# Data that used to live in the HTML (or in a separate sheet)
# ------------------------------------------------------------------
STATES = [
    "Johor","Kedah","Kelantan","Malacca","Negeri Sembilan","Pahang",
    "Penang","Perak","Perlis","Sabah","Sarawak","Selangor",
    "Terengganu","Kuala Lumpur","Labuan","Putrajaya"
]

JOBS = ["Virtual Assistant","Marketing Assistant","Data Entry Specialist","Other"]

AVAILABILITIES = ["Full-time","Part-time","Flexible"]

LATEST_JOBS = [
    {"title":"Virtual Assistant","description":"Support businesses remotely with administrative tasks, scheduling, email management, and more. Flexibility is key!"},
    {"title":"Marketing Assistant","description":"Help execute marketing campaigns, manage social media, create content, and analyze performance from anywhere."},
    {"title":"Data Entry Specialist","description":"Accurately input and manage data for various projects. Attention to detail and efficiency are highly valued."}
]

ADVANTAGES = [
    {"title":"Verified Listings","description":"We thoroughly vet all job opportunities to ensure legitimacy and a safe working environment for our users."},
    {"title":"Flexible Hours","description":"Our platform focuses on jobs that offer the freedom to work on your own schedule, fitting perfectly into your life."},
    {"title":"Reliable Payments","description":"Rest assured, we partner with employers who are committed to timely and secure payments for your hard work."}
]

TESTIMONIALS = [
    {"quote":"EasyEarn helped me find a remote job that perfectly fits my family schedule. The process was smooth and the support was excellent!","author":"Sarah L., Virtual Assistant"},
    {"quote":"I was looking for extra income and found a great data entry role here. Payments are always on time. Highly recommend!","author":"Amir H., Data Entry Specialist"}
]

ABOUT_TEXT = (
    "EasyEarn is dedicated to connecting talented individuals with flexible and rewarding remote work opportunities. "
    "We believe everyone deserves a chance to earn on their own terms, and we strive to make that possible through "
    "carefully curated job listings and a user-friendly platform. Our mission is to empower you to achieve financial "
    "independence and work-life balance."
)

# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------
@app.route("/")
def index():
    return render_template(
        "index.html",
        states=STATES,
        jobs=JOBS,
        availabilities=AVAILABILITIES,
        latest_jobs=LATEST_JOBS,
        advantages=ADVANTAGES,
        testimonials=TESTIMONIALS,
        about_text=ABOUT_TEXT,
        current_year=datetime.now().year
    )

# ------------------------------------------------------------------
# API – receive the form
# ------------------------------------------------------------------
@app.route("/api/submit", methods=["POST"])
def submit_form():
    if not request.is_json:
        abort(400, "JSON required")

    data = request.get_json()

    # ----> YOUR PROCESSING LOGIC HERE <----
    # Example: save to DB, send email, call Google Sheets, etc.
    print("Received lead:", data)   # <-- replace with real storage

    # Simple validation (you can expand)
    required = ["fullName","email","whatsapp","state","interestedJob","availability"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify(success=False, message="Missing fields: " + ", ".join(missing))

    # Success response
    return jsonify(success=True, message="Thank you! We'll contact you soon.")

# ------------------------------------------------------------------
# Run (debug=False in production)
# ------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)