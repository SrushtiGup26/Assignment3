from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@DESKTOP-J64M37M\\SQLEXPRESS/Assignment3_AI_in_Enterprise?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    return render_template('Finalhtmlfile.html')

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    new_student = Student(
        first_name=data['first_name'],
        last_name=data['last_name'],
        dob=datetime.strptime(data['dob'], '%Y-%m-%d').date(),
        amount_due=data['amount_due']
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student created successfully!"}), 201

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    student_list = []
    for student in students:
        student_info = {
            'student_id': student.student_id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'dob': student.dob.strftime('%Y-%m-%d'),
            'amount_due': float(student.amount_due)
        }
        student_list.append(student_info)
    return jsonify(student_list)

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "Student not found!"}), 404
    student_info = {
        'student_id': student.student_id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'dob': student.dob.strftime('%Y-%m-%d'),
        'amount_due': float(student.amount_due)
    }
    return jsonify(student_info)

@app.route('/students/search/<first_name>', methods=['GET'])
def search_student_by_name(first_name):
    student = Student.query.filter_by(first_name=first_name).first()
    if not student:
        return jsonify(None)
    student_info = {
        'student_id': student.student_id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'dob': student.dob.strftime('%Y-%m-%d'),
        'amount_due': float(student.amount_due)
    }
    return jsonify(student_info)

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "Student not found!"}), 404

    student.first_name = data['first_name']
    student.last_name = data['last_name']
    student.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
    student.amount_due = data['amount_due']
    db.session.commit()
    return jsonify({"message": "Student updated successfully!"})

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "Student not found!"}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)
