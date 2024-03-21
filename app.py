
from flask import Flask, request, render_template, redirect, url_for, send_file
import qrcode
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/ANUSH/OneDrive/Desktop/Generator/Website/database/database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, default=datetime.datetime.utcnow)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        new_user = User(username=data['new_username'], password=data['new_password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if not user or user.password != data['password']:
            return 'Login failed!'
        user.last_login = datetime.datetime.utcnow()
        db.session.commit()
        return '<div style="background-color: lightgreen; padding: 10px;">Login successful!</div>'

    return render_template('login.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin_panel():
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/generate_qr', methods=['GET', 'POST'])
def generate_qr():
    if request.method == 'POST':
        # Get data from the form
        data = request.form['data']
        
       ''' # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create PIL image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save the image to disk
        img_path = os.path.join(app.static_folder, 'images', 'qr_code.png')
        img.save(img_path, 'PNG')

        return send_file(img_path, mimetype='image/png')

    return render_template('generate_qr.html')'''

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
