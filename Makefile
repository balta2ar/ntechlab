run:
	FLASK_APP=service.py flask run

run_debug:
	FLASK_DEBUG=1 FLASK_APP=service.py flask run

test:
	bash -x ./test.sh

unittest:
	python -m unittest test_model

.PHONY:
	run run_debug test unittest
