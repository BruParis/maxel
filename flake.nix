
{
  description = "A flake providing a dev shell for python with numpy";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux"; # Adjust if needed
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
      };
    in
    {

      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          python312
          python312Packages.pip
          python312Packages.numpy
        ];

        shellHook = ''
          echo "You are now using a NIX environment"
        '';
      };
    };
}
