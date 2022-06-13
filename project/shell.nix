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
		python310Packages.flask
		python310Packages.psycopg2
		myWerkzeug
	];

	shellHook = ''
	export FLASK_APP=main
	export FLASK_ENV=development
	'';
}
