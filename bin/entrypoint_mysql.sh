#!/bin/bash

set -e

if [ "$MYSQL_DATABASE1" ]; then
  mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS \`$MYSQL_DATABASE1\` ;"
fi

if [ "$MYSQL_DATABASE2" ]; then
  mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS \`$MYSQL_DATABASE2\` ;"
fi

# Run the original entrypoint script
/docker-entrypoint.sh "$@"