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
		python310
		python310Packages.flask
		myWerkzeug
	];

	shellHook = ''
	export FLASK_APP=main
	export FLASK_ENV=development
	'';
}
