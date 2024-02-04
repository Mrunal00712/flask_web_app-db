from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # SQLite database file
db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(255), nullable=False)
    test_duration = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        test_name = request.form['test_name']
        test_duration = int(request.form['test_duration'])

        new_test = Test(test_name=test_name, test_duration=test_duration)
        db.session.add(new_test)
        db.session.commit()

        return redirect(url_for('index'))

    tests = Test.query.all()
    return render_template('index.html', tests=tests)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

