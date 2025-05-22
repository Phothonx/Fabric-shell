{
  description = "Fabric shell";

  inputs = {
    nixpkgs.url = "nixpkgs";
    fabric.url = "https://github.com/Fabric-Development/fabric";
    fabric.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = {
    self,
    nixpkgs,
    ...
  }: let
    lib = nixpkgs.lib;

    systems = ["x86_64-linux"];

    pkgsFor = lib.genAttrs systems (
      system:
        import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        }
    );

    forEachSystem = f: lib.genAttrs systems (system: f pkgsFor.${system});
  in {
    devShells = forEachSystem (pkgs: {
      default = pkgs.mkShell {
        # if package not in nixpkgs: https://github.com/nix-community/pip2nix
        # ex: nix run github:nix-community/pip2nix -- generate
        # or directly builPythonPackage
        venvDir = ".venv";
        packages = [
          (pkgs.python3.withPackages (p:
            with p; [
              # ex:
              # matplotlib
              # scipy
              # requests
              # jupyter
            ]))
        ];
      };
    });
  };
}
