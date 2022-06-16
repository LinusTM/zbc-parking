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
	return render_template("registration.html", test_var="test")


