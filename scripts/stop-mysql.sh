#!/bin/sh

echo "Stopping MariaDB server..."
mysqladmin --defaults-file=./mysql/my.cnf shutdown
