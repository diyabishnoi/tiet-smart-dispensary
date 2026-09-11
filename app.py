from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# ============================================================
# FLASK SECRET KEY
# ============================================================

app.secret_key = "tiet-smart-dispensary-secret-key"


# ============================================================
# DEMO DATA
# ============================================================

# Demo medicines
MEDICINES = [
    {
        "name": "Paracetamol",
        "category": "Fever & Pain",
        "quantity": 50
    },
    {
        "name": "Cetirizine",
        "category": "Allergy",
        "quantity": 30
    },
    {
        "name": "ORS",
        "category": "Hydration",
        "quantity": 40
    },
    {
        "name": "Ibuprofen",
        "category": "Pain Relief",
        "quantity": 25
    },
    {
        "name": "Azithromycin",
        "category": "Antibiotic",
        "quantity": 0
    },
    {
        "name": "Antacid",
        "category": "Digestive Health",
        "quantity": 20
    }
]


# Demo doctors
DOCTORS = [
    "Dr. Ajay Gupta",
    "Dr. Harjit Singh",
    "Dr. Jeevan Jot Singh",
    "Dr. Mahroosh Nasir",
    "Dr. Ritu Bassi",
    "Dr. Sarabjeet Kaur"
]


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template("index.html")


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        student_id = request.form.get("student_id", "").strip()
        password = request.form.get("password", "").strip()

        # ----------------------------------------------------
        # DEMO LOGIN
        # ----------------------------------------------------

        if student_id == "TIET123" and password == "12345":

            # Save student ID in session
            session["student_id"] = student_id

            # Create appointment list for this session
            if "appointments" not in session:

                session["appointments"] = [
                    {
                        "doctor": "Dr. Ajay Gupta",
                        "date": "2026-09-11",
                        "time": "12:30",
                        "reason": "Fever",
                        "status": "Confirmed"
                    }
                ]

            return redirect(url_for("dashboard"))

        else:

            return render_template(
                "login.html",
                error="Invalid Student ID or Password."
            )

    return render_template("login.html")


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    # Student must be logged in
    if "student_id" not in session:

        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        student_id=session["student_id"]
    )


# ============================================================
# BOOK APPOINTMENT
# ============================================================

@app.route("/appointments", methods=["GET", "POST"])
def appointments():

    # Check login
    if "student_id" not in session:

        return redirect(url_for("login"))

    # --------------------------------------------------------
    # POST = BOOK APPOINTMENT
    # --------------------------------------------------------

    if request.method == "POST":

        doctor = request.form.get("doctor", "").strip()
        date = request.form.get("date", "").strip()
        time = request.form.get("time", "").strip()
        reason = request.form.get("reason", "").strip()

        # Basic validation
        if not doctor or not date or not time or not reason:

            return render_template(
                "appointments.html",
                doctors=DOCTORS,
                error="Please fill in all appointment details."
            )

        # ----------------------------------------------------
        # CREATE APPOINTMENT
        # ----------------------------------------------------

        new_appointment = {
            "doctor": doctor,
            "date": date,
            "time": time,
            "reason": reason,
            "status": "Confirmed"
        }

        # Get existing appointments
        appointments_list = session.get("appointments", [])

        # Add new appointment
        appointments_list.append(new_appointment)

        # Save back to session
        session["appointments"] = appointments_list

        # Make sure Flask saves session changes
        session.modified = True

        # Print appointment in terminal
        print("----------------------------------------")
        print("NEW APPOINTMENT")
        print("----------------------------------------")
        print("Student ID:", session["student_id"])
        print("Doctor:", doctor)
        print("Date:", date)
        print("Time:", time)
        print("Reason:", reason)
        print("Status:", "Confirmed")
        print("----------------------------------------")

        # Show confirmation page
        return render_template(
            "appointment_success.html",
            doctor=doctor,
            date=date,
            time=time,
            reason=reason
        )

    # --------------------------------------------------------
    # GET = SHOW BOOKING PAGE
    # --------------------------------------------------------

    return render_template(
        "appointments.html",
        doctors=DOCTORS
    )


# ============================================================
# APPOINTMENT HISTORY
# ============================================================

@app.route("/history")
def history():

    # Check login
    if "student_id" not in session:

        return redirect(url_for("login"))

    appointments_list = session.get("appointments", [])

    # --------------------------------------------------------
    # HISTORY PAGE
    # --------------------------------------------------------

    return render_template(
        "history.html",
        appointments=appointments_list,
        student_id=session["student_id"]
    )


# ============================================================
# MEDICINE AVAILABILITY
# ============================================================

@app.route("/medicines")
def medicines():

    # Check login
    if "student_id" not in session:

        return redirect(url_for("login"))

    # Get search text
    search = request.args.get("search", "").strip()

    # --------------------------------------------------------
    # FILTER MEDICINES
    # --------------------------------------------------------

    if search:

        search_lower = search.lower()

        filtered_medicines = [

            medicine
            for medicine in MEDICINES

            if (
                search_lower in medicine["name"].lower()
                or search_lower in medicine["category"].lower()
            )
        ]

    else:

        filtered_medicines = MEDICINES

    # --------------------------------------------------------
    # MEDICINE PAGE
    # --------------------------------------------------------

    return render_template(
        "medicines.html",
        medicines=filtered_medicines,
        search=search,
        student_id=session["student_id"]
    )


# ============================================================
# PRESCRIPTIONS
# ============================================================

@app.route("/prescriptions")
def prescriptions():

    # Check login
    if "student_id" not in session:

        return redirect(url_for("login"))

    return render_template(
        "prescriptions.html",
        student_id=session["student_id"]
    )


# ============================================================
# TALK TO A DOCTOR
# ============================================================

@app.route("/consult", methods=["GET", "POST"])
def consult():

    # Check login
    if "student_id" not in session:

        return redirect(url_for("login"))

    message = None

    # --------------------------------------------------------
    # START CONSULTATION
    # --------------------------------------------------------

    if request.method == "POST":

        symptoms = request.form.get("symptoms", "").strip()
        mode = request.form.get("mode", "Chat")
        doctor = request.form.get("doctor", "Any available")

        if symptoms:

            message = (
                "Your consultation request has been submitted. "
                "A campus doctor will respond during dispensary hours."
            )

        else:

            message = "Please describe your symptoms before starting a consultation."

    return render_template(
        "consult.html",
        message=message,
        doctors=DOCTORS,
        student_id=session["student_id"]
    )


# ============================================================
# EMERGENCY
# ============================================================

@app.route("/emergency")
def emergency():

    # Check login
    if "student_id" not in session:

        return redirect(url_for("login"))

    return render_template(
        "emergency.html",
        student_id=session["student_id"]
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    # Remove all session information
    session.clear()

    return redirect(url_for("home"))


# ============================================================
# RUN FLASK APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )