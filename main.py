from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///milestones.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Milestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date_achieved = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    success = request.args.get('success')
    entries = Milestone.query.order_by(Milestone.id.desc()).all()
    return render_template('index.html', entries=entries, success=success)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('content')
    date = request.form.get('date')
    if title and date:
        new_milestone = Milestone(title=title, date_achieved=date)
        db.session.add(new_milestone)
        db.session.commit()
    return redirect('/?success=1')

@app.route('/delete/<int:id>')
def delete(id):
    milestone_to_delete = Milestone.query.get_or_404(id)
    db.session.delete(milestone_to_delete)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    milestone = Milestone.query.get_or_404(id)
    # We now update BOTH the title and the date
    milestone.title = request.form.get('new_title')
    milestone.date_achieved = request.form.get('new_date') 
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)