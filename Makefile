# Requirements to run make here:
#    - python 3.8 or higher
#    - pip 20.0.0 or higher
eSTORE_SERVER_HOST := 0.0.0.0:8000
ADMIN_EMAIL := admin@test.com
ADMIN_F_NAME := Admin
ADMIN_L_NAME := USER
ADMIN_PASSWORD := admin
APP := accounts
SHELL := /bin/bash

# Add migration folder here after adding new app
make_migration_deps := accounts/models.py
migration_deps := accounts/migrations
virtual_env_src := venv
requirements := requirements.txt
db := db.sqlite3

PYTHON := python3.8
PIP := pip3

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of the following:"
	@echo
	@echo -e "Usage:\n"
	@echo -e "build\t\t\tbuild virtualenv for project"
	@echo -e "install\t\t\tinstall requirements for local development"
	@echo -e "create-superuser\tcreate backend superuser (Available vars: ADMIN_EMAIL, ADMIN_EMAIL, ADMIN_L_NAME, ADMIN_PASSWORD)"
	@echo -e "perform-migration\tcreate and apply migrations"
	@echo -e "make-migrations\t\tcreate migrations (Available var: APP | Default: 'accounts')"
	@echo -e "migrate\t\t\tapply migrations"
	@echo -e "serve\t\t\tstart the dev server at 0.0.0.0:8000"
	@echo -e "clean\t\t\tdelete generated migrations, virtualenv and extra redundant files"
	@echo -e "clean-migrations\tdelete generated migrations"
	@echo -e "clean-env\t\tdelete generated virtualenv"
	@echo -e "clean-extra\t\tdelete generated extra redundant files"

.PHONY: build
build:
	$(PYTHON) -m venv $(virtual_env_src)

.PHONY: install
install: $(requirements)
	$(PIP) install -r $(requirements)

.PHONY: create-superuser
create-superuser:
	DJANGO_SUPERUSER_PASSWORD=$(ADMIN_PASSWORD) $(PYTHON) manage.py createsuperuser --email $(ADMIN_EMAIL) --f_name $(ADMIN_F_NAME) --l_name $(ADMIN_L_NAME) --noinput

.PHONY: perform-migration
perform-migration: mk-migrations migrate

.PHONY: mk-migrations
mk-migrations: $(make_migration_deps)
	$(PYTHON) manage.py makemigrations $(APP)
	# Add migration when new apps added

.PHONY: migrate
migrate: $(migration_deps)
	@echo "Running account app migration first"
	$(PYTHON) manage.py migrate
	# Add migration when new apps added

.PHONY: serve
serve:
	$(PYTHON) manage.py runserver $(eSTORE_SERVER_HOST)

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

.PHONY: clean-db
clean-db:
	@echo "Removing extra redundant files"
	rm -rf $(db)
	@echo "Success"
