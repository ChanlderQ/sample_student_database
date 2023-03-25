
from flask import Flask, request, jsonify,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
# Initialize app
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Student Class/Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), unique=False)
    last_name = db.Column(db.String(100), unique=False)
    dob = db.Column(db.String(10), unique=False)
    amount_due = db.Column(db.Float, unique=False)

    def __init__(self, id,first_name, last_name, dob, amount_due):
        self.id=id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.amount_due = amount_due
        
student_john = Student(id=1,first_name='john',
                       last_name='doe',
                       dob="19850207",
                       amount_due=10)

student_joy = Student(id=2,first_name='joy',
                      last_name='mk',
                       dob="19880325",
                       amount_due=20)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_student',methods=["GET","POST"])
def create_student():
    if request.method == 'POST':
        id=request.form['id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        amount_due = request.form['amount_due']

        new_student = Student(id=id,first_name=first_name,
                      last_name=last_name,
                       dob=dob,
                       amount_due=amount_due)
        try:
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue adding the student'

    return render_template('create_student.html')

@app.route('/delete_students/<int:id>',methods=['POST'])
def delete_students(id):
    student_to_delete = Student.query.get_or_404(id)
    try:
        db.session.delete(student_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was an issue deleting the student'
    
@app.route('/update_student', methods=['GET','POST'])
def update_student():
    if request.method == 'POST':
        
        id_number=int(request.form['id'])
        update_student = Student.query.get_or_404(id_number)
        update_student.first_name = request.form['first_name']
        update_student.last_name = request.form['last_name']
        update_student.dob = request.form['dob']
        update_student.amount_due = request.form['amount_due']
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue adding the student'
    return render_template('update_student.html')


@app.route('/view_students')
def view_students():
    all_students=Student.query.all()
    return render_template('view_students.html',students=all_students)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.add(student_john)
        db.session.add(student_joy)
        db.session.commit()
    app.run(debug=True, port=8000, use_reloader=False)
    
