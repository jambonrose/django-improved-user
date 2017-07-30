.PHONY: all clean dist release

all:
	@echo 'Available Commands:'
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null \
		| awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' \
		| sort \
		| egrep -v -e '^[^[:alnum:]]' -e '^$@$$' \
		| xargs -I {} echo '    {}'

dist:
	python setup.py sdist --formats=gztar bdist_wheel
	gpg --armor --detach-sign -u 5878672C -a dist/django_improved_user*.whl
	gpg --armor --detach-sign -u 5878672C -a dist/django-improved-user*.tar.gz

release:
	git tag v`bumpversion --dry-run --list patch | grep current | cut -d'=' -f 2`
	twine upload dist/*
	git push --tags

clean:
	rm -f .coverage
	rm -f .coverage.*
	rm -rf *.egg-info
	rm -rf .eggs
	rm -rf .tox
	rm -rf build
	rm -rf dist
	rm -rf htmlcov
	find . -name "*.py[co]" -delete
	find . -name "__pycache__" -delete
