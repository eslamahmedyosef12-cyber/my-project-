from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'youssef_secret_key' # غيرها لأي كلمة سر خاصة بك

ADMIN_PASSWORD = '123' # كلمة سر الدخول للوحة التحكم

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    name = request.form['name']
    phone = request.form['phone']
    with open('orders.txt', 'a', encoding='utf-8') as f:
        f.write(f"الاسم: {name} | الهاتف: {phone}\n")
    return render_template('thankyou.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('logged_in'):
        try:
            with open('orders.txt', 'r', encoding='utf-8') as f:
                orders = f.readlines()
        except FileNotFoundError:
            orders = []
        return render_template('admin.html', orders=orders)
    
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect('/admin')
        return "كلمة سر خاطئة! <a href='/admin'>حاول مرة أخرى</a>"
            
    return '<form method="post"><input type="password" name="password" placeholder="كلمة السر"><button type="submit">دخول</button></form>'

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

