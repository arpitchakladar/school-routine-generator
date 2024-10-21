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

				# Create a my.cnf config file to disable Unix socket and enable networking
				echo "Writing my.cnf to disable Unix socket..."
				cat > ./mysql/my.cnf <<EOF
[mysqld]
bind-address = 0.0.0.0
skip-networking = 0
skip-external-locking
skip-grant-tables
socket = /tmp/school-routine-generator/mysql/run/socket
EOF

				# Start MariaDB server with custom configuration file
				echo "Starting MariaDB server with network-only configuration..."
				mysqld --defaults-file=./mysql/my.cnf --datadir=./mysql/data &
				MYSQL_PID=$!

				# Stop MariaDB when exiting shell
				trap "echo 'Stopping MariaDB server...'; kill $MYSQL_PID" EXIT
			'';
		};
	};
}
