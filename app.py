from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'construsafe_secret_key'
app.database = os.path.join(app.instance_path, 'construsafe.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.database)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = get_db().cursor()
        cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cur.fetchone()
        if user:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Usuário ou senha incorretos.'
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM occurrences WHERE user = ?", (session['user'],))
    occurrences = cur.fetchall()
    return render_template('dashboard.html', user=session['user'], occurrences=occurrences)

@app.route('/add', methods=['GET', 'POST'])
def add_occurrence():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        date = request.form['date']
        location = request.form['location']
        type_ = request.form['type']
        description = request.form['description']
        db = get_db()
        db.execute("INSERT INTO occurrences (user, date, location, type, description) VALUES (?, ?, ?, ?, ?)",
                   (session['user'], date, location, type_, description))
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('add.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/epi', methods=['GET', 'POST'])
def add_epi():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        date = request.form['date']
        item = request.form['item']
        quantity = request.form['quantity']
        note = request.form['note']
        db.execute("INSERT INTO epis (user, date, item, quantity, note) VALUES (?, ?, ?, ?, ?)",
                   (session['user'], date, item, quantity, note))
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_epi.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM occurrences WHERE user = ?", (session['user'],))
    occurrences = cur.fetchall()
    # Gráfico de ocorrências por tipo
    cur.execute("SELECT type, COUNT(*) FROM occurrences WHERE user = ? GROUP BY type", (session['user'],))
    results = cur.fetchall()
    chart_labels = [r[0] for r in results]
    chart_data = [r[1] for r in results]
    return render_template('dashboard.html', user=session['user'], occurrences=occurrences,
                           chart_labels=chart_labels, chart_data=chart_data)
        

if __name__ == '__main__':

    app.run(debug=True)

from flask import send_file
import pandas as pd
from fpdf import FPDF

@app.route('/export/excel')
def export_excel():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    user_filter = session['user'] if session['role'] != 'admin' else None
    if user_filter:
        df = pd.read_sql_query("SELECT * FROM occurrences WHERE user = ?", db, params=(user_filter,))
    else:
        df = pd.read_sql_query("SELECT * FROM occurrences", db)
    path = "instance/ocorrencias_export.xlsx"
    df.to_excel(path, index=False)
    return send_file(path, as_attachment=True)

@app.route('/export/pdf')
def export_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    user_filter = session['user'] if session['role'] != 'admin' else None
    if user_filter:
        data = db.execute("SELECT date, place, type, description FROM occurrences WHERE user = ?", (user_filter,)).fetchall()
    else:
        data = db.execute("SELECT user, date, place, type, description FROM occurrences").fetchall()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório de Ocorrências", ln=1, align='C')
    for row in data:
        pdf.cell(200, 10, txt=" | ".join(str(x) for x in row), ln=1)
    path = "instance/ocorrencias_export.pdf"
    pdf.output(path)
    return send_file(path, as_attachment=True)
