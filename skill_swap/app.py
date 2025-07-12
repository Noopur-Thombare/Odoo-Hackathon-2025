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
    return render_template('index.html')

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

@app.route('/respond_swap/<int:swap_id>', methods=['POST'])
def respond_swap(swap_id):
    if 'user_id' not in session:
        return redirect('/login')

    response = request.form['response']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        UPDATE swaps SET status=? WHERE id=? AND receiver_id=?
    ''', (response, swap_id, session['user_id']))
    db.commit()
    return redirect('/my_swaps')

@app.route('/my_swaps')
def my_swaps():
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT swaps.id, users.name, swaps.status
        FROM swaps JOIN users ON swaps.requester_id = users.id
        WHERE swaps.receiver_id=?
    ''', (session['user_id'],))
    swaps = cursor.fetchall()
    return render_template('swaps.html', swaps=swaps)

# 🚀 App entry point
if __name__ == '__main__':
    app.run(debug=True)
