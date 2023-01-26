with import <nixpkgs> {};
with pkgs.python3Packages;

buildPythonPackage rec {
  name = "BittyTax";
  src = ./.;
  # propagatedBuildInputs = [];
}
