{
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-25.11";
  };

  outputs = { self, nixpkgs }: 
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
    in
      {
        packages.x86_64-linux.default = 
          #      with import nixpkgs { system = "x86_64-linux"; };          
          pkgs.python3Packages.buildPythonPackage rec {
          name = "BittyTax";
          src = ./.;
          pyproject = true;
          build-system = [ pkgs.python3Packages.setuptools ];
          propagatedBuildInputs = with pkgs.python3Packages; [ colorama defusedxml jinja2 openpyxl python-dateutil
                                                               pyyaml requests typing-extensions tqdm xhtml2pdf
                                                               xlrd xlsxwriter ];
        };
      };
        
      # Development environments
  # devShells = forEachSupportedSystem ({ pkgs }: {
  #   default = pkgs.mkShell {
  #     # Pinned packages available in the environment
  #     packages = with pkgs; [
  #       python311
  #       (with python311Packages; [  ])
  #       git
  #       jq
  #       nixpkgs-fmt
  #     ];
  #   };
  # });
}
