{ pkgs ? import <nixpkgs> {} }:

with pkgs;

let myWerkzeug = python310Packages.werkzeug.overridePythonAttrs (oldAttrs: rec {
			postPatch = ''
		substituteInPlace src/werkzeug/_reloader.py \
			--replace "rv = [sys.executable]" "return sys.argv"
	''; });

in mkShell {
	buildInputs = [
		nodePackages.pyright
		python310
		python39Packages.psycopg2
		python310Packages.flask
<<<<<<< HEAD
		python39Packages.wtforms
		python39Packages.requests
		python39Packages.flask_wtf
=======
		python310Packages.psycopg2
>>>>>>> 0e7deb5c5a35a2e45c85841a7a2e7a5d8d2a15e3
		myWerkzeug
	];

	shellHook = ''
	export FLASK_APP=main
	'';
}
