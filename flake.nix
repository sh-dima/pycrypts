{
  description = "A pygame adventure featuring a sprawling underground dungeon filled with enemies and loot";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
  };

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      packages.${system}.default = pkgs.python3Packages.buildPythonApplication {
        pname = "pycrypts";
        version = "0.1.0";
        src = ./.;

        format = "pyproject";

        nativeBuildInputs = with pkgs.python3Packages; [
          setuptools
          wheel
        ];

        propagatedBuildInputs = with pkgs; [
          python3Packages.pygame

          inkscape
        ];

        postPatch = ''
          find pycrypts -type l -exec bash -c '
            for link; do
              target=$(readlink "$link")
              if [ -n "$target" ]; then
                rm "$link"

                (cd $(dirname "$link") && cp "$target" $(basename "$link"))
              fi
            done
          ' bash {} +

          ${pkgs.inkscape}/bin/inkscape "./pycrypts/assets/images/entities/living/monsters/zombie.svg" -o "./pycrypts/assets/images/entities/living/monsters/zombie.png" --export-width=512 --export-height=512
          ${pkgs.inkscape}/bin/inkscape "./pycrypts/assets/images/entities/helmet.svg" -o "./pycrypts/assets/images/entities/helmet.png" --export-width=512 --export-height=512
        '';

        meta = with pkgs.lib; {
          description = "A pygame adventure featuring a sprawling underground dungeon filled with enemies and loot";
          license = licenses.agpl3Only;
        };
      };

      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          python3
          python3Packages.pip
          python3Packages.virtualenv
          python3Packages.pygame
        ];

        shellHook = ''
          if [ ! -d .venv/ ]; then
            python -m venv .venv/
          fi

          source .venv/bin/activate

          pip install -r requirements.txt
        '';
      };
    };
}
