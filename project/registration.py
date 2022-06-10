@app.route("/registration")
def registration_page():
	return render_template("registration.html", test_var="test")
