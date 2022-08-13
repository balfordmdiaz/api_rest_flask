from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import validates
from dotenv import load_dotenv

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'SQLALCHEMY_DATABASE_URI'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


class Employees(db.Model):

    __tablename__ = "tbl_employees"

    idemployee = db.Column(db.Integer, primary_key=True, nullable=False)
    idl_employee = db.Column(db.String(45), nullable=False)
    name = db.Column(db.String(45), nullable=False)
    lastname = db.Column(db.String(45), nullable=False)
    identification = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(45), nullable=False)
    phone = db.Column(db.String(45), nullable=False)

    def __init__(self, idl, name, lastname, identif, address, phone):
        self.idl_employee = idl 
        self.name = name 
        self.lastname = lastname 
        self.identification = identif 
        self.address = address 
        self.phone = phone


    @validates('idl_employee')
    def validate_idl(self, key, value):

        if not value:
            raise AssertionError('The idl phone is missing!')

        if value.isspace():
            raise AssertionError('The field has space!')

        if Employees.query.filter(Employees.idl_employee == value).first():
            raise AssertionError('The idl_employee is already in use!')

        return value

    
    @validates('name', 'lastname', 'identification', 'address')
    def validate_name(self, key, value):

        if not value:
            raise AssertionError('One of the field is missing!')

        if value.isspace():
            raise AssertionError('One of the field has space!')

        return value


    @validates('phone')
    def validate_phone(self, key, phone):

        if not phone:
            raise AssertionError('The field phone is missing!')

        if phone.isspace():
            raise AssertionError('The field has space!')

        if len(phone) > 8 or len(phone) < 8:
            raise AssertionError('The length of field phone must be 8 digits!')

        return phone


#Esquema categoria
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('idemployee','idl_employee','name', 'lastname', 'identification', 'address', 'phone')


#una sola respuesta
employee_schema = EmployeeSchema()
#varias respuesta
employees_schema = EmployeeSchema(many=True)


@app.route('/employee', methods=['GET'])
def get_employees():

    all_employees = Employees.query.all()
    result = employees_schema.dump(all_employees)

    return jsonify(result)


@app.route('/employee/<id>', methods=['GET'])
def get_categorie_by_id(id):

    employee = Employees.query.get(id)

    return employee_schema.jsonify(employee)


#POST
@app.route('/employee', methods=['POST'])
def insert_categorie():
    '''
    Force to send a json
    '''
    data = request.get_json(force=True)

    idl = data['idl_employee']
    name = data['name']
    lastname = data['lastname']
    identif = data['identification']
    address = data['address']
    phone = data['phone']

    new_register = Employees(idl, name, lastname, identif, address, phone)

    db.session.add(new_register)
    db.session.commit()

    return employee_schema.jsonify(new_register)


#PUT (UPDATE)
@app.route('/employee/<id>', methods=['PUT'])
def update_categorie(id):

    updateEmp = Employees.query.get(id)

    data = request.get_json(force=True)

    idl = data['idl_employee']
    name = data['name']
    lastname = data['lastname']
    identif = data['identification']
    address = data['address']
    phone = data['phone']

    updateEmp.idl = idl
    updateEmp.name = name
    updateEmp.lastname = lastname
    updateEmp.identif = identif
    updateEmp.address = address
    updateEmp.phone = phone

    db.session.commit()
    return employee_schema.jsonify(updateEmp)

#DELETE
@app.route('/employee/<id>', methods=['DELETE'])
def delete_categorie(id):

    deleteEmp = Employees.query.get(id)

    db.session.delete(deleteEmp)
    db.session.commit()

    return employee_schema.jsonify(deleteEmp)



if __name__=="__main__":
    app.run(debug=True)