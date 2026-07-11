	mport os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

app = Flask(__name__)

# إعدادات الحماية وقاعدة البيانات في المجلد المؤقت لتعمل على Vercel
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('/tmp', 'test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# تعريف المستخدم
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return "مرحباً، موقعي يعمل الآن بنجاح على Vercel!"

if __name__ == '__main__':
    # التأكد من إنشاء قاعدة البيانات في المجلد المؤقت عند التشغيل المحلي
    with app.app_context():
        db.create_all()
    app.run()

