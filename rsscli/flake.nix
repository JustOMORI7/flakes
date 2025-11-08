{
  description = "rsscli - Basic CLI RSS Reader";

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
        packages.rsscli = pythonPkgs.buildPythonApplication {
          pname = "rsscli";
          version = "1.0.0";

          src = ./.;
          format = "other";

          propagatedBuildInputs = with pythonPkgs; [
            feedparser
	    rich
	    beautifulsoup4
          ];

          installPhase = ''
            runHook preInstall
            mkdir -p $out/bin
            cp ${./main.py} $out/bin/rsscli
            chmod +x $out/bin/rsscli
            runHook postInstall
          '';

          meta = with pkgs.lib; {
            description = "rsscli - Basic CLI RSS Reader";
            license = licenses.mit;
            platforms = platforms.linux;
          };
        };
      });
}