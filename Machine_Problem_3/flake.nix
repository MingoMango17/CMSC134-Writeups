{
  description = "CMSC 134 Machine Problem 3: Vulnerable Web Application";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-23.11";
  };

  outputs = { self, nixpkgs, ... }:
    let
      system = "x86_64-linux";
    in
    {
      devShells."${system}".default =
        let
          pkgs = import nixpkgs {
            inherit system;
          };
        in
        pkgs.mkShell {
          packages = with pkgs; [
            python312
          ];
          shellHook = ''
            echo "Setup complete: CMSC 134 Machine Problem 3"
            fish
          '';
        };
    };
}
