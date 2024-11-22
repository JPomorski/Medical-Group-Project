from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
api = Api(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    blood_type = db.Column(db.String(100), nullable=False)
    allergies = db.Column(db.String(100))
    diseases = db.Column(db.String(100))
    on_medication = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()
class PatientRegistration(Resource):
    def post(self):
        data = request.json
        name = data['name']
        surname = data['surname']
        age = data['age']
        gender = data['gender']
        blood_type = data['blood_type']
        allergies = data['allergies']
        diseases = data['diseases']
        on_medication = True if 'on_medication' in request.form else False

        if not name or not surname or not age or not gender or not blood_type:
            return {'message' : 'Missing information'}, 400
        # if Patient.query.filter_by(username = username).first():
        #     return {'message' : 'Username already taken'}, 400

        new_patient = Patient(name = name, surname = surname, age = age, gender = gender, blood_type = blood_type, allergies = allergies, diseases = diseases, on_medication = on_medication)
        db.session.add(new_patient)
        db.session.commit()
        return {'message' : 'Patient added successfully'}, 200
        #return redirect('/login')

# accident form panel
@app.route('/', methods=['GET', 'POST'])
def main():  # put application's code here
    return render_template('main_site.html')

# registration panel
@app.route('/register', methods=['GET', 'POST'])
def register():  # put application's code here
    if request.method == 'POST':
        return PatientRegistration().post()
    return render_template('register.html')

# forms panel
@app.route('/all')
def all():  # put application's code here
    patients = Patient.query.all()  # Pobranie wszystkich pacjentów z bazy danych
    return render_template('all.html', patients=patients)

api.add_resource(PatientRegistration, '/register')

# injuries panel
@app.route('/body_injuries')
def body_injuries():  # put application's code here
    return render_template('body_injuries.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
