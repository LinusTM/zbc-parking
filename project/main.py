#!/usr/bin/env python3
from flask import Flask, render_template
from registration import registration

app = Flask(__name__)

app.register_blueprint(registration)

@app.route("/")
def main_page():
	return render_template("main.html", test_var="test")

if __name__ == "__main__":
	app.run(debug=True)
