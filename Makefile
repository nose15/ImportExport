.DEFAULT_GOAL := help
install: ## Init project
	cp -n .env.dev .env
	docker-compose build

start: ## Run docker for a project
	docker-compose up -d

stop: ## Stop all containers for a project
	docker-compose down --remove-orphans

bash: ## Exec bash for python container
	docker-compose exec django bash

kill-all: ## Kill all running containers
	docker container kill $$(docker container ls -q)

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
