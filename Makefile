include .env

.PHONY: init
init:
	cp -p .env.example .env && docker-compose run --rm node yarn install

.PHONY: generate-locust-model
generate-locust-model:
	docker-compose run --rm node yarn openapi-generator-cli generate \
		-t /root/src/templates/model \
		-i /root/api/openapi.yaml \
		-g python \
		-o dist \
		--package-name locust \
		--global-property models,modelTests=false,modelDocs=false

.PHONY: generate-init-model
generate-init-model:
	docker-compose run --rm python3 sh -c "mkinit --verbose --inplace './dist/locust/model'"

.PHONY: generate-locust-api
generate-locust-api:
	docker-compose run --rm node yarn openapi-generator-cli generate \
		-t /root/src/templates/api \
		-i /root/api/openapi.yaml \
		-g python \
		-o dist \
		--package-name locust \
		--global-property apis,apiTests=false,apiDocs=false

.PHONY: generate-init-api
generate-init-api:
	docker-compose run --rm python3 sh -c "mkinit --verbose --inplace './dist/locust/api'"

.PHONY: generate-locust-example
generate-locust-example:
	docker-compose run --rm node sh -c " \
		rm -rf dist/locust/example \
		&& yarn openapi-generator-cli generate \
		-t /root/src/templates/example \
		-i /root/api/openapi.yaml \
		-g python \
		-o dist/tmp \
		--package-name locust \
		--global-property models,modelTests=false,modelDocs=false \
		&& mv -f dist/tmp/locust/model dist/locust/example \
		&& rm -rf dist/tmp"

.PHONY: generate-init-example
 generate-init-example:
	docker-compose run --rm python3 sh -c "mkinit --verbose --inplace './dist/locust/example'"

.PHONY: lint-python
lint-python:
	docker-compose run --rm python3 sh -c " \
	    isort --show-files --force-single-line-imports './dist/locust' && \
		autoflake -v -v --recursive --in-place --remove-all-unused-imports --remove-duplicate-keys --ignore-init-module-imports --remove-unused-variables './dist/locust' && \
		black --verbose --exclude '.gitignore' './dist/locust' && \
		isort --show-files --multi-line 3 './dist/locust'"

.PHONY: generate-locust
generate-locust:
	make generate-locust-model && make generate-init-model && make generate-locust-api && make generate-init-api && make lint-python
