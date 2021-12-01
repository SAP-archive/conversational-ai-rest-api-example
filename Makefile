# Common tasks according to https://gazr.io/

TO := _

ifdef BUILD_NUMBER
NUMBER = $(BUILD_NUMBER)
else
NUMBER = 1
endif

ifdef JOB_BASE_NAME
PROJECT_ENCODED_SLASH = $(subst %2F,$(TO),$(JOB_BASE_NAME))
PROJECT = $(subst /,$(TO),$(PROJECT_ENCODED_SLASH))
# Run on CI
COMPOSE = docker-compose -f docker-compose.yml -p dataset_translation_$(PROJECT)_$(NUMBER)
else
# Run Locally
COMPOSE = docker-compose -p dataset_translation
endif

.PHONY: down
down:
	$(COMPOSE) down --rmi local --volume

.PHONY: test
test:
	$(COMPOSE) run test
