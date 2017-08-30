.venv: requirements.txt
	virtualenv -p python3.6 .venv
	source .venv/bin/activate; pip install -r requirements.txt; \
	jupyter-nbextension install rise --py --sys-prefix; \
	jupyter-nbextension enable rise --py --sys-prefix
	touch .venv/installed

.PHONY: notebook
notebook: .venv
	source .venv/bin/activate; jupyter notebook

.PHONY: slides
slides: .venv
	source .venv/bin/activate; jupyter nbconvert ./presentation.ipynb --to slides --post serve
