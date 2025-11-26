from flask import Flask, render_template, request, redirect
import pymysql

# -----------------------------------------
# MYSQL CONNECTION
# -----------------------------------------
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Sanj@1234",
        database="therapy_db",
        cursorclass=pymysql.cursors.DictCursor,
        charset="utf8mb4",
        autocommit=True
    )


app = Flask(__name__)


# -----------------------------------------
# HOME PAGE
# -----------------------------------------
@app.route("/")
def home():
    return render_template("home.html")


# -----------------------------------------
# PATIENTS
# -----------------------------------------
@app.route("/patients")
def patients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()
    conn.close()
    return render_template("patients.html", patients=data)


@app.route("/patients/add", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        name = request.form["name"]
        gender = request.form["gender"]
        dob = request.form["dob"]
        address = request.form["address"]
        phone = request.form["phone"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patients(name, gender, dob, address, phone) VALUES (%s, %s, %s, %s, %s)",
            (name, gender, dob, address, phone)
        )
        conn.commit()
        conn.close()

        return redirect("/patients")

    return render_template("add_patient.html")


# -----------------------------------------
# CLINICIANS


# -----------------------------------------
# CLINICIANS
# -----------------------------------------

@app.route("/clinicians", methods=["GET", "POST"])
def clinicians():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        specialization = request.form["specialization"]
        phone = request.form["phone"]

        cursor.execute(
            "INSERT INTO clinicians (name, specialization, phone) VALUES (%s, %s, %s)",
            (name, specialization, phone)
        )
        conn.commit()

    cursor.execute("SELECT * FROM clinicians")
    data = cursor.fetchall()

    conn.close()
    return render_template("clinicians.html", clinicians=data)


# -----------------------------------------
# ADD SEPARATE ADD PAGE (if using button)
# -----------------------------------------
@app.route("/clinicians/add", methods=["GET", "POST"])
def add_clinician():
    if request.method == "POST":
        name = request.form["name"]
        specialization = request.form["specialization"]
        phone = request.form["phone"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clinicians (name, specialization, phone) VALUES (%s, %s, %s)",
            (name, specialization, phone)
        )
        conn.commit()
        conn.close()

        return redirect("/clinicians")

    return render_template("add_clinician.html")


# -----------------------------------------
# EDIT CLINICIAN
# -----------------------------------------
@app.route("/clinicians/edit/<int:id>", methods=["GET", "POST"])
def edit_clinician(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        specialization = request.form["specialization"]
        phone = request.form["phone"]

        cursor.execute("""
            UPDATE clinicians 
            SET name=%s, specialization=%s, phone=%s 
            WHERE id=%s
        """, (name, specialization, phone, id))

        conn.commit()
        conn.close()
        return redirect("/clinicians")

    cursor.execute("SELECT * FROM clinicians WHERE id=%s", (id,))
    clinician = cursor.fetchone()
    conn.close()

    return render_template("edit_clinician.html", clinician=clinician)


# -----------------------------------------
# DELETE CLINICIAN
# -----------------------------------------
@app.route("/clinicians/delete/<int:id>")
def delete_clinician(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM clinicians WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return redirect("/clinicians")
@app.route("/delete_patient/<int:id>")
def delete_patient(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete logs linked through sessions → assessments → logs
    cursor.execute("DELETE FROM logs WHERE session_id IN (SELECT id FROM sessions WHERE patient_id=%s)", (id,))
    
    # Delete assessments linked to the patient’s sessions
    cursor.execute("DELETE FROM assessments WHERE session_id IN (SELECT id FROM sessions WHERE patient_id=%s)", (id,))
    
    # Delete sessions linked with the patient
    cursor.execute("DELETE FROM sessions WHERE patient_id=%s", (id,))
    
    # Finally delete the patient
    cursor.execute("DELETE FROM patients WHERE id=%s", (id,))

    conn.commit()
    conn.close()

    return redirect("/patients")



@app.route("/edit_patient/<int:id>", methods=["GET", "POST"])
def edit_patient(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE id = %s", (id,))
    patient = cursor.fetchone()

    if request.method == "POST":
        cursor.execute("""
            UPDATE patients 
            SET name=%s, gender=%s, dob=%s, address=%s, phone=%s
            WHERE id=%s
        """, (
            request.form['name'],
            request.form['gender'],
            request.form['dob'],
            request.form['address'],
            request.form['phone'],
            id
        ))
        conn.commit()
        conn.close()
        return redirect("/patients")

    conn.close()
    return render_template("edit_patient.html", patient=patient)

# -----------------------------------------
# SESSIONS
@app.route("/sessions", methods=["GET", "POST"])
def sessions():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Fetch patients to populate dropdown
    cursor.execute("SELECT id, name FROM patients")
    patients = cursor.fetchall()

    # Fetch clinicians to populate dropdown
    cursor.execute("SELECT id, name FROM clinicians")
    clinicians = cursor.fetchall()

    # When form submitted
    if request.method == "POST":
        patient_id = request.form["patient_id"]
        clinician_id = request.form["clinician_id"]
        session_date = request.form["session_date"]
        notes = request.form["notes"]

        cursor2 = conn.cursor()
        cursor2.execute(
            "INSERT INTO sessions (patient_id, clinician_id, session_date, notes) VALUES (%s, %s, %s, %s)",
            (patient_id, clinician_id, session_date, notes)
        )
        conn.commit()

    # Fetch all sessions to display
    cursor.execute("""
        SELECT 
            sessions.id, sessions.session_date, sessions.notes,
            patients.name AS patient_name,
            clinicians.name AS clinician_name
        FROM sessions
        JOIN patients ON sessions.patient_id = patients.id
        JOIN clinicians ON sessions.clinician_id = clinicians.id
        ORDER BY sessions.id DESC
    """)
    sessions_data = cursor.fetchall()

    conn.close()

    return render_template(
        "sessions.html",
        patients=patients,
        clinicians=clinicians,
        sessions=sessions_data
    )

@app.route("/sessions/add", methods=["GET", "POST"])
def add_session():
    conn = get_db_connection()
    cursor = conn.cursor()

    # dropdown data
    cursor.execute("SELECT id, name FROM patients")
    patients = cursor.fetchall()

    cursor.execute("SELECT id, name FROM clinicians")
    clinicians = cursor.fetchall()

    if request.method == "POST":
        patient_id = request.form["patient_id"]
        clinician_id = request.form["clinician_id"]
        session_date = request.form["session_date"]
        notes = request.form["notes"]

        cursor2 = conn.cursor()
        cursor2.execute(
            "INSERT INTO sessions(patient_id, clinician_id, session_date, notes) "
            "VALUES (%s, %s, %s, %s)",
            (patient_id, clinician_id, session_date, notes)
        )
        conn.commit()
        conn.close()
        return redirect("/sessions")

    conn.close()
    return render_template("add_session.html", patients=patients, clinicians=clinicians)


# -----------------------------------------
# ASSESSMENTS
# -----------------------------------------
@app.route("/assessments", methods=["GET", "POST"])
def assessments():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Fetch sessions for dropdown
    cursor.execute("""
        SELECT 
            sessions.id,
            patients.name AS patient_name,
            clinicians.name AS clinician_name
        FROM sessions
        JOIN patients ON sessions.patient_id = patients.id
        JOIN clinicians ON sessions.clinician_id = clinicians.id
    """)
    sessions = cursor.fetchall()

    # Handle form submission
    if request.method == "POST":
        session_id = request.form["session_id"]
        assessment_type = request.form["assessment_type"]
        score = request.form["score"]
        remarks = request.form["remarks"]

        cursor2 = conn.cursor()
        cursor2.execute(
            "INSERT INTO assessments (session_id, assessment_type, score, remarks) VALUES (%s, %s, %s, %s)",
            (session_id, assessment_type, score, remarks)
        )
        conn.commit()

    # Fetch all assessments to display
    cursor.execute("""
        SELECT 
            assessments.id,
            assessments.assessment_type,
            assessments.score,
            assessments.remarks,
            sessions.id AS session_display,
            patients.name AS patient_name,
            clinicians.name AS clinician_name
        FROM assessments
        JOIN sessions ON assessments.session_id = sessions.id
        JOIN patients ON sessions.patient_id = patients.id
        JOIN clinicians ON sessions.clinician_id = clinicians.id
        ORDER BY assessments.id DESC
    """)
    assessment_list = cursor.fetchall()

    conn.close()

    return render_template(
        "assessments.html",
        sessions=sessions,
        assessments=assessment_list
    )

@app.route("/assessments/add", methods=["GET", "POST"])
def add_assessment():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM sessions")
    sessions = cursor.fetchall()

    if request.method == "POST":
        session_id = request.form["session_id"]
        assessment_type = request.form["assessment_type"]
        score = request.form["score"]
        remarks = request.form["remarks"]

        cursor2 = conn.cursor()
        cursor2.execute(
            "INSERT INTO assessments(session_id, assessment_type, score, remarks) "
            "VALUES (%s, %s, %s, %s)",
            (session_id, assessment_type, score, remarks)
        )
        conn.commit()
        conn.close()
        return redirect("/assessments")

    conn.close()
    return render_template("add_assessment.html", sessions=sessions)


# -----------------------------------------
# LOGS
# -----------------------------------------
@app.route("/logs", methods=["GET", "POST"])
def logs():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Add Log Entry
    if request.method == "POST":
        session_id = request.form.get("session_id")
        log_time = request.form.get("time")
        log_date = request.form.get("date")
        details = request.form.get("details")

        cursor.execute("""
            INSERT INTO logs(session_id, time, date, details)
            VALUES (%s, %s, %s, %s)
        """, (session_id, log_time, log_date, details))

        conn.commit()

    # Fetch all logs
    cursor.execute("""
        SELECT logs.id,
               logs.time,
               logs.date,
               logs.details,
               CONCAT('Session ', sessions.id) AS session_display,
               patients.name AS patient_name,
               clinicians.name AS clinician_name
        FROM logs
        JOIN sessions ON logs.session_id = sessions.id
        JOIN patients ON sessions.patient_id = patients.id
        JOIN clinicians ON sessions.clinician_id = clinicians.id
        ORDER BY logs.id DESC
    """)
    logs_data = cursor.fetchall()

    # Fetch sessions for dropdown
    cursor.execute("""
        SELECT sessions.id,
               patients.name AS patient_name,
               clinicians.name AS clinician_name
        FROM sessions
        JOIN patients ON sessions.patient_id = patients.id
        JOIN clinicians ON sessions.clinician_id = clinicians.id
    """)
    session_list = cursor.fetchall()

    conn.close()

    return render_template("logs.html", logs=logs_data, sessions=session_list)
@app.route("/logs/add", methods=["GET", "POST"])
def add_log():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM sessions")
    sessions = cursor.fetchall()

    if request.method == "POST":
        session_id = request.form["session_id"]
        log_type = request.form["log_type"]
        description = request.form["description"]
        log_date = request.form["log_date"]

        cursor2 = conn.cursor()
        cursor2.execute(
            "INSERT INTO logs(session_id, log_type, description, log_date) "
            "VALUES (%s, %s, %s, %s)",
            (session_id, log_type, description, log_date)
        )
        conn.commit()
        conn.close()
        return redirect("/logs")

    conn.close()
    return render_template("add_log.html", sessions=sessions)



# -----------------------------------------
# RUN APP
# -----------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
