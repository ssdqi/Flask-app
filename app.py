from flask import Flask, request, redirect, url_for, render_template
import sqlite3


app = Flask(__name__)

@app.route('/')
def index():
    db = get_db_connection()
    students = db.execute('SELECT * FROM students').fetchall()
    db.close()
    return render_template('index.html', students=students)


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
    db.commit()
    db.close()



@app.route('/add', methods=['GET', 'POST'])
def add_student_page():
    if request.method == 'POST':
        name = request.form['name']
        student_class = request.form['class']
        add_student(name, student_class)
        return redirect(url_for('index'))  # Kullanıcıyı ana sayfaya yönlendir
    return render_template('add_student.html')

    db.close()


if __name__ == '__main__':
    init_db()  # Veritabanını ilk defa oluştur
    app.run(debug=True)
