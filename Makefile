# simple file commands
run: 
	python src/main.py

parser: 
	python src/main.py

api: 
	poetry run uvicorn src.api.api:app --reload

production:
	python src/main.py


ready:
	git add . && git commit && git push

# run:
# 	poetry run uvicorn src.main:app --log-level debug

# production:
# 	uvicorn src.main:app --host 0.0.0.0 --port 8000