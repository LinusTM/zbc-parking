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
		myWerkzeug
		python39Packages.psycopg2
		python39Packages.flask
		python39Packages.wtforms
		python39Packages.pandas
		python39Packages.json5
		python39Packages.dataclasses-json
	];

	shellHook = ''
	export FLASK_APP=main
	export FLASK_ENV=development
	'';
}
