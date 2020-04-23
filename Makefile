# Requirements to run make here:
#    - python 3.8 or higher
#    - pip

SHELL = /bin/bash
# Add migration folder here after adding new app
make_migration_deps = accounts/models.py
migration_deps = accounts/migrations
virtual_env_src = venv
PYTHON := python3.8

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of the following:"
	@echo
	@echo -e "Usage:\n"
	@echo -e "make build\t\t\tinstall requirements for local development"
	@echo -e "make migrate\t\t\tapply migrations"
	@echo -e "make serve\t\t\tstart the dev server at localhost:8002"
	@echo -e "make clean-all\t\t\tdelete generated migrations, virtualenv and extra redundant files"
	@echo -e "make clean-migrations\t\tdelete generated migrations"
	@echo -e "make clean-env\t\t\tdelete generated virtualenv"
	@echo -e "make clean-extra\t\tdelete generated extra redundant files"

.PHONY: perform-migration
perform-migration: make-migration migrate

.PHONY: make-migration
make-migration: $(make_migration_deps)
	$(PYTHON) manage.py makemigrations accounts
	# Add migration when new apps added

.PHONY: migrate
migrate: $(migration_deps)
	@echo "Running account app migration first"
	$(PYTHON) manage.py migrate
	# Add migration when new apps added

.PHONY: clean
clean-all: clean-migrations clean-env clean-extra

.PHONY: clean-migrations
clean-migrations: $(migration_deps)
	@echo "Removing migrations files"
	rm -Rf $(migration_deps)
	@echo "Success"

.PHONY: clean-env
clean-env: $(virtural_env_src)
	@echo "Removing virtualenv files"
	rm -rf $(virtural_env_src)
	@echo "Success"

.PHONY: clean-extra
clean-extra:
	@echo "Removing extra redundant files"
	rm -rf .idea .vscode
	@echo "Success"
