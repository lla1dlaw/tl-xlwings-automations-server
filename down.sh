#!/usr/bin/env bash

# elevate privilages if needed
[[ "$EUID" == 0 ]] || exec sudo -s ${BASH_SOURCE[0]} "$@"

sudo docker compose down
