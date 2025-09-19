{
  description = "youmusicdown - YouTube music downloader";

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
        packages.ymdown = pythonPkgs.buildPythonApplication {
          pname = "ymdown";
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
            cp ${./main.py} $out/bin/ymdown
            chmod +x $out/bin/ymdown
            runHook postInstall
          '';

          meta = with pkgs.lib; {
            description = "youmusicdown - YouTube music downloader";
            license = licenses.mit;
            platforms = platforms.linux;
          };
        };
      });
}
