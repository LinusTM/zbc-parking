{ pkgs ? import <nixpkgs> {} }:

with pkgs;

mkShell {
	buildInputs = [
		nodePackages.pyright
		python310
		python310Packages.flask
	];

	shellHook = ''
	export FLASK_APP=main
	'';
}
