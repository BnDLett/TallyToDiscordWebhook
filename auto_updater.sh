#!/bin/sh

SCRIPT_PATH=$(dirname "$(realpath "$0")")
cd "$SCRIPT_PATH" || (echo "Failed to start program." && exit)

while true
do
  echo "Checking for updates..."
  git pull
  # Sleeps for 3600 seconds; aka 1 hour.
  sleep 3600
done
