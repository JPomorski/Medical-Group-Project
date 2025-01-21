from flask import Flask, request, render_template, jsonify
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
    svg_content = db.Column(db.Text, nullable=False)  
    descriptions = db.Column(db.Text, nullable=True)  
    timestamp = db.Column(db.DateTime, server_default=db.func.now())  
    priority = db.Column(db.Integer, nullable=False, default=0)

# class SVGRecord(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     svg_content = db.Column(db.Text, nullable=False)  # Przechowuje zawartość SVG
#     descriptions = db.Column(db.Text, nullable=True)  # Pole na opisy
#     timestamp = db.Column(db.DateTime, server_default=db.func.now())  # Data zapisu

with app.app_context():
    db.create_all()

class PatientRegistration(Resource):
    def post(self):
        data = request.json

        name = data.get('name')
        surname = data.get('surname')
        age = data.get('age')
        gender = data.get('gender')
        blood_type = data.get('blood_type')
        allergies = data.get('allergies')
        diseases = data.get('diseases')
        on_medication = data.get('on_medication', '').lower() == 'yes'
        svg_content = data.get('svg_content')
        descriptions = data.get('descriptions')
        priority = data.get('priority')

        if not name or not surname or not age or not gender or not blood_type:
            return jsonify({'message': 'Missing information'}), 400

        new_patient = Patient(
            name=name,
            surname=surname,
            age=age,
            gender=gender,
            blood_type=blood_type,
            allergies=allergies,
            diseases=diseases,
            on_medication=on_medication,
            svg_content=svg_content,  
            descriptions=descriptions,
            priority=priority
        )

        db.session.add(new_patient)
        db.session.commit()

        message = 'Patient added successfully'
        if svg_content:
            message += ' and SVG saved successfully'
        if descriptions:
            message += ' and descriptions saved successfully'

        return jsonify({'message': message}), 200


class PatientDeletion(Resource):
    @staticmethod
    def delete(patient_id):
        try:
            patient = db.session.get(Patient, patient_id)

            if not patient:
                return {'message': 'Patient not found'}, 404

            db.session.delete(patient)
            db.session.commit()

            return {'message': 'Patient deleted successfully'}, 200

        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500


api.add_resource(PatientDeletion, '/delete/<int:patient_id>')


class PatientEdition(Resource):
    @staticmethod
    def get(patient_id):
        patient = db.session.get(Patient, patient_id)

        if not patient:
            return jsonify({'message': 'Patient not found'}), 404

        patient_data = {
            'name': patient.name,
            'surname': patient.surname,
            'age': patient.age,
            'gender': patient.gender,
            'blood_type': patient.blood_type,
            'allergies': patient.allergies,
            'diseases': patient.diseases,
            'on_medication': 'Yes' if patient.on_medication else 'No',
            'priority': patient.priority
        }
        return jsonify(patient_data), 200


class PatientUpdate(Resource):
    @staticmethod
    def put(patient_id):
        data = request.json
        patient = db.session.get(Patient, patient_id)

        if not patient:
            return jsonify({'message': 'Patient not found'}), 404

        patient.name = data.get('name')
        patient.surname = data.get('surname')
        patient.age = data.get('age')
        patient.gender = data.get('gender')
        patient.blood_type = data.get('blood_type')
        patient.allergies = data.get('allergies')
        patient.diseases = data.get('diseases')
        patient.on_medication = data.get('on_medication', '').lower() == 'yes'
        patient.priority = data.get('priority')

        db.session.commit()

        return jsonify({'message': "Patient's data updated successfully"}), 200

@app.route('/', methods=['GET', 'POST'])
def main():  
    return render_template('main_site.html')


@app.route('/register', methods=['GET', 'POST'])
def register():  
    if request.method == 'POST':
        return PatientRegistration().post()
    return render_template('register.html')

@app.route('/delete/<int:patient_id>', methods=['DELETE'])
def delete(patient_id):
    return PatientDeletion().delete(patient_id)

@app.route('/edit/<int:patient_id>', methods=['GET'])
def edit(patient_id):
    return PatientEdition().get(patient_id)

@app.route('/update/<int:patient_id>', methods=['PUT'])
def update(patient_id):
    return PatientUpdate().put(patient_id)


@app.route('/all')
def all():  
    patients = Patient.query.all()  
    return render_template('all.html', patients=patients)

api.add_resource(PatientRegistration, '/register')

@app.route('/display_svg_with_bg/<int:patient_id>', methods=['GET'])
def display_svg_with_bg(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient or not patient.svg_content:
        return "SVG not found or patient has no SVG data", 404

    svg_with_bg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="612" height="612" preserveAspectRatio="none">
        <image width="612" height="612" preserveAspectRatio="none" xlink:href="/static/images/human_body_model.jpg" />
        {patient.svg_content}
    </svg>"""

    return render_template(
        'display_svg.html',
        svg_content=svg_with_bg,
        descriptions=patient.descriptions
    )



if __name__ == '__main__':
    app.run(debug=True, port=5001)