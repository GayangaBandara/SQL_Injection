from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Initialize database and add default users
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'secret')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('user1', 'pass123')")
    conn.commit()
    conn.close()

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# LOGIN vulnerable to SQL injection
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # VULNERABLE: Using string formatting
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"Executing Query: {query}")  # To display in console logs

        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        if user:
            return render_template('welcome.html', username=username)
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

# SEARCH vulnerable to SQL injection
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # VULNERABLE: Using string formatting
        query = f"SELECT username FROM users WHERE username LIKE '%{search_term}%'"
        print(f"Executing Query: {query}")  # To display in console logs

        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
    return render_template('search.html', results=results)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
