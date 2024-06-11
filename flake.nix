{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    systems.url = "github:nix-systems/default";
    devenv.url = "github:cachix/devenv";
    devenv.inputs.nixpkgs.follows = "nixpkgs";
    nixpkgs-python.url = "github:cachix/nixpkgs-python";
    nixpkgs-python.inputs = {
      nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      devenv,
      systems,
      ...
    }@inputs:
    let
      forEachSystem = nixpkgs.lib.genAttrs (import systems);
    in
    {
      packages = forEachSystem (system: {
        devenv-up = self.devShells.${system}.default.config.procfileScript;
      });

      devShells = forEachSystem (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          default = devenv.lib.mkShell {
            inherit inputs pkgs;
            modules = [
              {
                # https://devenv.sh/reference/options/
                packages = [ pkgs.cairo ];

                languages.python = {
                  enable = true;
                  poetry = {
                    enable = true;
                    install = {
                      enable = true;
                      installRootPackage = false;
                      onlyInstallRootPackage = false;
                      compile = false;
                      quiet = false;
                      groups = [ ];
                      ignoredGroups = [ ];
                      onlyGroups = [ ];
                      extras = [ ];
                      allExtras = false;
                      verbosity = "no";
                    };
                    activate.enable = true;
                  };
                };
              }
            ];
          };
        }
      );
    };
}
