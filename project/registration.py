from flask import Blueprint, render_template

registration = Blueprint('registration', __name__)

@registration.route("/registration")
def registration_page():
	return render_template("registration.html", test_var="test")
