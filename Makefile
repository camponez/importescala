PYTHON=PYTHONPATH=. python

log:
	@./gen_log.sh

run_test:
	$(PYTHON) test/test_escala.py

all: \
	run_test \
	log
