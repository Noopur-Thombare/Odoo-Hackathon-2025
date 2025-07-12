from flask import Flask, render_template, request, redirect, session, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATABASE = 'database.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')  # We'll create this file next

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/request_swap/<int:receiver_id>')
def request_swap(receiver_id):
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO swaps (requester_id, receiver_id, status)
        VALUES (?, ?, 'pending')
    ''', (session['user_id'], receiver_id))
    db.commit()
    return redirect('/browse')
