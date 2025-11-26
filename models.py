from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ------------------------
# Patient
# ------------------------
class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(10))
    dob = db.Column(db.String(20))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))

    # Relationships
    sessions = db.relationship("Session", backref="patient", lazy=True)
    logs = db.relationship("DailyLog", backref="patient", lazy=True)
    assessments = db.relationship("EmotionalAssessment", backref="patient", lazy=True)


# ------------------------
# Clinician
# ------------------------
class Clinician(db.Model):
    __tablename__ = "clinicians"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    license_number = db.Column(db.String(50))
    phone = db.Column(db.String(20))

    # Relationships
    sessions = db.relationship("Session", backref="clinician", lazy=True)


# ------------------------
# Session
# ------------------------
class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    session_type = db.Column(db.String(100))
    duration = db.Column(db.String(20))

    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    clinician_id = db.Column(db.Integer, db.ForeignKey("clinicians.id"), nullable=False)

    # Relationships
    assessments = db.relationship("EmotionalAssessment", backref="session", lazy=True)
    logs = db.relationship("DailyLog", backref="session", lazy=True)


# ------------------------
# Emotional Assessment
# ------------------------
class EmotionalAssessment(db.Model):
    __tablename__ = "assessments"

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    severity_level = db.Column(db.String(50))

    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)


# ------------------------
# Daily Log
# ------------------------
class DailyLog(db.Model):
    __tablename__ = "daily_logs"

    id = db.Column(db.Integer, primary_key=True)
    mood_rating = db.Column(db.String(50))
    journal_entry = db.Column(db.Text)

    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)
