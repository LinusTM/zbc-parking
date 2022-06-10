from flask import Flask, render_template
from flask import Blueprint

registration = Blueprint('registration', __name__)

@registration.route("/registration")
def registration_page():
	return render_template("registration.html", test_var="test")
