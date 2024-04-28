default: help

.PHONY: run run-debug update-deps help

run: # Runs in info logging mode
	poetry run python main.py

run-debug: # Runs in debug loggin mode
	DEBUG=true poetry run python main.py

update-deps: # Update Poetry dependencies
	poetry update

help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done