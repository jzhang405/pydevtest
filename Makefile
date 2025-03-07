.PHONY: run
run:
	@if [ -d ".venv" ]; then \
		.venv/bin/python pydevtest.py; \
	else \
		echo "Creating virtual environment..."; \
		uv venv .venv && .venv/bin/python -m pip install . && .venv/bin/python pydevtest.py; \
	fi

