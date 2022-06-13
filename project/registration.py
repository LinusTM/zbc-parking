from flask import Blueprint, render_template, request
from wtforms import Form, SelectField, StringField, validators
from dataclasses import dataclass

registration = Blueprint('registration', __name__)

@dataclass
class Person:
    fname: str
    lname: str
    email: str
    role: int

class RegistrationForm(Form):
    fname   = StringField('fname', [validators.Length(min=4, max=25)])
    lname   = StringField('lname', [validators.Length(min=4, max=25)])
    email   = StringField('Email', [validators.Length(min=8, max=35)])
    role    = SelectField('role', choices=[(1, "Gæst"), (2, "Medarbejder"), (3, "Elev")])

@registration.route("/registration", methods=['GET', 'POST'])
def registration_page():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        Person.fname = form.fname.data 
        Person.lname = form.lname.data 
        Person.email = form.email.data
        Person.role = form.role.data

        # Send values to database
        cur.execute("""
            INSERT INTO people(fname, lname, email, role_id)
            VALUES (%S, %S, %S, %S)
            """,
            (Person.fname, Person.lname, Person.email, Person.role))

    return render_template("registration.html", form=form)

