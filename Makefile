.PHONY: deps tasks seed-check dev feedback heldout noise evolve ui audit e2e

deps:
	pip install numpy pandas scipy statsmodels fastapi uvicorn python-multipart pymupdf playwright

tasks:
	python3 tasks/generator/make_tasks.py --split dev --n 3 --seed 101
	python3 tasks/generator/make_tasks.py --split feedback --n 6 --seed 202
	python3 tasks/generator/make_hard_tasks.py --split feedback --n 10 --seed 505 --start-index 7
	python3 tasks/generator/make_tasks.py --split heldout --n 6 --seed 303
	python3 tasks/generator/make_hard_tasks.py --split heldout --n 10 --seed 606 --start-index 7

seed-check:
	python3 evalkit/run_eval.py --split dev --harness-dir seed/harness --run-id dev_seed_check

dev:
	python3 evalkit/run_eval.py --split dev --harness-dir harness --run-id dev_$(shell git rev-parse --short HEAD)

feedback:
	python3 evalkit/run_eval.py --split feedback --harness-dir harness --repeats 3 --run-id fb_$(shell git rev-parse --short HEAD)_x3

heldout:
	python3 evalkit/run_eval.py --split heldout --harness-dir harness --repeats 3 --run-id ho_$(shell git rev-parse --short HEAD)_x3

noise:
	python3 evalkit/noise.py --run-id fb_H0_x3

audit:
	python3 evalkit/audit_harness.py harness

evolve:
	python3 evolve/evolve.py --rounds 1

ui:
	python3 ui/server.py

e2e:
	python3 ui/e2e_test.py
