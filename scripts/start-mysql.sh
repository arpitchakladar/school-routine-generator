#!/bin/sh

echo "Starting MariaDB server with network-only configuration..."
mysqld --defaults-file=./mysql/my.cnf --datadir=./mysql/data &
