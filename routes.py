from flask import render_template, request, redirect, url_for
from models import db, Patient, Clinician, Session, DailyLog, EmotionalAssessment

def init_app(app):

    # Home route
    @app.route("/")
    def home():
        return render_template("base.html")

    # ----------------------
    # Patient Routes
    # ----------------------
    @app.route("/patients")
    def patients():
        all_patients = Patient.query.all()
        return render_template("patient.html", patients=all_patients)

    @app.route("/add_patient", methods=["POST"])
    def add_patient():
        name = request.form["name"]
        gender = request.form["gender"]
        dob = request.form["dob"]
        address = request.form["address"]
        phone = request.form["phone"]

        new_patient = Patient(name=name, gender=gender, dob=dob, address=address, phone=phone)
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for("patients"))

    # ----------------------
    # Clinician Routes
    # ----------------------
    @app.route("/clinicians")
    def clinicians():
        all_clinicians = Clinician.query.all()
        return render_template("clinician.html", clinicians=all_clinicians)

    @app.route("/add_clinician", methods=["POST"])
    def add_clinician():
        name = request.form["name"]
        license_number = request.form["license_number"]
        phone = request.form["phone"]

        new_c = Clinician(name=name, license_number=license_number, phone=phone)
        db.session.add(new_c)
        db.session.commit()
        return redirect(url_for("clinicians"))

    # ----------------------
    # Sessions
    # ----------------------
    @app.route("/sessions")
    def sessions():
        all_sessions = Session.query.all()
        return render_template("sessions.html", sessions=all_sessions)

    @app.route("/add_session", methods=["POST"])
    def add_session():
        session_type = request.form["session_type"]
        duration = request.form["duration"]
        patient_id = request.form["patient_id"]
        clinician_id = request.form["clinician_id"]

        new_session = Session(
            session_type=session_type,
            duration=duration,
            patient_id=patient_id,
            clinician_id=clinician_id,
        )
        db.session.add(new_session)
        db.session.commit()
        return redirect(url_for("sessions"))

    # ----------------------
    # Emotional Assessments
    # ----------------------
    @app.route("/assessments")
    def assessments():
        all_assess = EmotionalAssessment.query.all()
        return render_template("assessments.html", assessments=all_assess)

    @app.route("/add_assessment", methods=["POST"])
    def add_assessment():
        score = request.form["score"]
        severity_level = request.form["severity_level"]
        patient_id = request.form["patient_id"]

        assess = EmotionalAssessment(
            score=score,
            severity_level=severity_level,
            patient_id=patient_id,
        )
        db.session.add(assess)
        db.session.commit()
        return redirect(url_for("assessments"))

    # ----------------------
    # Daily Logs
    # ----------------------
    @app.route("/logs")
    def logs():
        all_logs = DailyLog.query.all()
        return render_template("logs.html", logs=all_logs)

    @app.route("/add_log", methods=["POST"])
    def add_log():
        mood_rating = request.form["mood_rating"]
        journal_entry = request.form["journal_entry"]
        patient_id = request.form["patient_id"]

        log = DailyLog(
            mood_rating=mood_rating,
            journal_entry=journal_entry,
            patient_id=patient_id,
        )
        db.session.add(log)
        db.session.commit()
        return redirect(url_for("logs"))
