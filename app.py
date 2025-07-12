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

