from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    equipment_type = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    problem_description = db.Column(db.Text, nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(50), default='Новая заявка')

@app.route('/')
def index():
    requests = Request.query.all()
    return render_template('index.html', requests=requests)

@app.route('/add', methods=['GET', 'POST'])
def add_applications():
    if request.method == 'POST':
        new_request = Request(
            equipment_type=request.form['equipment_type'],
            model=request.form['model'],
            problem_description=request.form['problem_description'],
            client_name=request.form['client_name'],
            phone_number=request.form['phone_number'],
            status=request.form['status']
        )
        db.session.add(new_request)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_applications.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
