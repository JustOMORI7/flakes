{
  description = "m4adown - YouTube M4A downloader";

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
        packages.m4adown = pythonPkgs.buildPythonApplication {
          pname = "m4adown";
          version = "0.1.0";

          src = ./.;
          format = "other";

          propagatedBuildInputs = with pythonPkgs; [
            yt-dlp
            tkinter 
          ] ++ [
            pkgs.ffmpeg
          ];

          installPhase = ''
            runHook preInstall
            mkdir -p $out/bin
            cp ${./main.py} $out/bin/m4adown
            chmod +x $out/bin/m4adown
            runHook postInstall
          '';

          meta = with pkgs.lib; {
            description = "m4adown - YouTube M4A downloader";
            license = licenses.mit;
            platforms = platforms.linux;
          };
        };
      });
}
