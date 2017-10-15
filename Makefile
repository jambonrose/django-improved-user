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
	rm -rf build
	rm -rf dist
	rm -rf example*_project/db.sqlite3
	rm -rf htmlcov
	rm -rf src/*.egg-info
	rm -rf src/*.eggs
	find -X . \( -path '*/.tox/*' -o -path '*/.git/*' \) -prune -o \( -name "*.py[co]" -type f -print0 \) | xargs -0 -I {} rm {}
	find -X . \( -path '*/.tox/*' -o -path '*/.git/*' \) -prune -o \( -name ".coverage" -type f -print0 \) | xargs -0 -I {} rm {}
	find -X . \( -path '*/.tox/*' -o -path '*/.git/*' \) -prune -o \( -name ".coverage.*" -type f -print0 \) | xargs -0 -I {} rm {}
	find -X . \( -path '*/.tox/*' -o -path '*/.git/*' \) -prune -o \( -name "__pycache__" -type d -print0 \) | xargs -0 -I {} rm -r {}
