{ pkgs ? import <nixpkgs> {} }:

with pkgs;

let myWerkzeug = python39Packages.werkzeug.overridePythonAttrs (oldAttrs: rec {
			postPatch = ''
		substituteInPlace src/werkzeug/_reloader.py \
			--replace "rv = [sys.executable]" "return sys.argv"
	''; });

in mkShell {
	buildInputs = [
		nodePackages.pyright
		python39
		python39Packages.psycopg2
		python39Packages.flask
		python39Packages.wtforms
		myWerkzeug
	];

	shellHook = ''
	export FLASK_APP=main
	'';
}
