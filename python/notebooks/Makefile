.venv: requirements.txt
	test ! -f .venv && python -m venv .venv
	source .venv/bin/activate; pip install -r requirements.txt

.PHONY: notebook
notebook: .venv
	source  .venv/bin/activate; jupyter notebook
