from flask import Flask, request, redirect, url_for, render_template
import sqlite3


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary')
def summary():
    db = get_db_connection()
    students = db.execute('SELECT * FROM students').fetchall()
    # Burada öğrencilerin tercihlerine göre gerekli sorguları yapabilirsiniz.
    db.close()
    # Daha sonra öğrenci verileri ve diğer gerekli bilgileri summary.html'e gönderin.
    return render_template('summary.html', students=students)


@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if request.method == 'POST':
        # Formdan gelen verileri işleyin ve veritabanına kaydedin
        # Örneğin: Öğrenci ID, öğretmen ID, seçilen ders ve arkadaş tercihleri
        return redirect(url_for('summary'))  # Anket doldurulduktan sonra özete yönlendir
    else:
        db = get_db_connection()
        students = db.execute('SELECT * FROM students').fetchall()
        teachers = db.execute('SELECT * FROM teachers').fetchall()  # Öğretmenler tablosunu da eklemeniz gerekir
        courses = db.execute('SELECT * FROM courses').fetchall()  # Dersler tablosunu da eklemeniz gerekir
        db.close()
        return render_template('questionnaire.html', students=students, teachers=teachers, courses=courses)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def add_student(name, student_class):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('INSERT INTO students (name, class) VALUES (?, ?)', (name, student_class))
    db.commit()
    db.close()


def init_db():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class TEXT NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class TEXT NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    ''')
    cursor.execute('''
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
    db.close()



if __name__ == '__main__':
    init_db()  # Veritabanını ilk defa oluştur
    app.run(debug=True)
