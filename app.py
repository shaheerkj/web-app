from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "students.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- HTML Templates ----------

HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Student Registration</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 0 20px; }
        h1 { color: #2c3e50; }
        form { background: #f4f4f4; padding: 20px; border-radius: 8px; }
        input, select { width: 100%; padding: 8px; margin: 8px 0 16px 0; box-sizing: border-box; }
        button { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2980b9; }
        table { width: 100%; border-collapse: collapse; margin-top: 30px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background: #3498db; color: white; }
        tr:nth-child(even) { background: #f2f2f2; }
        .success { color: green; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Student Registration System</h1>

    {% if message %}
        <p class="success">{{ message }}</p>
    {% endif %}

    <form id="registration-form" method="POST" action="/register">
        <label>Full Name:</label>
        <input type="text" id="name" name="name" placeholder="Enter full name" required>

        <label>Email:</label>
        <input type="email" id="email" name="email" placeholder="Enter email" required>

        <label>Course:</label>
        <select id="course" name="course">
            <option value="DevOps">DevOps for Cloud Computing</option>
            <option value="AI">Artificial Intelligence</option>
            <option value="SE">Software Engineering</option>
            <option value="DB">Database Systems</option>
        </select>

        <button id="submit-btn" type="submit">Register Student</button>
    </form>

    <h2>Registered Students</h2>
    {% if students %}
    <table id="students-table">
        <tr>
            <th>ID</th><th>Name</th><th>Email</th><th>Course</th>
        </tr>
        {% for student in students %}
        <tr>
            <td>{{ student['id'] }}</td>
            <td>{{ student['name'] }}</td>
            <td>{{ student['email'] }}</td>
            <td>{{ student['course'] }}</td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
        <p>No students registered yet.</p>
    {% endif %}
</body>
</html>
'''

# ---------- Routes ----------

@app.route('/')
def home():
    conn = get_db()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template_string(HOME_TEMPLATE, students=students, message=None)

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    course = request.form.get('course')

    if name and email and course:
        conn = get_db()
        conn.execute('INSERT INTO students (name, email, course) VALUES (?, ?, ?)',
                     (name, email, course))
        conn.commit()
        conn.close()

    return redirect(url_for('home') + '?msg=success')

@app.route('/students')
def students_list():
    conn = get_db()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template_string(HOME_TEMPLATE, students=students, message="Student list loaded.")

@app.route('/health')
def health():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
