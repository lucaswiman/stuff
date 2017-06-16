.PHONY: clean
clean:
	rm -rf cy_migrations/management/commands/makemigrations.pyx
	rm -rf cy_migrations/management/commands/migrate.pyx
	rm -rf cy_migrations/upstream/*
	mkdir -p cy_migrations/upstream
	mkdir -p cy_migrations/management/commands
	echo > cy_migrations/management/__init__.py
	echo > cy_migrations/management/commands/__init__.py

.PHONY: build
build: clean
	cp -r upstream_django/django/db/migrations/* cy_migrations/upstream/
	cp upstream_django/django/core/management/commands/makemigrations.py cy_migrations/management/commands/makemigrations.pyx
	cp upstream_django/django/core/management/commands/migrate.py cy_migrations/management/commands/migrate.pyx
	find cy_migrations/upstream -name "*.py" -not -name __init__.py -exec bash -c 'mv "$$1" "$${1%.py}".pyx' - '{}' \;

