.PHONY: default
default: clean test build publish

.PHONY: clean
clean:
	@echo "Cleaning up..."
	rm -rvf build/
	rm -rvf dist/
	rm -rvf gitbatch.egg-info
	rm -rvf .pytest_cache
	rm -rvf MANIFEST.in
	rm -rvf git-batch/__pycache__ distro/*.pyc
	rm -rvf test/__pycache__ test/*.pyc

.PHONY: test
test:
	@echo "Running tests..."
	@pylint gitbatch
	@pytest

.PHONY: build
build: clean
	@python setup.py sdist bdist bdist_egg
	@twine check dist/*

.PHONY: test-publish
test-publish: build
	@rm -f dist/gitbatch-*mac*.tar.gz
	@twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: publish
publish: build
	@rm -f dist/gitbatch-*mac*.tar.gz
	@twine upload dist/*
