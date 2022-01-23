test:
	pytest ./tests/test_*.py -vvv --junitxml=./reports/unittest-results.xml


check:
	flake8 ./pyPlugin --ignore E501
	find ./pyPlugin -name '*.py' \
	| xargs pylint -d invalid-name \
	               -d locally-disabled \
	               -d missing-docstring \
	               -d too-few-public-methods \
	               -d line-too-long \
	               -d no-self-use \
	               -d too-many-arguments


coverage:
	coverage run tests/test_*.py
	coverage html
	open htmlcov/index.html


develop:
	./setup_env.sh


clean:
	rm -rf build
	rm -rf _trial*
	rm -rf htmlcov
	rm -f twistd.log*
	rm -rf *.egg-info


to_pypi_test:
	python setup.py register -r pypitest
	python setup.py sdist upload -r pypitest

to_pypi:
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi
