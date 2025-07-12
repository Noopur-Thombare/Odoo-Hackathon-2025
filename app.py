<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, session, g, flash
import sqlite3
import hashlib

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash("Username already exists.")
            return redirect('/register')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['id']
            session['username'] = username
            return redirect('/profile')
        else:
            flash("Invalid credentials.")
            return redirect('/login')
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        offered = request.form['skills_offered']
        needed = request.form['skills_needed']
        availability = request.form['availability']

        cursor.execute('''
            UPDATE users 
            SET skills_offered=?, skills_needed=?, availability=? 
            WHERE id=?
        ''', (offered, needed, availability, session['user_id']))
        db.commit()
        return redirect('/browse')

    cursor.execute("SELECT * FROM users WHERE id=?", (session['user_id'],))
    user = cursor.fetchone()
    return render_template('profile.html', user=user)

@app.route('/browse')
def browse():
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id != ?", (session['user_id'],))
    users = cursor.fetchall()
    return render_template('browse.html', users=users)

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
=======
from flask import Flask, render_template, request
import sqlite3  # 🔁 Don't forget this import for DB

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to Skill Swap Platform!'

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        name = request.form['name']
        skills_offered = request.form['skills_offered']
        skills_needed = request.form['skills_needed']
        availability = request.form['availability']

        # Save to DB
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO profiles (name, skills_offered, skills_needed, availability) VALUES (?, ?, ?, ?)",
                  (name, skills_offered, skills_needed, availability))
        conn.commit()
        conn.close()

        return "✅ Profile saved to database!"
    
    return render_template('profile.html')

@app.route('/browse')
def browse():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM profiles")
    profiles = c.fetchall()
    conn.close()
    
    print("🟡 Profiles from DB:")
    print(profiles)  # This will print in terminal

    return render_template('browse.html', profiles=profiles)

@app.route('/request_swap', methods=['POST'])
def request_swap():
    receiver_name = request.form['receiver_name']
    requester_name = "Kiran Dhamande"  # 🔁 Later this should come from session/login

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO swaps (requester_name, receiver_name, status) VALUES (?, ?, ?)",
              (requester_name, receiver_name, "pending"))
    conn.commit()
    conn.close()

    return f"✅ Swap request sent to {receiver_name}!"

@app.route('/my_swaps', methods=['GET', 'POST'])
def my_swaps():
    current_user = "Kiran Dhamande"  # You can make dynamic later

    if request.method == 'POST':
        swap_id = request.form['swap_id']
        action = request.form['action']  # accept or reject

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE swaps SET status = ? WHERE id = ?", (action, swap_id))
        conn.commit()
        conn.close()

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Swaps sent by current user
    c.execute("SELECT receiver_name, status FROM swaps WHERE requester_name = ?", (current_user,))
    sent = c.fetchall()

    # Swaps received by current user (also get swap_id)
    c.execute("SELECT id, requester_name, status FROM swaps WHERE receiver_name = ?", (current_user,))
    received = c.fetchall()

    conn.close()
    return render_template("my_swaps.html", sent=sent, received=received)



if __name__ == '__main__':
    app.run(debug=True)

>>>>>>> d287679bf1a62fa0d2e674c94f65881bba75e939
