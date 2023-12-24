TAG?=emptywordpad:latest

all: build

# Create a properly-named docker container
build:
	docker build -t "${TAG}" .

run: build
	docker run --rm -e PORT=8000 -p8000:8000 -ti "${TAG}"

verbose: build
	docker run --rm -e PORT=8000 -e VERBOSE=True -p8000:8000 -ti "${TAG}"

debug: build
	docker run --rm -e PORT=8000 -e DEBUG=True -p8000:8000 -ti "${TAG}"

clean:
	docker rmi "${TAG}"

push: build
	docker push "${TAG}"

deploy:
	cd app; gcloud app deploy