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

class SVGRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    svg_content = db.Column(db.Text, nullable=False)  # Przechowuje zawartość SVG
    descriptions = db.Column(db.Text, nullable=True)  # Pole na opisy
    timestamp = db.Column(db.DateTime, server_default=db.func.now())  # Data zapisu

with app.app_context():
    db.create_all()
class PatientRegistration(Resource):
    def post(self):
        data = request.json

        # Pobieranie danych rejestracyjnych pacjenta
        name = data.get('name')
        surname = data.get('surname')
        age = data.get('age')
        gender = data.get('gender')
        blood_type = data.get('blood_type')
        allergies = data.get('allergies')
        diseases = data.get('diseases')
        on_medication = data.get('on_medication', '').lower() == 'yes'

        # Walidacja wymaganych danych
        if not name or not surname or not age or not gender or not blood_type:
            return jsonify({'message': 'Missing information'}), 400

        # Tworzenie nowego pacjenta
        new_patient = Patient(
            name=name,
            surname=surname,
            age=age,
            gender=gender,
            blood_type=blood_type,
            allergies=allergies,
            diseases=diseases,
            on_medication=on_medication
        )

        db.session.add(new_patient)
        db.session.commit()

        # Pobieranie i zapisywanie danych SVG oraz opisów
        svg_content = data.get('svg_content')
        descriptions = data.get('descriptions')

        if svg_content or descriptions:
            new_svg_record = SVGRecord(
                svg_content=svg_content or '',
                descriptions=descriptions or ''  # Upewnienie się, że pole jest wypełnione, nawet jeśli brak opisów
            )
            db.session.add(new_svg_record)
            db.session.commit()

        message = 'Patient added successfully'
        if svg_content:
            message += ' and SVG saved successfully'
        if descriptions:
            message += ' and descriptions saved successfully'

        return jsonify({'message': message}), 200


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

@app.route('/display_svg_with_bg/<int:svg_id>', methods=['GET'])
def display_svg_with_bg(svg_id):
    svg_record = SVGRecord.query.get(svg_id)
    if not svg_record:
        return "SVG not found", 404

    # Dodanie obrazu tła do SVG
    svg_with_bg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="612" height="612" preserveAspectRatio="none">
        <image width="612" height="612" preserveAspectRatio="none" xlink:href="/static/images/human_body_model.jpg" />
        {svg_record.svg_content}
    </svg>"""

    # Przekazanie opisów do szablonu
    return render_template(
        'display_svg.html',
        svg_content=svg_with_bg,
        descriptions=svg_record.descriptions
    )



if __name__ == '__main__':
    app.run(debug=True, port=5001)