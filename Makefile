.PHONY: install start-backend start-worker simulate-agents test

install:
	pip install -r backend/requirements.txt
	cd frontend && npm install

start-backend:
	uvicorn backend.app.main:app --reload

start-worker:
	python -m backend.app.workers.trace_processor

simulate:
	python scripts/simulate_agents.py

docker-up:
	docker-compose up --build

test:
	pytest tests/
