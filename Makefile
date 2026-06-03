-include .env
export

UV ?= uv
DBT_PROFILES_DIR ?= config
LOAD_ARGS ?= --limit 1

SNOWFLAKE_ADMIN_CONNECTION ?= CONN_ADMIN
SNOWFLAKE_DEV_CONNECTION ?= CONN_MMM

.PHONY: setup-admin setup setup-all load dbt-debug dbt-build test lint typecheck check

setup-admin:
	@set -eu; \
	test -n "$(SNOWFLAKE_PUBLIC_KEY_PATH)" || (echo "SNOWFLAKE_PUBLIC_KEY_PATH is required"; exit 1); \
	public_key="$$(sed '/BEGIN PUBLIC KEY/d;/END PUBLIC KEY/d' "$(SNOWFLAKE_PUBLIC_KEY_PATH)" | tr -d '[:space:]')"; \
	test -n "$$public_key" || (echo "SNOWFLAKE_PUBLIC_KEY_PATH must point to a public key file"; exit 1); \
	$(UV) run snow sql -c $(SNOWFLAKE_ADMIN_CONNECTION) -f scripts/setup_snowflake_by_admin.sql \
		-D "dbt_user_rsa_public_key=$$public_key"

setup:
	$(UV) run snow sql -c $(SNOWFLAKE_DEV_CONNECTION) -f scripts/setup_snowflake.sql

setup-all:
	$(MAKE) setup-admin
	$(MAKE) setup

load:
	$(UV) run dbt-test load-raw $(LOAD_ARGS)

dbt-debug:
	DBT_PROFILES_DIR=$(DBT_PROFILES_DIR) $(UV) run dbt debug --project-dir dbt

dbt-build:
	DBT_PROFILES_DIR=$(DBT_PROFILES_DIR) $(UV) run dbt build --project-dir dbt

test:
	$(UV) run pytest

lint:
	$(UV) run ruff check src tests

typecheck:
	$(UV) run pyright

check: lint typecheck test
