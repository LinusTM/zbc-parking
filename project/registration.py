from flask import Blueprint, render_template, request
from wtforms import Form, SelectField, StringField, validators

registration = Blueprint('registration', __name__)

class RegistrationForm(Form):
    fname   = StringField('fname', [validators.Length(min=4, max=25)])
    lname   = StringField('lname', [validators.Length(min=4, max=25)])
    email   = StringField('Email', [validators.Length(min=8, max=35)])
    role    = SelectField('role', choices=[(1, "Gæst"), (2, "Medarbejder"), (3, "Elev")])

@registration.route("/registration", methods=['GET', 'POST'])
def registration_page():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        person.fname = form.fname.data 
        person.lname = form.lname.data 
        person.email = form.email.data
        person.role = form.role.data

        # Send values to database
        cur.execute("""
            INSERT INTO people(fname, lname, email, role_id)
            VALUES (%S, %S, %S, %S)
            """,
            (person.fname, person.lname, person.email, person.role))

    return render_template("registration.html", form=form)

