{
  description = "mp3down - YouTube MP3 downloader";

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
        packages.mp3down = pythonPkgs.buildPythonApplication {
          pname = "mp3down";
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
            cp ${./main.py} $out/bin/mp3down
            chmod +x $out/bin/mp3down
            runHook postInstall
          '';

          meta = with pkgs.lib; {
            description = "mp3down - YouTube MP3 downloader";
            license = licenses.mit;
            platforms = platforms.linux;
          };
        };
      });
}
