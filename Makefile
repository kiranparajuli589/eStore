# Requirements to run make here:
#    - python 3.8 or higher
#    - pip

SHELL := /bin/bash
# Add migration folder here after adding new app
make_migration_deps = accounts/models.py
migration_deps = accounts/migrations
virtual_env_src = venv
requirements = requirements.txt
PYTHON := python3.8
PIP := pip3

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of the following:"
	@echo
	@echo -e "Usage:\n"
	@echo -e "make build\t\t\tinstall requirements for local development"
	@echo -e "make migrate\t\t\tapply migrations"
	@echo -e "make serve\t\t\tstart the dev server at localhost:8002"
	@echo -e "make clean\t\t\tdelete generated migrations, virtualenv and extra redundant files"
	@echo -e "make clean-migrations\t\tdelete generated migrations"
	@echo -e "make clean-env\t\t\tdelete generated virtualenv"
	@echo -e "make clean-extra\t\tdelete generated extra redundant files"

.PHONY: build-env
build-env:
	$(PYTHON) -m venv $(virtual_env_src)

.PHONY: install
install: $(requirements)
	$(PIP) install -r $(requirements)

.PHONY: create-superuser
create-superuser:
	DJANGO_SUPERUSER_PASSWORD=admin $(PYTHON) manage.py createsuperuser --email admin@test.com --f_name Admin --l_name User --noinput

.PHONY: perform-migration
perform-migration: make-migrations migrate

.PHONY: make-migrations
make-migrations: $(make_migration_deps)
	$(PYTHON) manage.py makemigrations accounts
	# Add migration when new apps added

.PHONY: migrate
migrate: $(migration_deps)
	@echo "Running account app migration first"
	$(PYTHON) manage.py migrate
	# Add migration when new apps added

.PHONY: clean
clean: clean-migrations clean-env clean-extra

.PHONY: clean-migrations
clean-migrations:
	@echo "Removing migrations files"
	rm -rf $(migration_deps)
	@echo "Success"

.PHONY: clean-env
clean-env:
	@echo "Removing virtualenv files"
	rm -rf $(virtual_env_src)
	@echo "Success"

.PHONY: clean-extra
clean-extra:
	@echo "Removing extra redundant files"
	rm -rf .idea .vscode
	@echo "Success"
