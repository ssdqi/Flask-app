from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

# Database setup and connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as db:

        db.execute('DROP TABLE IF EXISTS preferences')
        db.execute('DROP TABLE IF EXISTS courses')
        db.execute('DROP TABLE IF EXISTS teachers')
        db.execute('DROP TABLE IF EXISTS students')
        # Create students table and insert initial data
        db.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                class TEXT NOT NULL
            );
        ''')
        students_data = [
            ('John Doe', 14, '1A'),
            ('Jane Smith', 14, '1A'),
            ('Michael Johnson', 15, '1A'),
            ('Emily Davis', 14, '1A'),
            ('Daniel Brown', 15, '1A'),
            ('Olivia Wilson', 14, '1B'),
            ('William Taylor', 14, '1B'),
            ('Sophia Moore', 15, '1B'),
            ('James Anderson', 14, '1B'),
            ('Isabella Thomas', 15, '1B'),
            ('Ethan Martin', 14, '1C'),
            ('Charlotte White', 14, '1C'),
            ('Logan Harris', 15, '1C'),
            ('Ava Clark', 14, '1C'),
            ('Jacob Lewis', 15, '1C')
        ]
        db.executemany('INSERT INTO students (name, age, class) VALUES (?, ?, ?)', students_data)

        # Create teachers table and insert initial data
        db.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                class TEXT NOT NULL
            );
        ''')
        teachers_data = [
            ('Alice Johnson', '1A'),
            ('Bob Smith', '1B'),
            ('Carol Taylor', '1C'),
        ]
        db.executemany('INSERT INTO teachers (name, class) VALUES (?, ?)', teachers_data)

        # Create courses table and insert initial data
        db.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
        ''')
        courses_data = [
            ('Mathematics',),
            ('Science',),
            ('History',),
            ('English',),
            ('Art',)
        ]
        db.executemany('INSERT INTO courses (name) VALUES (?)', courses_data)

        # Create preferences table
        db.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                teacher_id INTEGER,
                course_id INTEGER,
                first_choice_id INTEGER,
                second_choice_id INTEGER,
                third_choice_id INTEGER,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (teacher_id) REFERENCES teachers(id),
                FOREIGN KEY (course_id) REFERENCES courses(id),
                FOREIGN KEY (first_choice_id) REFERENCES students(id),
                FOREIGN KEY (second_choice_id) REFERENCES students(id),
                FOREIGN KEY (third_choice_id) REFERENCES students(id)
            );
        ''')
        db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary')
def summary():
    with get_db_connection() as db:
        students = db.execute('SELECT * FROM students').fetchall()
    return render_template('summary.html', students=students)

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if request.method == 'POST':
        student_id = request.form['student_id']
        teacher_id = request.form['teacher_id']
        course_id = request.form['favorite_course']
        first_choice_id = request.form['first_preference']
        second_choice_id = request.form['second_preference']
        third_choice_id = request.form['third_preference']
        with get_db_connection() as db:
            db.execute('''
                INSERT INTO preferences (
                    student_id, teacher_id, course_id, first_choice_id, second_choice_id, third_choice_id
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, teacher_id, course_id, first_choice_id, second_choice_id, third_choice_id))
            db.commit()
        return redirect(url_for('summary'))
    else:
        with get_db_connection() as db:
            students = db.execute('SELECT * FROM students').fetchall()
            teachers = db.execute('SELECT * FROM teachers').fetchall()
            courses = db.execute('SELECT * FROM courses').fetchall()
        return render_template('questionnaire.html', students=students, teachers=teachers, courses=courses)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
