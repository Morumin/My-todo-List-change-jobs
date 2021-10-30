import sqlite3

from flask import Flask, render_template, request, redirect, url_for ,session
app = Flask(__name__)
app.secret_key = 'secret_key'

sqlite_path = 'db/mytodo.db'


def get_db_connection():
    connection = sqlite3.connect(sqlite_path)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def login():
    your_name = request.args.get('name', '')
    
    if your_name:
        session['username'] = your_name
        return redirect(url_for('index'))
    else:
        return render_template('mytodo_login.html')


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/todolist", methods=["GET", "POST"])
def index():    
    connection = get_db_connection()
    cursor = connection.cursor()
    res = cursor.execute('SELECT * FROM mytodo') 
    return render_template('mytodo_open.html', mytodo1 = res.fetchall())


@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == 'GET': 
        todo = {}
        return render_template('mytodo_edit.html', mytodo1=todo)
    else:
        connection = get_db_connection()
        cursor = connection.cursor()
        error = []

        if not request.form['name']:  
            error.append('タスクが未入力です')

        if error:
            todo = request.form['name']
            return render_template('mytodo_open.html', mytodo1=todo, error_list=error)

        cursor.execute('INSERT INTO mytodo(name) VALUES(?)',
                      (request.form['name'],))
        connection.commit()
        return redirect(url_for('index'))


@app.route("/delete/<int:id>")
def delete(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM mytodo WHERE id = ? ', (id,))
    connection.commit()
    return redirect(url_for('index'))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_task(id):
    if request.method == 'GET':
        connection = get_db_connection()
        cursor = connection.cursor()
        res = cursor.execute('SELECT * FROM mytodo WHERE id = ?', (id,))
        return render_template('mytodo_edit.html', mytodo1=res.fetchone())
    else:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('UPDATE mytodo SET name = ? WHERE id = ?',
                       (request.form['name'],id))
        connection.commit()
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)