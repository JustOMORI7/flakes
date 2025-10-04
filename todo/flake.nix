{
  description = "todo - Simple todo list";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python3;
        pythonPkgs = python.pkgs;
      in {
        packages.todo = pythonPkgs.buildPythonApplication {
          pname = "todo";
          version = "1.0.0";

          src = ./.;
          format = "other";

          installPhase = ''
            runHook preInstall
            mkdir -p $out/bin
            cp ${./main.py} $out/bin/todo
            chmod +x $out/bin/todo
            runHook postInstall
          '';

          meta = with pkgs.lib; {
            description = "todo - Simple todo list";
            license = licenses.mit;
            platforms = platforms.linux;
          };
        };
      });
}