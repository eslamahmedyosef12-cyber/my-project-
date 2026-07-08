from flask import Flask, render_template_string, request, session, g
import sqlite3, hashlib, os

app = Flask(__name__)
app.secret_key = 'super_secret_key_12345'
DATABASE = 'pentest.db'

# ======== HTML Templates كاملة جوه الملف ========

INDEX_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Pentest Lab — Home</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0a0a0a; color: #e0e0e0; margin: 0; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: #1a1a1a; padding: 30px; border-radius: 10px; border: 1px solid #333; }
        h1 { color: #ff4444; text-align: center; }
        h3 { color: #ffaa00; }
        .menu { display: flex; gap: 15px; flex-wrap: wrap; margin: 20px 0; justify-content: center; }
        .menu a, a { display: inline-block; padding: 10px 20px; background: #ff4444; color: white; text-decoration: none; border-radius: 5px; margin: 5px; }
        .menu a:hover, a:hover { background: #cc0000; }
        input { width: 100%; padding: 10px; margin: 10px 0; background: #2a2a2a; border: 1px solid #444; color: white; border-radius: 5px; }
        button { padding: 10px 30px; background: #00aa00; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .query-box { background: #2a2a2a; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #ffaa00; }
        code { color: #00ff00; word-break: break-all; }
        .error { background: #440000; padding: 10px; border-radius: 5px; border: 1px solid #ff4444; color: #ff4444; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        th, td { padding: 10px; border: 1px solid #444; text-align: left; }
        th { background: #333; }
        ul { line-height: 2; }
        .search-term { margin-top: 20px; padding: 15px; background: #2a2a2a; border-radius: 5px; border-left: 4px solid #ff4444; }
        .footer { margin-top: 30px; text-align: center; color: #666; }
        .user-info { background: #2a2a2a; padding: 15px; border-radius: 5px; margin: 15px 0; }
        .payloads { background: #1a2a1a; padding: 15px; border-radius: 5px; margin: 15px 0; }
        .success { background: #004400; padding: 10px; border-radius: 5px; border: 1px solid #00ff00; color: #00ff00; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔴 Pentest Lab</h1>
        <p style="text-align:center;">Vulnerable Web Application — Authorized Testing Only</p>
        <div class="menu">
            <a href="/">🏠 Home</a>
            <a href="/login">🔑 SQLi Login</a>
            <a href="/search">🔍 Search (SQLi + XSS)</a>
            <a href="/profile/1">👤 Profile (IDOR)</a>
            <a href="/admin">⚡ Admin Panel</a>
            <a href="/flags">🚩 All Flags</a>
        </div>
        <div class="footer">
            <small>Authorized penetration testing only. Flags are hidden in the database.</small>
        </div>
    </div>
</body>
</html>
'''

LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login — Pentest Lab</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0a0a0a; color: #e0e0e0; margin: 0; padding: 20px; }
        .container { max-width: 700px; margin: 0 auto; background: #1a1a1a; padding: 30px; border-radius: 10px; border: 1px solid #333; }
        h1 { color: #ff4444; }
        h3 { color: #ffaa00; }
        input { width: 100%; padding: 10px; margin: 10px 0; background: #2a2a2a; border: 1px solid #444; color: white; border-radius: 5px; box-sizing: border-box; }
        button { padding: 10px 30px; background: #00aa00; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .query-box { background: #2a2a2a; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #ffaa00; }
        code { color: #00ff00; word-break: break-all; }
        .error { background: #440000; padding: 10px; border-radius: 5px; border: 1px solid #ff4444; color: #ff4444; }
        .success { background: #004400; padding: 10px; border-radius: 5px; border: 1px solid #00ff00; color: #00ff00; }
        a { display: inline-block; padding: 10px 20px; background: #ff4444; color: white; text-decoration: none; border-radius: 5px; margin: 5px; }
        a:hover { background: #cc0000; }
        ul { line-height: 2; }
        .menu { margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔑 SQL Injection Login</h1>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        {% if success_msg %}
        <div class="success">{{ success_msg }}</div>
        {% endif %}
        
        {% if query %}
        <div class="query-box">
            <strong>SQL Query Executed:</strong><br>
            <code>{{ query }}</code>
        </div>
        {% endif %}
        
        {% if user_data %}
        <div class="query-box">
            <strong>✅ User Data Retrieved:</strong><br>
            <code>ID: {{ user_data[0] }} | Username: {{ user_data[1] }} | Role: {{ user_data[2] }} | Flag: {{ user_data[3] }}</code>
        </div>
        {% endif %}
        
        <form method="POST">
            <label><strong>Username:</strong></label>
            <input type="text" name="username" placeholder="admin' OR '1'='1">
            <label><strong>Password:</strong></label>
            <input type="password" name="password" placeholder="anything">
            <button type="submit">🚀 Inject & Login</button>
        </form>
        
        <div class="payloads">
            <h3>🎯 Payloads جاهزة</h3>
            <ul>
                <li><code>admin' OR '1'='1</code> — أي باسورد</li>
                <li><code>admin' --</code> — تعليق الباقي</li>
                <li><code>' OR 1=1 --</code> — كل المستخدمين</li>
                <li><code>' UNION SELECT 1,2,3,4 --</code> — Union test</li>
                <li><code>' UNION SELECT id, username, role, sql FROM sqlite_master --</code> — جلب هيكل الجداول</li>
                <li><code>' UNION SELECT id, credit_card, ssn, pin FROM secrets --</code> — سرقة البيانات</li>
            </ul>
        </div>
        
        <div class="menu">
            <a href="/">← Home</a>
        </div>
    </div>
</body>
</html>
'''

SEARCH_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Search — Pentest Lab</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0a0a0a; color: #e0e0e0; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: #1a1a1a; padding: 30px; border-radius: 10px; border: 1px solid #333; }
        h1 { color: #ff4444; }
        h3 { color: #ffaa00; }
        input { width: 80%; padding: 10px; background: #2a2a2a; border: 1px solid #444; color: white; border-radius: 5px; }
        button { padding: 10px 20px; background: #00aa00; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .query-box { background: #2a2a2a; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #ffaa00; }
        code { color: #00ff00; word-break: break-all; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        th, td { padding: 10px; border: 1px solid #444; text-align: left; }
        th { background: #333; }
        .search-term { margin-top: 20px; padding: 15px; background: #2a2a2a; border-radius: 5px; border-left: 4px solid #ff4444; }
        a { display: inline-block; padding: 10px 20px; background: #ff4444; color: white; text-decoration: none; border-radius: 5px; margin: 5px; }
        a:hover { background: #cc0000; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Search Users (SQLi + XSS)</h1>
        
        <form method="GET">
            <input type="text" name="q" placeholder="Search or inject..." value="{{ search_term }}">
            <button type="submit">🔍 Search</button>
        </form>
        
        {% if query %}
        <div class="query-box">
            <strong>SQL Query:</strong><br>
            <code>{{ query }}</code>
        </div>
        {% endif %}
        
        {% if results %}
        <h3>Results:</h3>
        <table>
            <tr><th>ID</th><th>Username</th><th>Role</th></tr>
            {% for r in results %}
            <tr><td>{{ r[0] }}</td><td>{{ r[1] }}</td><td>{{ r[2] }}</td></tr>
            {% endfor %}
        </table>
        {% endif %}
        
        <!-- ⚠️ XSS Reflected -->
        <div class="search-term">
            <strong>You searched for:</strong> {{ search_term | safe }}
        </div>
        
        <a href="/">← Home</a>
    </div>
</body>
</html>
'''

PROFILE_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Profile — Pentest Lab</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0a0a0a; color: #e0e0e0; margin: 0; padding: 20px; }
        .container { max-width: 700px; margin: 0 auto; background: #1a1a1a; padding: 30px; border-radius: 10px; border: 1px solid #333; }
        h1 { color: #ff4444; }
        h3 { color: #ffaa00; }
        .user-info { background: #2a2a2a; padding: 15px; border-radius: 5px; margin: 15px 0; }
        .secrets { background: #2a1a1a; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #ff0000; }
        a { display: inline-block; padding: 10px 20px; background: #ff4444; color: white; text-decoration: none; border-radius: 5px; margin: 5px; }
        a:hover { background: #cc0000; }
        .menu { margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>👤 User Profile (IDOR)</h1>
        
        {% if user %}
        <div class="user-info">
            <p><strong>ID:</strong> {{ user[0] }}</p>
            <p><strong>Username:</strong> {{ user[1] }}</p>
            <p><strong>Role:</strong> {{ user[2] }}</p>
            <p><strong>Secret Flag:</strong> <code>{{ user[4] }}</code></p>
        </div>
        {% endif %}
        
        {% if secrets %}
        <div class="secrets">
            <h3>💳 Financial Data (Leaked!)</h3>
            <p><strong>Credit Card:</strong> {{ secrets[2] }}</p>
            <p><strong>SSN:</strong> {{ secrets[3] }}</p>
            <p><strong>PIN:</strong> {{ secrets[4] }}</p>
        </div>
        {% endif %}
        
        <div class="menu">
            <strong>Browse Profiles (IDOR):</strong><br>
            <a href="/profile/1">Admin (ID=1)</a>
            <a href="/profile/2">User 1 (ID=2)</a>
            <a href="/profile/3">User 2 (ID=3)</a>
            <a href="/profile/4">Hacker (ID=4)</a>
            <a href="/profile/5">IDOR Test (ID=5)</a>
            <a href="/">← Home</a>
        </div>
    </div>
</body>
</html>
'''

ADMIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Admin — Pentest Lab</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0a0a0a; color: #e0e0e0; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: #1a1a1a; padding: 30px; border-radius: 10px; border: 1px solid #333; }
        h1 { color: #ff4444; }
        h3 { color: #ffaa00; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        th, td { padding: 10px; border: 1px solid #444; text-align: left; }
        th { background: #333; }
        code { color: #00ff00; }
        .query-box { background: #2a2a2a; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #ffaa00; }
        a { display: inline-block; padding: 10px 20px; background: #ff4444; color: white; text-decoration: none; border-radius: 5px; margin: 5px; }
        a:hover { background: #cc0000; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Admin Panel (Auth Bypass)</h1>
        <p style="color: #ffaa00;">كل البيانات مسربة — مفيش صلاحيات</p>
        
        {% if query %}
        <div class="query-box">
            <strong>Query:</strong><br>
            <code>{{ query }}</code>
        </div>
        {% endif %}
        
        <h3>📋 All Users:</h3>
        <table>
            <tr><th>ID</th><th>Username</th><th>Role</th><th>Secret Flag</th></tr>
            {% for u in all_users %}
            <tr>
                <td>{{ u[0] }}</td>
                <td>{{ u[1] }}</td>
                <td>{{ u[2] }}</td>
                <td><code>{{ u[3] }}</code></td>
            </tr>
            {% endfor %}
        </table>
        
        <h3>💳 All Financial Data:</h3>
        <table>
            <tr><th>User ID</th><th>Credit Card</th><th>SSN</th><th>PIN</th></tr>
            {% for s in all_secrets %}
            <tr>
                <td>{{ s[1] }}</td>
                <td>{{ s[2] }}</td>
                <td>{{ s[3] }}</td>
                <td>{{ s[4] }}</td>
            </tr>
            {% endfor %}
        </table>
        
        <a href="/">← Home</a>
    </div>
</body>
</html>
'''

FLAGS_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Flags — Pentest Lab</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0a0a0a; color: #e0e0e0; margin: 0; padding: 20px; }
        .container { max-width: 700px; margin: 0 auto; background: #1a1a1a; padding: 30px; border-radius: 10px; border: 1px solid #333; }
        h1 { color: #ff4444; }
        h3 { color: #ffaa00; }
        code { color: #00ff00; font-size: 18px; }
        .flag { background: #2a2a2a; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #ffaa00; }
        a { display: inline-block; padding: 10px 20px; background: #ff4444; color: white; text-decoration: none; border-radius: 5px; margin: 5px; }
        a:hover { background: #cc0000; }
        ul { line-height: 2.5; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚩 All Flags</h1>
        <p>كل الفلاجات اللي محتاج تطلعها من اللاب:</p>
        
        <div class="flag">
            <strong>Flag 1 — SQLi Login:</strong><br>
            <code>{{ flags[0] }}</code>
            <p style="color: #888;">من users جدول — Secret field</p>
        </div>
        <div class="flag">
            <strong>Flag 2 — Union Injection:</strong><br>
            <code>{{ flags[1] }}</code>
            <p style="color: #888;">جلب data من جدول secrets</p>
        </div>
        <div class="flag">
            <strong>Flag 3 — IDOR:</strong><br>
            <code>{{ flags[2] }}</code>
            <p style="color: #888;">الوصول لبروفايل المستخدمين التانيين</p>
        </div>
        <div class="flag">
            <strong>Flag 4 — Admin Bypass:</strong><br>
            <code>{{ flags[3] }}</code>
            <p style="color: #888;">جلب كل حاجة من الـAdmin panel</p>
        </div>
        
        <h3>🎯 ازاي تطلع كل Flag:</h3>
        <ul>
            <li><strong>Flag 1:</strong> <code>admin' OR '1'='1</code> في صفحة login</li>
            <li><strong>Flag 2:</strong> <code>' UNION SELECT id, credit_card, ssn, pin FROM secrets --</code></li>
            <li><strong>Flag 3:</strong> افتح <code>/profile/2</code> و <code>/profile/3</code> و <code>/profile/4</code></li>
            <li><strong>Flag 4:</strong> افتح <code>/admin</code> — كل البيانات مسربة</li>
        </ul>
        
        <a href="/">← Home</a>
    </div>
</body>
</html>
'''

# ======== Database Functions ========

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user',
        flag TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS secrets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        credit_card TEXT,
        ssn TEXT,
        pin TEXT
    )''')
    
    users_data = [
        ('admin', hashlib.md5('admin123'.encode()).hexdigest(), 'admin', 'FLAG{SQL_1nj3ct10n_M45t3r}'),
        ('user1', hashlib.md5('password1'.encode()).hexdigest(), 'user', 'FLAG{L4zy_P4ssw0rd}'),
        ('user2', hashlib.md5('123456'.encode()).hexdigest(), 'user', 'FLAG{W34k_H4sh}'),
        ('hacker', hashlib.md5('letmein'.encode()).hexdigest(), 'user', 'FLAG{Un1c0rn_1337}')
    ]
    
    c.executemany('INSERT OR IGNORE INTO users (username, password, role, flag) VALUES (?,?,?,?)', users_data)
    
    secrets_data = [
        (1, '4111-1111-1111-1111', '123-45-6789', '1234'),
        (2, '5500-0000-0000-0004', '987-65-4321', '5678'),
        (3, '3400-0000-0000-009', '456-78-9123', '9012'),
        (4, '6011-0000-0000-0004', '321-54-9876', '3456')
    ]
    
    c.executemany('INSERT OR IGNORE INTO secrets (user_id, credit_card, ssn, pin) VALUES (?,?,?,?)', secrets_data)
    
    conn.commit()
    conn.close()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is None:
        return
    db.close()

# ======== Routes ========

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/login', methods=['GET', 'POST'])
def login():
    query = None
    user_data = None
    error = None
    success_msg = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # ⚠️ SQL Injection Vulnerability
        query = f"SELECT id, username, role, flag FROM users WHERE username = '{username}' AND password = '{hashlib.md5(password.encode()).hexdigest()}'"
        
        db = get_db()
        cursor = db.execute(query)
        user = cursor.fetchone()
        
        if user:
            user_data = user
            success_msg = f"✅ Welcome, {user[1]}! Role: {user[2]}"
        else:
            error = '❌ Invalid credentials! Try SQL injection.'
    
    return render_template_string(LOGIN_HTML, query=query, user_data=user_data, error=error, success_msg=success_msg)

@app.route('/search')
def search():
    q = request.args.get('q', '')
    
    query = f"SELECT id, username, role FROM users WHERE username LIKE '%{q}%'"
    
    db = get_db()
    try:
        cursor = db.execute(query)
        results = cursor.fetchall()
    except:
        results = []
    
    return render_template_string(SEARCH_HTML, query=query, results=results, search_term=q)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    db = get_db()
    
    cursor = db.execute(f"SELECT * FROM users WHERE id = {user_id}")
    user = cursor.fetchone()
    
    cursor2 = db.execute(f"SELECT * FROM secrets WHERE user_id = {user_id}")
    secrets = cursor2.fetchone()
    
    return render_template_string(PROFILE_HTML, user=user, secrets=secrets)

@app.route('/admin')
def admin():
    db = get_db()
    
    query = "SELECT id, username, role, flag FROM users"
    all_users = db.execute(query).fetchall()
    
    all_secrets = db.execute("SELECT * FROM secrets").fetchall()
    
    return render_template_string(ADMIN_HTML, all_users=all_users, all_secrets=all_secrets, query=query)

@app.route('/flags')
def flags():
    flags = [
        'FLAG{SQL_1nj3ct10n_M45t3r}',
        'FLAG{S3cr3ts_4r3nt_S4f3}',
        'FLAG{1DOR_1s_D4ng3r0us}',
        'FLAG{4uth_Byp4ss_1s_E4sy}'
    ]
    return render_template_string(FLAGS_HTML, flags=flags)

# ======== Main ========

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        print("[*] Initializing database...")
        init_database()
        print("[+] Database created with vulnerable data!")
    
    print("\n" + "="*50)
    print("🔴 PENTEST LAB RUNNING")
    print("="*50)
    print("📌 Open: http://127.0.0.1:5000")
    print("📌 Ctrl+C to stop")
    print("="*50 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
