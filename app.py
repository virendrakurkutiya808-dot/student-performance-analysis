from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

DB = Path(__file__).with_name("students.db")


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            study_hours REAL DEFAULT 0,
            attendance REAL DEFAULT 0,
            assignment REAL DEFAULT 0,
            mid_term REAL DEFAULT 0,
            final_exam REAL DEFAULT 0,
            average REAL DEFAULT 0,
            grade TEXT DEFAULT '',
            report TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def calculate_grade(avg):
    if avg >= 90:
        return "A+"
    if avg >= 80:
        return "A"
    if avg >= 70:
        return "B"
    if avg >= 60:
        return "C"
    return "D"


@app.route("/")
def dashboard():
    conn = get_db()
    students = conn.execute(
        "SELECT * FROM students ORDER BY average DESC"
    ).fetchall()
    total = conn.execute("SELECT COUNT(*) AS c FROM students").fetchone()["c"]
    avg = conn.execute(
        "SELECT COALESCE(AVG(average), 0) AS a FROM students"
    ).fetchone()["a"]
    conn.close()
    return render_template("dashboard.html", students=students,
                           total=total, class_average=round(avg, 2))


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        try:
            student_id = request.form["student_id"].strip()
            name = request.form["name"].strip()
            study_hours = float(request.form["study_hours"])
            attendance = float(request.form["attendance"])
            assignment = float(request.form["assignment"])
            mid_term = float(request.form["mid_term"])
            final_exam = float(request.form["final_exam"])
            report = request.form.get("report", "").strip()

            if not student_id or not name:
                raise ValueError("Student ID and Name are required.")

            if not 0 <= attendance <= 100:
                raise ValueError("Attendance must be between 0 and 100.")

            for value in [assignment, mid_term, final_exam]:
                if not 0 <= value <= 100:
                    raise ValueError("Marks must be between 0 and 100.")

            average = round((assignment + mid_term + final_exam) / 3, 2)
            grade = calculate_grade(average)

            conn = get_db()
            conn.execute("""
                INSERT INTO students
                (student_id, name, study_hours, attendance, assignment,
                 mid_term, final_exam, average, grade, report)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (student_id, name, study_hours, attendance, assignment,
                  mid_term, final_exam, average, grade, report))
            conn.commit()
            conn.close()

            flash("Student data saved successfully.", "success")
            return redirect(url_for("dashboard"))

        except sqlite3.IntegrityError:
            flash("Student ID already exists.", "error")
        except ValueError as e:
            flash(str(e), "error")

    return render_template("add_student.html")


@app.route("/student/<int:student_db_id>")
def student_detail(student_db_id):
    conn = get_db()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (student_db_id,)
    ).fetchone()
    conn.close()

    if student is None:
        flash("Student not found.", "error")
        return redirect(url_for("dashboard"))

    return render_template("student_detail.html", student=student)


@app.route("/delete/<int:student_db_id>", methods=["POST"])
def delete_student(student_db_id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id = ?", (student_db_id,))
    conn.commit()
    conn.close()
    flash("Student deleted.", "success")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
