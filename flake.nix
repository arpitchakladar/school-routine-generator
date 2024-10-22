{
	description = "Flake for development environment for School Routine Generator.";

	inputs = {
		nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
	};

	outputs = { self, nixpkgs }:
	let
		pkgs = nixpkgs.legacyPackages."x86_64-linux";
		python3Env = pkgs.python3.withPackages (ps: with ps; [
			mysql-connector
		]);
	in {
		devShells."x86_64-linux".default = pkgs.mkShell {
			packages = with pkgs; [
				python3Env
				mariadb
			];

			# Set environment variables to set up and manage MariaDB server
			shellHook = ''
				# Create mysql_data directory if it doesn't exist
				if [ ! -d ./mysql/data ]; then
					echo "Creating MariaDB data directory..."
					mkdir -p ./mysql/data
				fi

				# Initialize MariaDB data directory if it hasn't been initialized
				if [ ! -f ./mysql/data/ibdata1 ]; then
					echo "Initializing MariaDB data directory..."
					mariadb-install-db --datadir=./mysql/data
				fi

				mkdir -p /tmp/school-routine-generator/mysql/run
			'';
		};
	};
}
