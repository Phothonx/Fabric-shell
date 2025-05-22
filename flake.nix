{
  description = "Fabric shell";

  inputs = {
    nixpkgs.url = "nixpkgs";
    fabric.url = "github:Fabric-Development/fabric";
    fabric.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = {
    self,
    nixpkgs,
    ...
  } @ inputs: let
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
      default = inputs.fabric.devShells.${pkgs.system}.default;
    });
  };
}
