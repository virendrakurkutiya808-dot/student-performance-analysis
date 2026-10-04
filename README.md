# Student Performance Analysis using Python

GTU Micro Project – BE05000231 Python for Data Science

## Features
- Web dashboard
- Add and store student records
- SQLite database
- Automatic average and grade calculation
- Student performance report/remarks
- View individual student report
- Delete student record
- Responsive HTML/CSS interface

## Run the project

1. Install Python 3.x.
2. Open terminal in this project folder.
3. Create a virtual environment (optional):
   python -m venv venv

4. Activate it:
   Windows:
   venv\Scripts\activate

   Linux/macOS:
   source venv/bin/activate

5. Install Flask:
   pip install -r requirements.txt

6. Run:
   python app.py

7. Open in browser:
   http://127.0.0.1:5000

The SQLite file `students.db` is created automatically when the application starts.

## Project structure

student_performance_web/
├── app.py
├── requirements.txt
├── README.md
├── students.db        # created automatically
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── add_student.html
│   └── student_detail.html
└── static/
    └── style.css
